# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# pypi/conda library
import uvicorn
from fastapi import FastAPI, HTTPException, Response, status

# scip plugin
from eureka.model.application_model import ApplicationModel
from eureka.model.applications_model import ApplicationsModel
from eureka.model.instance_info_model import InstanceInfoModel
from eureka.server.registry.instance_registry import InstanceRegistry

DEFAULT_DURATION = 30

eureka_server = FastAPI()
registry = InstanceRegistry()


@eureka_server.post("/eureka/v2/apps/{app_id}")
def register_instance(request: InstanceInfoModel, app_id: str):
    instance_info = request.to_entity()

    if instance_info.app_name != app_id:
        message = "Application name in the url and the request body should be the same."
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=message)

    registry.register(instance_info, DEFAULT_DURATION)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@eureka_server.delete("/eureka/v2/apps/{app_id}/{instance_id}")
def cancel_instance(app_id: str, instance_id: str):
    result = registry.cancel(app_id, instance_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cancellation failed.")

    return Response(status_code=status.HTTP_200_OK)


@eureka_server.get("/eureka/v2/apps/{app_id}")
def get_application(app_id: str) -> ApplicationModel:
    application = registry.get_presenter().query_application(app_id)
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return registry.get_presenter().query_application(app_id)


@eureka_server.get("/eureka/v2/apps")
def get_applications() -> ApplicationsModel:
    return registry.get_presenter().query_applications()


if __name__ == "__main__":
    # standard library
    import os

    port = int(os.getenv("port"))
    uvicorn.run(eureka_server, host="0.0.0.0", port=port)
