token = ''
subdomain =''
url = f'https://{subdomain}.okta.com'

import requests
import csv

session = requests.session()
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'SSWS {token}',
}
session.headers.update(headers)


def get_uid(user):
    #return session.get(f'{url}/api/v1/users/{user}')
    #line 18 will only output response code
    return session.get(f'{url}/api/v1/users/{user}').json().get("id")

def del_user_from_groupid(gid,uid):
    return session.delete(f'{url}/api/v1/groups/{gid}/users/{uid}')

with open ('genie.csv','r') as csv_file:
    report=csv.reader(csv_file)
    next(report)
    for row in report:
        group_id=(row[0])
        username = (row[1])
        print (username)
        #print(get_uid(username))
        userid = get_uid(username)
        print(del_user_from_groupid(row[0],userid).json)




