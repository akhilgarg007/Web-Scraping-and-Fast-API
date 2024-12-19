import re

from pydantic import BaseModel, field_validator, HttpUrl


class Product(BaseModel):
    """
    A model representing a product with a name, price, and image URL.
    
    Attributes:
        name (str): The name of the product.
        price (Decimal): The price of the product.
        image (HttpUrl): The URL of the product's image.

    Methods:
        validate_image_url: Validates that the image URL points to a valid image file
                            with one of the specified extensions (jpg, jpeg, png, gif, bmp, webp).
    """

    product_title: str
    product_price: int
    path_to_image: str

    @field_validator("path_to_image")
    def validate_image_url(cls, image_url):
        if image_url:
            # Regular expression to check if URL ends with valid image file extensions
            image_extension_pattern = re.compile(r'https://.*\.(jpg|jpeg|png|gif|bmp|webp)$', re.IGNORECASE)
            if not image_extension_pattern.search(str(image_url)):
                raise ValueError(
                    'Invalid image URL: must point to a valid image file (e.g., jpg, jpeg, png, gif, bmp, webp).'
                )
        return image_url
