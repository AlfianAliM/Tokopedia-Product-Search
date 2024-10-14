# Scrape Product Tokopedia

This is a Streamlit application that allows users to search for products on Tokopedia by entering a keyword. The app utilizes the Tokopedia GraphQL API to fetch product data and displays relevant information.

## Features

- User-friendly interface to input search keywords.
- Fetches product data using Tokopedia's GraphQL API.
- Displays product details including name, price, image, rating, and more.

## Requirements

To run this application, you need the following Python packages:

- Streamlit
- Requests
- Pandas
- gspread
- oauth2client

You can install the required packages using pip:

```bash
pip install streamlit requests pandas gspread oauth2client

```

How to Run the Application
Clone this repository to your local machine.
Navigate to the directory where the application file is located.
Run the application with the following command:

```
streamlit run app.py
```

You need to create the credentials.json file to send it to the spreadsheet.
