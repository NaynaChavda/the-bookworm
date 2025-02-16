import pickle
import sys
import os
import csv
import ast
from flask import Flask, render_template, request
import pandas as pd
from typing import List, Dict

# Dynamically add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

app = Flask(__name__)

MODEL_PATH = 'books_model.pkl'
CSV_PATH = 'cleaned_books_data.csv'

def filter_books_by_genres(csv_file: str, target_genres: List[str], match_all: bool = False) -> List[Dict]:
    """
    Filter books from a CSV file based on genres.
    
    Args:
        csv_file (str): Path to the CSV file
        target_genres (List[str]): List of genres to search for
        match_all (bool): If True, books must match all target genres
    
    Returns:
        List[Dict]: List of matching books with their details
    """
    target_genres = [genre.lower() for genre in target_genres]
    matching_books = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                book_genres = [genre.lower() for genre in ast.literal_eval(row['genres'])]
                
                try:
                    row['rating'] = float(row['rating'])
                except (ValueError, KeyError):
                    row['rating'] = 0.0
                
                if match_all:
                    if all(genre in book_genres for genre in target_genres):
                        matching_books.append(row)
                else:
                    if any(genre in book_genres for genre in target_genres):
                        matching_books.append(row)
    
        matching_books.sort(key=lambda x: x['rating'], reverse=True)
        return matching_books
    
    except Exception as e:
        print(f"Error in filter_books_by_genres: {e}")
        return []


# Load the pickle model
with open('book_recommender.pkl', 'rb') as file:
    saved_data = pickle.load(file)

# Simplified recommender class to avoid import
class PickleRecommender:
    def __init__(self, df, genre_freq):
        self.df = df
        self.genre_freq = genre_freq
    
    def get_weighted_recommendations(self, book_title, n_recommendations=8):
        try:
            # Find the input book
            book_idx = self.df[self.df['title'] == book_title].index[0]
            input_book_genres = self.df.iloc[book_idx]['genres']
            
            recommendations = []
            for idx, row in self.df.iterrows():
                if idx == book_idx:
                    continue
                
                # Calculate similarity (simplified version)
                common_genres = set(input_book_genres) & set(row['genres'])
                genre_match = len(common_genres) / len(set(input_book_genres)) if input_book_genres else 0
                
                # Calculate rating factor
                rating_factor = min(float(row['rating']) / 5.0, 1.0) if 'rating' in row and pd.notna(row['rating']) else 0.5
                
                # Final score calculation
                final_score = (
                    genre_match * 0.5 +
                    rating_factor * 0.3
                )
                
                recommendations.append({
                    'title': row['title'],
                    'genres': row['genres'],
                    'final_score': final_score
                })
            
            return sorted(recommendations, key=lambda x: x['final_score'], reverse=True)[:n_recommendations]
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return []


# Create recommender instance
recommender = PickleRecommender(saved_data['df'], saved_data['genre_freq'])


@app.route('/')
def index():
    # Get popular books from the DataFrame
    file_path = 'personal.csv'
    
    # Read the Excel file into a DataFrame
    df = pd.read_csv(file_path)

    # Extract necessary columns from the DataFrame
    special_books = df[['title', 'author', 'cover_url']].to_dict(orient='records')
    
    return render_template('index.html', special_books=special_books)

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    
    try:
        # Get recommendations
        recommendations = recommender.get_weighted_recommendations(user_input)
        
        # Prepare recommendation data
        data = []
        for rec in recommendations:
            item = [
                rec['title'],
                recommender.df[recommender.df['title'] == rec['title']]['author'].values[0],
                ', '.join(rec['genres']),
                recommender.df[recommender.df['title'] == rec['title']]['cover_url'].values[0]
            ]
            data.append(item)
        
        return render_template('recommend.html', data=data)
    
    except Exception as e:
        return render_template('recommend.html', error=str(e))

@app.route('/genrematch')
def genre_match_ui():
    return render_template('genrematch.html')

@app.route('/filter_books', methods=['POST'])
def filter_books():
    genres = [g.strip() for g in request.form.get('genres', '').split(',') if g.strip()]
    match_all = request.form.get('match_all', 'true').lower() == 'true'
    
    try:
        # Use the filter_books_by_genres function
        matching_books = filter_books_by_genres(CSV_PATH, genres, match_all)
        
        # Format the books data
        formatted_books = [{
            'title': book['title'],
            'author': book['author'],
            'genres': book['genres'],
            'rating': book['rating'],
            'cover_url': book.get('cover_url', '')
        } for book in matching_books]
        
        return render_template('genrematch.html', books=formatted_books)
    
    except Exception as e:
        return render_template('genrematch.html', error=f"Error filtering books: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)