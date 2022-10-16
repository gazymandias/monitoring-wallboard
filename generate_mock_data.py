import requests
import random
from time import sleep

status = ["success", "error", "warning", "danger", ""]
task = ["exit_sap", "open_sap", "action_1", "action_2", "action_3", "run_checks"]


def send_request(request_type, url, data=None):
    try:
        if request_type.upper() == 'POST':
            x = requests.post(url, json=data)
            print("item created")
            return x
        if request_type.upper() == 'GET':
            x = requests.get(url)
            print(x)
            return x
        if request_type.upper() == 'UPDATE':
            x = requests.put(url, json=data)
            print("item updated")
            return x
    except Exception as e:
        print(e)
        raise


def create_dummy_data(count: int):
    while count > 0:
        numerator = random.randint(1, 10)
        send_request(request_type='post', url="http://localhost:80/items", data={
            "name": f"robot_{count}",
            "status": random.choice(status),
            "task": random.choice(task),
            "process": f"process_{count}",
            "numerator": numerator,
            "denominator": numerator + random.randint(0, 10),
            "started_at": "2022-10-16"
        })
        count -= 1
    return


def simulate_data_change(id):
    numerator = random.randint(1, 10)
    x = send_request(request_type='UPDATE', url=f"http://localhost:80/items/{id}", data={
        "name": f"robot_{id}",
        "status": random.choice(status),
        "task": random.choice(task),
        "process": f"process_{id}",
        "numerator": numerator,
        "denominator": numerator + random.randint(0, 10),
        "started_at": "2022-10-16"
    })
    return x


def main():
    dummy_records = 16
    create_dummy_data(dummy_records)
    loop_count = 10
    while loop_count > 0:
        dupe_count = 4
        while dupe_count > 0:
            id = random.randint(1, dummy_records)
            simulate_data_change(id)
            dupe_count -= 1
        sleep(5)
        loop_count -= 1
    return


if __name__ == '__main__':
    # main()
    count = 16
    print(random.randint(1, count))
