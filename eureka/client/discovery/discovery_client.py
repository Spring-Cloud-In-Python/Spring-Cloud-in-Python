# -*- coding: utf-8 -*-
# scip plugin
from spring_cloud.utils import logging

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# standard library
import asyncio
from abc import ABC, abstractmethod
from typing import List, TypeVar

# scip plugin
from eureka.client.app_info.instance_info import InstanceInfo
from eureka.client.discovery.eureka_client import EurekaClient
from eureka.client.discovery.eureka_client_config import EurekaClientConfig
from eureka.client.discovery.shared import Application, Applications
from eureka.client.discovery.shared.resolver.cluster_resolver import DefaultClusterResolver
from eureka.client.discovery.shared.transport import DefaultEurekaTransportConfig, EurekaTransportConfig
from eureka.client.discovery.shared.transport.asyncio_eureka_http_client_factory import AsyncIOEurekaHttpClientFactory
from eureka.client.discovery.shared.transport.transport_client_factory import TransportClientFactory

ApplicationInfoManager = TypeVar("ApplicationInfoManager")


class DiscoveryClient(EurekaClient):
    def __init__(self, application_info_manager: ApplicationInfoManager, eureka_client_config: EurekaClientConfig):
        self.logger = logging.getLogger("eureka.DiscoveryClient")
        self._application_info_manager = application_info_manager
        self._eureka_client_config = eureka_client_config
        self._eureka_transport_config = DefaultEurekaTransportConfig()

        self._event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._event_loop)

        # scip plugin
        from eureka.client.discovery.asyncio_eureka_transport import AsyncIOEurekaTransport

        self._eureka_transport = AsyncIOEurekaTransport(
            self, AsyncIOEurekaHttpClientFactory(), self._eureka_transport_config
        )

        self.applications = Applications()

        if eureka_client_config.should_enforce_registration_on_init:
            self._event_loop.run_until_complete(self._eureka_transport.register())

        self._schedule_background_tasks()

    def _schedule_background_tasks(self):
        # standard library
        import threading

        t = threading.Thread(target=self._run_periodic_background_tasks)
        # Daemon thread is killed when the main program exits
        t.daemon = True
        t.start()

    def _run_periodic_background_tasks(self):
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        event_loop.create_task(self._periodic_background_tasks())
        event_loop.run_forever()

    async def _periodic_background_tasks(self):
        await asyncio.gather(self._eureka_transport.refresh_local_registry(), self._eureka_transport.send_heart_beat())

    def get_application(self, application_name: str) -> Application:
        application = self.applications.get_registered_application(application_name)
        if application:
            return application
        else:
            raise ValueError("Given application name doesn't exist.")

    def get_applications(self) -> Applications:
        return self.applications if self.applications else Applications()

    def get_next_instance_from_eureka_server(self, virtual_host_name: str, secure: bool) -> InstanceInfo:
        return next(self.applications.get_instances_by_virtual_host_name(virtual_host_name))

    def get_instances_by_virtual_host_name(self, virtual_host_name: str, secure: bool) -> List[InstanceInfo]:
        instances: List[InstanceInfo] = list(self.applications.get_instances_by_virtual_host_name(virtual_host_name))
        self.logger.debug(f'Got Instances by vhost: {[f"{i.ip_address}:{i.port}" for i in instances]}')
        return instances

    @property
    def eureka_client_config(self) -> EurekaClientConfig:
        return self._eureka_client_config

    @property
    def application_info_manager(self) -> ApplicationInfoManager:
        return self._application_info_manager

    def shutdown(self):
        if self._eureka_client_config.should_unregister_on_shutdown:
            self._event_loop.run_until_complete(self._eureka_transport.unregister())

        self._event_loop.run_until_complete(self._eureka_transport.shutdown())

        if self._event_loop.is_running():
            for task in asyncio.all_tasks():
                task.cancel()
            self._event_loop.stop()

        if not self._event_loop.is_closed():
            self._event_loop.close()


class EurekaTransport(ABC):
    def __init__(
        self,
        discovery_client: DiscoveryClient,
        transport_client_factory: TransportClientFactory,
        eureka_transport_config: EurekaTransportConfig,
    ):
        self._discovery_client = discovery_client
        self._transport_client_factory = transport_client_factory
        self._eureka_transport_config = eureka_transport_config
        self._cluster_resolver = DefaultClusterResolver(self._discovery_client.eureka_client_config)

        # Initialise EurekaHttpClient
        cluster_endpoint = next(endpoint for endpoint in self._cluster_resolver.get_cluster_endpoints() if endpoint)
        self.registration_client = self._transport_client_factory.create(cluster_endpoint)
        self.query_client = self._transport_client_factory.create(cluster_endpoint)

    @abstractmethod
    def refresh_local_registry(self):
        raise NotImplemented

    @abstractmethod
    def send_heart_beat(self):
        raise NotImplemented

    @abstractmethod
    def register(self):
        raise NotImplemented

    @abstractmethod
    def unregister(self):
        raise NotImplemented

    @abstractmethod
    def shutdown(self):
        raise NotImplemented
