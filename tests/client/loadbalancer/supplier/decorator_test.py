# -*- coding: utf-8 -*-
# standard library
from unittest.mock import Mock

# scip plugin
from commons.client.loadbalancer.supplier.decorator import CachingServiceInstanceListSupplier
from external.cache.cache_manager import NaiveCacheManager
from tests.client.loadbalancer.supplier.stubs import INSTANCES

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


class TestCachingServiceInstanceListSupplier:
    def setup_class(self):
        self.delegate = Mock()
        self.delegate.get = Mock(return_value=INSTANCES)
        self.supplier = CachingServiceInstanceListSupplier(NaiveCacheManager(), self.delegate)

    def test_Given_cache_When_10_invocations_Then_only_1_cache_miss_and_delegate(self):
        for i in range(1, 10):
            self.supplier.get()
        assert self.delegate.get.call_count == 1
