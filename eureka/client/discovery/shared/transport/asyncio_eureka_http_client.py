# -*- coding: utf-8 -*-

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# standard library
import asyncio
from typing import Union
from urllib.parse import urljoin

# pypi/conda library
import aiohttp

# scip plugin
from eureka.client.app_info import InstanceInfo
from eureka.client.discovery.shared.transport.eureka_http_client import EurekaHttpClient
from eureka.client.discovery.shared.transport.eureka_http_response import EurekaHttpResponse


class AsyncIOEurekaHttpClient(EurekaHttpClient):
    def __init__(self, service_url: str, connection_timeout: int = 300):
        self._session = None
        self._connection_timeout = connection_timeout
        self._is_shutdown = False
        self._service_url = service_url

    @property
    def connection_timeout(self) -> int:
        return self._connection_timeout

    @connection_timeout.setter
    def connection_timeout(self, connection_timeout: int):
        self._connection_timeout = connection_timeout

    async def register(self, instance: InstanceInfo) -> Union[EurekaHttpResponse, None]:
        # scip plugin
        from eureka.model.instance_info_model import InstanceInfoModel

        session = self._get_session(self._is_shutdown)
        if session:
            eureka_http_response = None
            try:
                url = urljoin(self._service_url, f"apps/{instance.app_name}")
                async with session.post(
                    url, data=InstanceInfoModel.from_entity(instance).json(), timeout=self._connection_timeout
                ) as response:
                    eureka_http_response = EurekaHttpResponse(
                        status_code=response.status, headers=dict(response.headers)
                    )
            except asyncio.TimeoutError:
                # TODO: add logging
                raise
            except RuntimeError as e:
                # Session may be closed by other coroutine during registration task.
                # TODO: add logging
                pass
            finally:
                return eureka_http_response

    async def get_applications(self) -> Union[EurekaHttpResponse, None]:
        # scip plugin
        from eureka.model.applications_model import ApplicationsModel

        session = self._get_session(self._is_shutdown)
        if session:
            eureka_http_response = None
            try:
                url = urljoin(self._service_url, "apps")
                async with session.get(url, timeout=self._connection_timeout) as response:
                    data = await response.json()
                    applications_model = ApplicationsModel(**data)
                    eureka_http_response = EurekaHttpResponse(
                        status_code=response.status,
                        headers=dict(response.headers),
                        entity=applications_model.to_entity(),
                    )
            except asyncio.TimeoutError:
                # TODO: add logging
                raise
            except RuntimeError as e:
                # Session may be closed by other coroutine during refresh registry task.
                # TODO: add logging
                pass
            finally:
                return eureka_http_response

    async def cancel(self, instance: InstanceInfo) -> Union[EurekaHttpResponse, None]:
        session = self._get_session(self._is_shutdown)
        if session:
            eureka_http_response = None
            try:
                session = self._get_session(self._is_shutdown)
                url = urljoin(self._service_url, f"apps/{instance.app_name}/{instance.instance_id}")
                async with session.delete(url, timeout=self._connection_timeout) as response:
                    eureka_http_response = EurekaHttpResponse(
                        status_code=response.status, headers=dict(response.headers)
                    )
            except asyncio.TimeoutError:
                # TODO: add logging
                raise
            except RuntimeError as e:
                # Session may be closed by other coroutine during cancel task.
                # TODO: add logging
                pass
            finally:
                return eureka_http_response

    def _get_session(self, is_shutdown: bool):
        if not is_shutdown and not self._session:
            self._session = aiohttp.ClientSession()
        return self._session

    async def shutdown(self):
        self._is_shutdown = True
        if self._session:
            await self._session.close()
            self._session = None


# if __name__ == '__main__':
#     from tests.eureka.client.discovery.shared.stubs import instance_info
#     asyncio_eureka_http_client = AsyncIOEurekaHttpClient("http://localhost:8000/eureka/v2/")
#     event_loop_ = asyncio.get_event_loop()
#
#     eureka_http_response_register_1 = event_loop_.run_until_complete(asyncio_eureka_http_client.register(instance_info(num=1)))
#     eureka_http_response_register_2 = event_loop_.run_until_complete(asyncio_eureka_http_client.register(instance_info(num=2)))
#     eureka_http_response_register_3 = event_loop_.run_until_complete(asyncio_eureka_http_client.register(instance_info(num=3)))
#
#     eureka_http_response_get_applications = event_loop_.run_until_complete(asyncio_eureka_http_client.get_applications())
#
#     print("initial size: ", eureka_http_response_get_applications.entity.size())
#     for app in eureka_http_response_get_applications.entity.get_registered_applications():
#         print(app.name)
#         for instance in app.get_all_instances_from_local_cache():
#             print(instance.instance_id)
#
#     eureka_http_response_cancel = event_loop_.run_until_complete(asyncio_eureka_http_client.cancel(instance_info(num=1)))
#
#     eureka_http_response_get_applications = event_loop_.run_until_complete(
#         asyncio_eureka_http_client.get_applications())
#
#     print("after unregister size: ", eureka_http_response_get_applications.entity.size())
#     for app in eureka_http_response_get_applications.entity.get_registered_applications():
#         print(app.name)
#         for instance in app.get_all_instances_from_local_cache():
#             print(instance.instance_id)
#
#     event_loop_.run_until_complete(asyncio_eureka_http_client.shutdown())
