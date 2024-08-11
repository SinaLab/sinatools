import pickle
from sinatools.DataDownload import downloader
import os 

synonyms_level2_dict = {} 
level2_dict = 'graph_l2.pkl'
path = downloader.get_appdatadir()
file_path = os.path.join(path, level2_dict)
with open(file_path, 'rb') as f:
    synonyms_level2_dict = pickle.load(f, encoding='utf-8')


synonyms_level3_dict = {}    
level3_dict = 'graph_l3.pkl'
path = downloader.get_appdatadir()
file_path = os.path.join(path, level3_dict)
with open(file_path, 'rb') as f:
   synonyms_level3_dict = pickle.load(f, encoding='utf-8')