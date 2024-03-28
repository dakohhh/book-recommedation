# -*- coding: utf-8 -*-
"""BOOK RECOMMENDATION.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lU631nznO_jBJHCr6aYL942NoF4gU6hk
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors


import warnings
warnings.filterwarnings("ignore")

data = pd.read_csv("book_with_genre_dataset.csv")

"""##### VIEWING THE IMPORTED DATASET

"""

data.head(5)

"""#### DATA PREPROCESSING"""

data.info()

data.describe()

"""Checking for missing values"""

data.isnull().sum()

data = data.dropna(subset=['genres'])

data.head(2)

data.drop(["isbn", "isbn13", "ratings_count", "text_reviews_count"], axis=1, inplace=True)

data.head()

data["genres"] = data["genres"].str.split(";")

def split_with_comma(value:list):

  new_list = []

  for i in range(len(value)):

      if "," in value[i]:
          temp_value = value[i]

          new_list.extend(temp_value.split(","))

      else:
          new_list.append(value[i])

  return new_list



data["genres"] = data["genres"].apply(split_with_comma)

"""GETTING ALL UNIQUE GENRES AND ADDING THEM TO A SET"""

unique_genres = set()

for genres in data['genres']:
  unique_genres.update(genres)


unique_genres

for genre in unique_genres:
    data[genre] = data['genres'].apply(lambda x: 1 if genre in x else 0)

preprocessed_data = data.copy()

preprocessed_data.drop(["language_code", "num_pages", "publication_date", "average_rating", "Author", "Title", "publisher"], axis=1, inplace=True)

preprocessed_data.head(2)

preprocessed_data.set_index("Book Id", inplace=True)

preprocessed_data.drop("genres", axis=1, inplace=True)

preprocessed_data

"""NOW WE CAN BUILD OUR RECOMMENDER"""

preprocessed_data.loc[1]

from sklearn.neighbors import NearestNeighbors


nn_model = NearestNeighbors(metric="minkowski")
nn_model.fit(preprocessed_data)

target_book_field = preprocessed_data.loc[28].values.reshape(1, -1)



distances, neighbors = nn_model.kneighbors(target_book_field, n_neighbors=30)

neighbors

data.iloc[17]

row = data.loc[data['Book Id'] == 10432]


list(row["genres"])

data.head(20)

