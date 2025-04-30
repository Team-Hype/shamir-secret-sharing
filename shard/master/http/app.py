# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt
import uvicorn
from shard.master.db.models import User
from shard.master.http.logic import get_current_user, get_db, create_access_token
from shard.master.db import Session
import shard.master.grpc.communication as communication
from shard.master.http.models import KeyValueSecret, KeySecret


app = FastAPI()


# Endpoints
@app.post("/register")
def register(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = bcrypt.hash(form_data.password)
    new_user = User(username=form_data.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully"}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not bcrypt.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"msg": f"Hello, {current_user.username}. This is a protected route."}


@app.get("/")
def public_route():
    return {"msg": "This is a public route."}


@app.post("/store-key")
async def store_key(
    secret : KeyValueSecret,
    current_user: User = Depends(get_current_user)
):
    if await communication.store_key(current_user.id, secret.key, secret.value):
        return status.HTTP_201_CREATED

    raise HTTPException(status_code=400, detail="what happenes???")


@app.post("/get-key")
async def get_key( 
    secret : KeySecret,
    current_user: User = Depends(get_current_user)
):
    try:
        res = await communication.get_key(current_user.id, secret.key)
        return {"secret" : res}
    except:
        raise HTTPException(status_code=404, detail="key not found")