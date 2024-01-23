# Mini Project 1 - Cuisine Recommendation System

This is a simple cuisine recommendation system developed for the COMP4605 Data Mining course (Fall 2023) Mini Project 1.

## Project Description

The goal of this project is to build a cuisine recommendation system based on user preferences and ratings. The system utilizes a dataset consisting of user information, restaurant information, cuisine details, and ratings given by users.

## Dataset

The project uses the following CSV files:
- `userprofile.csv`: User information
- `ratings.csv`: Ratings given by users
- `places.csv`: Restaurant information
- `place_cuisine.csv`: Information about the types of cuisine served by restaurants

## Implementation

The project is implemented in Python and utilizes the pandas and numpy libraries for data manipulation. The main functionalities include:
- Reading and parsing the dataset
- Constructing a user ratings dictionary
- Calculating the overall cuisine rating based on a specific formula
- Displaying a menu for user interaction

## Getting Started

1. Install the required dependencies:
   ```bash
   pip install pandas numpy
2. Run the project
   - python your_project_file.py

## Project Structure
- your_project_file.py: Main Python script containing the project implementation.
- userprofile.csv, ratings.csv, places.csv, place_cuisine.csv: Dataset files.

## Menu Options
1. Select a similarity metric (Euclidean or Pearson).
2. Display cuisine (item) similarity matrix.
3. Select a recommendation model (User-based or Item-based).
4. Set the maximum number of recommendations to be made.
5. List similar persons to a given person, together with their similarity scores.
6. Make a recommendation to a specific user.
7. Exit the program.

## Acknowledgments
This project was developed as part of the COMP4605 Data Mining course.



