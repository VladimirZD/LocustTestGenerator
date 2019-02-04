from locust import HttpLocust, TaskSet, task
from locust.clients import HttpSession
from requests_ntlm import HttpNtlmAuth
import uuid
import json

#Tests which are not generated, this tests are written by user and it won't be overwritten by generated ones.
class CustomTests(TaskSet):
	@task(2)
	def CustomTest1(self):
		self.client.get('/')
	#@task(1)
	def CustomTest2(self):
		self.client.get('/')
		


