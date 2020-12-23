# -*- coding: utf-8 -*-
# scip plugin
from integration_tests.app.db import Users
from integration_tests.app.entities import User
from integration_tests.app.errors import NotFoundError
from spring_cloud.utils import logging, validate

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

# pypi/conda library
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

# scip plugin
import spring_cloud.context.bootstrap_client as spring_cloud_bootstrap

app = FastAPI()
logger = logging.getLogger("user-service")


class SignInRequest(BaseModel):
    account: str
    password: str


class SignUpRequest(BaseModel):
    name: str
    account: str
    password: str


get_user_load = 0


@app.get("/metrics/get_user_load/load")
def get_load_of_get_user_load_api():
    return get_user_load


@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    global get_user_load
    get_user_load += 1
    user = Users.find_by_id(user_id)
    if not user:
        raise NotFoundError()
    return present_user(user)


@app.post("/api/users/signIn")
def sign_in(request: SignInRequest):
    logger.info(f"Signing in the user with account={request.account}.")
    user = Users.find_by_account_and_password(request.account, request.password)
    logger.info(f"Successfully Signed in the user (id={user.id}, name={user.name}).")
    return present_user(user)


@app.post("/api/users/signUp")
def sign_up(request: SignUpRequest):
    logger.info(f"Signing up the user with (name={request.name}, account={request.account}).")
    user = Users.save(User(**request.__dict__))
    logger.info(f"Successfully Signed up the user (id={user.id}, name={user.name}).")
    return present_user(user)


def present_user(user: User):
    return {"id": user.id, "name": user.name, "account": user.account}


@app.on_event("shutdown")
def shutdown_event():
    client.shutdown()


if __name__ == "__main__":
    # standard library
    import os

    port = int(os.getenv("port") or 80)
    eureka_server_url = validate.not_none(os.getenv("eureka-server-url"))
    client = spring_cloud_bootstrap.enable_service_discovery(
        service_id="user-service", port=port, eureka_server_urls=[eureka_server_url]
    )
    uvicorn.run(app, host="0.0.0.0", port=port)
