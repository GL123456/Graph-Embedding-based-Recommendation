# -*- coding: utf-8 -*-
"""Data Preprocessing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WcYaXcuYltrmKJ5FXnLQMGGJ6XsYI2_R
"""

from google.colab import drive
drive.mount('/content/gdrive')

import json
import pandas as pd
import pickle
import time
import networkx as nx

review_df = pd.read_csv("/content/gdrive/My Drive/8thSemProjectFiles/yelp_review.csv")

keep_review_col=['business_id','user_id','review_id','stars']
review_df=review_df[keep_review_col]

user_df = pd.read_csv("/content/gdrive/My Drive/8thSemProjectFiles/yelp_user.csv") 
user_df.head()

keeps_user_col=['user_id','review_count','average_stars','friends']
user_df=user_df[keeps_user_col]
user_df = user_df.rename(columns={'review_count': 'user_review_count'})
user_df = user_df.rename(columns={'name': 'user_Name'})

high_review_users= user_df.copy()

business_df = pd.read_csv("/content/gdrive/My Drive/8thSemProjectFiles/yelp_business.csv")
business_df.head()

keeps = ['name', 'city',  'stars', 'categories', 'review_count', 'business_id']
business_df = business_df[keeps]

business_df.dropna(how='any')

business_df=business_df[business_df['categories'].str.contains('Restaurants')]

restaurants=business_df

grouped= restaurants['review_count'].groupby(restaurants['city']).sum().reset_index()
grouped.sort_index(ascending=False)

grouped = grouped.sort_values(by = ['review_count'], ascending=[False])

NUM_REVIEW_THRESH = 100
NUM_REVIEW_THRESHB= 100

high_review_restaurants_all = restaurants[restaurants.review_count > NUM_REVIEW_THRESHB].copy()
high_review_restaurants_for_LV = high_review_restaurants_all[(high_review_restaurants_all.city == 'Las Vegas')].copy()
high_review_restaurants_for_Ph = high_review_restaurants_all[(high_review_restaurants_all.city == 'Phoenix')].copy()
high_review_restaurants_for_city = pd.concat([high_review_restaurants_for_LV,high_review_restaurants_for_Ph])

high_review_restaurants_for_city['overall_stars'] = high_review_restaurants_for_city['stars']

high_review_users[high_review_users.user_id == "I-W_at9CPQox-t0xGveymw"]

merged_reviews_bus = review_df.merge(high_review_restaurants_for_city, on='business_id', how='inner')
merged_reviews_user = high_review_users.merge(review_df, on='user_id', how='inner')

merged_reviews_user[merged_reviews_user.user_id == "I-W_at9CPQox-t0xGveymw"]

merged_reviews_bus[merged_reviews_bus.user_id == "I-W_at9CPQox-t0xGveymw"]

del review_df
del high_review_users
del business_df
del restaurants
del grouped
del high_review_restaurants_all
del high_review_restaurants_for_city

unique_users = merged_reviews_bus.user_id.unique()
unique_users = unique_users.tolist()
unique_users_df = pd.DataFrame({"user_id" : unique_users})

unique_users_df.shape

unique_users_details_df = unique_users_df.merge(user_df, on = "user_id", how = "inner")

unique_users_details_df[unique_users_details_df.user_id == "I-W_at9CPQox-t0xGveymw"]

user_friends_df = unique_users_details_df[["user_id","friends"]]

d = dict(zip(user_friends_df.user_id,user_friends_df.friends))

for key in d:
  if(d[key] == 'None'):
    d[key] = []
  else:
    lst_val = d[key].split(",")
    d[key] = lst_val

user_friends_dict = open("user_friends_dict.pickle", "wb")
pickle.dump(d,user_friends_dict)

del user_df

del unique_users_details_df
del unique_users_df

user_friends_df_file = open("user_friends_df.pickle", "wb")
pickle.dump(user_friends_df, user_friends_df_file)
del user_friends_df

review_business_df_file = open("review_business_df.pickle", "wb")
pickle.dump(merged_reviews_bus, review_business_df_file)
del merged_reviews_bus

merged_reviews_user_df_file = open("review_users_df.pickle", "wb")
pickle.dump(merged_reviews_user, merged_reviews_user_df_file)
del merged_reviews_user

del merged_reviews_bus
del merged_reviews_user

friends = user_friends_df["friends"]

users = user_friends_df["user_id"]
users = list(users)

friends_list = []
friends = list(friends)
for f in friends:
  if f is not None:
    f = f.split(",")
    for fr in f:
      friends_list.append(fr)

final_users = list(set(users).intersection(friends_list))
len(final_users)

final_d = {}
c = 0
for user in final_users:
  val = []
  for each in d[user]:
    if(each not in final_users):
      continue
    else:
      val.append(each)
  final_d[user] = val
  print(c)
  c = c + 1

len(final_d)

graph = nx.Graph(final_d)

nx.info(graph)

user_friends_dict_final = open("user_friends_dict_final.pickle", "wb")
pickle.dump(final_d, user_friends_dict_final)

nx.write_gml(graph, "final_graph.gml")

graph.size() #number of edges

from google.colab import files

files.download('user_friends_dict_final.pickle')
files.download('final_graph.gml')

import networkx as nx

graph = nx.read_gml("/content/gdrive/My Drive/8th_Sem_Project PES_293_323_355/final_graph.gml")

from matplotlib import pylab
import matplotlib.pyplot as plt

def save_graph(graph,file_name):
    #initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph,pos)
    nx.draw_networkx_edges(graph,pos)
    nx.draw_networkx_labels(graph,pos)

    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    plt.savefig(file_name,bbox_inches="tight")
    pylab.close()
    del fig

#Assuming that the graph g has nodes and edges entered
save_graph(graph,"my_graph.pdf")

nx.info(graph)

