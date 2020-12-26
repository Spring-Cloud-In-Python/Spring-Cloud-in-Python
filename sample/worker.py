# -*- coding: utf-8 -*-
# standard library
import time
from typing import List

# scip plugin
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
load = 0


class SumRequest(BaseModel):
    numbers: List[int]


@app.post("/api/sum")
def sign_in(request: SumRequest):
    global load
    load += 1
    numbers = request.numbers
    if len(numbers) == 1:
        return numbers[0]
    sum1 = int(client.post("http://sum-service/api/sum", json={"numbers": numbers[::2]}).text)
    sum2 = int(client.post("http://sum-service/api/sum", json={"numbers": numbers[1::2]}).text)
    logger.info(f"Sum: {numbers[::2]} + {numbers[1::2]} = {sum1 + sum2}")
    return sum1 + sum2


@app.get("/api/sum/load")
def get_load():
    return load


@app.on_event("shutdown")
def shutdown_event():
    client.shutdown()


if __name__ == "__main__":
    # standard library
    import os

    time.sleep(3)
    port = int(os.getenv("port") or 80)
    eureka_server_url = validate.not_none(os.getenv("eureka-server-url"))
    client = spring_cloud_bootstrap.enable_service_discovery(
        service_id="sum-service", port=port, eureka_server_urls=[eureka_server_url]
    )
    logger = logging.getLogger(f"sum:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
