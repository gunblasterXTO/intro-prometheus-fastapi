import random
import time

from fastapi import FastAPI
from prometheus_client import Counter, Histogram, make_asgi_app


app = FastAPI()
metric_app = make_asgi_app()
app.mount("/metrics", metric_app)


http_req_count = Counter(
    name="http_request_total",
    documentation="The total number of processed HTTP requests.",
    labelnames=["endpoint", "method", "status_code"]
)
http_req_latency = Histogram(
    name="http_request_latency",
    documentation="The total time needed to process an HTTP request.",
    labelnames=["endpoint", "method"]
)


@app.get("/hello")
def hello():
    start_time = time.perf_counter()

    time.sleep(random.randint(0, 1))

    http_req_latency\
        .labels("/hello", "GET")\
        .observe(time.perf_counter() - start_time)

    http_req_count.labels("/hello", "GET", "200").inc()

    return "hello world!"
