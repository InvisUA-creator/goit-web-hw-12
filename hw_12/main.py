from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.dbase.dbase import get_db
from src.routes import contacts
from src.routes import auth


app = FastAPI()

app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")


@app.get("/")
def index():
    return {"message": "Welcome to the Contacts API"}


@app.get("/api/healthchecker")
async def healthchecker(dbase: AsyncSession = Depends(get_db)):
    try:
        # Check if the database is reachable
        result = await dbase.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Database is healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
