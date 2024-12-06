from fastapi import FastAPI
from app.database import engine, Base
from app.routers import ban, user #, server, character

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(user.router)
app.include_router(ban.router)
#app.include_router(server.router)
#app.include_router(character.router)