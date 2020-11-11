# -*- coding: utf-8 -*-

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"


class LeaseInfo:
    """
    Represents the lease information with Eureka.
    Eureka decides to remove the instance out of its view depending on
    the duration. The lease also tracks the last time it was renewed.
    """

    DEFAULT_LEASE_RENEWAL_INTERVAL = 30
    DEFAULT_LEASE_DURATION = 90

    def __init__(
        self,
        registration_timestamp: int = 0,
        last_renewal_timestamp: int = 0,
        eviction_timestamp: int = 0,
        service_up_timestamp: int = 0,
        lease_renewal_interval_in_secs: int = DEFAULT_LEASE_RENEWAL_INTERVAL,
        lease_duration_in_secs: int = DEFAULT_LEASE_DURATION,
    ):
        self._lease_renewal_interval_in_secs = lease_renewal_interval_in_secs
        self._lease_duration_in_secs = lease_duration_in_secs
        self._registration_timestamp = registration_timestamp
        self._last_renewal_timestamp = last_renewal_timestamp
        self._eviction_timestamp = eviction_timestamp
        self._service_up_timestamp = service_up_timestamp

    @property
    def registration_timestamp(self) -> int:
        return self._registration_timestamp

    @property
    def last_renewal_timestamp(self) -> int:
        return self._last_renewal_timestamp

    @property
    def eviction_timestamp(self) -> int:
        return self._eviction_timestamp

    @property
    def service_up_timestamp(self) -> int:
        return self._service_up_timestamp

    @property
    def lease_renewal_interval_in_secs(self) -> int:
        return self._lease_renewal_interval_in_secs

    @property
    def lease_duration_in_secs(self) -> int:
        return self._lease_duration_in_secs
