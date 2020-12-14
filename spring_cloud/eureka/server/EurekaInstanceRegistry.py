# -*- coding: utf-8 -*-

__author__ = "Ricky"
__license__ = "Apache 2.0"
# scip plugin
from eureka.client.app_info.instance_info import InstanceInfo
from eureka.server.registry.instance_registry import InstanceRegistry
from spring_cloud.utils.logging import getLogger


class EurekaInstanceRegistry(InstanceRegistry):
    def __init__(
        self,
        server_config,
        client_config,
        server_codecs,
        eureka_client,
        expected_number_of_clients_sending_renews=1,
        default_open_for_traffic_cnt=1,
    ):
        super().__init__()
        self._server_config = server_config
        self._client_config = client_config
        self._server_codecs = server_codecs
        self._eureka_client = eureka_client
        self.__logger = getLogger("spring_cloud")
        self._expected_number_of_clients_sending_renews = expected_number_of_clients_sending_renews
        self._default_open_for_traffic_cnt = default_open_for_traffic_cnt
        self._application_context = None

    def set_application_context(self, applicationContext):
        self._application_context = applicationContext

    def register(self, instance_info: InstanceInfo, lease_duration):
        self.handle_registration(instance_info, lease_duration)
        super().register(instance_info, lease_duration)

    def cancel(self, app_name: str, server_id: str) -> bool:
        self.handle_cancellation(app_name, server_id)
        return super().cancel(app_name, server_id)

    def handle_cancellation(self, app_name: str, id: str):
        self.__logger.info("cancel " + app_name + " server_id " + id)

    def handle_registration(self, info: InstanceInfo, lease_duration: int):
        self.__logger.info(
            "register " + info.app_name + " vip " + info.vip_address + ", lease_duration " + str(lease_duration)
        )
