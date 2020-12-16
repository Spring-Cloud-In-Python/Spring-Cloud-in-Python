# -*- coding: utf-8 -*-

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from typing import Dict, List, Optional
from unittest.mock import Mock

# scip plugin
from spring_cloud.gateway.filter.http_headers_filter import (
    ForwardedHeadersFilter,
    RemoveHopByHopHeadersFilter,
    XForwardedHeadersFilter,
)
from spring_cloud.gateway.server import DefaultServerWebExchange, StaticServerHttpRequest


def dose_not_contains_key(headers: Dict[str, str], keys: List[str]):
    if any(headers.get(key) for key in keys):
        return False
    return True


default_http_headers = {
    "User-Agent": "PostmanRuntime/7.26.8",
    "Accept": "*/*",
    "Host": "127.0.0.1:8888",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}


def assert_default_headers(headers: Dict[str, str]):
    assert headers["User-Agent"] == "PostmanRuntime/7.26.8"
    assert headers["Accept"] == "*/*"
    assert headers["Host"] == "127.0.0.1:8888"
    assert headers["Accept-Encoding"] == "gzip, deflate, br"
    assert headers["Connection"] == "keep-alive"


class TestForwardedHeadersFilter:
    def given_forward_header(self, headers: Dict[str, str]):
        request = StaticServerHttpRequest(
            url_="http://127.0.0.1:8888/get", headers=headers, remote_addr=("10.0.0.1", 51630)
        )
        response = Mock()
        self.exchange = DefaultServerWebExchange(request, response)
        self.filter = ForwardedHeadersFilter()

    def test_Given_forward_headers_When_Then_return_new_headers(self):
        self.given_forward_header({"Forwarded": "for=12.34.56.78;host=example.com;proto=https; for=23.45.67.89"})
        headers = self.filter.filter(self.exchange.request.headers, self.exchange)
        assert (
            headers[self.filter.FORWARDED_HEADER]
            == 'for=12.34.56.78;host=example.com;proto=https; for=23.45.67.89;host="127.0.0.1";proto=http;for="10.0.0.1:51630"'
        )

    def test_Given_forward_headers_does_not_exist_When_Then_return_new_headers(self):
        self.given_forward_header({"Host": "127.0.0.1:8888"})
        headers = self.filter.filter(self.exchange.request.headers, self.exchange)
        assert headers[self.filter.FORWARDED_HEADER] == 'host="127.0.0.1";proto=http;for="10.0.0.1:51630"'


class TestXForwardedHeadersFilter:
    filter = XForwardedHeadersFilter()

    def given_http_request(self, headers: Dict[str, str], raddr: Optional[tuple], laddr: Optional[tuple]):
        request = StaticServerHttpRequest(
            url_="http://127.0.0.1:8888/get", headers=headers, remote_addr=raddr, local_addr=laddr
        )
        response = Mock()
        self.exchange = DefaultServerWebExchange(request, response)

    def test_Given_remote_addr_is_none(self):
        self.given_http_request({"chao": "fish"}, None, None)
        headers = self.filter.filter(self.exchange.request.headers, self.exchange)
        assert headers[self.filter.X_FORWARDED_HOST_HEADER] == "127.0.0.1:8888"
        assert headers[self.filter.X_FORWARDED_PROTO_HEADER] == "http"
        assert headers[self.filter.X_FORWARDED_PORT_HEADER] == "8888"

    def test_Given_x_forwarded_headers_do_not_exist(self):
        self.given_http_request({"chao": "fish"}, ("10.0.0.1", 51630), ("10.0.0.1", 51333))
        headers = self.filter.filter(self.exchange.request.headers, self.exchange)
        assert headers[self.filter.X_FORWARDED_HOST_HEADER] == "127.0.0.1:8888"
        assert headers[self.filter.X_FORWARDED_PROTO_HEADER] == "http"
        assert headers[self.filter.X_FORWARDED_PORT_HEADER] == "8888"
        assert headers[self.filter.X_FORWARDED_FOR_HEADER] == "10.0.0.1"

    def test_Given_x_forwarded_headers_Then_append_headers(self):
        headers = {
            self.filter.X_FORWARDED_FOR_HEADER: "192.168.0.2",
            self.filter.X_FORWARDED_HOST_HEADER: "example.com",
            self.filter.X_FORWARDED_PORT_HEADER: "443",
            self.filter.X_FORWARDED_PROTO_HEADER: "https",
        }
        self.given_http_request(headers, ("10.0.0.1", 51630), ("10.0.0.1", 51333))
        headers = self.filter.filter(self.exchange.request.headers, self.exchange)
        assert headers[self.filter.X_FORWARDED_HOST_HEADER] == "example.com,127.0.0.1:8888"
        assert headers[self.filter.X_FORWARDED_PROTO_HEADER] == "https,http"
        assert headers[self.filter.X_FORWARDED_PORT_HEADER] == "443,8888"
        assert headers[self.filter.X_FORWARDED_FOR_HEADER] == "192.168.0.2,10.0.0.1"


class TestRemoveHopByHopHeadersFilter:
    filter = RemoveHopByHopHeadersFilter()

    def given_http_request(self, hop_by_hop_headers: Dict[str, str]):
        headers = {**default_http_headers, **hop_by_hop_headers}
        request = StaticServerHttpRequest(url_="http://127.0.0.1:8888/get", headers=headers)
        response = Mock()
        self.exchange = DefaultServerWebExchange(request, response)

    def test_Given_hop_by_hop_header_Then_remove_all_of_them(self):
        hop_by_hop_headers = {}
        for header in self.filter.HEADERS_REMOVED_ON_REQUEST:
            hop_by_hop_headers[header] = f"{header}_1"
        self.given_http_request(hop_by_hop_headers)
        headers = self.filter.filter(self.exchange.request.headers, self.exchange)
        assert dose_not_contains_key(headers, self.filter.HEADERS_REMOVED_ON_REQUEST)

    def test_Given_hop_by_hop_header_in_lower_case_Then_remove_all_of_them(self):
        hop_by_hop_headers = {}
        for header in self.filter.HEADERS_REMOVED_ON_REQUEST:
            hop_by_hop_headers[header] = f"{header.lower()}_1"
        self.given_http_request(hop_by_hop_headers)
        headers = self.filter.filter(self.exchange.request.headers, self.exchange)
        assert dose_not_contains_key(headers, self.filter.HEADERS_REMOVED_ON_REQUEST)

    def test_Given_Connection_header_Then_remove_all_of_them(self):
        hop_by_hop_headers = {"connection": "upgrade,keep-alive", "upgrade": "WebSocket", "Keep-Alive": "timeout:5"}
        self.given_http_request(hop_by_hop_headers)
        headers = self.filter.filter(self.exchange.request.headers, self.exchange)
        assert dose_not_contains_key(headers, self.filter.HEADERS_REMOVED_ON_REQUEST)
