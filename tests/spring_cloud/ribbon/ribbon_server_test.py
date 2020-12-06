# -*- coding: utf-8 -*-

__author__ = "Ssu-Tsen"
__license__ = "Apache 2.0"

# scip plugin
from ribbon.loadbalancer.server import Server
from spring_cloud.ribbon.ribbon_server import RibbonServer

server_ = Server(host="127.0.0.1", port=56747, scheme="https")
server2 = Server(uri="http://127.0.0.1:56747")
ribbon_server = RibbonServer(service_id="1", server=server_, secure=True)
ribbon_server2 = RibbonServer(service_id="1", server=server2, secure=True)


def test_get_instance_id():
    assert ribbon_server2.instance_id == server2.id


def test_get_service_id():
    assert ribbon_server.service_id == "1"


def test_get_host():
    assert ribbon_server.host == server_.host


def test_get_port():
    assert ribbon_server.port == server_.port


def test_secure():
    assert ribbon_server.secure == True


def test_get_uri():
    host_ = ribbon_server.host
    port_ = ribbon_server.port
    assert ribbon_server.uri == f"https://{host_}{port_}"


def test_get_scheme():
    assert ribbon_server.scheme == "https"
