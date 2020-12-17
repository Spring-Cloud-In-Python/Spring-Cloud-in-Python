# -*- coding: utf-8 -*-

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"


# scip plugin
from eureka.client.discovery.shared.resolver import EurekaEndpoint
from eureka.client.discovery.shared.transport import EurekaHttpClient
from eureka.client.discovery.shared.transport.asyncio_eureka_http_client import AsyncIOEurekaHttpClient
from eureka.client.discovery.shared.transport.transport_client_factory import TransportClientFactory


class AsyncIOEurekaHttpClientFactory(TransportClientFactory):
    def create(self, eureka_endpoint: EurekaEndpoint) -> EurekaHttpClient:
        return AsyncIOEurekaHttpClient(eureka_endpoint.service_url)
