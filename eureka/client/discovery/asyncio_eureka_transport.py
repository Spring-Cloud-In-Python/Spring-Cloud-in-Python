# -*- coding: utf-8 -*-

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# standard library
import asyncio
from http import HTTPStatus

# scip plugin
from eureka.client.discovery.discovery_client import EurekaTransport
from eureka.client.discovery.eureka_client_config import EurekaClientConfig
from eureka.utils.asyncio_utils import CoroutineSupervisor


class AsyncIOEurekaTransport(EurekaTransport):
    async def register(self):
        await asyncio.create_task(self._registration_task(), name="registration_task")

    async def _registration_task(self) -> bool:
        instance_ = self._discovery_client.application_info_manager.instance_info
        eureka_http_response = await self.registration_client.register(instance_)

        return eureka_http_response.status_code == HTTPStatus.NO_CONTENT if eureka_http_response else False

    async def refresh_local_registry(self):
        eureka_client_config = self._discovery_client.eureka_client_config
        coroutine_supervisor = CoroutineSupervisor(
            float(eureka_client_config.registry_fetch_interval_in_secs),
            eureka_client_config.registry_cache_refresh_executor_exponential_back_off_bound,
            float(eureka_client_config.registry_fetch_interval_in_secs),
            eureka_client_config.registry_cache_refresh_executor_thread_pool_size,
            self._supervised_refresh_local_registry_task,
            eureka_client_config,
            self._discovery_client,
        )

        await asyncio.create_task(coroutine_supervisor.start())

    async def _supervised_refresh_local_registry_task(self, eureka_client_config: EurekaClientConfig, discovery_client):
        eureka_http_response = await asyncio.create_task(
            self.query_client.get_applications(), name="refresh_local_registry_task"
        )

        if eureka_http_response and eureka_http_response.status_code == HTTPStatus.OK:
            if eureka_client_config.should_disable_delta:
                discovery_client.applications = eureka_http_response.entity
                discovery_client.applications.shuffle_instances(eureka_client_config.should_filter_only_up_instance)

    async def send_heart_beat(self):
        pass

    async def unregister(self):
        instance_ = self._discovery_client.application_info_manager.instance_info
        eureka_http_response = await self.registration_client.cancel(instance_)

        if not eureka_http_response or eureka_http_response != HTTPStatus.NO_CONTENT:
            # TODO: add logging
            pass

    async def shutdown(self):
        await asyncio.create_task(self.registration_client.shutdown())
        await asyncio.create_task(self.query_client.shutdown())

        # See https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
        await asyncio.sleep(0.250)
