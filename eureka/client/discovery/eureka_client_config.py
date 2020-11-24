# -*- coding: utf-8 -*-

# standard library
from abc import ABC, abstractmethod

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from typing import List

# scip plugin
from eureka.client.discovery.shared.transport import EurekaTransportConfig


class EurekaClientConfig(ABC):
    """
    Configuration information required by the eureka clients to register an
    instance with Eureka server.

    See com.netflix.discovery.EurekaClientConfig.
    """

    @property
    @abstractmethod
    def registry_fetch_interval_in_secs(self) -> int:
        """
        Indicates how often (in seconds) to fetch the registry information from
        the eureka server.

        Returns: the fetch interval in seconds.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def instance_info_replication_interval_in_secs(self) -> int:
        """
        Indicates how often (in seconds) to replicate instance changes to be
        replicated to the eureka server.

        Returns: the instance replication interval in seconds.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def initial_instance_info_replication_interval_in_secs(self) -> int:
        """
        Indicates how long initially (in seconds) to replicate instance info
        to the eureka server.

        Returns: the instance initial replication interval in seconds.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def eureka_service_url_poll_interval_in_secs(self) -> int:
        """
        Indicates how often (in seconds) to poll for changes to eureka server
        information.

        Returns: the interval to poll for eureka service url changes.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def should_gzip_content(self) -> bool:
        """
        Indicates whether the content fetched from eureka server has to be
        compressed whenever it is supported by the server. The registry
        information from the eureka server is compressed for optimum network
        traffic.

        Returns: true, if the content need to be compressed, false otherwise.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def eureka_server_read_timeout_in_secs(self) -> int:
        """
        Indicates how long to wait (in seconds) before a read from eureka server
        needs to timeout.

        Returns: time in seconds before the read should timeout.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def eureka_server_connection_timeout_in_secs(self) -> int:
        """
        Indicates how long to wait (in seconds) before a connection to eureka
        server needs to timeout.

        Returns: time in seconds before the connections should timeout.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def eureka_server_total_connections(self) -> int:
        """
        Gets the total number of connections that is allowed from eureka client
        to all eureka servers.

        Returns: total number of allowed connections from eureka client to all eureka servers.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def eureka_server_total_connections_per_host(self) -> int:
        """
        Gets the total number of connections that is allowed from eureka client
        to a eureka server host.

        Returns: total number of allowed connections from eureka client to a eureka server.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def should_register_with_eureka(self) -> bool:
        """
        Indicates whether or not this instance should register its information
        with eureka server for discovery by others. In some cases, you do not
        want your instances to be discovered whereas you just want do discover
        other instances.

        Returns: true if this instance should register with eureka, false otherwise.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def should_unregister_on_shutdown(self) -> bool:
        """
        Indicates whether the client should explicitly unregister itself from the remote server
        on client shutdown.

        Returns: true if this instance should unregister with eureka on client shutdown, false otherwise.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def allow_redirect(self) -> bool:
        """
        Indicates whether server can redirect a client request to a backup server/cluster.
        If set to false, the server will handle the request directly, If set to true, it may
        send HTTP redirect to the client, with a new server location.

        Returns: true if HTTP redirects are allowed, false otherwise.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def should_log_delta_diff(self) -> bool:
        """
        Indicates whether to log differences between the eureka server and the
        eureka client in terms of registry information.
        Eureka client tries to retrieve only delta changes from eureka server to
        minimize network traffic. After receiving the deltas, eureka client
        reconciles the information from the server to verify it has not missed
        out some information. Reconciliation failures could happen when the
        client has had network issues communicating to server.If the
        reconciliation fails, eureka client gets the full registry information.
        While getting the full registry information, the eureka client can log
        the differences between the client and the server and this setting
        controls that.
        The changes are effective at runtime at the next registry fetch cycle as
        specified by registry_fetch_interval_in_secs.

        Returns: true if the eureka client should log delta differences in the case of
        reconciliation failure.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def should_disable_delta(self) -> bool:
        """
        Indicates whether the eureka client should disable fetching of delta and
        should rather resort to getting the full registry information.
        Note that the delta fetches can reduce the traffic tremendously, because
        the rate of change with the eureka server is normally much lower than the
        rate of fetches.
        The changes are effective at runtime at the next registry fetch cycle as
        specified by registry_fetch_interval_in_secs.

        Returns: true to enable fetching delta information for registry, false to
        get the full registry.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def eureka_server_service_urls(self) -> List[str]:
        """
        Gets the list of fully qualified urls to communicate with eureka server.
        Typically the eureka server urls carry protocol,host,port,context
        and version information if any.
        Example: http://ec2-256-156-243-129.compute-1.amazonaws.com:7001/eureka/v2/,
                 http://localhost:8080/eureka/v2/

        Returns: the list of eureka server service urls for eureka clients to talk to.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def should_filter_only_up_instance(self) -> bool:
        """
        Indicates whether to get the applications after filtering the
        applications for instances with only UP states.

        Returns: true to filter, false otherwise.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def eureka_connection_idle_timeout_in_secs(self) -> int:
        """
        Indicates how much time (in seconds) that the HTTP connections to eureka
        server can stay idle before it can be closed.

        Returns: time in seconds the connections to eureka can stay idle before it
        can be closed.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def should_fetch_registry(self) -> bool:
        """
        Indicates whether this client should fetch eureka registry information from eureka server.

        Returns: true if registry information has to be fetched, false otherwise.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def should_enforce_fetch_registry_on_init(self) -> bool:
        """
        Returns: true or false for whether the client initialization should enforce an initial fetch.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def heartbeat_executor_thread_pool_size(self) -> int:
        """
        Returns: the heartbeat_executor thread pool size.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def heartbeat_executor_exponential_back_off_bound(self) -> int:
        """
        Heartbeat executor exponential back off related property.
        It is a maximum multiplier value for retry delay, in case where
        a sequence of timeouts occurred.

        Returns: maximum multiplier value for retry delay.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def registry_cache_refresh_executor_thread_pool_size(self) -> int:
        """
        Returns: the thread pool size for the registry_cache_refresh_executor.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def registry_cache_refresh_executor_exponential_back_off_bound(self) -> int:
        """
        Returns: maximum multiplier value for retry delay.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def should_on_demand_update_status_change(self) -> bool:
        """
        If set to true, local status updates via ApplicationInfoManager.setInstanceStatus()
        will trigger on-demand (but rate limited) register/updates to remote eureka servers.

        Returns: true or false for whether local status updates should be updated to remote servers on-demand.

        """
        raise NotImplemented

    @property
    @abstractmethod
    def should_enforce_registration_on_init(self) -> bool:
        raise NotImplemented

    @property
    @abstractmethod
    def eureka_transport_config(self) -> EurekaTransportConfig:
        raise NotImplemented


class DefaultEurekaClientConfig(EurekaClientConfig):
    def __init__(self, eureka_transport_config: EurekaTransportConfig):
        self._eureka_transport_config = eureka_transport_config

    @property
    def registry_fetch_interval_in_secs(self) -> int:
        return 30

    @property
    def instance_info_replication_interval_in_secs(self) -> int:
        return 30

    @property
    def initial_instance_info_replication_interval_in_secs(self) -> int:
        return 40

    @property
    def eureka_service_url_poll_interval_in_secs(self) -> int:
        return 5 * 60 * 1000 // 1000

    @property
    def should_gzip_content(self) -> bool:
        return False

    @property
    def eureka_server_read_timeout_in_secs(self) -> int:
        return 8

    @property
    def eureka_server_connection_timeout_in_secs(self) -> int:
        return 5

    @property
    def eureka_server_total_connections(self) -> int:
        return 200

    @property
    def eureka_server_total_connections_per_host(self) -> int:
        return 50

    @property
    def should_register_with_eureka(self) -> bool:
        return True

    @property
    def should_unregister_on_shutdown(self) -> bool:
        return True

    @property
    def allow_redirect(self) -> bool:
        return False

    @property
    def should_log_delta_diff(self) -> bool:
        return False

    @property
    def should_disable_delta(self) -> bool:
        return False

    @property
    def eureka_server_service_urls(self) -> List[str]:
        return ["http://localhost:8080/eureka/v2/"]

    @property
    def should_filter_only_up_instance(self) -> bool:
        return True

    @property
    def eureka_connection_idle_timeout_in_secs(self) -> int:
        return 30

    @property
    def should_fetch_registry(self) -> bool:
        return True

    @property
    def should_enforce_fetch_registry_on_init(self) -> bool:
        return False

    @property
    def heartbeat_executor_thread_pool_size(self) -> int:
        return 5

    @property
    def heartbeat_executor_exponential_back_off_bound(self) -> int:
        return 10

    @property
    def registry_cache_refresh_executor_thread_pool_size(self) -> int:
        return 5

    @property
    def registry_cache_refresh_executor_exponential_back_off_bound(self) -> int:
        return 10

    @property
    def should_on_demand_update_status_change(self) -> bool:
        return True

    @property
    def should_enforce_registration_on_init(self) -> bool:
        return False

    @property
    def eureka_transport_config(self) -> EurekaTransportConfig:
        return self._eureka_transport_config
