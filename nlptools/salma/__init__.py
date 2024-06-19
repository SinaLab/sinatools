from nlptools.salma import settings 
import pickle
from nlptools.DataDownload import downloader
import os 

#filename = 'glosses_dic.pickle'
#path =downloader.get_appdatadir()
#file_path = os.path.join(path, filename)
#with open(file_path, 'rb') as f:
#    #Load the serialized data from the file
#    settings.glosses_dic = pickle.load(f)
settings.glosses_dic = {}