from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
import pandas as pd

final_df = pd.DataFrame()
my_path = 'fight-dataframes/'

files = [f for f in listdir(my_path) if isfile(join(my_path, f))]

for ff in files:

    df = pd.read_csv(my_path + ff)
    
    print(df.columns)
    
    df = df.drop('Unnamed: 0', axis=1)
    final_df = pd.concat([df, final_df])
    
final_df.to_csv('final_df.csv')

