# web_data_app.py
# June 2024
# Modified by: Raakin
#
# A simple program for demonstrating web applications using Flask and web scraping of data using Beautiful Soup.
# Detailed specifications are provided via the Assignment 5 README file.

import pandas as pd
from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re

# Initialize our FLASK application object from the Flask class
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    match_object = re.match("[a-zA-Z]+", name)
    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! Welcome to Assignment 5. It's " + formatted_now
    return content

@app.route("/data")
def book_data():
    print("Accessed /data route")
    source = requests.get("http://books.toscrape.com/")
    print("Fetched data from website")
    soup = BeautifulSoup(source.content, 'html.parser')
    print("Parsed HTML content")
    book_results = soup.find_all(attrs={'class': 'product_pod'})
    print(f"Found {len(book_results)} book results")

    titles = []
    prices = []

    for book in book_results:
        try:
            titles.append(book.h3.a.get('title'))
            prices.append(float(book.find('p', class_="price_color").text[1:]))
        except Exception as e:
            print(f"Error extracting data for a book: {e}")

    # Create a DataFrame using the two lists
    try:
        book_data = pd.DataFrame(list(zip(titles, prices)), columns=['Titles', 'Prices'])
        # Calculate the sale price (reduced by 25%) and add it as a new column
        book_data['Sale Price'] = book_data['Prices'] * 0.75
        print(book_data)
    except Exception as e:
        print(f"Error creating DataFrame: {e}")

    # Format and print the DataFrame using the html template provided in the templates subdirectory
    try:
        return render_template('template.html', tables=[book_data.to_html(classes='data')], titles=book_data.columns.values)
    except Exception as e:
        print(f"Error rendering template: {e}")
        return "Error rendering template"

@app.route("/learn")
def learn():
    return "I learned how to create web applications using Flask and how to scrape and manipulate data using BeautifulSoup and Pandas."

if __name__ == '__main__':
    app.run(debug=True)