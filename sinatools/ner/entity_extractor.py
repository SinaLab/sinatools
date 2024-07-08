import os
from collections import namedtuple
from sinatools.ner.helpers import load_checkpoint
from sinatools.ner.data import get_dataloaders, text2segments
from sinatools.DataDownload import downloader
import sinatools

def extract(text, batch_size=32):
    """
    This method processes an input text and returns named entites for each token within the text, based on the specified batch size. As follows:

    Args:
        text (:obj:`str`): The Arabic text to be tagged.
        batch_size (int, optional): Batch size for inference. Default is 32.

    Returns:
        list (:obj:`list`): A list of JSON objects, where each JSON could be contains:
        token: The token from the original text.
        NER tag: The label pairs for each segment.

    **Example:**

     .. highlight:: python
     .. code-block:: python

        from sinatools.ner.entity_extractor import extract
        extract('ذهب محمد إلى جامعة بيرزيت')
        [{
            "word":"ذهب",
            "tags":"O"
          },{
            "word":"محمد",
            "tags":"B-PERS"
          },{
            "word":"إلى",
            "tags":"O"
          },{
            "word":"جامعة",
            "tags":"B-ORG"
          },{
            "word":"بيرزيت",
            "tags":"B-GPE I-ORG"
        }]
    """    
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
    
    for segment in segments:
        for token in segment:
            segments_list = {}
            segments_list["word"] = token.text
            list_of_tags = [t['tag'] for t in token.pred_tag]
            list_of_tags = [i for i in list_of_tags if i not in('O',' ','')]
            if list_of_tags == []:
               segments_list["tag"] = ' '.join(['O'])
            else:
               segments_list["tag"] = ' '.join(list_of_tags)
            segments_lists.append(segments_list)  
    return segments_lists
