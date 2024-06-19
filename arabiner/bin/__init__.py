from nlptools.DataDownload import downloader
import os
from nlptools.arabiner.utils.helpers import load_checkpoint
import nlptools

nlptools.tagger = None
nlptools.tag_vocab = None
nlptools.train_config = None

filename = 'Wj27012000.tar'
path =downloader.get_appdatadir()
model_path = os.path.join(path, filename)
print('1',model_path)
nlptools.tagger, nlptools.tag_vocab, nlptools.train_config = load_checkpoint(model_path)