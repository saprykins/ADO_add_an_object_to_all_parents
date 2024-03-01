import requests
import json
import base64

pat = "a*" # full tempo
organization = 'g'
project = 'M'
workitemtype = "T"

# 1/ get all apps (not always applicable)
# 2/ get link for each application
# 3/ upload a task to application

# 1/ OK
def get_all_applications_list_from_ado():
    """
    The function uses query that is defined in ADO
    url to be specified for each task
    Tasks should be attached to User stories, not applications
    """
    list_of_all_applications = []
    
    url = "https://dev.azure.com/" + organization + "/" + project + "/_apis/wit/wiql/70faf48b-3359-4598-b4c1-23cef480a968"

    headers = {
        "Content-Type": "application/json-patch+json"
    }

    response = requests.get(
        url = url,
        headers=headers,
        auth=("", pat), 
    )

    applications_raw_data = response.json()["workItems"]
    for application in applications_raw_data:
        list_of_all_applications.append(application["id"])
    return list_of_all_applications


# 2/
def get_app_url(application_wi_id):   
    '''
    Get the link of the parent
    '''

    url = 'https://dev.azure.com/' + organization + '/_apis/wit/workItems/' + str(application_wi_id) + '?$expand=all'
    
    headers = {
        "Content-Type": "application/json-patch+json"
    }

    response = requests.get(
        url = url,
        headers=headers,
        auth=("", pat), 
    )
    # print(response)
    lnk = response.json()["url"]
    return lnk





# 3/
def add_task_to_one_ms_app(app):
    '''
    Add task to the specified parent
    '''
    url = "https://dev.azure.com/{}/{}/_apis/wit/workitems/${}?api-version=7.0".format(organization, project, workitemtype)

    headers = {
        "Content-Type": "application/json-patch+json"
    }


    task_link = """
    Documentation is available here:
    <br><a href="https://confluence..."> DNS TTL link </a>
    """

    body = [
        {
        "op": "add",
        "path": "/fields/System.Title",
        "value": "TA40.10.035 - Hello"
        },
        {
        "op": "add",
        "path": "/fields/System.Description",
        "value": "Follow instructions in the Documentation link. "
        },
        {
        "op": "add",
        "path": "/fields/Custom.DocumentationLink",
        "value": task_link
        },
        {
        "op": "add",
        "path": "/fields/Custom.TMinusIdentifier",
        "value": "T-10"
        },
        {
        "op": "add",
        "path": "/fields/System.Parent",
        "value": app
        },
        {
        "op": "add",
        "path": "/relations/-",
        "value": {
            "rel":"System.LinkTypes.Hierarchy-Reverse",
            "url":get_app_url(app)
            }
        }
    ]


    r = requests.post(
        url,
        data=json.dumps(body),
        headers=headers,
        auth=("", pat),
    )

    print(r)


# MAIN

app_list = get_all_applications_list_from_ado()
print(app_list)
# app_list = [16326] # A template User story

'''
for app in app_list:
    add_task_to_one_ms_app(app)
'''
