# User-based-Collaborative-Filtering
User-based Collaborative Filtering in Python
(Adapted from University of Minnesota CSci 1901H Class project)

## Overview

Implement a simple user-based collaborative filtering recommender system for predicting the ratings of an item using the data given. This prediction should be done using k nearest neighbors and Pearson correlation. Finally using the similarity of the k nearest neighbors, it is required to predict the ratings of the new item for the given user.

## Format of ratings file
- The input file consists of one rating event per line. Each rating event is of the form: user_id\trating\tmovie_title
- The user_id is a string that contains only alphanumeric characters and hyphens and spaces (no tabs).
- The rating is one of the float values 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, and 5.0.
- The movie_title is a string that may contain space characters (to separate the words).
- The three fields -- user_id, rating, and the movie_title -- are separated by a single tab character (\t).

## Requirements

1. pearson_correlation(user1, user2)
- This function calculates the pearson correlation between 2 users.
- Return value is a float between 1 and -1.
- For calculating the average for each user, include all the user’s ratings and not just the intersection
of the 2 user’s ratings.
- However when computing summation, use only items that both users have rated.
2. K_nearest_neighbors(user1, k) :
- This function calculates the k nearest neighbors of user1 based on pearson similarity.
- Returns a list of k nearest neighbors and their similarity.
- For calculating the average for each user, include all the user’s ratings and not just the intersection
of the 2 user’s ratings.
- However when computing summation, use only items that both users have rated.
- When sorting similarities, if 2 users have the same similarity sort them by user id.
3. Predict(user1, item, k_nearest_neighbors) :
- This function calculates the final prediction for item for user1 using k nearest neighbors.
- You will compute a simple weighted average of the ratings provided by the k nearest neighbors.
- Use only the neighbors who have rated the input item.
- Prediction = ∑(Wi,1)*(rating i,item) / ∑(Wi,1) where Wi,1 is the similarity of user i with user1 from
the k nearest neighbors.

## Execution
Python collabFilter.py ratings-dataset.tsv Kluver ‘The Fugitive’ 10
ratings-dataset.tsv: input file Kluver: User id
Movie: The Fugitive
K: 10

## Output:

The program will output:
- K nearest neighbors with their user ids and similarity values separated by space as per the output
file
- Rating prediction for item.

