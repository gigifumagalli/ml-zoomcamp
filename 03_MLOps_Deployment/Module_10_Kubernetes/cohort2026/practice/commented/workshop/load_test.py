# Commented copy of ../../../notebooks/workshop/load_test.py (2025 workshop).
# GOAL: hammer the service with concurrent requests so CPU rises and the HPA scales out.
# Run it while `kubectl get hpa -w` and `kubectl get pods -w` are open in two other terminals.
# NOTE: for HW10 the load-test observation is optional and not graded; the URL and body would have to be
#       changed to the lead-scoring API (localhost:9696/predict + a lead record).

import time
import requests

from concurrent.futures import ThreadPoolExecutor, as_completed


# WHY: port 30080 is the local end of `kubectl port-forward service/clothing-classifier 30080:8080`.
#      Caveat: port-forward tunnels to ONE pod, so a load test through it does not spread over replicas.
url = 'http://localhost:30080/predict'

request_data = {
    "url": "http://bit.ly/mlbookcamp-pants"
}


# GOAL: one request; return the status code, or the error text instead of crashing the whole test.
# PYTHON: the argument is unused (named _ by convention); executor.submit needs something to pass.
def send_request(_):
    try:
        response = requests.post(url, json=request_data, timeout=5)
        return response.status_code
    except Exception as e:
        return f"Error: {e}"


print("Starting load test...")

print("Watch HPA with: kubectl get hpa -w")
print("Watch pods with: kubectl get pods -w")

num_requests = 1000
concurrent_workers = 50


print(f"Sending {num_requests} requests with {concurrent_workers} concurrent workers")
print()

start_time = time.time()


# WHY: threads are fine here: each one mostly WAITS on the network (I/O-bound), so the GIL does not matter.
# PYTHON: submit() schedules a call and returns a Future; as_completed() yields futures as they finish.
with ThreadPoolExecutor(max_workers=concurrent_workers) as executor:
    futures = [executor.submit(send_request, i) for i in range(num_requests)]
    results = [future.result() for future in as_completed(futures)]


end_time = time.time()
duration = end_time - start_time

# PYTHON: sum(1 for ... if ...) counts the items that satisfy the condition.
success_count = sum(1 for r in results if r == 200)
error_count = len(results) - success_count


print("Load test complete!")

print(f"Duration: {duration:.2f} seconds")
print(f"Requests per second: {len(results)/duration:.2f}")
print(f"Successful requests: {success_count}")
print(f"Failed requests: {error_count}")
print()
