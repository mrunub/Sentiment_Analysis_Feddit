Title: Sentiment Analysis API for Feddit Comments

Description:
This Flask API provides sentiment analysis functionality for comments retrieved from Feddit, allowing users to analyze the sentiment of comments based on various parameters such as subfeddit ID, date range, and polarity.

Features:

Analyzes sentiment of comments retrieved from Feddit using TextBlob.
Allows filtering comments based on subfeddit ID, date range, and polarity.
Supports sorting comments by polarity score.
Provides JSON response containing analyzed comments.
Endpoints:

GET /classfeddit: Analyzes comments based on provided parameters.
Parameters:
subfeddit_id: ID of the subfeddit.
limit: Maximum number of comments to retrieve.
skip: Number of comments to skip.
start_date: Start date of the date range (YYYY-MM-DD).
end_date: End date of the date range (YYYY-MM-DD).
sort_by_polarity: Indicates whether to sort comments by polarity score (true/false).
Returns: JSON response containing analyzed comments or error message.
POST /classfeddit: Handles POST requests (not implemented).
Example Requests:

plaintext
Copy code
Sample input endpoints:

For positive:
http://127.0.0.1:5000/classfeddit?subfeddit_id=1&limit=100&start_date=2024-04-16&end_date=2024-04-18&sort_by_polarity=true

For negative:
http://127.0.0.1:5000/classfeddit?subfeddit_id=1&limit=10&sort_by_polarity=true&skip=30000
Usage:

Ensure the Flask application is running.
Make HTTP GET requests to the specified endpoints with appropriate parameters.
Receive JSON response containing analyzed comments.
Dependencies:

Flask
Flask-RESTful
TextBlob
Requests
Pandas
Note:

This API is designed to analyze comments retrieved from Feddit.
The sentiment analysis is based on the TextBlob library.
Date parameters (start_date, end_date) should be provided in the format 'YYYY-MM-DD'.

