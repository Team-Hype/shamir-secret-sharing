# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt
import uvicorn
from models import User
from logic import get_current_user, get_db, create_access_token
from db import Session

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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")