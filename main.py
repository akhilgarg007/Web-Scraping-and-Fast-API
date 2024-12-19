from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from redis.asyncio import Redis

from settings import settings
from storage import Storage


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        password=settings.redis_password
    )

    print("Connected to Redis")
    yield  # Application runs during this context
    print("Disconnecting from Redis...")

    # Close Redis connection on shutdown
    app.state.redis.close()
    await app.state.redis.wait_closed()
    print("Redis connection closed")

app = FastAPI(
    title="Products API",
    description="API for managing and retrieving product information.",
    version="1.0.0",
    lifespan=lifespan
)

# Initialize storage
storage = Storage()

@app.get("/")
async def root():
    """
    Root endpoint to check the service status.
    """
    return {"message": "Welcome to the Products API"}

@app.get("/products")
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

@app.get("/redis_test")
async def redis_test():
    # Set and get a value in Redis
    await app.state.redis.set("key", "value")
    value = await app.state.redis.get("key")
    return {"key": value}
