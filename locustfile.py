# locust -f locust_files/my_locust_file.py --host=http://example.com
#'To run Locust distributed across multiple processes we would start a master process by specifying --master:
# locust -f D:\Development\CentrixLoadTest/locustfile.py --host=http://rdrazvoj/Centrix2VelikaBaza --no-web -c 4 -r 1
# locust -f D:\Development\CentrixLoadTest/locustfile.py --master --host=http://rdrazvoj/Centrix2VelikaBaza
# locust -f locust_files/locustfile.py --slave --master-host=127.0.0.1 --host=http://rdrazvoj/Centrix2VelikaBaza
#start of file


from locust import HttpLocust, TaskSet, task
from locust.clients import HttpSession
import requests
from requests_ntlm import HttpNtlmAuth

auth=HttpNtlmAuth('os\\test1','Omega12345;'))

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def login(self):
        self.auth=auth
        #self.client.post("/login", {"username":"ellen_key", "password":"education"})
        #print ("tu sam")
        #self.client.auth
        print ("Login")
        #session = requests.Session()
        #session = self.client.session()
       # self.client.get('http://rdrazvoj/Centrix2VelikaBaza')   

    def logout(self):
        #self.client.post("/logout", {"username":"ellen_key", "password":"education"})
        print ("Logout")

    @task(3)
    def HomePage(self):
        self.client.get("/",auth=auth)
        #self.client.get("/")
    @task(2)
    def PismenoBrowse(self):
        #self.client.get("/EvidencijaPismena/Pismeno/Browse")
        self.client.get("http://rdrazvoj/Centrix2VelikaBaza/EvidencijaPismena/Pismeno/Browse",auth=HttpNtlmAuth('os\\test1','Omega12345;'))
        #session = requests.Session()
        #session.get("/EvidencijaPismena/Pismeno/Browse")

   # @task(1)
    def PredmetBrowse(self):
       self.client.get("/EvidencijaPismena/Predmet/Browse",auth=HttpNtlmAuth('os\\vladimir','VolimCokoladu1926'))

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000