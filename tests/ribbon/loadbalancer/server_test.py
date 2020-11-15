# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from ribbon.loadbalancer.server import Server


def test_init():
    server = Server(id="http://127.0.0.1:56747")
    assert server.get_host() == "127.0.0.1"
    assert server.get_port() == 56747
    assert server.is_ready_to_serve() == True
    assert server.is_alive() == False


def test_init_spam1():
    server = Server(id="this is a spam")
    assert server.get_host() == "this is a spam"
    assert server.get_port() == 80
    assert server.get_id() == "this is a spam:80"


def test_normalized_id():
    assert Server.normalize_id("HTTP://127.0.0.1:56747") == "127.0.0.1:56747"


def test_get_host_port():
    hostPort = Server.get_host_port("HTTP://127.0.0.1:56747")
    assert hostPort[0] == "127.0.0.1"
    assert hostPort[1] == 56747


def test_staic_variables():
    assert Server.UNKNOWN_ZONE == "UNKNOWN"


def test_get_set_host():
    server = Server(id="http://127.0.0.1:56747")
    server.set_host("195.23.54.1")
    assert server.get_host() == "195.23.54.1"


def test_get_set_port():
    server = Server(id="http://127.0.0.1:56747")
    server.set_port(8080)
    assert server.get_port() == 8080


def test_get_set_zone():
    server = Server(id="http://127.0.0.1:56747")
    server.set_zone("Asia")
    assert server.get_zone() == "Asia"


def test_get_set_ready_to_serve():
    server = Server(id="http://127.0.0.1:56747")
    server.set_ready_to_serve(True)
    assert server.is_ready_to_serve() == True
