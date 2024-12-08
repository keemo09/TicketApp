from fastapi import FastAPI
from routers.user_router import user_router
from routers.campaign_router import campaign_router
from cron_job import cronjob
from database import Base, engine
import uvicorn
import pdb

app = FastAPI()

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# Include the user router with a prefix and tags
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(campaign_router, prefix="/campaign", tags=["campaign"])
app.include_router(cronjob)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)