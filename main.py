from fastapi import FastAPI
from app.graphql.schema import graphql_app

app = FastAPI(title="JDruwa API")
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def root():
    return {"message": "JDruwa API is running 🚀"}
