from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import random
import time

app = Flask(__name__)

# List of user agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64',
    # Add more user agents as needed
]

# List of proxies - Replace with actual proxies
proxies = [
    'http://50.145.24.181',
    'http://50.217.226.45',
    'http://50.218.57.66',
    'http://50.223.239.183',
    'http://50.168.72.114',
    'http://50.218.57.74',
    'http://50.207.199.80',
    'http://155.94.241.132',
    'http://32.223.6.94',
    'http://50.146.203.174',
    'http://50.220.168.134',
    'http://50.231.110.26',
    'http://50.223.239.194',
    'http://50.174.145.11',
    'http://50.174.145.8',
    'http://50.223.239.168',
    # Add more proxies as needed
]

# Function to fetch Amazon data with proxies and random user agents
def fetch_amazon_data(product_name, max_price=None):
    base_url = "https://www.amazon.in/s"
    params = {
        'k': product_name.replace(' ', '+'),
        'ref': 'nb_sb_noss'
    }

    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'en-US,en;q=0.5'
    }

    try:
        # Send a GET request to the URL with headers, params, and proxies
        proxy = {'http': random.choice(proxies)}
        response = requests.get(base_url, params=params, headers=headers, proxies=proxy, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all product links
        product_links = soup.select('.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')

        # Prepare list to store product data
        products = []

        # Iterate through each product link
        for link in product_links[:5]:  # Limiting to first 5 links for example
            product_url = "https://www.amazon.in" + link['href']
            headers['User-Agent'] = random.choice(user_agents)

            # Send request to product URL with random user agent and proxy
            proxy = {'http': random.choice(proxies)}
            product_response = requests.get(product_url, headers=headers, proxies=proxy, timeout=10)
            product_response.raise_for_status()
            product_soup = BeautifulSoup(product_response.content, 'html.parser')

            # Extract product details
            try:
                name = product_soup.find("span", {'id': 'productTitle'}).get_text(strip=True)
            except AttributeError:
                name = 'Not available'

            try:
                price = product_soup.find("span", {'class': 'a-price-whole'}).get_text(strip=True)
            except AttributeError:
                price = 'Not available'

            try:
                rating = product_soup.find("span", {'class': 'a-icon-alt'}).get_text(strip=True)
            except AttributeError:
                rating = 'Not available'

            # Skip products where price is not available
            if price == 'Not available':
                continue

            # Convert price to float
            try:
                price_float = float(price.replace(',', ''))
            except ValueError:
                continue  # Skip if price cannot be converted to float

            # Filter by max_price if specified
            if max_price and price_float > max_price:
                continue

            # Append product data to list
            products.append({
                'Product Name': name,
                'Link': product_url,
                'Price': price,
                'Rating': rating
            })

            # Add a short delay between requests to avoid rate limiting
            time.sleep(random.uniform(1, 3))

        return products

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Amazon data: {e}")
        return None

# Flask routes
@app.route('/', methods=['GET', 'POST'])
def index():
    products = []
    max_price = None

    if request.method == 'POST':
        product_name = request.form['product_name']
        max_price_str = request.form['max_price']

        if max_price_str:
            max_price = float(max_price_str)

        # Fetch Amazon data with the provided product_name and max_price
        products = fetch_amazon_data(product_name, max_price=max_price)
        
        # If max_price is None (not provided by user), fetch all products
        if max_price is None:
            products = fetch_amazon_data(product_name)

    return render_template('index.html', products=products, max_price=max_price)

if __name__ == '__main__':
    import socket
    import sys

    # Find an available port
    def find_free_port():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        port = sock.getsockname()[1]
        sock.close()
        return port

    port = find_free_port()

    # Run the Flask app
    app.run(port=port, debug=True)

