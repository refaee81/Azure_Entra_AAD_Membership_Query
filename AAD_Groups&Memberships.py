# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 11:43:58 2023

@author: abdera
"""

#Graph API Call


# Define imports
import msal

#Using spn (sp-xxxxxxxxxxx)

# Enter the details of your AAD app registration
client_id = 'xxxxx-xxxxx-xxxxx-xxxx-xxxxxxx'
client_secret = 'xxxxx-xxxxx-xxxxx-xxxx-xxxxxxx'
authority = 'https://login.microsoftonline.com/{tenand id}
scope = ['https://graph.microsoft.com/.default']

# Create an MSAL instance providing the client_id, authority and client_credential parameters
client = msal.ConfidentialClientApplication(client_id, authority=authority, client_credential=client_secret, verify=False)

# First, try to lookup an access token in cache
token_result = client.acquire_token_silent(scope, account=None)

# If the token is available in cache, save it to a variable
if token_result:
  access_token = 'Bearer ' + token_result['access_token']
  print('Access token was loaded from cache')

# If the token is not available in cache, acquire a new one from Azure AD and save it to a variable
if not token_result:
  token_result = client.acquire_token_for_client(scopes=scope)
  access_token = 'Bearer ' + token_result['access_token']
  print('New access token was acquired from Azure AD')

print(access_token)
################

# Define imports
import requests
import json
import pandas as pd
# Copy access_token and specify the MS Graph API endpoint you want to call, e.g. 'https://graph.microsoft.com/v1.0/groups' to get all groups in your organization


url = 'https://graph.microsoft.com/v1.0/groups?$select=id,displayName&$expand=members($select=id,displayName)'


headers = {
  'Authorization': access_token
}

# Make a GET request to the provided url, passing the access token in a header
graph_result = requests.get(url=url, headers=headers)

d_sample_100= json.loads(graph_result.text)

###### Loop for full dataset 

# Initiate a variable to store data from all pages
graph_results = []

# Call the endpoint, if there is the @odata.nextLink property, set the url variable to it's value
# and continue making requests until looped through all pages
while url:
  try:
    graph_result = requests.get(url=url, headers=headers).json()
    graph_results.extend(graph_result['value'])
    url = graph_result['@odata.nextLink']
    
  except:
    break

test = pd.json_normalize(graph_results, record_path=('members'), meta=['id','displayName'], record_prefix='_')
test.rename(columns = {'_id':'User_GUID', '_displayName':'User', 'id':'AAD_GUID', 'displayName':'AAD_Group'}, inplace = True)


df = pd.DataFrame(test)
writer = pd.ExcelWriter('C:/Users/......../AADgroupsmembership.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save()



#####
