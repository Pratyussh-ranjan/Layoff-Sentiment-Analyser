# backend.py
from flask import Flask, jsonify
from flask_cors import CORS
import threading
from selenium import webdriver
import random
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ChromeOptions
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import re

app = Flask(__name__)
CORS(app)

# Twitter Functions
def run_twitter_backend():
    # Define a function to clean the text
    def clean_tweet(text):
        text = re.sub(r'http\S+', '', text)  # Remove URLs
        text = re.sub(r'@\w+', '', text)     # Remove mentions
        text = re.sub(r'#\w+', '', text)     # Remove hashtags
        text = re.sub(r'[^A-Za-z0-9\s]+', '', text)  # Remove special characters
        text = re.sub(r'\s+', ' ', text).strip()  # Remove extra whitespace
        return text


    def search_in_explore(driver, search_query):
        # Wait for the search bar to be visible in the Explore section
        search_bar = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[data-testid="SearchBox_Search_Input"]')))
        search_bar.clear()
        search_bar.send_keys(search_query)
        search_bar.send_keys(Keys.ENTER)



    def scrape_posts():
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2.5, 4.5))

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2.5, 4.5))

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2.5, 4.5))

        soup = BeautifulSoup(driver.page_source, features='lxml')

        posts_data = []

        all_posts = soup.find_all('div', class_='css-146c3p1 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim')
        for post in all_posts:
            post_text = post.get_text().strip()
            posts_data.append([post_text])

        return posts_data



    def save_to_csv(data, filename):
        with open(filename, 'a', newline='\n', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)



    nltk.download('vader_lexicon')


    # Example usage of the function
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=options)
    url = "https://twitter.com/i/flow/login"
    driver.get(url)

    # Wait for the username input to be visible and enter the username
    username = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
    username.send_keys("@VaibhavPra87631")
    username.send_keys(Keys.ENTER)

    # Wait for the password input to be visible and enter the password
    password = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    password.send_keys("vaibhav@4076")
    password.send_keys(Keys.ENTER)

    # Wait for the login process to complete
    time.sleep(10)

    # Wait for the Explore button to be visible and click on it
    explore_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/explore"]')))
    explore_button.click()

    # Wait for the Explore section to load
    time.sleep(5)

    # Call the search function
    search_query = "layoff lang:hi -filter:links"
    search_in_explore(driver, search_query)

    posts_data = scrape_posts()
    all_posts_csv_file = 'all_x_posts.csv'
    save_to_csv(posts_data, all_posts_csv_file)



    print(f"All posts stored in {all_posts_csv_file} file.")
    print("\n")


    # Load the dataset
    file_path = 'all_x_posts.csv'  # Replace with the path to your CSV file
    df = pd.read_csv(file_path, on_bad_lines='skip')

    # Display the first few rows to understand the structure
    # print("Initial Data:")
    # print(df.head())

    # Assuming 'text' is the column containing the tweets; adjust if necessary
    if 'text' in df.columns:
        df['text'] = df['text'].apply(clean_tweet)

    # Drop rows with missing values
    df.dropna(inplace=True)

    # Ensure each post is on a single line
    df['text'] = df['text'].str.replace('\n', ' ')

    # Save the cleaned data to a new CSV file
    cleaned_file_path = 'cleaned_x.csv'  # Replace with your desired output path
    df.to_csv(cleaned_file_path, index=False)

    # print(f"Cleaned data saved to {cleaned_file_path}")

    # Display the first few rows of the cleaned data
    # print("Cleaned Data:")
    # print(df.head())

    train_file_path = './train_dataset.csv'  # Replace with the path to your training CSV file
    train_df = pd.read_csv(train_file_path, on_bad_lines='skip')

    # Drop rows with missing values
    train_df.dropna(inplace=True)

    X_train, X_test, y_train, y_test = train_test_split(train_df['text'], train_df['sentiment'], test_size=0.2, random_state=42)

    # Initialize CountVectorizer for text preprocessing
    vectorizer = CountVectorizer(stop_words='english')

    # Fit and transform the training data, transform the test data
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Initialize and train the Naive Bayes classifier
    nb_classifier = MultinomialNB()
    nb_classifier.fit(X_train_vec, y_train)

    # Predict the sentiment labels for the test set
    y_pred = nb_classifier.predict(X_test_vec)

    # Evaluate the classifier's performance
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f'Accuracy: {accuracy}')

    # Split the training data into features and labels
    X_train = train_df['text']
    y_train = train_df['sentiment']

    # Initialize CountVectorizer for text preprocessing
    vectorizer = CountVectorizer(stop_words='english')

    # Fit and transform the training data
    X_train_vec = vectorizer.fit_transform(X_train)

    # Initialize and train the Naive Bayes classifier
    nb_classifier = MultinomialNB()
    nb_classifier.fit(X_train_vec, y_train)

    # Load the test dataset
    test_file_path = './cleaned_x.csv'  # Replace with the path to your test CSV file
    test_df = pd.read_csv(test_file_path, on_bad_lines='skip')

    # Drop rows with missing values
    test_df.dropna(inplace=True)

    # Transform the test data using the same vectorizer
    X_test_vec = vectorizer.transform(test_df['text'])

    # Predict the sentiment labels for the test set
    test_df['predicted_sentiment'] = nb_classifier.predict(X_test_vec)

    # Save the classified test data to a new CSV file
    # classified_test_file_path = './output_x.csv'  # Replace with your desired output path
    # test_df.to_csv(classified_test_file_path, index=False)

    # print(f'Classified test data saved to {classified_test_file_path}')

    # Create separate DataFrames for each sentiment category
    positive_df = test_df[test_df['predicted_sentiment'] == 'positive']
    negative_df = test_df[test_df['predicted_sentiment'] == 'negative']
    neutral_df = test_df[test_df['predicted_sentiment'] == 'neutral']

    # Save each sentiment category to a separate CSV file
    positive_file_path = './positive_x.csv'
    negative_file_path = './negative_x.csv'
    neutral_file_path = './neutral_x.csv'

    positive_df.to_csv(positive_file_path, index=False)
    negative_df.to_csv(negative_file_path, index=False)
    neutral_df.to_csv(neutral_file_path, index=False)

    print(f'Positive statements saved to {positive_file_path}')
    print(f'Negative statements saved to {negative_file_path}')
    print(f'Neutral statements saved to {neutral_file_path}')


