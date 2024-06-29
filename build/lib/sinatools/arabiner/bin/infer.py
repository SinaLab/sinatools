import os
from collections import namedtuple
from sinatools.arabiner.utils.helpers import load_checkpoint
from sinatools.arabiner.utils.data import get_dataloaders, text2segments
from sinatools.DataDownload import downloader
import sinatools
def ner(text, batch_size=32):
    """
    This method takes a text as input, and a batch size, then performs named entity recognition (NER) on the input text and returns a list of tagged mentions.

    Args:
        text (str): The input text to perform NER on.
        batch_size (int, optional): Batch size for inference. Default is 32.

    Returns:
        list: A list of lists containing token and label pairs for each segment.
              Each inner list has the format ['token', 'label1 label2 ...'].
    **Example:**

     .. highlight:: python
     .. code-block:: python

            from sinatools.arabiner.bin import infer
            infer.ner('ذهب محمد الى جامعة بيرزيت')

            #the output   
            [['ذهب', 'O'],
            ['محمد', 'B-PERS'],
            ['الى', 'O'],
            ['جامعة', 'B-ORG'],
            ['بيرزيت', 'B-GPE I-ORG']]
    """    
    # Load tagger
    # filename = 'Wj27012000.tar'
    # path =downloader.get_appdatadir()
    # model_path = os.path.join(path, filename)
    # print('1',model_path)
    # tagger, tag_vocab, train_config = load_checkpoint(model_path)
    

    # Convert text to a tagger dataset and index the tokens in args.text
    dataset, token_vocab = text2segments(text)

    vocabs = namedtuple("Vocab", ["tags", "tokens"])
    vocab = vocabs(tokens=token_vocab, tags=sinatools.tag_vocab)

    # From the datasets generate the dataloaders
    dataloader = get_dataloaders(
        (dataset,),
        vocab,
        sinatools.train_config.data_config,
        batch_size=batch_size,
        shuffle=(False,),
    )[0]

    # Perform inference on the text and get back the tagged segments
    segments = sinatools.tagger.infer(dataloader)
    segments_lists = []
    # Print results
    for segment in segments:
        for token in segment:
            segments_list = []
            segments_list.append(token.text)
            #print([t['tag'] for t in token.pred_tag])
            list_of_tags = [t['tag'] for t in token.pred_tag]
            list_of_tags = [i for i in list_of_tags if i not in('O',' ','')]
            #print(list_of_tags)
            if list_of_tags == []:
               segments_list.append(' '.join(['O']))
            else:
               segments_list.append(' '.join(list_of_tags))
            segments_lists.append(segments_list)         
    return segments_lists

#Print results
    # for segment in segments:
    #     s = [
    #         (token.text, token.pred_tag[0]['tag'])
    #         for token in segment
    #         if token.pred_tag[0]['tag'] != 'O'
    #     ]
    #     print(", ".join([f"({token}, {tag})" for token, tag in s]))

def extract_tags(text):
    tags = []
    tokens = text.split()
    for token in tokens:
        tag = token.split("(")[-1].split(")")[0]
        if tag != "O":
            tags.append(tag)
    return " ".join(tags)
