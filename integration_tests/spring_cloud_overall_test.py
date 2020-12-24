# -*- coding: utf-8 -*-
"""
The integration tests
"""

# standard library
import time

# pypi/conda library
import requests
from testcontainers.compose import DockerCompose

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

NUMBER_OF_MESSAGES = 10


def test():
    global NUMBER_OF_MESSAGES
    with DockerCompose(".", compose_file_name="overall-test.yml") as compose:
        # (*) Use gateway to route requests to the downstream services
        port = compose.get_service_port("api-gateway-svc", 80)
        time.sleep(8)  # wait for the server to be ready
        gateway_base_url = f"http://localhost:{port}"

        # (1) sign-up a new user
        user = sign_up_user_on_all_services(gateway_base_url=gateway_base_url)
        user_id = user["id"]
        assert user_id == 0, "New user's id should start from zero."

        # (2) post messages
        post_messages(poster_id=user_id, gateway_base_url=gateway_base_url)

        # (3) query messages (this involves service-discovery)
        query_all_messages(poster=user, repeat_time=6, gateway_base_url=gateway_base_url)

        stdout, stderr = compose.get_logs()
        print(stdout)
        print(stderr)


def sign_up_user_on_all_services(gateway_base_url):
    users = []
    for i in range(3):
        users.append(
            requests.post(
                f"{gateway_base_url}/api/users/signUp",
                json={"name": "johnny", "account": "account", "password": "password"},
            ).json()
        )
    for user in users:
        assert user["id"] == 0, (
            f"Assert load-balancing, the sign-up should be handled by the three replicas, "
            f"thus the ids all should be zeros. Given: {','.join([str(u['id']) for u in users])}"
        )

    return users[0]


def post_messages(poster_id, gateway_base_url):
    global NUMBER_OF_MESSAGES
    for i in range(0, NUMBER_OF_MESSAGES):
        message = requests.post(
            f"{gateway_base_url}/api/messages", headers={"poster-id": str(poster_id)}, json={"content": i}
        ).json()

        assert message["poster_id"] == poster_id
        assert message["id"] == i


def query_all_messages(poster, repeat_time: int, gateway_base_url):
    for i in range(0, repeat_time):
        messages = requests.get(f"{gateway_base_url}/api/messages").json()
        assert len(messages) == NUMBER_OF_MESSAGES
        assert (
            len([m for m in messages if m["content"] == str(m["id"]) and m["poster"] == poster]) == NUMBER_OF_MESSAGES
        ), "The aggregated message's response is incorrect."
