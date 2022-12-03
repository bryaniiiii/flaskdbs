from functools import wraps
import jwt
from flask import request, abort
import os
import datetime

from app.models.UserModel import UserModel

SECRET_KEY = os.getenv('SECRET_KEY')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user= UserModel().get_by_id(data["UserID"])
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated

def generate_token(username):
    token = jwt.encode({
        'user': username,
        'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=30)
      }, SECRET_KEY,algorithm="HS256"
    )
    return token