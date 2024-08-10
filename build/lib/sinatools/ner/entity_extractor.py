import os
from collections import namedtuple
from sinatools.ner.data_format import get_dataloaders, text2segments
from . import tagger, tag_vocab, train_config


def convert_nested_to_flat(nested_tags):
    flat_tags = []
    
    for entry in nested_tags:
        word = entry['token']
        tags = entry['tags'].split()
        
        # Initialize with the first tag in the sequence
        flat_tag = tags[0]
        
        for tag in tags[1:]:
            # Check if the tag is an "I-" tag, indicating continuation of an entity
            if tag.startswith('I-'):
                flat_tag = tag
                break
        
        flat_tags.append({
            'token': word,
            'tags': flat_tag
        })
    
    return flat_tags

def extract(text, ner_method="nested"):
    
    dataset, token_vocab = text2segments(text)

    vocabs = namedtuple("Vocab", ["tags", "tokens"])
    vocab = vocabs(tokens=token_vocab, tags=tag_vocab)

    dataloader = get_dataloaders(
        (dataset,),
        vocab,
        train_config.data_config,
        batch_size=32,
        shuffle=(False,),
    )[0]


    segments = tagger.infer(dataloader)
    segments_lists = []
    
    for segment in segments:
        for token in segment:
            segments_list = {}
            segments_list["token"] = token.text
            list_of_tags = [t['tag'] for t in token.pred_tag]
            list_of_tags = [i for i in list_of_tags if i not in('O',' ','')]
            if list_of_tags == []:
               segments_list["tags"] = ' '.join(['O'])
            else:
               segments_list["tags"] = ' '.join(list_of_tags)
            segments_lists.append(segments_list)  
    
    if ner_method == "flat":
      segments_lists = convert_nested_to_flat(segments_lists)          
    return segments_lists
