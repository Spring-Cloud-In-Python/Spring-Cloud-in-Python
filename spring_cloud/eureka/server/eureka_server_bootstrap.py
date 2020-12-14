# -*- coding: utf-8 -*-

__author__ = "Ricky"
__license__ = "Apache 2.0"
# pypi/conda library
import uvicorn
from fastapi import FastAPI, HTTPException, Response, status

# scip plugin
from eureka.model.application_model import ApplicationModel
from eureka.model.applications_model import ApplicationsModel
from eureka.model.instance_info_model import InstanceInfoModel
from eureka.server.registry.instance_registry import InstanceRegistry


class EurekaServerBootstrap:
    def __int__(self):
        self._registry = InstanceRegistry()

    def run(self):
        DEFAULT_DURATION = 30

        eureka_server = FastAPI()

        @eureka_server.post("/eureka/v2/apps/{app_id}")
        def register_instance(request: InstanceInfoModel, app_id: str):
            instance_info = request.to_entity()

            if instance_info.app_name != app_id:
                message = "Application name in the url and the request body should be the same."
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=message)

            self._registry.register(instance_info, DEFAULT_DURATION)

            return Response(status_code=status.HTTP_204_NO_CONTENT)

        @eureka_server.delete("/eureka/v2/apps/{app_id}/{instance_id}")
        def cancel_instance(app_id: str, instance_id: str):
            result = self._registry.cancel(app_id, instance_id)

            if not result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cancellation failed.")

            return Response(status_code=status.HTTP_200_OK)

        @eureka_server.get("/eureka/v2/apps/{app_id}")
        def get_application(app_id: str) -> ApplicationModel:
            application = self._registry.get_presenter().query_application(app_id)
            if application is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            return self._registry.get_presenter().query_application(app_id)

        @eureka_server.get("/eureka/v2/apps")
        def get_applications() -> ApplicationsModel:
            return self._registry.get_presenter().query_applications()

        uvicorn.run(eureka_server, host="0.0.0.0", port=8787)


if __name__ == "__main__":
    EurekaServerBootstrap().run()
