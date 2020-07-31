import random
from locust import HttpUser, task, between


class MutantValidator(HttpUser):
    wait_time = between(1, 2)

    @task
    def index_page(self):
        self.client.get("/stats")

    @task(3)
    def view_item(self):
        self.client.post("/mutant", json={"dna": ["AAAA"]})
