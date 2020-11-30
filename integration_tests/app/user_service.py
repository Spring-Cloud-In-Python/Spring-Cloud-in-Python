# -*- coding: utf-8 -*-
# scip plugin
from integration_tests.app.db import Users
from integration_tests.app.entities import User

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

# pypi/conda library
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

# scip plugin
import spring_cloud.context.bootstrap as spring_cloud_bootstrap

spring_cloud_bootstrap.enable_service_discovery()
app = FastAPI()


class SignInRequest(BaseModel):
    account: str
    password: str


class SignUpRequest(BaseModel):
    name: str
    account: str
    password: str


@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    user = Users.find_by_id(user_id)
    return present_user(user)


@app.post("/api/users/signIn")
def sign_in(request: SignInRequest):
    user = Users.find_by_account_and_password(request.account, request.password)
    return present_user(user)


@app.post("/api/users/signUp")
def sign_up(request: SignUpRequest):
    user = Users.save(User(**request.__dict__))
    return present_user(user)


def present_user(user: User):
    return {"id": user.id, "name": user.name, "account": user.account}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
