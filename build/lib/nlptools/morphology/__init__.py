from nlptools.morphology import settings 
import pickle
from nlptools.DataDownload import downloader
import os 

#filename = 'ALMA27012000.pickle'
#path =downloader.get_appdatadir()
#file_path = os.path.join(path, filename)
#with open(file_path, 'rb') as f:
#    #Load the serialized data from the file
#    settings.div_dic = pickle.load(f)


filename = 'lemmas_dic.pickle'
path =downloader.get_appdatadir()
file_path = os.path.join(path, filename)
with open(file_path, 'rb') as f:
    #Load the serialized data from the file
    settings.div_dic = pickle.load(f)
    

#filename_five = 'five_grams.pickle'
#path =downloader.get_appdatadir()
#file_path = os.path.join(path, filename_five)
#with open(file_path, 'rb') as f:
#    #Load the serialized data from the file
#    settings.five_grams_dict = pickle.load(f, encoding='utf-8')
#
#
#filename_four = 'four_grams.pickle'
#path =downloader.get_appdatadir()
#file_path = os.path.join(path, filename_four)
#with open(file_path, 'rb') as f:
#    #Load the serialized data from the file
#    settings.four_grams_dict = pickle.load(f, encoding='utf-8')
#    
#       
#filename_three = 'three_grams.pickle'
#path =downloader.get_appdatadir()
#file_path = os.path.join(path, filename_three)
#with open(file_path, 'rb') as f:
#    #Load the serialized data from the file
#    settings.three_grams_dict = pickle.load(f, encoding='utf-8')
#    
#
#filename_two = 'two_grams.pickle'
#path =downloader.get_appdatadir()
#file_path = os.path.join(path, filename_two)
#with open(file_path, 'rb') as f:
#    #Load the serialized data from the file
#    settings.two_grams_dict = pickle.load(f, encoding='utf-8')
#    