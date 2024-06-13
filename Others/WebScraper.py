# Description:
# This script performs web scraping to extract product names and prices from a specified webpage. 
# It uses requests to fetch the page content and BeautifulSoup to parse and extract the desired information. 
# The extracted data is then saved to a CSV file using pandas.

# Usage:
# python WebScraper.py

import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page to scrape
url = 'https://example.com/products'

# Perform a GET request to the page
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the products
products = soup.find_all('div', class_='product')

# Lists to store product data
product_names = []
product_prices = []

# Extract data from each product
for product in products:
    name = product.find('h2', class_='product-name').text
    price = product.find('span', class_='product-price').text
    
    product_names.append(name)
    product_prices.append(price)

# Create a DataFrame with the data
df = pd.DataFrame({
    'Product Name': product_names,
    'Product Price': product_prices
})

# Save the data to a CSV file
df.to_csv('products.csv', index=False)

print("Product data saved to 'products.csv'")