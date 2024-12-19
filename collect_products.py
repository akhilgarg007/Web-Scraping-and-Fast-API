import sys
from math import inf

from scraper import Scraper
from storage import Storage
from constants import PRODUCTS_FILE_NAME


class CollectProducts:
    def __init__(self, page_count: int | None = None, proxy: str = None):
        """
        Initialize the CollectProducts instance with page count and optional proxy.

        Args:
            page_count (int): The number of pages to scrape. Default is infinity (scrape all pages).
            proxy (str): Optional proxy URL for scraping requests.
        """
        self.page_count = page_count
        self.proxy = proxy
        self.scraper = Scraper(proxy=self.proxy)

    @staticmethod
    def get_arguments() -> tuple:
        """
        Parse command line arguments to get the page count and proxy (if any).

        Returns:
            tuple: (page_count, proxy) values extracted from command line arguments.
        """
        if len(sys.argv) == 2:
            return int(sys.argv[1]), None
        elif len(sys.argv) == 3:
            return int(sys.argv[1]), sys.argv[2]
        else:
            return inf, None

    def create_products_dict(self) -> list:
        """
        Scrape products from the website.

        Returns:
            list: A list of scraped product dictionaries.
        """
        products = []
        print("Website parsing started...")
        current_page = 1
        while current_page < self.page_count + 1:
            try:
                print(f"Started parsing page {current_page}")
                current_page_products = self.scraper.get_products_of_the_page(current_page)
                if current_page_products:
                    products.extend(current_page_products)
                else:
                    print(f"No products found on page {current_page}. Stopping.")
                    break
                print(f"Completed parsing page {current_page}")
            except Exception as e:
                print(f"Error occurred while scraping page {current_page}: {e}")
                break
            current_page += 1

        print("Website parsing completed!")
        print(f"Open {PRODUCTS_FILE_NAME} file to see the results")
        return products

    def save_products(self, products: list):
        """
        Save the scraped products to a storage file.

        Args:
            products (list): List of product dictionaries to be saved.
        """
        try:
            Storage().write_products(products)
            print(f"Products successfully saved to {PRODUCTS_FILE_NAME}")
        except Exception as e:
            print(f"Error occurred while saving products: {e}")


if __name__ == '__main__':
    page_count, proxy = CollectProducts.get_arguments()
    collect_products = CollectProducts(page_count=page_count, proxy=proxy)
    products = collect_products.create_products_dict()
    if products:
        collect_products.save_products(products)
    else:
        print("No products were scraped.")
