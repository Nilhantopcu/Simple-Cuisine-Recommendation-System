# Mini Cuisine Recommendation System

This project implements a simple cuisine recommendation system based on user preferences and ratings. The system utilizes a dataset containing user information, restaurant information, cuisine information, and user ratings.

## Project Overview

- **Data Files:**
  - `userprofile.csv`: Contains user identifiers and names.
  - `places.csv`: Contains restaurant identifiers and names.
  - `ratings.csv`: Contains ratings given by users to restaurants.
  - `place_cuisine.csv`: Contains information about the types of cuisine served by some restaurants.

- **Dataset Construction:**
  - Parses CSV files, skips the first lines with column meta-data.
  - Constructs a user rating dictionary.

- **Overall Cuisine Rating Calculation:**
  - Combines general, food, and service ratings to calculate an overall cuisine rating.

- **Cuisine Rank Calculation:**
  - Ranks cuisine based on appearance order in the `place_cuisine.csv` file.

- **User Ratings Dictionary Example:**
  ```python
  {
    "BEDIRHAN": {"Chinese": 2.4, "Turkish": 3.0, ...},
    "MUSTAFA CEBECI": {"Fast_Food": 1.8, "Mexican": 0.9, ...},
    ...
  }

## Menu Options
1. Select Similarity Metric:
   - Choose between Euclidean or Pearson similarity.
2. Display Cuisine Similarity Matrix:
   - View the similarity matrix for cuisines.
3. Select Recommendation Model:
   - Choose between User-based or Item-based recommendation.
4. Set Maximum Recommendations:
   -Set the maximum number of recommendations.
5. List Similar Persons:
   - List persons similar to a given person with their similarity scores.
6. Make Recommendations:
   - Make recommendations to a specific user based on the selected model.
7. Exit:
   - Exit the program.

## Getting Started
To run the program, follow these steps:

1. Clone the repository to your local machine.
2. Ensure you have the required dependencies installed.
3. Run the program in your preferred Python environment.

## Acknowledgments
This project was developed as part of the Data Mining course.



