# -*- coding: utf-8 -*-
# standard library
import threading
from abc import ABC, abstractmethod
from typing import Optional
from urllib.parse import ParseResult, urlparse

# scip plugin
from eureka.client.app_info import InstanceInfo, LeaseInfo
from eureka.client.app_info.application_info_manager import ApplicationInfoManager
from eureka.client.discovery import DefaultEurekaClientConfig
from eureka.client.discovery.shared.transport import DefaultEurekaTransportConfig
from ribbon.client.config.client_config import ClientConfig
from ribbon.eureka.discovery_enabled_niws_server_list import DiscoveryEnabledNIWSServerList
from ribbon.loadbalancer.dynamic_server_list_load_balancer import DynamicServerListLoadBalancer
from ribbon.loadbalancer.load_balancer import LoadBalancer
from ribbon.loadbalancer.round_robin_rule import RoundRobinRule
from spring_cloud.commons.client.loadbalancer import LoadBalancerClient, ServiceInstance
from spring_cloud.commons.http import ClientHttpRequestInterceptor, HttpRequest, RestTemplate
from spring_cloud.eureka.eureka_discovery_client import EurekaDiscoveryClient
from spring_cloud.ribbon.ribbon_load_balancer_client import RibbonLoadBalancerClient
from spring_cloud.ribbon.spring_client_factory import SpringClientFactory
from spring_cloud.utils import logging

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

has_setup_service_discovery = False


def enable_service_discovery(service_id: str, port: int) -> RestTemplate:
    global has_setup_service_discovery
    if not has_setup_service_discovery:
        rest_template = __setup_and_launch_discovery_client(service_id, port)
        has_setup_service_discovery = True
        return rest_template
    else:
        raise Exception("You can't setup service discovery twice.")


class LoadBalancerInterceptor(ClientHttpRequestInterceptor):
    def __init__(self, loadbalancer_client: LoadBalancerClient):
        self.logger = logging.getLogger("spring_cloud.LoadBalancerInterceptor")
        self.loadbalancer_client = loadbalancer_client

    def intercept(self, http_request: HttpRequest):
        self.logger.debug("Intercepting...")
        parse_result: ParseResult = urlparse(http_request.url)
        instance: ServiceInstance = self.loadbalancer_client.choose(parse_result.hostname, http_request)
        self.logger.info(f"Transform host: {parse_result.hostname} --> {instance.host}.")
        http_request.url = parse_result._replace(netloc=instance.host)
        self.logger.debug(f"Successfully Intercepted. (url={http_request.url})")


def __setup_and_launch_discovery_client(service_id: str, port: int) -> RestTemplate:
    eureka_client = __eureka_discovery_client(service_id, port)
    discovery_client = __spring_cloud_discovery_client(eureka_client)
    loadbalancer_client = __spring_cloud_loadbalancer_client(eureka_client)
    rest_template = RestTemplate([LoadBalancerInterceptor(loadbalancer_client)])
    return rest_template


def __spring_cloud_discovery_client(eureka_client: EurekaClient) -> EurekaDiscoveryClient:
    return EurekaDiscoveryClient(eureka_client)


def __spring_cloud_loadbalancer_client(eureka_client: EurekaClient) -> RibbonLoadBalancerClient:
    rb_spring_client_factory = SpringClientFactory(eureka_client)
    loadbalancer_client = RibbonLoadBalancerClient(rb_spring_client_factory)
    return loadbalancer_client


def __eureka_discovery_client(service_id: str, port: int) -> EurekaClient:
    id_address = None  # TODO should be generated via some way
    instance_info = InstanceInfo(
        instance_id=service_id,
        app_name=service_id,
        app_group_name=service_id,
        ip_address=id_address,
        vip_address=service_id,
        secure_vip_address=service_id,
        lease_info=LeaseInfo(),
        metadata={},
        host_name="localhost",
        port=port,
    )
    app_info_manager = ApplicationInfoManager(DefaultEurekaInstaneConfig(service_id), instance_info)

    eureka_client_config = DefaultEurekaClientConfig(DefaultEurekaTransportConfig())
    return DiscoveryClient(app_info_manager, eureka_client_config)


def enable_service_registry(port=8761):
    # TODO: Fake, should be substituted with the real implementation
    # standard library
    import time

    while True:
        time.sleep(3)
        print("Tick...")  # simulate service' running
