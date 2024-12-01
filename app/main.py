from fastapi import FastAPI
from app.routes import auth
from app.database.mongodb import mongo_connection_obj
from app.utils.utilities import AuthEngine
app = FastAPI()

app.include_router(auth.router)

@app.on_event("startup")
async def startup_db_client():
    try:
        AuthEngine().mongoDb = await mongo_connection_obj()
        AuthEngine().mongoDb.command("ping")
        print(f"Database connection established successfully.")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
