from django.shortcuts import render
from django.http import JsonResponse
from django.apps import apps
import csv
import os
import logging
import re
from ntscraper import Nitter  # Correct import

# Load Nitter Scraper
scraper = Nitter()
logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'index.html')

# Preprocessing function
def preprocess_text(text, stop_words):
    text = re.sub(r"[^a-zA-Z]", " ", text)  # Remove special characters
    text = text.lower().split()  # Convert to lowercase & split
    text = [word for word in text if word not in stop_words]  # Remove stopwords
    return " ".join(text)

def fetch_tweets(request):
    """Fetch tweets, save to CSV, and analyze sentiment."""
    if request.method == "POST":
        username = request.POST.get("inputValue", "").strip()
        if not username:
            return JsonResponse({"error": "No username provided."}, status=400)

        try:
            tweets = scraper.get_tweets(username, mode="user", number=5)  # Get 10 tweets
            tweet_list = tweets["tweets"]

            if not tweet_list:
                return JsonResponse({"error": "No tweets found."}, status=404)

            # Path to CSV file
            csv_file_path = os.path.join("static", "tweets.csv")

            # Get sentiment analysis model
            app_config = apps.get_app_config("xapp")
            if not hasattr(app_config, "model") or not hasattr(app_config, "vector"):
                return JsonResponse({"error": "Model or vectorizer not loaded."}, status=500)

            stop_words = {"the", "is", "in", "and", "to", "it"}  # Example stop words

            # Save tweets & analyze sentiment
            analyzed_tweets = []
            with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["username", "content", "sentiment"])  # CSV header

                for tweet in tweet_list:
                    text = tweet["text"]
                    processed_text = preprocess_text(text, stop_words)
                    transformed_text = app_config.vector.transform([processed_text])
                    sentiment = app_config.model.predict(transformed_text)[0]

                    writer.writerow([tweet["user"]["username"], text, sentiment])
                    analyzed_tweets.append({"username": tweet["user"]["username"], "text": text, "sentiment": sentiment})

            return JsonResponse({"tweets": analyzed_tweets})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

def msg(request):
    """Handle sentiment analysis for user comments."""
    if request.method == "POST":
        try:
            text = request.POST.get("inputValue", "").strip()
            if not text:
                return JsonResponse({"error": "No text provided."}, status=400)

            app_config = apps.get_app_config("xapp")
            if not hasattr(app_config, "model") or not hasattr(app_config, "vector"):
                return JsonResponse({"error": "Model or vectorizer not loaded."}, status=500)

            stop_words = {"the", "is", "in", "and", "to", "it"}  # Example stop words
            processed_text = preprocess_text(text, stop_words)
            transformed_text = app_config.vector.transform([processed_text])
            prediction = app_config.model.predict(transformed_text)

            return JsonResponse({"prediction": prediction[0]})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)
