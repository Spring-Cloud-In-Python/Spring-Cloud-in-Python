# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from ribbon.loadbalancer.server_list import ServerList
from ribbon.loadbalancer.server_list_filter import ServerListFilter
from ribbon.loadbalancer.server_list_filter_factory import ServerListFilterFactory

"""
The class includes an API to create a filter to be use by load balancer
to filter the servers returned from {@link #getUpdatedListOfServers()}
or {@link #getInitialListOfServers()}.
"""


class AbstractServerList(ServerList):
    def get_filter_impl(self, serverListFilterFactory: ServerListFilterFactory) -> ServerListFilter:
        serverListFilter = serverListFilterFactory.create()

        return serverListFilter
