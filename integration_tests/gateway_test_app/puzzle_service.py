# -*- coding: utf-8 -*-
# standard library

# pypi/conda library

# pypi/conda library
from pydantic import BaseModel

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

# pypi/conda library
import uvicorn
from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/api/puzzle")
def puzzle_endpoint(name: str, token: str = Header(None)):
    return f"HI, {name} ({token}), Question: 1 + 1 = ?"


class Answer(BaseModel):
    content: str


@app.post("/api/answer")
def answer_endpoint(name: str, answer: Answer, token: str = Header(None)):
    result = "correct" if answer.content.strip() == "2" else "wrong"
    return f"HI, {name} ({token}), your answer ({answer}) is {result}."


if __name__ == "__main__":
    # standard library
    import os

    port = int(os.getenv("port"))
    uvicorn.run(app, host="0.0.0.0", port=port)
