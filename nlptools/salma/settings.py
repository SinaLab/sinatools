from transformers import BertTokenizer,BertForSequenceClassification
import warnings
warnings.filterwarnings("ignore")
import pandas as pd




from nlptools.DataDownload import downloader
import os 

glosses_dic = {}

model_file_name = "bert-base-arabertv02_22_May_2021_00h_allglosses_unused01"
path =downloader.get_appdatadir()
model_file_path = os.path.join(path, model_file_name)

tokenizer_file_name = "bert-base-arabertv02"
path =downloader.get_appdatadir()
tokenizer_file_path = os.path.join(path, tokenizer_file_name)

dftrue = pd.DataFrame()

# model = BertForSequenceClassification.from_pretrained('{}'.format("bert-base-arabertv02_22_May_2021_00h_allglosses_unused01"),
                                                    #   output_hidden_states = True,
                                                    #   num_labels=2
                                                    #  )

model = BertForSequenceClassification.from_pretrained(model_file_path, output_hidden_states=True, num_labels=2)

tokenizer = BertTokenizer.from_pretrained('{}'.format(tokenizer_file_path))