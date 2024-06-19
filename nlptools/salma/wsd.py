from nlptools.salma import settings 
import re
import warnings
warnings.filterwarnings("ignore")
import torch
import numpy as np
import pandas as pd
from nlptools.arabert.preprocess import ArabertPreprocessor

def normalizearabert(s):
  model_name = 'aubmindlab/bert-base-arabertv02'
  arabert_prep = ArabertPreprocessor(model_name.split("/")[-1])
  return arabert_prep.preprocess(str(s))



def glosses1(dfcand,target):
# """
# takes a dataframe 
# return 
	# 'none' if the maximum logistic regression score for TRUE class is less than -2 OR
	# the predicted gloss having the maximum logistic regression score
# """

  wic_c = []
  wic_c, _ = read_data(dfcand,normalizearabert,target)
  tokenizedwic_c = np.array([settings.tokenizer.encode(x, max_length=512,padding='max_length',truncation='longest_first',add_special_tokens=True) for x in wic_c])
  max_len = 512
  segmentswic = torch.tensor([get_segments(settings.tokenizer.convert_ids_to_tokens(i),max_len) for i in tokenizedwic_c])
  paddedwic = tokenizedwic_c
  attention_maskwic = np.where(paddedwic != 0, 1, 0)
  input_idswic = torch.tensor(paddedwic)  
  attention_maskwic = torch.tensor(attention_maskwic)
  settings.model = settings.model.eval()
  wicpredictions , wictrue_labels = [], []
  b_input_ids = input_idswic
  b_input_mask =  attention_maskwic
  b_input_seg = segmentswic

  with torch.no_grad():
    outputs = settings.model(b_input_ids,token_type_ids=b_input_seg,attention_mask=b_input_mask)

  logits = outputs[0]
  wicpredictions.append(logits)
  wicflat_predictions = np.concatenate(wicpredictions, axis=0)

  return dfcand['Concept_id'].to_list()[np.argmax(wicflat_predictions, axis=0).flatten()[1]],dfcand['Gloss'].to_list()[np.argmax(wicflat_predictions, axis=0).flatten()[1]]

def read_data(data,normalize,target):
  c = []
  labels = []
  for i,row in data.iterrows():
      
      example = normalize(row['Example'])
      gloss = normalize(row['Gloss'])
      label = row['Label']
      
      c.append('{} [SEP] {}: {}'.format(example,target,gloss))
      if label == 1.0:
          labels.append(1)
      else:
          labels.append(0)
  return c,labels

def inserttag1(sentence,tag,start,end):
    before = sentence[:start]
    after = sentence[end:]
    target = sentence[start:end]
    return before+tag+sentence[start:end]+tag+after

def get_segments(tokens, max_seq_length):
    if len(tokens)>max_seq_length:
        raise IndexError("Token length more than max seq length!")
    segments = []
    current_segment_id = 0
    for token in tokens:
        segments.append(current_segment_id)
        if token == "[SEP]":
            current_segment_id = 1
    return segments + [0] * (max_seq_length - len(tokens))

def senttarget(target,example):
  start = -1
  try:
    start = example.index(target)
  except ValueError:
    return -1
  end = example.index(target)+len(target)
  return inserttag1(example,"[UNUSED0]",start,end)


def GlossPredictor(diac_lemma, undiac_lemma,target,example,glosses):
# """ 
# takes 
	# a lemma
	# corresponding target word 
	# an example
	# glosses as a dictionay, following an example:
	#	glosses =	{"Concept_id1": "gloss1",  "Concept_id2": "gloss2",  "Concept_id3": "gloss3"}
# returns 
	# -1   if the example does not contain the target word  OR
	# 'none' if no records in dftrue for the lemma and if the maximum logistic regression score for TRUE class is less than -2 OR
	# the predicted gloss for the target word 
	# 
# """
  example = senttarget(target,example)
  if example == -1:
    return -1,-1
  
  data = []
  for g in glosses:
      data.append([g,diac_lemma,undiac_lemma, glosses[g], target,example,0,1,'','',''])
  dfcolumns = ['Concept_id', 'Diac_lemma', 'Undiac_lemma', 'Gloss', 'Target', 'Example', 'Is_training', 'Label', 'concept_id', 'lemma_id', 'POS']
  dfcand = pd.DataFrame(data,columns=dfcolumns)
  
  
  if len(dfcand) > 0:
    dfcand['Example'] = dfcand['Example'].apply(lambda x: example)
    dfcand['Target'] = dfcand['Target'].apply(lambda x: target)
    dfcand = dfcand.drop_duplicates()
  
    dfcand['Example'] = dfcand['Example'].apply(lambda x: x.upper())
    dfcand['Example'] = dfcand['Example'].apply(lambda x: re.sub(r'^((.?\[UNUSED0\].?){1})\[UNUSED0\]', r'\1[UNUSED1]', x) )
    return glosses1(dfcand,target)
  else:
    return 'none','none'