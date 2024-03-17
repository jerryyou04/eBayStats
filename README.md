# eBay Price Check Flask Application

The eBay Price Check Flask application allows users to search for average prices of items sold on eBay based on a search term. It scrapes eBay listing data and calculates the filtered final average price, along with the lowest and highest prices in the filtered list.

## Features

- Search eBay listings by keyword.
- Display the filtered final average, lowest, and highest price of search results.
- Show total number of prices analyzed.
- Provide direct link to the eBay search page.

## Installation

Before running the application, ensure you have Python installed on your system. This application was developed with Python 3.8, but it should be compatible with Python 3.6 and newer versions.

Create a Virtual Environment (Recommended) if you're running on a headless environment
Windows:
python -m venv venv
.\venv\Scripts\activate

Unix/MacOS:
python3 -m venv venv
source venv/bin/activate

Install Required Packages
pip install Flask requests beautifulsoup4

## Usage
Run the application with the following command:

python app.py
By default, the Flask server will start on http://127.0.0.1:5000/. Open this URL in your web browser to access the application.

How to Use
Once the application is running, navigate to the home page.
Enter a search term for the eBay item you're interested in, and submit the form.

The application will display the filtered final average price, lowest and highest prices, and the total number of prices analyzed. A direct link to the eBay search results is also provided.

## Requirements
Flask
Requests
BeautifulSoup4

You can install all required packages via pip:
python -m pip install Flask requests beautifulsoup4
python -m pip install Flask requests requests
python -m pip install Flask requests Flask


