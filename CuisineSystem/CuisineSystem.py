# MiniProject1
"""

import pandas as pd
import numpy as np
user_profile = pd.read_csv('userprofile.csv', skiprows=1, delimiter=';', names=['userID', 'Name'])
ratings = pd.read_csv('ratings.csv', skiprows=1, delimiter=';', names=['userID', 'placeID', 'rating', 'food_rating', 'service_rating'])
places = pd.read_csv('places.csv', skiprows=1, delimiter=';', names=['placeID', 'name'])
cuisine = pd.read_csv('place_cuisine.csv', skiprows=1, delimiter=';', names=['placeID', 'cuisine'])
# Step 2: Merge Datasets
print("User Profile Columns:", user_profile.columns)
print("Ratings Columns:", ratings.columns)
print("Places Columns:", places.columns)
print("Cuisine Columns:", cuisine.columns)

# If the 'user_id' column is present in ratings, adjust the merging accordingly
if 'userID' in ratings.columns:
    merged_data = pd.merge(ratings, user_profile, on='userID')
    merged_data = pd.merge(merged_data, places, on='placeID')
    merged_data = pd.merge(merged_data, cuisine, on='placeID')
else:
    print("No 'user_id' column found in ratings.")

# Step 3: Construct a User Ratings Dictionary
user_ratings = {}

for index, row in merged_data.iterrows():
    userID = row['userID']
    cuisine = row['cuisine']
    rating = row['rating']

    if userID not in user_ratings:
        user_ratings[userID] = {}

    user_ratings[userID][cuisine] = rating

# Example: Print the user ratings for each user
for userID, ratings_dict in user_ratings.items():
    print(f"User {userID} Ratings: {ratings_dict}")

# Step 4: Calculate Overall Cuisine Rating
random_number = np.random.uniform(0, 10, len(merged_data))
merged_data['overall_cuisine_rating'] = (
    (merged_data['rating'] * 1.4 + merged_data['food_rating'] * 2.5 + merged_data['service_rating'] * 1.8 + random_number)
    * merged_data.groupby(['placeID', 'cuisine']).cumcount()  # Rank of the cuisine for that restaurant
)


# Aggregate results based on user and cuisine
user_cuisine_ratings = merged_data.groupby(['userID', 'cuisine'])['overall_cuisine_rating'].mean().reset_index()

# Print the results
print(user_cuisine_ratings)

#step5
merged_data['restaurant_type'] = np.where(merged_data['cuisine'].isnull(), 'Regular Food', 'Specialized Cuisine')
user_restaurant_type_ratings = merged_data.groupby(['userID', 'restaurant_type'])['overall_cuisine_rating'].mean().reset_index()

print(user_restaurant_type_ratings)

#step6

# Assuming you have loaded your place_cuisine.csv file into the place_cuisine DataFrame
place_cuisine = pd.read_csv('place_cuisine.csv', skiprows=1, delimiter=';', names=['placeID', 'cuisine'])

# Sort the place_cuisine DataFrame by 'placeID' and 'cuisine' to ensure proper ordering
place_cuisine_sorted = place_cuisine.sort_values(by=['placeID', 'cuisine'])

# Calculate the normalized rank for each cuisine
place_cuisine_sorted['normalized_rank'] = 2.0 - (place_cuisine_sorted.groupby('placeID').cumcount() / place_cuisine_sorted.groupby('placeID').cumcount().max())

# Print the resulting DataFrame with cuisine ranks
print(place_cuisine_sorted[['placeID', 'cuisine', 'normalized_rank']])

#step7
user_ratings_dict = {}

for index, row in merged_data.iterrows():
    user_name = row['Name']
    cuisine = row['cuisine']
    overall_rating = (row['rating'] + row['food_rating'] + row['service_rating']) / 3.0

    if user_name not in user_ratings_dict:
        user_ratings_dict[user_name] = {}

    if cuisine not in user_ratings_dict[user_name]:
        user_ratings_dict[user_name][cuisine] = []

    user_ratings_dict[user_name][cuisine].append(overall_rating)

# Calculate average ratings for each cuisine for each user
for user_name, cuisine_ratings in user_ratings_dict.items():
    for cuisine, ratings in cuisine_ratings.items():
        avg_rating = sum(ratings) / len(ratings)
        user_ratings_dict[user_name][cuisine] = avg_rating

# Print the resulting dictionary
for user_name, cuisine_ratings in user_ratings_dict.items():
    print(f'"{user_name}": {cuisine_ratings},')

from math import sqrt
person1 = input("İlk person ismini girin: ")
person2 = input("İkinci person ismini girin: ")
#1.similarity
def sim_distance(user_ratings_dict, person1, person2):
    # Get the list of shared_items
    si = {}
    for item in user_ratings_dict[person1]:
        if item in user_ratings_dict[person2]:
            si[item] = 1

    # if they have no ratings in common, return 0
    if len(si) == 0:
        return 0

    # Add up the squares of all the differences
    sum_of_squares = sum([pow(user_ratings_dict[person1][item] - user_ratings_dict[person2][item], 2) for item in si])

    return 1 / (1 + sqrt(sum_of_squares))

# Returns the Pearson correlation coefficient for person1 and person2
def sim_pearson(user_ratings_dict,person1,person2):
  # Get the list of mutually rated items
  si={}
  for item in user_ratings_dict[person1]:
    if item in user_ratings_dict[person2]: si[item]=1

  # if they are no ratings in common, return 0
  if len(si)==0: return 0

  # Sum calculations
  n=len(si)

  # Sums of all the preferences
  sum1=sum([user_ratings_dict[person1][it] for it in si])
  sum2=sum([user_ratings_dict[person2][it] for it in si])

  # Sums of the squares
  sum1Sq=sum([pow(user_ratings_dict[person1][it],2) for it in si])
  sum2Sq=sum([pow(user_ratings_dict[person2][it],2) for it in si])

  # Sum of the products
  pSum=sum([user_ratings_dict[person1][it]*user_ratings_dict[person2][it] for it in si])

  # Calculate r (Pearson score)
  num=pSum-(sum1*sum2/n)
  den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
  if den==0: return 0
  r=num/den
  return r



#2.cuisine sim. matrix
def transformPrefs(user_ratings_dict):
  result = {}
  for person in user_ratings_dict:
      for item in user_ratings_dict[person]:
          result.setdefault(item, {})
          result[item][person] = user_ratings_dict[person][item]
  return result

def topMatches(user_ratings_dict,person,n=5,similarity=sim_pearson):
    scores=[(similarity(user_ratings_dict,person,other),other)
    for other in user_ratings_dict if other!=person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

def calculateSimilarItems(user_ratings_dict, sim=sim_distance, n=10):
      # Create a dictionary of items showing
      # which other items they are most similar to.
      result = {}
      # Invert the preference matrix to be item-centric
      itemRatings = transformPrefs(user_ratings_dict)
      for item in itemRatings:
          # Find the most similar items to this one
          scores = topMatches(itemRatings,item,n,sim_distance)
          result[item] = scores
      return result

#3.select recomendation model user based
user=input("enter the user")
def getRecommendedItems(user_ratings_dict, itemSim, user):
  userRatings = user_ratings_dict[user]
  scores = {}
  totalSim ={}
# Loop over items rated by this user
  for item, rating in userRatings.items():
      # Loop over items similar to this one
          for similarity, item2 in itemSim[item]:
          # Ignore if this user has already rated this item
              if item2 in userRatings: continue
              # Weighted sum of rating times similarity
              scores.setdefault(item2, 0)
              scores[item2] += similarity * rating
              # Sum of all the similarities
              totalSim.setdefault(item2,0)
              totalSim[item2] += similarity
              # Divide each total score by total weighing to get an average
  rankings = [(score/totalSim[item], item) for item, score in scores.items()]
  # Return the rankings from highest to lowest
  rankings.sort(reverse=True)
  return rankings

#4.Take a number of recommendation

def makeRecommendations(user_ratings_dict, sim_distance, user, num_recommendations=5):
    userRatings = user_ratings_dict[user]
    scores = {}
    totalSim = {}

    for (item, rating) in userRatings.items():
        for (similarity, item2) in sim_distance[item]:
            if item2 in userRatings:
                continue
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity

    rankings = [(score / totalSim[item], item) for item, score in scores.items()]
    rankings.sort(reverse=True)
    recommendations = rankings[:num_recommendations]

    return recommendations

#5.select max number of recomendation
from math import sqrt

def listSimilarPersons(prefs, person, similarity_func=sim_distance, max_similar_persons=5):
    scores = [(similarity_func(prefs, person, other), other) for other in prefs if other != person]
    scores.sort(reverse=True)
    similar_persons = scores[:max_similar_persons]
    return similar_persons

#6.rec. for specific person
def makeRecommendations(user_ratings_dict, sim_distance, user, num_recommendations=5):
    """
     It makes suggestions to the user.

     Parameters:
     - user_ratings_dict: Dictionary containing user ratings data.
     - item_similarity_model: Precomputed similarity model.
     - user: The username to make suggestions.
     - num_recommendations: Number of recommendations to make.

     Returns:
     - recommendations: List of recommendations made to the user.
     """
    userRatings = user_ratings_dict[user]
    scores = {}
    totalSim = {}

    # Loop over items rated by this user
    for (item, rating) in userRatings.items():
        # Check if the item exists in the similarity model
        if item not in sim_distance:
            continue

        # Loop over items similar to this one
        for (similarity, item2) in sim_distance[item]:
            # Ignore if this user has already rated this item
            if item2 in userRatings:
                continue
            # Weighted sum of rating times similarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating
            # Sum of all the similarities
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity

    # Divide each total score by total weighting to get an average
    rankings = [(score / totalSim[item], item) for item, score in scores.items()]

    # Return the top N recommendations
    rankings.sort(reverse=True)
    recommendations = rankings[:num_recommendations]

    return recommendations

# Main menu loop
while True:
    print("\nMain Menu:")
    print("1. Select a similarity metric (Euclidean or Pearson).")
    print("2. Display cuisine (item) similarity matrix.")
    print("3. Select a recommendation model (User-based or Item-based).")
    print("4. Set the maximum number of recommendations to be made.")
    print("5. List similar persons to a given person, together with their similarity scores.")
    print("6. Make a recommendation to a specific user.")
    print("7. Exit the program.")
    choice = input("Enter your choice (1-7): ")

    if choice == "1":
        choice = input("Enter your choice for similarity metric (Euclidean or Pearson)(1-2): ")
        if choice == "1":
          print("You selected 1. Select a Euclidean Similarity Metric.")
          person1 = input("İlk person ismini girin: ")
          person2 = input("İkinci person ismini girin: ")
          print(sim_distance(user_ratings_dict, person1 ,person2))
        else :
          print("You selected 1. Select a Pearson Similarity Metric.")
          person1 = input("İlk person ismini girin: ")
          person2 = input("İkinci person ismini girin: ")
          print(sim_pearson(user_ratings_dict, person1 ,person2))
    elif choice == "2":
          similar_items = calculateSimilarItems(user_ratings_dict, sim=sim_distance, n=10)

          print(similar_items)
          for item, scores in similar_items.items():
              print(f"{item}: {scores}")
    elif choice == "3":
        print("You selected 3. Select a recommendation model.")
        user=input("enter the user:")
        recommended_items = getRecommendedItems(user_ratings_dict, similar_items, user)
        print(recommended_items)
    elif choice == "4":
      print("You selected 4. Set the maximum number of recommendations to be made.")
      user = input("Enter the user name:")
      num_recommendations = int(input("Enter the maximum number of recommendations: "))
      user_recommendations = makeRecommendations(user_ratings_dict, similar_items,user, num_recommendations)
      print("\nRecommendations:")
      for score, item in user_recommendations:
          print(f"{item}: {score}")

    elif choice == "5":
        print("You selected 5. List similar persons to a given person, together with their similarity scores.")
        person=input("Enter the person name :")
        print("\nSimilar Persons:")
        for similarity, person in similar_persons:
              print(f"{person}: {similarity}")
    elif choice == "6":
        print("You selected 6. Make a recommendation to a specific user.")
        user = input("ente the user name:")
        user_recommendations = makeRecommendations(user_ratings_dict, similar_items,user, num_recommendations=5)

        print("\nÖnerilenler:")
        for score, item in user_recommendations:
                 print(f"{item}: {score}")
    elif choice == "7":
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 7.")
