import json
import httplib2
from config import SERVER

http = httplib2.Http()

# print json.loads(http.request("http://172.28.101.30:8080/api/v1/family/1/?format=json", 'GET')[1])

def json_result(url, method='GET'):
    response = http.request('http://%s%s?format=json&username=bogdan&api_key=1234123443214321' % (SERVER, url), method)[1]
    # print 'URL', url
    # print 'RESP', json.loads(response)
    if response:
        return json.loads(response)
    else:
        return {}

family_members = None

def poll():
    global family_members
    if not family_members:
        family = json_result('/api/v1/family/1/')
        family_members = family[u'members']
    members = []
    for m in family_members:
        member = json_result(m)
        rewards = filter(lambda r: not r[u'consumed'],
                         [json_result(r) for r in member[u'rewards']])
        for r in rewards:
            # json_result(r[u'resource_uri'] + 'consume/')
            pass
        # List of triplets (first name, username, list of rewards to consume)
        members.append((member[u'first_name'], member[u'username'], rewards))
    return members

# print poll()
