from locust import HttpLocust, TaskSet, task
from locust.clients import HttpSession
from requests_ntlm import HttpNtlmAuth
from argparse import Namespace
from generated_tests import LoadTests
import requests
import locust.stats

class WebsiteUser(HttpLocust):
    locust.stats.CSV_STATS_INTERVAL_SEC = 600
    task_set = LoadTests
    min_wait = 500
    max_wait = 12000