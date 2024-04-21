"""
Defines a Flask API for analyzing sentiment of comments retrieved from Feddit.
"""
import json
from datetime import datetime

import requests
import pandas as pd
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from textblob import TextBlob

COMMENTS_URL = "http://localhost:8080/api/v1/comments"

app = Flask(__name__)
api = Api(app)

def analyze_sentiment(comment):
    """
    Analyzes sentiment of a comment using TextBlob.

    Args:
        comment (dict): The comment data.

    Returns:
        dict: The comment data with added sentiment analysis.
    """
    polarity_score = TextBlob(comment['text']).sentiment.polarity
    comment['polarity_score'] = polarity_score
    comment['classification'] = 'positive' if polarity_score >= 0 else 'negative'
    return comment

class ClassFeddit(Resource):
    """
    Represents the API resource for analyzing comments from Feddit.
    """

    def get(self):
        """
        Handles GET requests for analyzing comments.

        Returns:
            Response: JSON response containing analyzed comments.
        """
        subfeddit_id = request.args.get('subfeddit_id')
        limit = request.args.get('limit')
        skip = request.args.get('skip')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        sort_by_polarity = request.args.get('sort_by_polarity')

        if subfeddit_id is not None:
            subfeddit_id = int(subfeddit_id)
            params = {
                "subfeddit_id": subfeddit_id,
                "skip": skip,
                "limit": limit
            }

            response = requests.get(COMMENTS_URL, params=params, timeout=10)
            if response.status_code == 200:
                comments_data = response.json().get('comments', [])
                df_comments = pd.DataFrame(comments_data)

                if start_date and end_date:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                    end_date = datetime.strptime(end_date, '%Y-%m-%d')
                    df_comments['created_date'] = pd.to_datetime(df_comments['created_at'],
                                                                 unit='s')
                    df_comments = df_comments[(df_comments['created_date'] >= start_date) &
                                                (df_comments['created_date'] <= end_date)]
                else:
                    # If date range is not provided, analyze sentiment for all comments
                    df_comments['created_date'] = pd.to_datetime(df_comments['created_at'],
                                                                 unit='s')

                if df_comments.empty:
                    return jsonify({"message": "No comments within the specified date range."})

                # Apply sentiment analysis and classification
                df_comments = df_comments.apply(analyze_sentiment, axis=1)

                if sort_by_polarity:
                    df_comments = df_comments.sort_values(by='polarity_score', ascending=False)

                # Drop unwanted columns
                df_comments = df_comments[['id', 'text', 'polarity_score', 'classification']]

                # Convert DataFrame to JSON
                json_data = df_comments.to_json(orient='records')
                parsed_json_data = json.loads(json_data)

                # Return JSON response
                return jsonify(parsed_json_data)
            return jsonify({"error": f"Error: {response.status_code} - {response.reason}"})
        return jsonify({"error": "Subfeddit ID parameter is missing"})

    def post(self):
        """
        Handles POST requests (if needed in the future).

        Returns:
            Response: JSON response.
        """

    def endpoint_request(self):
        """
        Provides example requests
        """
        print("""
            Sample input endpoints:

            For positive:
            http://127.0.0.1:5000/classfeddit?subfeddit_id=1&limit=100&start_date=2024-04-16&end_date=2024-04-18&sort_by_polarity=true

            For negative:
            http://127.0.0.1:5000/classfeddit?subfeddit_id=1&limit=10&sort_by_polarity=true&skip=30000
            """)

api.add_resource(ClassFeddit, "/classfeddit")

if __name__ == "__main__":
    app.run(debug=True)
