from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
import pandas as pd


my_path = 'fight-page-table-dump/'

files = [f for f in listdir(my_path) if isfile(join(my_path, f))]

#for file in files:
#    print(file)
for ff in files:
    fight_file=open(my_path + ff, "r")
    
    
    bs=BeautifulSoup(fight_file.read(), 'html.parser')
    
    #print(files[0])
    
    tdList = bs.find_all('td')
    i = 0
    
    winners = []
    losers = []
    weight_classes = []
    for td in tdList:
        #print(f"{i}, {td}")
        if i%8 == 1:
            winner=td.get_text()
            winner=winner.rstrip("n")
            winner=winner.rstrip("\\")
            #print(winner)
            winners.append(winner)
        if i%8 == 3:
            loser=td.get_text()
            loser=loser.rstrip("n")
            loser=loser.rstrip("\\")
            losers.append(loser)
        if i%8 == 0:
            weight_class=td.get_text()
            weight_class=weight_class.rstrip("n")
            weight_class=weight_class.rstrip("\\")
            weight_classes.append(weight_class)
        
        i=i+1
        
        
    df = pd.DataFrame(list(zip(winners, losers, weight_classes)), 
                      columns=['winner', "loser", "weight_class"])
    
    #display(df)
    
    #Strip the table part
    event_name = ff[:-6]
    
    df["event"] = event_name
    #display(df)
    
    df.to_csv(f'fight-dataframes/{event_name}.csv')