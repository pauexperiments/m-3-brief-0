from fastapi import FastAPI
from routes_regions import router as regions_router
from routes_borrowers import router as borrowers_router

APP_NAME = "Borrower API"


app = FastAPI(title=APP_NAME)

@app.get("/")
def root():
    return {"name": APP_NAME}

app.include_router(regions_router)
app.include_router(borrowers_router)


