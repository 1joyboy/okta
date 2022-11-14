token = ''
subdomain = ''
fqdn = f'https://{subdomain}.okta.com'

import requests
import json
import itertools
from datetime import datetime
import time

LIMIT_REMAINING = 10
dict_store={}
list_store=[]

#Use requests.Session() to improve performance (up to 2x !!!) by keeping the session open. If you don't use it, requests will close the session after each call and then create a new one. Also, you don't have to specify the headers each time, just once at the beginning.
session = requests.session()
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'SSWS {token}'
}
session.headers.update(headers)

def list_apps():
    response = session.get(f"{fqdn}/api/v1/apps?limit=200")
    return response

def snooze(response):
    remaining = int(response.headers['X-Rate-Limit-Remaining'])
    limit = int(response.headers['X-Rate-Limit-Limit'])
    if remaining <= LIMIT_REMAINING:
        reset = datetime.utcfromtimestamp(int(response.headers['X-Rate-Limit-Reset']))
        #print('sleeping...', remaining, limit, reset)
        while reset > datetime.utcnow():
            time.sleep(1)


def get_pages(url):
    while url:
        r = session.get(url)
        yield r.json()
        url = r.links.get('next', {}).get('url')


def get_app_id():
    app_id=[]
    for apps in get_pages(f"{fqdn}/api/v1/apps?limit=200"):
        for app in apps:
            #print(app['id'],app['label'])
            app_id.append(app['id'])
    return(app_id) 


def get_app_name():
    app_name=[]
    for apps in get_pages(f"{fqdn}/api/v1/apps?limit=200"):
        for app in apps:
            #print(app['id'],app['label'])
            app_name.append(app['label'])
    return(app_name) 


#will arugment in fucntion take prescedence of global variable? 
def get_app_groups(id):
    r = session.get(f"{fqdn}/api/v1/apps/{id}/groups?expand=group")
    snooze(r)
    return(r)

list_store=list(dict.fromkeys(get_app_name()).keys())
#dict.fromkeys(get_app_name()).keys()
dict_store={ key:[] for key in list_store }
#print(dict_store, '\n')

for id,name in zip (get_app_id(), get_app_name()):
    groups = get_app_groups(id).json()
    #print(groups, '\n') #<Response [200]> OR <Response [429]>
    #print(groups.json())
    gid_placeholder=[]
    gname_placeholder=[]
    for group in groups:
        gid_placeholder.append(group['id'])
        gname_placeholder.append(group["_embedded"]["group"]["profile"]["name"])
        dict_store[name]=gname_placeholder
#print(dict_store)    

new_list =[]
for k in dict_store.keys():
    value = dict_store[k]
    ##takes array and denote it with a comma
    line = k+","+(",".join(value))
    new_list.append(line)
print("\n".join(new_list))




# response = list_apps()
# apps = response.json()
# #To paginate, response.links gives you the fqdn of the next page. Don't create your own fqdn from parts:
# page = response.links.get('next')
# header = response.headers.keys()

# #apps is <class 'list'>
# #print (apps['id'], '\n')
# #TypeError: list indices must be integers or slices, not str

# print (header, '\n')
# print (apps, '\n')
# print (page, '\n')

# for a in apps:
#     print(a['label'])
#     # if page is not None:
        
# #add while statement 

# while fqdn:
#     response = session.get(fqdn+'/api/v1/users')
#     users = response.json()
#     for user in users:
#         print(user['profile']['login'])
#     next = response.links.get('next')
#     fqdn = next['fqdn'] if next else None

# if page is not None:
#     print('true, there is next pgae')
# else: 
#     print('false, there is no next pgae')
    


#watch
#https://www.youtube.com/watch?v=bD05uGo_sVI
#https://www.youtube.com/watch?v=6iF8Xb7Z3wQ
#https://macadmins.slack.com/archives/C0LFP9CP6/p1630708387138000?thread_ts=1630598404.101200&cid=C0LFP9CP6
