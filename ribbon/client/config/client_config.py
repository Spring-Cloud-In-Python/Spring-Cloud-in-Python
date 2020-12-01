# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# standard library
import sys
from collections import OrderedDict

# scip plugin
from spring_cloud.utils.dot_map import DotMap

DefaultClientConfig = DotMap(
    {
        "PRIORITIZE_VIP_ADDRESS_BASED_SERVERS": True,
        "NFLOADBALANCER_PING_CLASSNAME": "com.netflix.loadbalancer.DummyPing",
        "NFLOADBALANCER_RULE_CLASSNAME": "com.netflix.loadbalancer.AvailabilityFilteringRule",
        "NFLOADBALANCER_CLASSNAME": "com.netflix.loadbalancer.ZoneAwareLoadBalancer",
        "USEIPADDRESS_FOR_SERVER": False,
        "CLIENT_CLASSNAME": "com.netflix.niws.client.http.RestClient",
        "VIPADDRESS_RESOLVER_CLASSNAME": "com.netflix.client.SimpleVipAddressResolver",
        "PRIME_CONNECTIONS_URI": "/",
        "MAX_TOTAL_TIME_TO_PRIME_CONNECTIONS": 30000,
        "MAX_RETRIES_PER_SERVER_PRIME_CONNECTION": 9,
        "ENABLE_PRIME_CONNECTIONS": False,
        "MAX_REQUESTS_ALLOWED_PER_WINDOW": sys.maxsize,
        "REQUEST_THROTTLING_WINDOW_IN_MILLIS": 60000,
        "ENABLE_REQUEST_THROTTLING": False,
        "ENABLE_GZIP_CONTENT_ENCODING_FILTER": False,
        "CONNECTION_POOL_CLEANER_TASK_ENABLED": True,
        "FOLLOW_REDIRECTS": False,
        "PERCENTAGE_NIWS_EVENT_LOGGED": 0.0,
        "MAX_AUTO_RETRIES_NEXT_SERVER": 1,
        "MAX_AUTO_RETRIES": 0,
        "BACKOFF_INTERVAL": 0,
        "READ_TIMEOUT": 5000,
        "CONNECTION_MANAGER_TIMEOUT": 2000,
        "CONNECT_TIMEOUT": 2000,
        "ENABLE_CONNECTION_POOL": True,
        "MAX_CONNECTIONS_PER_HOST": 50,
        "MAX_TOTAL_CONNECTIONS": 200,
        "MIN_PRIME_CONNECTIONS_RATIO": 1.0,
        "PRIME_CONNECTIONS_CLASS": "com.netflix.niws.client.http.HttpPrimeConnection",
        "SEVER_LIST_CLASS": "com.netflix.loadbalancer.ConfigurationBasedServerList",
        "SERVER_LIST_UPDATER_CLASS": "com.netflix.loadbalancer.PollingServerListUpdater",
        "CONNECTION_IDLE_TIMERTASK_REPEAT_IN_MSECS": 30000,
        "CONNECTIONIDLE_TIME_IN_MSECS": 30000,
        "POOL_MAX_THREADS": 200,
        "POOL_MIN_THREADS": 1,
        "POOL_KEEP_ALIVE_TIME": 900,
        "ENABLE_ZONE_AFFINITY": False,
        "ENABLE_ZONE_EXCLUSIVITY": False,
        "PORT": 7001,
        "ENABLE_LOADBALANCER": True,
        "PROPERTY_NAME_SPACE": "ribbon",
        "OK_TO_RETRY_ON_ALL_OPERATIONS": False,
        "ENABLE_NIWS_EVENT_LOGGING": True,
        "IS_CLIENT_AUTH_REQUIRED": False,
    }
)


class ClientConfig:
    def __init__(self, nameSpace: str = None):
        self.__property_name_space = nameSpace or DefaultClientConfig.PROPERTY_NAME_SPACE
        self.__properties = OrderedDict()
        self.__enable_dynamic_properties = False

    def load_default_values(self):
        self.__properties = DefaultClientConfig

    def add_property(self, key: str, val: object):
        self.__properties[key] = val

    def delete_property(self, key: str):
        del self.__properties[key]

    def get_property(self, key: str):
        try:
            return self.__properties[key]
        except KeyError:
            return None

    @property
    def properties(self):
        return self.__properties
