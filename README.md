# the-bookworm

The Bookworm is a book recommendation system based on the concept of content-based filtering. It recommends books based on the content (genres) of the books themselves, rather than relying on user interactions or collaborative data. Specifically, it uses genre similarity, popularity, and ratings to generate recommendations, which are all content-based features. 

The homepage:
![the-bookworm](static/images/index_result1.png)
![the-bookworm](static/images/index_result2.png)

The recommendations page:
![the-bookworm](static/images/recommend_result1.png)
![the-bookworm](static/images/recommend_result2.png)

The genre-match page:
![the-bookworm](static/images/genre_result1.png)
![the-bookworm](static/images/genre_result2.png)

## About the Dataset
The file summary_extract.ipynb is a Jupyter Notebook that contains a Python script for scraping book data from Goodreads and displaying it in a structured format. The script uses a class to scrape book details from Goodreads lists. It extracts information such as title, author, rating, summary, genres, and cover URL. The scraped data is saved to a CSV file named books_dataset.csv.
Another class is defined for displaying the saved data. It provides functionalities to print basic dataset information, detailed book information, and tabulated data.

## Data Pre-processing
The collected data is in raw format, and hence needs processed. This is done as displayed in the preprocessing.ipynb file. Some of the included cleaning steps include:
- Fixes encoding issues in textual data using ftfy, ensuring proper character representation.
- Detects the language of book titles and keeps only English entries.
- Removes rows with missing or invalid entries to maintain data quality.
- Eliminates redundant records to avoid biased analysis.
The final cleaned data is stored as cleaned_books_data.csv.

## Recommendation Model Creation
The model.ipynb file shows implementation of a book recommendation system that suggests books based on genre similarity, popularity, and user ratings. It processes a dataset of books, computes genre frequencies, and generates recommendations by combining these factors into a weighted score. The system can save and load its state using serialization, allowing for reuse without retraining. The basic mechanism includes:

### Genre Similarity Calculation:
 - The function _compute_genre_similarity() calculates the similarity between two books by comparing the intersection over the total set of genres.
 - This similarity measure helps prioritize books with the most overlapping genres.
### Weighted Scoring Formula:
 - To rank books, the system combines multiple factors into a weighted score:
   Final Score = (0.5 × Genre Similarity) + (0.3 × Rating Factor) + (0.2 × Popularity Bonus)
 - Genre Similarity (50%)
   1. Measures how many genres two books have in common.
   2. Books with a higher genre overlap get a better score.
 - Rating Factor (30%)
   1. Books with higher user ratings (out of 5) are preferred.
   2. If a book’s rating is missing, a default mid-range rating is assumed.
 - Popularity Bonus (20%)
   1. More popular genres (those occurring frequently in the dataset) get a small boost.
   2. The most popular genre is used as a normalization factor to scale this value.

When a user provides a book title, the system:
1.Finds the Book in the dataset.
2.Extracts Its Genres to serve as a reference for similarity comparisons.
3.Iterates Over Other Books and calculates their final scores based on genre similarity, rating, and popularity.
4.Sorts Books by Score in descending order and returns the top N recommendations.

The final model is saved as a Pickle file named book_recommender.pkl.

## Genre-based search Model Creation
The genre_match.ipynb displays creation of a simple model that filters books from a CSV file based on genre criteria. The code allows filtering books based on one or more genres, with options to match any or all specified genres. The filtering criteria is set to Match all genres (strictly filter books that contain every specified genre). 
The final model is saved as a Pickle file named books_model.pkl.

## Setting up the Project

### 1. Clone the Repository
```sh
git clone https://github.com/NaynaChavda/the-bookworm.git
```

### 2. Navigate to the Project Directory
```sh
cd the-bookworm
```

### 3. Create a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
```
Activate it:
For Windows:
```sh
venv\Scripts\activate
```
For Mac/Linux:
```sh
source venv/bin/activate
```

### 4. Install Dependencies
```sh
pip install -r requirements.txt
```

### 5. Run the Application
```sh
python app.py
```

## Usage
The home page displays the personal list of book recommendations ftom 'the bookworm'.
The recommendation page gives a list of book titles similar to a given title.
The genre match page gives a list of books of given genres.
