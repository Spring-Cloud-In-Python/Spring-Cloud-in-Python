# -*- coding: utf-8 -*-

# standard library
from abc import ABC, abstractmethod

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"


class EurekaTransportConfig(ABC):
    """
    Config class that governs configurations relevant to the transport layer.

    See com.netflix.discovery.shared.transport.EurekaTransportConfig.
    """

    @property
    @abstractmethod
    def sessioned_client_reconnect_interval_in_secs(self) -> int:
        """
        @return: the reconnect interval to use for sessioned clients
        """
        raise NotImplemented

    @property
    @abstractmethod
    def retryable_client_quarantine_set_refresh_percentage(self) -> float:
        """
        @return: the percentage of the full endpoints set above which the quarantine set is cleared in the range [0, 1.0].
        """
        raise NotImplemented

    @property
    @abstractmethod
    def applications_resolver_data_staleness_threshold_in_secs(self) -> int:
        """
        @return: the max staleness threshold tolerated by the applications resolver.
        """
        raise NotImplemented

    @property
    @abstractmethod
    def async_resolver_refresh_interval_in_millis(self) -> int:
        """
        @return:the interval to poll for the async resolver.
        """
        raise NotImplemented

    @property
    @abstractmethod
    def async_resolver_warm_up_timeout_in_millis(self) -> int:
        """
        @return: the async refresh timeout threshold.
        """
        raise NotImplemented

    @property
    @abstractmethod
    def async_resolver_executor_thread_pool_size(self) -> int:
        """
        @return: the max thread pool size for the async resolver's executor.
        """
        raise NotImplemented

    @property
    @abstractmethod
    def write_eureka_server_cluster_vip(self) -> str:
        """
        @return: the remote vip address of the primary eureka server cluster to register with.
        """
        raise NotImplemented

    @property
    @abstractmethod
    def read_eureka_server_cluster_vip(self) -> bool:
        """
        The remote vip address of the eureka server cluster (either the primaries or a readonly replica) to fetch registry.

        @return: the vip address for the readonly cluster to redirect to, if applicable (can be the same as the bootstrap).
        """
        raise NotImplemented

    @property
    @abstractmethod
    def bootstrap_resolver_strategy(self) -> str:
        """
        Can be used to specify different bootstrap resolve strategies. Current supported strategies are:
        - default (if no match): bootstrap from dns txt records or static config hostnames
        - composite: bootstrap from local registry if data is available
          and warm (see applications_resolver_data_staleness_threshold_in_secs), otherwise
          fall back to a backing default

        @return: null for the default strategy, by default
        """
        raise NotImplemented

    @property
    @abstractmethod
    def use_bootstrap_resolver_for_query(self) -> bool:
        """
        By default, the transport uses the same (bootstrap) resolver for queries.

        Set this property to false to use an indirect resolver to resolve query targets
        via read_eureka_server_cluster_vip. This indirect resolver may or may not return the same
        targets as the bootstrap servers depending on how servers are setup.

        @return: true by default.
        """
        raise NotImplemented
