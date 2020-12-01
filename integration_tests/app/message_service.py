# -*- coding: utf-8 -*-
# standard library
from typing import Optional

# pypi/conda library
import requests
from pydantic import BaseModel

# scip plugin
from integration_tests.app.db import Messages
from integration_tests.app.entities import Message

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

# pypi/conda library
import uvicorn
from fastapi import FastAPI, Header

# scip plugin
import spring_cloud.context.bootstrap as spring_cloud_bootstrap

spring_cloud_bootstrap.enable_service_discovery()
app = FastAPI()


class CreateMessageRequest(BaseModel):
    content: str


@app.get("/api/messages")
def get_messages():
    messages = Messages.find_all()

    results = []
    for message in messages:
        poster = __request_poster(message.poster_id)
        results.append(__present_message(message, poster))
    return results


@app.post("/api/messages")
def create_message(request: CreateMessageRequest, poster_id: Optional[int] = Header(None, convert_underscores=True)):
    message = Messages.save(Message(poster_id, request.content))
    return message


def __request_poster(poster_id):
    return requests.get(f"http://user-service/api/users/{poster_id}").json()


def __present_message(message: Message, poster):
    return {"id": message.id, "content": message.content, "poster": poster}


if __name__ == "__main__":
    # standard library
    import os

    port = int(os.getenv("port"))
    uvicorn.run(app, host="0.0.0.0", port=port)
