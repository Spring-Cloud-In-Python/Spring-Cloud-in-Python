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


def test_init_given_uri_with_more_than_two_slash_after_http_or_https_should_raise():
    with pytest.raises(Exception):
        server = Server(uri="http:///127.0.0.1:56747")


def test_init_given_uri_without_port_and_semicolon_should_raise():
    with pytest.raises(Exception):
        server = Server(uri="https://127.0.0.1")


def test_init_given_uri_without_port_should_raise():
    with pytest.raises(Exception):
        server = Server(uri="https://127.0.0.1:")


def test_init_given_uri_less_than_two_slash_after_http_or_https_should_raise():
    with pytest.raises(Exception):
        server = Server(uri="http:/127.0.0.1:56747")


def test_init_given_uri_with_path():
    server = Server(uri="http://127.0.0.1:56747/account/saved")
    assert server.get_host() == "127.0.0.1"
    assert server.get_port() == 56747


def test_init_given_uri_with_multiple_semiclon_before_port_should_raise():
    with pytest.raises(Exception):
        server = Server(uri="http://127.0.0.1::56747")


def test_init_given_uri_without_http_or_https_should_raise():
    with pytest.raises(Exception):
        server = Server(uri="127.0.0.1:56747")


def test_init_given_host_port_scheme():
    server = Server(host="127.0.0.1", port=56747, scheme="https")
    assert server.get_host() == "127.0.0.1"
    assert server.get_port() == 56747


def test_init_given_inconsistent_host_and_uri_should_raise():
    with pytest.raises(Exception):
        server = Server(host="127.0.0.1", uri="http://198.21.3.4:5432/")


def test_init_given_inconsistent_port_and_uri_should_raise():
    with pytest.raises(Exception):
        server = Server(port=80, uri="http://198.21.3.4:5432/")


def test_init_given_inconsistent_scheme_and_uri_should_raise():
    with pytest.raises(Exception):
        server = Server(scheme="https", uri="http://198.21.3.4:5432/")


def test_init_given_spam_without_semicolon():
    with pytest.raises(Exception):
        server = Server(uri="this is a spam")


def test_init_given_spam_with_semicolon():
    with pytest.raises(Exception):
        server = Server(uri="this is a spam:")


def test_normalized_id():
    assert Server.normalize_id("HTTP://127.0.0.1:56747") == "127.0.0.1:56747"
