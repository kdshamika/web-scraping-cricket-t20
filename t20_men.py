##################################################
#This Python code creates a csv file that contains ball-by-ball data for Sri Lankan vs Indian T20 matches for men
#Data is downloaded from https://cricsheet.org/downloads/ on 10th of October 2022

#Instructions:
    #download the requred data into a folder (for this code, t20s_male_json) in your local computer
    #unzip the folder and t20s_male_json folder contains json files for all match data for countries
    #copy this python script file into a location outside of the unzipped folder
    
#Output: 
    #output of this python script is a csv file that contains all Sri Lankan vs Indian T20 match data 
    
#Changes/modifications to this code: 
    #selected countries can be changed within the for loop
    #to create a csv file for T20 matches, download the relavant file and change file name in variable 'path' 
                         
##################################################
#importing libraries
import json
import os
import glob
import pandas as pd
import re
 
################################################## 
#The following commented lines are to explore data in a single match
# Opening JSON file
# f = open('t20s_male_json/1262757.json')
  
# returns JSON object as a dictionary
# data = json.load(f)

# printing data
# print(json.dumps(data, indent=4))

#match info
# data['info']['teams']
# data['info']['dates']
# data['info']['gender']
# data['info']['match_type']

#to extract total score of the first over
# data['innings'][0]['overs'][0]['deliveries'][3]['runs']['total']
#####################################################

#unzipped folder downloaded from the website
#this file contains men odt match data for all avalable countries
path = 't20s_male_json'

#for loop is to extract only Sri Lanka vs India match files only
#and saving into a csv file, as the output
#match_id is the unique identifier and it is same as the downloaded json file names 
for filename in glob.glob(os.path.join(path, '*.json')):
    f = open(filename)
    data = json.load(f)
    teams = data["info"]["teams"]
    if "Sri Lanka" in teams and "India" in teams:
        records = []
        innings = data['innings']
        for i in range(len(innings)):
            inning = innings[i]
            overs = inning['overs']
            for o in range(len(overs)):
                over = overs[o]
                deliveries = over['deliveries']
                for d in range(len(deliveries)):
                    delivery = deliveries[d]
                    runs = delivery["runs"]
                    extras = delivery["extras"] if "extras" in delivery else None
                    wickets= 1 if "wickets" in delivery else 0
                    records.append({
                        "match_id": re.search('(\d+).json$', filename, re.IGNORECASE).group(1),
                        "inning": i+1,
                        "target": inning["target"]["runs"] if i%2 == 1 else None,
                        "team": inning["team"],
                        "over": over["over"],
                        "delivery": d+1,
                        "batsman_striker": delivery["batter"],
                        "batsman_non_striker": delivery["non_striker"],
                        "bowler": delivery["bowler"],
                        "runs_striker": runs["batter"],
                        "runs_extras_byes": extras["byes"] if extras is not None and "byes" in extras else 0,
                        "runs_extras_legbyes": extras["legbyes"] if extras is not None and "legbyes" in extras else 0,
                        "runs_extras_wides": extras["wides"] if extras is not None and "wides" in extras else 0,
                        "runs_extras_noballs": extras["noballs"] if extras is not None and "noballs" in extras else 0,
                        "runs_extras_total": runs["extras"],
                        "runs_total": runs["total"],
                        "wickets": wickets 
                    })
        df = pd.json_normalize(records)
        df.to_csv("final_t20_men_SL_IND.csv",index=False,mode="w",line_terminator="") if i == 0 else df.to_csv("final_t20_men_SL_IND.csv",index=False,mode="a",header=False,line_terminator="")
			
########################################
#calculating required parameters for the SDE

df = pd.read_csv("final_t20_men_SL_IND.csv",names=['match_id', 'inning', 'target', 'team', 'over', 'delivery', 'batsman_striker', 'batsman_non_striker', 'bowler', 'runs_striker', 'runs_extras_byes', 'runs_extras_legbyes', 'runs_extras_wides', 'runs_extras_noballs', 'runs_extras_total', 'runs_total', 'wickets'])
print(df.head())

#checking maximum total runs 
df["runs_total"].max()
#answer: 7

#number of SL vs IND matches
no_of_matches=df["match_id"].nunique()
no_of_matches
#answer: 25

#number of balls per match
no_of_balls_per_match=df["match_id"].value_counts()
no_of_balls_per_match

#total number of balls (number of records) per team
total_balls_sl=df[df["team"]=="Sri Lanka"]["runs_total"].count()
total_balls_sl
#answer: 2933

total_balls_ind=df[df["team"]=="India"]["runs_total"].count()
total_balls_ind
#answer: 2986

#counting balls and wickets per team
count_sl_ind_runs_wickets=df.groupby(["team","runs_total","wickets"])["match_id"].count()

#to calculate probabilities
df_prob=count_sl_ind_runs_wickets.to_frame()
df_prob.rename(columns = {'match_id':'count'}, inplace = True)
df_prob.to_csv("count_sl_ind_runs_wickets_t20.csv",index=True)















