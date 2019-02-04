from locust import HttpLocust, TaskSet, task
from locust.clients import HttpSession
from requests_ntlm import HttpNtlmAuth
from argparse import Namespace
from generated_tests import GeneratedTests
from custom_tests import CustomTests
import requests
import locust.stats

class PerfTestTasks(TaskSet):
    tasks = {
        GeneratedTests: 80,
        CustomTests: 20
    }
  
class WebsiteUser(HttpLocust):
    locust.stats.CSV_STATS_INTERVAL_SEC = 600
    task_set = PerfTestTasks
    min_wait = 0.5*1000
    max_wait = 12*1000