# -*- coding: utf-8 -*-
"""
A RESTful http client
"""
# standard library
from abc import ABC, abstractmethod
from typing import List, Tuple
from urllib.parse import ParseResult, urlparse

# pypi/conda library
from requests import sessions

# scip plugin
from spring_cloud.utils import logging

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


class HttpRequest:
    def __init__(
        self, method: str, url: str, params=None, headers=None, files=None, data=None, cookies=None, json=None, **kwargs
    ):
        self.__method = method
        self.url = url
        self.headers = headers
        self.files = files
        self.data = data
        self.params = params
        self.cookies = cookies
        self.json = json

    @property
    def method(self):
        return self.__method

    @method.setter
    def method(self, method: str):
        raise Exception("You can't set the http method.")

    def __str__(self):
        return str(self.__dict__)


class ClientHttpRequestInterceptor(ABC):
    @abstractmethod
    def intercept(self, http_request: HttpRequest):
        """
        Intercept the http request.
        Modify the http request's attribute to transform the request.
        """
        pass


class RestTemplate:
    """
    A Http Client instance that allows interception to every request.
    The implementation of this class is simply delegating to the lib `psf/requests`
    The documentation is also taken from `psf/requests`.
    """

    def __init__(self, interceptors: List[ClientHttpRequestInterceptor] = None):
        if interceptors is None:
            interceptors = []
        self.__interceptors = interceptors
        self.__logger = logging.getLogger("spring_cloud.http.RestTemplate")

    def request(self, method, url, **kwargs):
        """Constructs and sends a :class:`Request <Request>`.
        :param method: method for the new :class:`Request` object: ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
        :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
        :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
            ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
            or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
            defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
            to add for the file.
        :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional) How many seconds to wait for the server to send data
            before giving up, as a float, or a :ref:`(connect timeout, read
            timeout) <timeouts>` tuple.
        :type timeout: float or tuple
        :param allow_redirects: (optional) Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to ``True``.
        :type allow_redirects: bool
        :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
        :param verify: (optional) Either a boolean, in which case it controls whether we verify
                the server's TLS certificate, or a string, in which case it must be a path
                to a CA bundle to use. Defaults to ``True``.
        :param stream: (optional) if ``False``, the response content will be immediately downloaded.
        :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        Usage::
          >>> import requests
          >>> req = requests.request('GET', 'https://httpbin.org/get')
          >>> req
          <Response [200]>
        """
        self.__logger.info(f"[{method.upper()}] {url}")
        self.__logger.debug(str(kwargs))

        # By using the 'with' statement we are sure the session is closed, thus we
        # avoid leaving sockets open which can trigger a ResourceWarning in some
        # cases, and look like a memory leak in others.
        with sessions.Session() as session:
            return session.request(method=method, url=url, **kwargs)

    def get(self, url, params=None, **kwargs):
        r"""Sends a GET request.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param **kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        kwargs.setdefault("allow_redirects", True)
        kwargs["params"] = params
        url, kwargs = self.__intercept_request("get", url, kwargs)
        return self.request("get", url, **kwargs)

    def options(self, url, **kwargs):
        r"""Sends an OPTIONS request.
        :param url: URL for the new :class:`Request` object.
        :param **kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        kwargs.setdefault("allow_redirects", True)
        url, kwargs = self.__intercept_request("options", url, kwargs)
        return self.request("options", url, **kwargs)

    def head(self, url, **kwargs):
        r"""Sends a HEAD request.
        :param url: URL for the new :class:`Request` object.
        :param **kwargs: Optional arguments that ``request`` takes. If
            `allow_redirects` is not provided, it will be set to `False` (as
            opposed to the default :meth:`request` behavior).
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        kwargs.setdefault("allow_redirects", False)
        url, kwargs = self.__intercept_request("head", url, kwargs)
        return self.request("head", url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        r"""Sends a POST request.
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param **kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        kwargs["data"] = data
        kwargs["json"] = json
        url, kwargs = self.__intercept_request("post", url, kwargs)
        return self.request("post", url, **kwargs)

    def put(self, url, data=None, **kwargs):
        r"""Sends a PUT request.
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param **kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        kwargs["data"] = data
        url, kwargs = self.__intercept_request("put", url, kwargs)
        return self.request("put", url, **kwargs)

    def patch(self, url, data=None, **kwargs):
        r"""Sends a PATCH request.
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param **kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        kwargs["data"] = data
        url, kwargs = self.__intercept_request("patch", url, kwargs)
        return self.request("patch", url, **kwargs)

    def delete(self, url, **kwargs):
        r"""Sends a DELETE request.
        :param url: URL for the new :class:`Request` object.
        :param **kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        url, kwargs = self.__intercept_request("delete", url, kwargs)
        return self.request("delete", url, **kwargs)

    def __intercept_request(self, method, url, kwargs) -> Tuple[str, dict]:
        """
        Intercept the request and return the url after intercepted
        Returns:
            thr url (str)
        """
        http_request = HttpRequest(method=method, url=url, **kwargs)
        for interceptor in self.__interceptors:
            interceptor.intercept(http_request)

            # replace the attributes with the intercepted one if exists
            if http_request.params:
                kwargs["params"] = http_request.params
            if http_request.headers:
                kwargs["headers"] = http_request.headers
            if http_request.files:
                kwargs["files"] = http_request.files
            if http_request.data:
                kwargs["data"] = http_request.data
            if http_request.cookies:
                kwargs["cookies"] = http_request.cookies
            if http_request.json:
                kwargs["json"] = http_request.json
        return http_request.url, kwargs


# DEMO
class MyInterceptor(ClientHttpRequestInterceptor):
    def intercept(self, http_request: HttpRequest):
        url: ParseResult = urlparse(http_request.url)
        replaced: ParseResult = url._replace(netloc="vocabulary.com")
        http_request.url = replaced.geturl()
        if http_request.method == "get":
            http_request.params = {"get": "True"}
        if http_request.method == "options":
            http_request.cookies = {"options": "True"}
        if http_request.method == "head":
            http_request.params = {"head": "True"}
        if http_request.method == "post":
            http_request.json = '{"post": True}'
        if http_request.method == "patch":
            http_request.data = b"patch"
        if http_request.method == "put":
            http_request.data = b"put"
        if http_request.method == "delete":
            http_request.headers = {"delete": "True"}


if __name__ == "__main__":
    api = RestTemplate([MyInterceptor()])
    api.get("http://google.com/get")
    api.post("http://google.com/post")
    api.patch("http://google.com/patch")
    api.put("http://google.com/put")
    api.delete("http://google.com/delete")
    api.options("http://google.com/options")
    api.head("http://google.com/head")
