# -*- coding: utf-8 -*-
"""
The integration tests
"""

# pypi/conda library
import requests
from testcontainers.compose import DockerCompose

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


def test():
    with DockerCompose(".", compose_file_name="gateway-test.yml") as compose:
        # (*) Use gateway to route requests to the downstream services
        port = compose.get_service_port("api-gateway-svc", 80)
        gateway_base_url = f"http://localhost:{port}"

        # (1) Happy Path
        assert f"HI, Johnny (user), Question: 1 + 1 = ?" == get_puzzle(gateway_base_url, "Johnny", "True")
        assert f"HI, Johnny (user), your answer (2) is correct." == post_answer(gateway_base_url, "Johnny", "True", "2")

        # (2) Sad Path --> (Guest): The cookie 'is-user' != (True|true|TRUE)
        assert f"HI, Johnny (guest), Question: 1 + 1 = ?" == get_puzzle(gateway_base_url, "Johnny", "False")
        assert f"HI, Johnny (guest), Question: 1 + 1 = ?" == get_puzzle(gateway_base_url, "Johnny", "T")
        assert f"HI, Johnny (guest), Question: 1 + 1 = ?" == get_puzzle(gateway_base_url, "Johnny", "TRue")
        assert f"HI, Johnny (guest), Question: 1 + 1 = ?" == get_puzzle(gateway_base_url, "Johnny", "tr ue")

        # (3) Sad Path --> Wrong Answer
        assert f"HI, Johnny (user), your answer (20000) is wrong." == post_answer(
            gateway_base_url, "Johnny", "True", "20000"
        )

        # (3) Sad Path --> 404 Not Found
        assert 404 == requests.get(f"{gateway_base_url}/notfound").status_code
        assert 404 == requests.get(f"{gateway_base_url}/api/puzzle").status_code
        assert 404 == requests.get(f"{gateway_base_url}/api/answer").status_code


def get_puzzle(gateway_base_url: str, name: str, is_user: str):
    return requests.get(f"{gateway_base_url}/puzzle", params={"name": name}, cookies={"is_user": is_user}).text


def post_answer(gateway_base_url: str, name: str, is_user: str, answer: str):
    return requests.post(
        f"{gateway_base_url}/answer", params={"name": name}, cookies={"is_user": is_user}, json={"content": answer}
    ).text
