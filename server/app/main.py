from fastapi import FastAPI

app = FastAPI(title="NL2SQL API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Welcome to NL2SQL API"}
