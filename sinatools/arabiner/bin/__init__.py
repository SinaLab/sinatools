from sinatools.DataDownload import downloader
import os
from sinatools.arabiner.utils.helpers import load_checkpoint
import sinatools

sinatools.tagger = None
sinatools.tag_vocab = None
sinatools.train_config = None

filename = 'Wj27012000.tar'
path =downloader.get_appdatadir()
model_path = os.path.join(path, filename)
print('1',model_path)
sinatools.tagger, sinatools.tag_vocab, sinatools.train_config = load_checkpoint(model_path)