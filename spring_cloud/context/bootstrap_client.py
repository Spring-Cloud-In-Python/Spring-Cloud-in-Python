# -*- coding: utf-8 -*-
# standard library
from typing import List, Optional, Tuple
from urllib.parse import ParseResult, urlparse

# scip plugin
from eureka.client.app_info import DefaultEurekaInstanceConfig, InstanceInfo, LeaseInfo
from eureka.client.app_info.application_info_manager import ApplicationInfoManager
from eureka.client.discovery import DefaultEurekaClientConfig, DiscoveryClient, EurekaClient
from eureka.client.discovery.shared.transport import DefaultEurekaTransportConfig
from spring_cloud.commons.client.discovery.discovery_client import DiscoveryClient as spring_cloud_DiscoveryClient
from spring_cloud.commons.client.loadbalancer import LoadBalancerClient, ServiceInstance
from spring_cloud.commons.http import ClientHttpRequestInterceptor, HttpRequest, RestTemplate
from spring_cloud.eureka.eureka_discovery_client import EurekaDiscoveryClient
from spring_cloud.ribbon.ribbon_load_balancer_client import RibbonLoadBalancerClient
from spring_cloud.ribbon.spring_client_factory import SpringClientFactory
from spring_cloud.utils import logging

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

has_setup_service_discovery = False
logger = logging.getLogger("spring_cloud.bootstrap_client")


class ServiceDiscoveryClient(RestTemplate, spring_cloud_DiscoveryClient):
    def __init__(self, rest_template: RestTemplate, discovery_client: spring_cloud_DiscoveryClient):
        super().__init__(rest_template.interceptors)
        self.discovery_client = discovery_client

    @property
    def services(self) -> List[str]:
        return self.discovery_client.services

    def get_instances(self, service_id: str) -> List[ServiceInstance]:
        return self.discovery_client.get_instances(service_id)

    def shutdown(self):
        self.discovery_client.shutdown()


def enable_service_discovery(
    service_id: str, port: int, eureka_server_urls: Optional[List[str]] = None
) -> ServiceDiscoveryClient:
    if eureka_server_urls is None:
        eureka_server_urls = ["http://localhost:8761/eureka/v2/"]
    logger.info(
        f'Enabling service discovery with the arguments: service_id={service_id}, port={port}, eureka_server_urls={",".join(eureka_server_urls)}'
    )
    global has_setup_service_discovery
    if not has_setup_service_discovery:
        rest_template, eureka_client = __setup_and_launch_discovery_client(service_id, port, eureka_server_urls)
        has_setup_service_discovery = True
        return ServiceDiscoveryClient(rest_template, eureka_client)
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
        http_request.url = parse_result._replace(netloc=f"{instance.host}:{instance.port}").geturl()
        self.logger.debug(f"Successfully Intercepted. (url={http_request.url})")


def __setup_and_launch_discovery_client(
    service_id: str, port: int, eureka_server_urls: List[str]
) -> Tuple[RestTemplate, spring_cloud_DiscoveryClient]:
    eureka_client = __eureka_discovery_client(service_id, port, eureka_server_urls)
    loadbalancer_client = __spring_cloud_loadbalancer_client(eureka_client)
    rest_template = RestTemplate([LoadBalancerInterceptor(loadbalancer_client)])
    return rest_template, __spring_cloud_discovery_client(eureka_client)


def __spring_cloud_discovery_client(eureka_client: EurekaClient) -> EurekaDiscoveryClient:
    return EurekaDiscoveryClient(eureka_client)


def __spring_cloud_loadbalancer_client(eureka_client: EurekaClient) -> RibbonLoadBalancerClient:
    rb_spring_client_factory = SpringClientFactory(eureka_client)
    loadbalancer_client = RibbonLoadBalancerClient(rb_spring_client_factory)
    return loadbalancer_client


def __eureka_discovery_client(service_id: str, port: int, eureka_server_urls: List[str]) -> EurekaClient:
    eureka_instance_config = DefaultEurekaInstanceConfig(app_name=service_id, unsecure_port=port)

    instance_info = InstanceInfo(
        instance_id=eureka_instance_config.instance_id,
        app_name=eureka_instance_config.app_name,
        ip_address=eureka_instance_config.ip_address,
        vip_address=eureka_instance_config.app_name,
        secure_vip_address=eureka_instance_config.virtual_host_name,
        lease_info=LeaseInfo(
            lease_renewal_interval_in_secs=eureka_instance_config.lease_renewal_interval_in_secs,
            lease_duration_in_secs=eureka_instance_config.lease_expiration_duration_in_secs,
        ),
        host_name=eureka_instance_config.host_name,
        port=eureka_instance_config.unsecure_port,
        secure_port=eureka_instance_config.secure_port,
    )

    app_info_manager = ApplicationInfoManager(DefaultEurekaInstanceConfig(service_id), instance_info)
    return DiscoveryClient(
        app_info_manager, DefaultEurekaClientConfig(DefaultEurekaTransportConfig(), eureka_server_urls)
    )
