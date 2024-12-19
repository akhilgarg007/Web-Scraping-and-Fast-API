# Web Scraping Project with FastAPI

## Overview
This project is a web scraping tool designed to extract product data from the website [https://dentalstall.com/](https://dentalstall.com/). It doesn't require login credentials and uses Beautiful Soup to parse HTML content and extract product details such as the product name, price, and image.

## Technologies Used:
- FastAPI for building the API endpoints.
- BeautifulSoup for scraping and parsing HTML content.
- Pipenv for managing project dependencies.
- Docker and Docker Compose for containerization and orchestration.

## Features:
- Scrapes product details (name, price, image) from [https://dentalstall.com/](https://dentalstall.com/).
- Data is stored in a JSON file for easy access.
- FastAPI endpoints to retrieve scraped product data.

## Prerequisites
Before running the project, ensure that Docker and Docker Compose are installed on your machine. You can download them from the official Docker website: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/).:

## Installation
- Clone the repository and navigate to the project folder.
- Build the services using Docker Compose::
```bash
docker-compose build
```

## Running the Project
**1. Scrape the Product Data**
Run the collect_products.py file to scrape product data from https://dentalstall.com/ and save it to a JSON file:
    - page_count: The number of pages to scrape (default is to scrape all pages).
    - proxy: A proxy URL for scraping (optional)

-   Example usage:

    - To scrape the first 5 pages without a proxy:
    ```bash
    docker-compose run app pipenv run python collect_products.py 5
    ```
    - To scrape the first 5 pages using a proxy:    
    ```bash
    docker-compose run app pipenv run python collect_products.py 5 http://myproxy.com
    ```
The scraped data will be saved to a JSON file named products.json.
**2. Start the FastAPI Application**
After collecting the products, run the FastAPI server using Uvicorn:
```bash
docker-compose up
```
This will start the FastAPI server, and you can access the API at http://127.0.0.1:8000/.

**Available Endpoints:**
- /products: Retrieve a list of all scraped products.
- /redis_test: Test the redis connection using set and get
