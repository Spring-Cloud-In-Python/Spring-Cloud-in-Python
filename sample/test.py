# standard library
import time

# pypi/conda library
import requests

# scip plugin
import spring_cloud.context.bootstrap_client as spring_cloud_bootstrap

if __name__ == "__main__":
    numbers = [i for i in range(1, 101)]

    client = spring_cloud_bootstrap.enable_service_discovery(
        service_id="test", port=35677, eureka_server_urls=["http://localhost:8761/eureka/v2/"]
    )
    time.sleep(2)

    instance = client.get_instances("sum-service")[0]
    sum = requests.post(f"http://{instance.host}:{instance.port}/api/sum", json={"numbers": numbers}).text
    print(f"Sum = {sum}")

    loads = []
    for instance in client.get_instances("sum-service"):
        loads.append(requests.get(f"http://{instance.host}:{instance.port}/api/sum/load").text)

    print("Workload:  ", end="")
    print(", ".join([load for load in loads]))