# LinkedIn Functions
def run_linkedin_backend():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.page_load_strategy = 'normal'
    driver = webdriver.Chrome(options=options)

    def login_linkedin():
        driver.get("https://www.linkedin.com/login")
        driver.maximize_window()

        username = driver.find_element(By.ID, 'username')
        username.send_keys('vaibhavprakash1927@gmail.com')

        password = driver.find_element(By.ID, 'password')
        password.send_keys('vaibhav@4076')

        driver.find_element(By.XPATH, '//*[@type="submit"]').click()
        time.sleep(3)

    def scrape_posts():
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2.5, 4.5))

        soup = BeautifulSoup(driver.page_source, features='lxml')
        posts_data = []

        all_posts = soup.find_all('div', class_='update-components-text relative update-components-update-v2__commentary')
        for post in all_posts:
            post_text = post.get_text().strip()
            posts_data.append([post_text])

        return posts_data

    def search_hashtag(hashtag):
        time.sleep(3)
        search_bar = driver.find_element(By.XPATH, '//input[@placeholder="Search"]')
        search_bar.clear()
        search_bar.send_keys(hashtag)
        search_bar.send_keys(Keys.RETURN)
        time.sleep(3)

    def click_posts_category():
        time.sleep(3)
        posts_tab = driver.find_element(By.XPATH, '//button[text()="Posts"]')
        posts_tab.click()
        time.sleep(3)

    def save_to_csv(data, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)

    nltk.download('vader_lexicon')
    positive_posts = []
    neutral_posts = []
    negative_posts = []

    # Initialize the global counters
    global x, y, z
    x = 0
    y = 0
    z = 0

    def analyze_sentiment(text):
        global x, y, z
        # Create an instance of the SentimentIntensityAnalyzer
        analyzer = SentimentIntensityAnalyzer()
        
        # Analyze the sentiment of the text
        sentiment_scores = analyzer.polarity_scores(text)
        
        # Extract the compound sentiment score
        compound_score = sentiment_scores['compound']
        
        # Classify the sentiment based on the compound score
        if compound_score >= 0.05:
            x += 1
            positive_posts.append([text])
        elif compound_score <= -0.05:
            y += 1
            negative_posts.append([text])
        else:
            z += 1
            neutral_posts.append([text])

    login_linkedin()
    search_hashtag('#layoff')
    click_posts_category()

    posts_data = scrape_posts()
    all_posts_csv_file = 'all_L_posts.csv'
    save_to_csv(posts_data, all_posts_csv_file)

    with open(all_posts_csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            column1 = row[0]
            analyze_sentiment(column1)

    positive_posts_csv_file = 'positive_L.csv'
    save_to_csv(positive_posts, positive_posts_csv_file)
    neutral_posts_csv_file = 'neutral_L.csv'
    save_to_csv(neutral_posts, neutral_posts_csv_file)
    negative_posts_csv_file = 'negative_L.csv'
    save_to_csv(negative_posts, negative_posts_csv_file)

    print(f"All posts stored in {all_posts_csv_file} file.")
    print("Number of posts with positive sentiments:", x)
    print("Number of posts with negative sentiments:", y)
    print("Number of posts with neutral sentiments:", z)

@app.route('/analyze/twitter', methods=['POST'])
def analyze_twitter():
    threading.Thread(target=run_twitter_backend).start()
    return jsonify({"message": "Twitter analysis started"}), 200

@app.route('/analyze/linkedin', methods=['POST'])
def analyze_linkedin():
    threading.Thread(target=run_linkedin_backend).start()
    return jsonify({"message": "LinkedIn analysis started"}), 200

if __name__ == '__main__':
    app.run(debug=True)
