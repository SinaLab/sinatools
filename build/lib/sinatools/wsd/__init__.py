from sinatools.wsd import settings 
import pickle
from sinatools.DataDownload import downloader
import os 

settings.glosses_dic = {}
filename = 'glosses_dic.pickle'
path =downloader.get_appdatadir()
file_path = os.path.join(path, filename)
with open(file_path, 'rb') as f:
    settings.glosses_dic = pickle.load(f)
