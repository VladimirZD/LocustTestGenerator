#TODO Post test





import argparse
import datetime
import fileinput, sys,os
import timeit
import shutil
import json
import re
import random
from collections import OrderedDict


def logEvent(message):
  print ('[%s] %s' % (str(datetime.datetime.now().time()),message))

def ensure_path_exists(path):
  '''Check if file/folder exists and create if not'''
  if not os.path.exists(path):
        os.mkdir(path)
      
def check_if_path_exists(path):
  '''Check if file/folder exists'''
  if not os.path.exists(path):
      msg = 'Path %s is invalid' %(path)
      raise IOError(msg)

def get_files_in_folder(path,extensions):
  files=[]
  try:
    for entry in os.scandir(path):
      if entry.is_file() and os.path.splitext(entry)[1].lower() in extensions:
        files.append(entry.path)
  except OSError:
      logEvent('Cannot access ' + path +'. Probably a permissions error')
  return files

def get_test_user(users,username):
  #returns user or random one if username =='random'
  key = username if username!='random' else (random.choice(list(users.keys())))
  return key,users[key]
  
def fill_test_users(userData):
  users=dict()
  for user in userData:
    users[user['username']]=user['password']
  return users

def escape_string(string):
  return string.replace("'", "\\'")

def generate_tests(requests):
  logEvent('Generating tests')
  generated_test_file = 'generated_tests.py'
  test_template_file='settings.json'
  
  with open(test_template_file) as json_file:  
    test_data = json.load(json_file)

  with open(generated_test_file, 'w') as destination:
      imports = test_data['imports']
      test_class = test_data['test_class']
      task_template = test_data['test_template']
      test_users = fill_test_users(test_data['test_users'])
      print (imports,file=destination)
      print (test_class,file=destination)
      i=0
      for item in requests.items():
        i+=1
        url =escape_string(item[1]['url'])
        group_name = url
        url = url+'?'+escape_string(item[1]['query_param'])
        weight = str(item[1]['count'])
        user,password =get_test_user(test_users,'random')
        task_name='Test%s' %(str(i))
        task =task_template.replace('<TASK_WEIGHT>',weight).replace('<URL>',url).replace('<TASK_NAME>',task_name).replace('<GROUP_NAME>',group_name).replace('<USER>',user).replace('<PASSWORD>',password)
        print (task,file=destination)

def remove_not_popular_requests(requests):
  requests_truncated=OrderedDict()
  total_cnt =0
  for item in requests.items():
     total_cnt =total_cnt+item[1]['count']
  target_cnt = total_cnt*cutoff
  cnt=0
  for item in requests.items():
    cnt =cnt+item[1]['count']
    requests_truncated[item[0]]=item[1]
    if (cnt>=target_cnt):
      logEvent('Processed %i%% requests breaking out...' %(cutoff*100))
      break

  logEvent('Total number of requests %i' %(len(requests_truncated)))
  return requests_truncated

def process_log_files():
    files =[]
    request_data=dict()
    if not logs_folder=='':
        files = get_files_in_folder(logs_folder,extensions)
    cnt =len(files)
    i=0
    start = timeit.default_timer()
    for file in files:
        start = timeit.default_timer()
        i+=1
        logEvent ('Processing file %s (file %d of %d) please wait.' % (file,i,cnt))
        request_data = parse_log_file(file,request_data)
        destination = os.path.join(os.path.split(file)[0],'Processed')
        ensure_path_exists(destination)
        newFileName = os.path.join(destination,os.path.split(file)[1])
        elapsed = timeit.default_timer()-start
        files_per_second = (i/elapsed)  
        logEvent ('File %s processed.Moving to %s. Current processing speed: %f files/second. Estimated remaining time %s' % (file,newFileName,files_per_second,str(datetime.timedelta(seconds=(cnt-i)/files_per_second))))  
    logEvent ('Sorting items')
    ordered_requests = OrderedDict(sorted(request_data.items(), key=lambda x: x[1]['count'],reverse=True ))
    final_requests = remove_not_popular_requests (ordered_requests)
    target_file ='payload.json'
    with open(target_file, 'w') as destination:
      logEvent ('Generating file %s. Please wait' % (target_file))
      dump = json.dumps(final_requests,indent=1)
      print(dump, file=destination)
    generate_tests(final_requests)

def parse_log_file(file_name,data):
  headers = ['date', 'time', 's-ip', 'cs-method', 'cs-uri-stem', 'cs-uri-query', 's-port', 'cs-username', 'c-ip', 'cs(User-Agent)', 'cs(Referer)', 'sc-status', 'sc-substatus', 'sc-win32-status', 'time-taken']
  lines = open(file_name,'r').read().split('\n')
  

  for line in lines:
    if not (line.startswith('#') or line==''):
      columns = line.split(' ')
      item = dict(zip(headers, columns))
      method = item['cs-method']
      url = item['cs-uri-stem']
      site_filter = '/'+site_name+'/'
      #we ned only 200s and GET
      if (method=='GET' and item['sc-status']=='200' and url.startswith(site_filter) and 'cassette.axd' not in url):
        key = '%s:%s?%s' %(method,url,item['cs-uri-query'])
        if (key not in data):
          url =url.replace(site_filter,'/',1)
          query_param =item['cs-uri-query']
          data[key]={'method':method,'url': url,'query_param':query_param ,'username':item['cs-username'],'count':1}
        else:
          data[key]['count']+=1
  return data

if __name__ == '__main__':
  logs_folder =''
  extensions = ['.log']
  cutoff =0.5
  
  parser = argparse.ArgumentParser()
  parser.add_argument('--site_name',  type=str, required=True, help='Folder to process, all log files in folder will be processed, subfolders ignored')
  parser.add_argument('--logs_folder',  type=str, required=False, help='Folder to process, all log files in folder will be processed, subfolders ignored')
  parser.add_argument('--cutoff',  type=int, choices=range(1, 100), required=True, help='When generating tests after creating tests for specified %% of requests process will stop')

  args = parser.parse_args()
  
  if args.logs_folder:
    logs_folder = args.logs_folder

  if args.site_name:
    site_name = args.site_name
  
  if not (logs_folder ==''):
    check_if_path_exists(logs_folder)
    ensure_path_exists(os.path.join(logs_folder,'processed'))

  if not (args.cutoff==''):
    cutoff=args.cutoff/100
  
  process_log_files()
  logEvent('All Done')

