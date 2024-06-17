from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, categories, products, comments

app = FastAPI()

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(comments.router)

# Allow CORS
origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

@app.get("/ping")
def root():
    return {"ping": "pong"}