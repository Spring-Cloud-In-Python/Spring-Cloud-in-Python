# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# pypi/conda library
import pytest

# scip plugin
from ribbon.loadbalancer.server import Server


def test_init_given_uri():
    server = Server(uri="http://127.0.0.1:56747")
    assert server.get_host() == "127.0.0.1"
    assert server.get_port() == 56747


def test_init_given_host_port_scheme():
    server = Server(host="127.0.0.1", port=56747, scheme="https")
    assert server.get_host() == "127.0.0.1"
    assert server.get_port() == 56747


def test_init_given_host_diff_in_uri():
    with pytest.raises(Exception):
        server = Server(host="127.0.0.1", uri="http://198.21.3.4:5432/")


def test_init_given_host_diff_in_port():
    with pytest.raises(Exception):
        server = Server(port=80, uri="http://198.21.3.4:5432/")


def test_init_given_host_diff_in_scheme():
    with pytest.raises(Exception):
        server = Server(scheme="https", uri="http://198.21.3.4:5432/")


def test_init_given_sapm_without_semicolon():
    server = Server(uri="this is a spam")
    assert server.get_host() == "this is a spam"
    assert server.get_port() == 80
    assert server.get_id() == "this is a spam:80"


def test_init_given_sapm_with_semicolon():
    with pytest.raises(ValueError):
        server = Server(uri="this is a spam:")


def test_normalized_id():
    assert Server.normalize_id("HTTP://127.0.0.1:56747") == "127.0.0.1:56747"
