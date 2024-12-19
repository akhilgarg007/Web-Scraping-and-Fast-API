from typing import List, Dict, Optional

from bs4 import BeautifulSoup
import requests

from constants import BASE_URL, TOKEN
from decorators import cached_result_decorator, retry_on_failure
from serializers import Product


class Scraper:
    def __init__(self, proxy: Optional[str] = None):
        """
        Initialize the scraper with an optional proxy.
        
        Args:
            proxy (Optional[str]): Proxy URL to be used for requests.
        """
        self.proxy = proxy

    def generate_url(self, page: int) -> str:
        """
        Generate the URL for a specific page.
        
        Args:
            page (int): The page number.
        
        Returns:
            str: The full URL for the page.
        """
        return f"{BASE_URL}/{page}/"

    @cached_result_decorator(expiry=3600)
    @retry_on_failure(max_attempts=3, retry_delay=1)
    def get_page(self, url: str) -> BeautifulSoup:
        """
        Fetch the content of the page using requests and parse it with BeautifulSoup.
        
        Args:
            url (str): The URL to fetch.
        
        Returns:
            BeautifulSoup: Parsed HTML content of the page.
        """
        proxies = {"https": self.proxy} if self.proxy else None
        try:
            response = requests.get(
                url, proxies=proxies, timeout=10, headers={'Authorization': f'Bearer {TOKEN}'}
            )
            if response.status_code == 404:
                print(f"Page not found (404): {url}. Stopping scraping.")
                return BeautifulSoup()
            response.raise_for_status()  # Raise HTTPError for bad responses
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch page {url}: {e}")
        return BeautifulSoup(response.content, "html.parser")

    async def get_products_of_the_page(self, page: int) -> List[Dict[str, str]]:
        """
        Extract product details (name, price, and image URL) from a given page.
        
        Args:
            page (int): The page number to scrape.
        
        Returns:
            List[Dict[str, str]]: A list of dictionaries with product details.
        """
        url = self.generate_url(page)
        page_content = await self.get_page(url)
        raw_products = page_content.find_all("div", class_="product-inner")

        products = []
        for product in raw_products:
            extracted_product = dict(self._extract_product_details(product))
            if extracted_product:
                products.append(extracted_product)

        return products

    @staticmethod
    def _extract_product_details(product: BeautifulSoup) -> Product:
        """
        Extract details (name, price, and image URL) from a product element.
        
        Args:
            product (BeautifulSoup): The product HTML element.
        
        Returns:
            Dict[str, str]: A dictionary containing product details.
        """
        # Extract product name
        name_tag = product.find("h2", class_="woo-loop-product__title")
        name = name_tag.text.strip() if name_tag else "Unknown"

        # Extract product price
        price_tag = product.find("ins") or product.find("span", class_="woocommerce-Price-amount")
        price = price_tag.text.strip().strip('\u20b9') if price_tag else "Price not available"

        # Extract product image URL
        image_tag = product.find(class_="mf-product-thumbnail").find("img")
        image = image_tag.get("data-lazy-src") or image_tag.get("src") if image_tag else ""
        product_dict = {
            "product_title": name,
            "product_price": price,
            "path_to_image": image,
        }
        try:       
            return Product(**product_dict)
        except Exception as e:
            print(f'An error occurred while parsing product {e} product_data:{product_dict}')
            return {}
