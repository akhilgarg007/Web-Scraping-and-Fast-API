import json
from typing import List, Dict, Any

from constants import PRODUCTS_FILE_NAME


class Storage:
    def write_products(self, products: List[Dict[str, Any]]) -> None:
        """
        Write the list of products to a JSON file.

        Args:
            products (List[Dict[str, Any]]): The list of products to store.
        """
        try:
            with open(PRODUCTS_FILE_NAME, mode="w", encoding="utf-8") as products_file:
                json.dump(products, products_file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error occurred while writing products to file: {e}")

    def get_all_products(self) -> List[Dict[str, Any]]:
        """
        Retrieve all products from the JSON file.

        Returns:
            List[Dict[str, Any]]: A list of products. Returns an empty list if an error occurs or the file is empty.
        """
        try:
            with open(PRODUCTS_FILE_NAME, mode="r", encoding="utf-8") as products_file:
                data = json.load(products_file)
            if not isinstance(data, list):
                raise ValueError("Invalid data format: Expected a list of products.")
            return data
        except FileNotFoundError:
            print(f"File '{PRODUCTS_FILE_NAME}' not found. Returning an empty list.")
            return []
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file '{PRODUCTS_FILE_NAME}'. Returning an empty list.")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []
