# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

__all__ = ["InstanceRegistry"]

# standard library
import threading
from typing import Optional

# scip plugin
from eureka.client.app_info import InstanceInfo, LeaseInfo
from eureka.client.discovery.shared import Application, Applications
from eureka.server.lease.lease import Lease
from eureka.server.registry.registry_presenter import RegistryPresenter
from eureka.utils.concurrent import ConcurrentMap


def decorate_instance_info(lease: Lease) -> InstanceInfo:
    """

    Get the InstanceInfo in the lease and set its attributes, like timestamps, setting of duration and so on.

    Args:
        lease (): A lease which holds a InstanceInfo.

    Returns: The decorated InstanceInfo.

    """
    info = lease.holder

    renewal_interval = LeaseInfo.DEFAULT_LEASE_RENEWAL_INTERVAL
    lease_duration = LeaseInfo.DEFAULT_LEASE_DURATION

    if info.lease_info is not None:
        renewal_interval = info.lease_info.lease_renewal_interval_in_secs
        lease_duration = info.lease_info.lease_duration_in_secs

    lease_info = LeaseInfo(
        registration_timestamp=lease.registration_timestamp,
        last_renewal_timestamp=lease.last_update_timestamp,
        service_up_timestamp=lease.service_up_timestamp,
        lease_renewal_interval_in_secs=renewal_interval,
        lease_duration_in_secs=lease_duration,
        eviction_timestamp=lease.eviction_timestamp,
    )

    info.lease_info = lease_info
    return info


class InstanceRegistry:
    def __init__(self):
        self.registry = ConcurrentMap()
        self.lock = threading.RLock()
        self.presenter = RegistryPresenter(self)

    def register(self, registrant: InstanceInfo, lease_duration: int):
        """

        Registers a new instance with a given duration.

        Args:
            registrant (): The application instance to register.
            lease_duration (): The duration before the lease to expire in seconds.

        """
        with self.lock:
            application_name = registrant.app_name
            application_map = self.registry.get(registrant.app_name)

            if application_map is None:
                new_application_map = ConcurrentMap()
                application_map = self.registry.put_if_absent(application_name, new_application_map)

            instance_id = registrant.instance_id
            existing_lease = application_map.get(instance_id)
            if existing_lease is not None and existing_lease.holder is not None:
                registrant = existing_lease.holder

            lease = Lease(registrant, lease_duration)
            if existing_lease is not None:
                lease.service_up_timestamp = existing_lease.service_up_timestamp

            application_map.put(instance_id, lease)
            if registrant.status == InstanceInfo.Status.UP:
                lease.service_up()

            registrant.action_type = InstanceInfo.ActionType.ADD
            registrant.set_last_updated_timestamp()

    def get_application(self, application_name: str) -> Optional[Application]:
        """

        Get the application information by name of the application.

        Args:
            application_name (): The name of the application

        Returns: The application or None if it doesn't exist in this registry.

        """
        with self.lock:
            application = None
            application_map = self.registry.get(application_name)

            if application_map is None or application_map.size() == 0:
                return None

            for _, entry_lease in application_map.entry_set():
                if application is None:
                    application = Application(application_name)

                application.add_instance(decorate_instance_info(entry_lease))

            return application

    def get_applications(self) -> Applications:
        """

        Get all applications in this instance registry.

        Returns: The applications.

        """
        with self.lock:
            applications = Applications()
            for application_name, application_map in self.registry.entry_set():
                application = None

                for _, lease in application_map.entry_set():
                    if application is None:
                        application = Application(lease.holder.app_name)

                    application.add_instance(decorate_instance_info(lease))

                if application is not None:
                    applications.add_application(application)

            applications.reconciliation_hash_code = applications.compute_reconciliation_hash_code()
            return applications

    def get_responser(self) -> RegistryPresenter:
        return self.presenter
