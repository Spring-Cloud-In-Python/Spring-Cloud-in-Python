# -*- coding: utf-8 -*-

# standard library
from enum import Enum
from typing import Dict, Optional

# scip plugin
from eureka.client.app_info.lease_info import LeaseInfo
from eureka.utils.timestamp import current_timestamp

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"


class InstanceInfo:
    """
    The class that holds information required for registration with
    Eureka Server and to be discovered by other components.

    See com.netflix.appinfo.InstanceInfo.
    """

    __slots__ = (
        "_instance_id",
        "_app_name",
        "_app_group_name",
        "_ip_address",
        "_vip_address",
        "_secure_vip_address",
        "_lease_info",
        "_metadata",
        "_last_updated_timestamp",
        "_last_dirty_timestamp",
        "_action_type",
        "_host_name",
        "_is_coordinating_discovery_server",
        "_is_secure_port_enabled",
        "_is_unsecure_port_enabled",
        "_port",
        "_secure_port",
        "_status",
        "_overridden_status",
        "_is_instance_info_dirty",
    )

    DEFAULT_PORT = 7001
    DEFAULT_SECURE_PORT = 7002

    class PortType(Enum):
        SECURE = "SECURE"
        UNSECURE = "UNSECURE"

    class Status(Enum):
        # Ready to receive traffic.
        UP = "UP"
        # Do not send traffic (Healthcheck callback failed).
        DOWN = "DOWN"
        # Do not send traffic (Just about starting and initializations are to be done).
        STARTING = "STARTING"
        # Intentionally shutdown for traffic.
        OUT_OF_SERVICE = "OUT_OF_SERVICE"

        UNKNOWN = "UNKNOWN"

    class ActionType(Enum):
        """
        Eureka server will set the action type on the instance to let
        Eureka client know what action to perform on this instance in
        its local registry.
        """

        ADD = "ADD"
        MODIFIED = "MODIFIED"
        DELETED = "DELETED"

    def __init__(
        self,
        instance_id: str,
        app_name: str,
        ip_address: str,
        vip_address: str,
        secure_vip_address: str,
        lease_info: LeaseInfo,
        host_name: str,
        app_group_name: str = None,
        metadata: Dict[str, str] = None,
        last_updated_timestamp: int = None,
        last_dirty_timestamp: int = None,
        action_type: ActionType = None,
        is_coordinating_discovery_server: bool = False,
        is_secure_port_enabled: bool = False,
        is_unsecure_port_enabled: bool = True,
        port: int = DEFAULT_PORT,
        secure_port: int = DEFAULT_SECURE_PORT,
        status: Status = Status.UP,
        overridden_status: Status = Status.UNKNOWN,
        is_instance_info_dirty: bool = False,
    ):
        """
        Args:
            instance_id: the unique id of the instance.
            app_name: the application name of the instance.This is mostly used in querying of instances.
            ip_address: the ip address, in AWS scenario it is a private IP.
            vip_address: the Virtual Internet Protocol address for this instance. Defaults to hostname if not specified.
            secure_vip_address: the Secure Virtual Internet Protocol address for this instance. Defaults to hostname if not specified.
            lease_info: the lease information regarding when it expires.
            host_name: the default network address to connect to this instance. Typically this would be the fully qualified public hostname.
            metadata: all application specific metadata set on the instance.
            last_updated_timestamp: last time when the instance was updated.
            last_dirty_timestamp: the last time when this instance was touched.
            port: the unsecure port number that is used for servicing requests.
            secure_port: the secure port that is used for servicing requests.
            status: the status indicating whether the instance can handle requests.
            overridden_status:the status indicating whether an external process has changed the status.
        """
        self._instance_id = instance_id
        self._app_name = app_name
        self._app_group_name = app_group_name
        self._ip_address = ip_address
        self._vip_address = vip_address
        self._secure_vip_address = secure_vip_address
        self._lease_info = lease_info
        self._metadata = metadata
        self._last_updated_timestamp = last_updated_timestamp
        self._last_dirty_timestamp = last_dirty_timestamp
        self._action_type = action_type
        self._host_name = host_name
        self._is_coordinating_discovery_server = is_coordinating_discovery_server
        self._is_secure_port_enabled = is_secure_port_enabled
        self._is_unsecure_port_enabled = is_unsecure_port_enabled
        self._port = port
        self._secure_port = secure_port
        self._status = status
        self._overridden_status = overridden_status
        self._is_instance_info_dirty = is_instance_info_dirty

    @property
    def instance_id(self) -> str:
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id: str):
        self._instance_id = instance_id

    @property
    def app_name(self) -> str:
        return self._app_name

    @app_name.setter
    def app_name(self, app_name: str):
        self._app_name = app_name

    @property
    def app_group_name(self) -> str:
        return self._app_group_name

    @app_group_name.setter
    def app_group_name(self, app_group_name: str):
        self._app_group_name = app_group_name

    @property
    def ip_address(self) -> str:
        return self._ip_address

    @ip_address.setter
    def ip_address(self, ip_address: str):
        self._ip_address = ip_address

    @property
    def vip_address(self) -> str:
        return self._vip_address

    @vip_address.setter
    def vip_address(self, vip_address: str):
        self._vip_address = vip_address

    @property
    def secure_vip_address(self) -> str:
        return self._secure_vip_address

    @secure_vip_address.setter
    def secure_vip_address(self, secure_vip_address: str):
        self._secure_vip_address = secure_vip_address

    @property
    def lease_info(self) -> LeaseInfo:
        return self._lease_info

    @lease_info.setter
    def lease_info(self, lease_info: LeaseInfo):
        self._lease_info = lease_info

    @property
    def metadata(self) -> Dict[str, str]:
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: Dict[str, str]):
        self._metadata = metadata

    @property
    def last_updated_timestamp(self) -> int:
        return self._last_updated_timestamp

    @last_updated_timestamp.setter
    def last_updated_timestamp(self, last_updated_timestamp: int):
        self._last_updated_timestamp = last_updated_timestamp

    @property
    def last_dirty_timestamp(self) -> int:
        return self._last_dirty_timestamp

    @last_dirty_timestamp.setter
    def last_dirty_timestamp(self, last_dirty_timestamp: int):
        self._last_dirty_timestamp = last_dirty_timestamp

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, port: int):
        self._port = port

    @property
    def secure_port(self) -> int:
        return self._secure_port

    @secure_port.setter
    def secure_port(self, secure_port: int):
        self._secure_port = secure_port

    @property
    def action_type(self) -> ActionType:
        return self._action_type

    @action_type.setter
    def action_type(self, action_type: ActionType):
        self._action_type = action_type

    @property
    def host_name(self) -> str:
        return self._host_name

    @host_name.setter
    def host_name(self, host_name: str):
        self._host_name = host_name

    @property
    def is_secure_port_enabled(self) -> bool:
        return self._is_secure_port_enabled

    @is_secure_port_enabled.setter
    def is_secure_port_enabled(self, is_secure_port_enabled: bool):
        self._is_secure_port_enabled = is_secure_port_enabled

    @property
    def is_unsecure_port_enabled(self) -> bool:
        return self._is_unsecure_port_enabled

    @is_unsecure_port_enabled.setter
    def is_unsecure_port_enabled(self, is_unsecure_port_enabled: bool):
        self._is_unsecure_port_enabled = is_unsecure_port_enabled

    @property
    def status(self) -> Status:
        return self._status

    @status.setter
    def status(self, status: Status):
        self._status = status

    @property
    def overridden_status(self) -> Status:
        return self._overridden_status

    @overridden_status.setter
    def overridden_status(self, overridden_status: Status):
        self._overridden_status = overridden_status

    @property
    def is_instance_info_dirty(self) -> bool:
        return self._is_instance_info_dirty

    @is_instance_info_dirty.setter
    def is_instance_info_dirty(self, is_instance_info_dirty: bool):
        self._is_instance_info_dirty = is_instance_info_dirty

    @property
    def is_coordinating_discovery_server(self) -> bool:
        return self._is_coordinating_discovery_server

    @is_coordinating_discovery_server.setter
    def is_coordinating_discovery_server(self, is_coordinating_discovery_server: bool):
        self._is_coordinating_discovery_server = is_coordinating_discovery_server

    def is_port_enabled(self, port_type: PortType) -> bool:
        """
        Checks whether a port is enabled for traffic or not.

        Args:
            port_type: indicates whether it is secure or unsecure port.

        Returns: true if the port is enabled, false otherwise.

        """
        return {
            InstanceInfo.PortType.UNSECURE: self._is_unsecure_port_enabled,
            InstanceInfo.PortType.SECURE: self._is_secure_port_enabled,
        }.get(port_type, False)

    def is_dirty(self) -> bool:
        """
        Return whether any state changed so that EurekaClient can
        check whether to retransmit info or not on the next heartbeat.

        Returns: true if the instance is dirty, false otherwise.

        """
        return self._is_instance_info_dirty

    def is_dirty_with_time(self) -> Optional[int]:
        return self._last_dirty_timestamp if self._is_instance_info_dirty else None

    def set_is_dirty(self):
        """
        Set the dirty flag so that the instance information can be carried to
        the eureka server on the next heartbeat.
        """
        self._is_instance_info_dirty = True
        self._last_dirty_timestamp = current_timestamp()

    def set_is_dirty_with_time(self) -> int:
        """
        Set the dirty flag, and also return the timestamp of the is_dirty event.

        Returns: the timestamp when the isDirty flag is set.

        """
        self.set_is_dirty()
        return self._last_dirty_timestamp

    def unset_is_dirty(self, unset_dirty_timestamp: int):
        """
        Unset the dirty flag iff the unset_dirty_timestamp matches the last_dirty_timestamp. No-op if
        last_dirty_timestamp > unset_dirty_timestamp

        Args:
            unset_dirty_timestamp: the expected last_dirty_timestamp to unset.

        """
        if self._last_dirty_timestamp <= unset_dirty_timestamp:
            self._is_instance_info_dirty = False

    def set_last_updated_timestamp(self):
        self._last_updated_timestamp = current_timestamp()

    def set_is_coordinating_discovery_server(self):
        """
        Set the flag if this instance is the same as the eureka discovery server that is
        return the instances. This flag is used by the discovery clients to
        identify the discovery server which is coordinating/returning the
        information.
        """
        self._is_coordinating_discovery_server = True

    def set_status(self, status: Status) -> Optional[Status]:
        """
        Set the status for this instance.

        Args:
            status: status to be set for this instance.

        Returns: the previous status if a different status from the current was set, none otherwise.

        """
        if self._status != status:
            previous_status = self._status
            self._status = status
            self.set_is_dirty()
            return previous_status
        return None

    def set_status_without_dirty(self, status: Status):
        """
        Set the status for this instance without updating the dirty timestamp.

        Args:
            status: status to be set for this instance.

        """
        if self._status != status:
            self._status = status

    def set_overridden_status(self, status: Status):
        """
        Set the overridden status for this instance. Normally set by an external
        process to disable instance from taking traffic.

        Args:
            status: overridden status to be for this instance.

        """
        if self._overridden_status != status:
            self._overridden_status = status

    def register_runtime_metadata(self, metadata: Dict[str, str]):
        """
        Register application specific metadata to be sent to the eureka
        server.

        Args:
            metadata: Dictionary containing key/value pairs.

        """
        self._metadata.update(metadata)
        self.set_is_dirty()
