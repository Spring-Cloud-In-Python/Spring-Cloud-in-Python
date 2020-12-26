# standard library
import time

# pypi/conda library
import requests

# scip plugin
import spring_cloud.context.bootstrap_client as spring_cloud_bootstrap

if __name__ == "__main__":
    numbers = [i for i in range(1, 200)]

    sum = requests.post("http://localhost:80/api/sum", json={"numbers": numbers}).text
    print(f"Sum = {sum}")

    client = spring_cloud_bootstrap.enable_service_discovery(
        service_id="test", port=35677, eureka_server_urls=["http://localhost:8761/eureka/v2/"]
    )
    time.sleep(2)
    loads = []
    for instance in client.get_instances("sum-service"):
        loads.append(requests.get(f"http://localhost:{instance.port}/api/sum/load").text)
    print(", ".join([load for load in loads]))
