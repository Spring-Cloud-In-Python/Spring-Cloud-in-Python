# -*- coding: utf-8 -*-
# scip plugin
from spring_cloud.utils import validate

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
from spring_cloud.utils.logging import getLogger


class AsyncIOEurekaHttpClient(EurekaHttpClient):
    def __init__(self, service_url: str, connection_timeout: int = 300):
        self._connection_timeout = connection_timeout
        self._service_url = validate.not_none(service_url)

        self._logger = getLogger("eureka.client.asyncio_eureka_http_client")
        self._logger.debug(f"Initiated with service_url={self._service_url}.")

    @property
    def connection_timeout(self) -> int:
        return self._connection_timeout

    @connection_timeout.setter
    def connection_timeout(self, connection_timeout: int):
        self._connection_timeout = connection_timeout

    async def register(self, instance: InstanceInfo) -> Union[EurekaHttpResponse, None]:
        # scip plugin
        from eureka.model.instance_info_model import InstanceInfoModel

        eureka_http_response = None
        url = urljoin(self._service_url, f"apps/{instance.app_name}")
        self._logger.trace(f"Requesting to {url}...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url, data=InstanceInfoModel.from_entity(instance).json(), timeout=self._connection_timeout
                ) as response:
                    eureka_http_response = EurekaHttpResponse(
                        status_code=response.status, headers=dict(response.headers)
                    )
                self._logger.debug(f"Registration Response: {response}")
        except asyncio.TimeoutError:
            self._logger.error(
                f"Connection timeout reached while registering instance {instance.instance_id} with {url}"
            )
            raise
        except RuntimeError:
            self._logger.warning(f"Session was closed while registering instance {instance.instance_id} with {url}")
        except Exception as e:
            self._logger.error(e)
        finally:
            return eureka_http_response

    async def get_applications(self) -> Union[EurekaHttpResponse, None]:
        # scip plugin
        from eureka.model.applications_model import ApplicationsModel

        eureka_http_response = None
        url = urljoin(self._service_url, "apps")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=self._connection_timeout) as response:
                    data = await response.json()
                    applications_model = ApplicationsModel(**data)
                    eureka_http_response = EurekaHttpResponse(
                        status_code=response.status,
                        headers=dict(response.headers),
                        entity=applications_model.to_entity(),
                    )
        except asyncio.TimeoutError:
            self._logger.error(f"Connection timeout reached while fetching full registry with {url}")
            raise
        except RuntimeError:
            self._logger.warning(f"Session was closed while fetching full registry with {url}")
        except Exception as e:
            self._logger.error(e)
        finally:
            return eureka_http_response

    async def cancel(self, instance: InstanceInfo) -> Union[EurekaHttpResponse, None]:
        eureka_http_response = None
        url = urljoin(self._service_url, f"apps/{instance.app_name}/{instance.instance_id}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.delete(url, timeout=self._connection_timeout) as response:
                    eureka_http_response = EurekaHttpResponse(
                        status_code=response.status, headers=dict(response.headers)
                    )
        except asyncio.TimeoutError:
            self._logger.error(
                f"Connection timeout reached while unregistering instance {instance.instance_id} with {url}"
            )
            raise
        except RuntimeError:
            self._logger.warning(f"Session was closed while unregistering instance {instance.instance_id} with {url}")
        except Exception as e:
            self._logger.error(e)
        finally:
            return eureka_http_response

    async def shutdown(self):
        # Some implementations here in the future
        pass
