import json
from typing import List, Dict, Any

from constants import PRODUCTS_FILE_NAME


class Storage:
    def write_products(self, products: List[Dict[str, Any]]) -> None:
        """
        Write the list of products to a JSON file. Only update the product if the price or image has changed.

        Args:
            products (List[Dict[str, Any]]): The list of products to store.
        """
        try:
            # Load existing products
            existing_products = self._load_existing_products()

            # Initialize a counter for updated or added products
            updated_count = 0  

            for new_product in products:
                existing_product = self._find_product_by_title_and_image(
                    existing_products, new_product['product_title'], new_product['path_to_image']
                )

                if existing_product:
                    if self._has_price_changed(existing_product, new_product):
                        self._update_product(existing_products, existing_product, new_product)
                        updated_count += 1
                else:
                    existing_products.append(new_product)
                    updated_count += 1

            # Save the updated products back to the file
            self._save_products(existing_products, updated_count)

        except Exception as e:
            print(f"Error occurred while writing products to file: {e}")

    def _load_existing_products(self) -> List[Dict[str, Any]]:
        """Load existing products from the file."""
        try:
            with open(PRODUCTS_FILE_NAME, mode="r", encoding="utf-8") as products_file:
                return json.load(products_file)
        except FileNotFoundError:
            return []  # Return an empty list if the file doesn't exist
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file '{PRODUCTS_FILE_NAME}'. Returning an empty list.")
            return []
        except Exception as e:
            print(f"Error occurred while loading the products: {e}")
            return []

    def _find_product_by_title_and_image(self, products: List[Dict[str, Any]], title: str, image: str) -> Dict[str, Any]:
        """Find a product by both title and image path."""
        return next((product for product in products if product.get('product_title') == title and product.get('path_to_image') == image), None)

    def _has_price_changed(self, existing_product: Dict[str, Any], new_product: Dict[str, Any]) -> bool:
        """Check if the product's price has changed."""
        return existing_product['product_price'] != new_product['product_price']

    def _update_product(self, products: List[Dict[str, Any]], existing_product: Dict[str, Any], new_product: Dict[str, Any]) -> None:
        """Update the product in the list."""
        index = products.index(existing_product)
        products[index] = new_product  # Replace the old product with the updated one

    def _save_products(self, products: List[Dict[str, Any]], updated_count: int) -> None:
        """Save products to the JSON file."""
        try:
            with open(PRODUCTS_FILE_NAME, mode="w", encoding="utf-8") as products_file:
                json.dump(products, products_file, indent=4, ensure_ascii=False)
            
            if updated_count > 0:
                print(f"{updated_count} products were updated or added.")
            else:
                print("No products were updated or added.")
        except Exception as e:
            print(f"Error occurred while saving products to file: {e}")

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
        except ValueError as ve:
            print(f"Error in data format: {ve}. Returning an empty list.")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []
