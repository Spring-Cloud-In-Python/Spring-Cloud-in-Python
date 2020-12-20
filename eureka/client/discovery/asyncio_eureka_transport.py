# -*- coding: utf-8 -*-

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# standard library
import asyncio
from http import HTTPStatus
from typing import TypeVar

# scip plugin
from eureka.client.discovery.discovery_client import EurekaTransport
from eureka.client.discovery.eureka_client_config import EurekaClientConfig
from eureka.client.discovery.shared.transport import EurekaTransportConfig
from eureka.client.discovery.shared.transport.transport_client_factory import TransportClientFactory
from eureka.utils.asyncio_utils import CoroutineScheduler
from spring_cloud.utils.logging import getLogger

DiscoveryClient = TypeVar("DiscoveryClient")


class AsyncIOEurekaTransport(EurekaTransport):
    def __init__(
        self,
        discovery_client: DiscoveryClient,
        transport_client_factory: TransportClientFactory,
        eureka_transport_config: EurekaTransportConfig,
    ):
        super().__init__(discovery_client, transport_client_factory, eureka_transport_config)

        self._logger = getLogger("eureka.client.discovery.asyncio_eureka_transport")

    async def register(self):
        await asyncio.create_task(self._registration_task(), name="registration_task")

    async def _registration_task(self) -> bool:
        instance = self._discovery_client.application_info_manager.instance_info
        try:
            eureka_http_response = await self.registration_client.register(instance)

            if eureka_http_response and eureka_http_response == HTTPStatus.NO_CONTENT:
                return True
            else:
                self._logger.error(f"Instance {instance.instance_id}'s registration task failed")
                return False

        except asyncio.TimeoutError:
            self._logger.error(f"Timeout reached while registering {instance.instance_id}")

    async def refresh_local_registry(self):
        eureka_client_config = self._discovery_client.eureka_client_config
        coroutine_scheduler = CoroutineScheduler(
            float(eureka_client_config.registry_fetch_interval_in_secs),
            eureka_client_config.registry_cache_refresh_executor_exponential_back_off_bound,
            float(eureka_client_config.registry_fetch_interval_in_secs),
            eureka_client_config.registry_cache_refresh_executor_thread_pool_size,
            self._supervised_refresh_local_registry_task,
            eureka_client_config,
            self._discovery_client,
        )

        await asyncio.create_task(coroutine_scheduler.start())

    async def _supervised_refresh_local_registry_task(
        self, eureka_client_config: EurekaClientConfig, discovery_client: DiscoveryClient
    ):
        # Shuffle on temporary registry instead of client's cached registry to avoid
        # inconsistency in registry when the timeout error or cancelled error happened during shuffle.
        registry_received_from_eureka_server = None
        try:
            eureka_http_response = await asyncio.create_task(
                self.query_client.get_applications(), name="refresh_local_registry_task"
            )

            if eureka_http_response and eureka_http_response.status_code == HTTPStatus.OK:
                if eureka_client_config.should_disable_delta:
                    registry_received_from_eureka_server = eureka_http_response.entity
                    registry_received_from_eureka_server.shuffle_instances(
                        eureka_client_config.should_filter_only_up_instance
                    )
        except (asyncio.TimeoutError, asyncio.CancelledError):
            self._logger.error("Timeout reached while refreshing local registry")
        else:
            discovery_client.applications = registry_received_from_eureka_server

    async def send_heart_beat(self):
        pass

    async def unregister(self):
        instance = self._discovery_client.application_info_manager.instance_info
        try:
            eureka_http_response = await self.registration_client.cancel(instance)

            if not eureka_http_response or eureka_http_response != HTTPStatus.NO_CONTENT:
                self._logger.error(f"Instance {instance.instance_id}'s cancellation task failed")
        except asyncio.TimeoutError:
            self._logger.error(f"Timeout reached while cancelling instance {instance.instance_id}")

    async def shutdown(self):
        await asyncio.create_task(self.registration_client.shutdown())
        await asyncio.create_task(self.query_client.shutdown())

        # See https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
        await asyncio.sleep(0.250)
