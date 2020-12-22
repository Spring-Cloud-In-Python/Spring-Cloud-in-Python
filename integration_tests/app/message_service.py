# -*- coding: utf-8 -*-
# standard library
from typing import Optional

# pypi/conda library
import requests
from pydantic import BaseModel

# scip plugin
from integration_tests.app.db import Messages
from integration_tests.app.entities import Message
from spring_cloud.utils import logging

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

# pypi/conda library
import uvicorn
from fastapi import FastAPI, Header

# scip plugin
import spring_cloud.context.bootstrap_client as spring_cloud_bootstrap

spring_cloud_bootstrap.enable_service_discovery()
app = FastAPI()
logger = logging.getLogger("message-service")


class CreateMessageRequest(BaseModel):
    content: str


@app.get("/api/messages")
def get_messages():
    logger.info("Get Messages...")
    messages = Messages.find_all()

    results = []
    for message in messages:
        poster = __request_poster(message.poster_id)
        results.append(__present_message(message, poster))

    logger.info(f"Messages: {[str(m) for m in results]}.")
    return results


@app.post("/api/messages")
def create_message(request: CreateMessageRequest, poster_id: Optional[int] = Header(None, convert_underscores=True)):
    logger.info(f"Creating a message: {request.content}.")
    message = Messages.save(Message(poster_id, request.content))
    logger.info(f"Successfully created a message (id={message.id}, poster_id={message.poster_id})")
    return message


def __request_poster(poster_id):
    user_service_host = os.getenv("user-service-host")
    url = f"http://{user_service_host}/api/users/{poster_id}"
    logger.info(f"Requesting to: {url}.")
    return requests.get(url).json()


def __present_message(message: Message, poster):
    return {"id": message.id, "content": message.content, "poster": poster}


if __name__ == "__main__":
    # standard library
    import os

    port = int(os.getenv("port"))
    uvicorn.run(app, host="0.0.0.0", port=port)
