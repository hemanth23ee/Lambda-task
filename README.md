# Amazon Product Scraper

## Overview

This project is a web application built with Flask and Python that allows users to search for products on Amazon and display their details such as name, price, rating, and a link to view them on Amazon's website. The application uses web scraping techniques to fetch real-time data from Amazon, providing users with up-to-date information.

## Features

- **Product Search:** Users can enter a product name and optionally specify a maximum price.
- **Dynamic Display:** Results are displayed in a table format, showing product details that match the search criteria.
- **Styling:** The interface is styled with CSS to enhance readability and user experience.
- **Error Handling:** Includes handling for various errors such as server errors (503), connection issues, and data parsing errors.
- **Random Proxies and User Agents:** Utilizes random selection of proxies and user agents to prevent IP blocking and ensure reliable data retrieval from Amazon.

## Technologies Used

- **Python:** Backend programming language.
- **Flask:** Micro web framework used for routing and handling requests.
- **Requests:** HTTP library for making requests to Amazon's website.
- **Beautiful Soup:** Python library for parsing HTML and XML documents.
- **HTML/CSS:** Frontend components for user interface and styling.
- **Jinja2:** Template engine for rendering data dynamically in HTML.

## Usage:
-Enter a product name in the search field.
-Optionally, specify a maximum price to filter results.
-Click the "Search" button to fetch and display product details.

## Setup Instructions

1. **Clone Repository:**
   ```bash
   git clone <repository-url>
   cd amazon-product-scraper
2. **Install Dependencies:**
 ```bash
   pip install -r requirements.txt
3.**Run the Application:**
```bash
python app.py

