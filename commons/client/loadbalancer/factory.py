# -*- coding: utf-8 -*-
# scip plugin
from commons.client.loadbalancer.loadbalancer import LoadBalancer

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


class LoadBalancerClientFactory:
    def get_instance(self, service_id: str) -> LoadBalancer:
        """
        :param service_id: (str)
        :return:
        """
        pass
