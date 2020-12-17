# scip plugin
from eureka.client.discovery.shared.resolver.eureka_endpoint import DefaultEndpoint


def test_default_endpoint_Given_valid_url():
    endpoint = DefaultEndpoint("https://myhostname:8000/eureka/v2")

    assert endpoint.host_name == "myhostname"
    assert endpoint.relative_uri == "/eureka/v2"
    assert endpoint.port == 8000
    assert endpoint.is_secure
