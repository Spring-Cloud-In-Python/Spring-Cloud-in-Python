# -*- coding: utf-8 -*-

__author__ = "Ricky"
__license__ = "Apache 2.0"

# scip plugin
from eureka.core.eureka_server_context import EurekaServerContext
from eureka.core.eureka_server_context_holder import EurekaServerContextHolder
from spring_cloud.utils.logging import getLogger


class EurekaServerBootstrap:
    def __init__(self, application_info_manager, eureka_client_config, eureka_server_config, registry, server_context):
        self._application_info_manager = application_info_manager
        self._eureka_client_config = eureka_client_config
        self._eureka_server_config = eureka_server_config
        self._registry = registry  # PeerAwareInstanceRegistry
        self._server_context = server_context
        self.__logger = getLogger("spring cloud")

    def context_initialized(self, context):
        try:
            self.init_eureka_environment()
            self.init_eureka_server_context()
            context.set_attribute(EurekaServerContext.__name__, self._server_context)

        except RuntimeError:
            self.__logger.info("Cannot bootstrap eureka server!")
            raise

    def context_destroyed(self, context):
        try:
            self.__logger.info("Shutting down Eureka Server..")
            context.remove_attribute(EurekaServerContext.__name__)
            self.destroy_eureka_server_context()
            self.destroy_eureka_environment()

        except RuntimeError:
            self.__logger.info()

        finally:
            self.__logger.info("Eureka Service is now shutdown...")

    def init_eureka_environment(self):
        self.__logger.info("Setting the eureka configuration..")
        pass

    def destroy_eureka_environment(self):
        pass

    def init_eureka_server_context(self):
        EurekaServerContextHolder.initialize(self._server_context)
        self.__logger.info("Initialized server context")

        registry_count = self._registry.sync_up()
        self._registry.open_for_traffic(self._application_info_manager, registry_count)

    def destroy_eureka_server_context(self):
        if self._server_context is not None:
            self._server_context.shutdown()
