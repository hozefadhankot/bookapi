from fastapi import FastAPI
from app.config import Base, engine
from app.routes import router as books_router

# Initialize FastAPI app
app = FastAPI()

# Create all database tables
Base.metadata.create_all(bind=engine)

# Include the router
app.include_router(books_router)
