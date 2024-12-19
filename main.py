from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from storage import Storage

app = FastAPI(
    title="Products API",
    description="API for managing and retrieving product information.",
    version="1.0.0"
)

# Initialize storage
storage = Storage()

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint to check the service status.
    """
    return {"message": "Welcome to the Products API"}

@app.get("/products", tags=["Products"])
async def get_all_products():
    """
    Retrieve all products from the storage.

    Returns:
        List[Dict[str, Any]]: A list of all products stored in the system.
    """
    try:
        products = storage.get_all_products()
        if not products:
            raise HTTPException(status_code=404, detail="No products found.")
        return JSONResponse(content={"products": products})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving products: {str(e)}")
