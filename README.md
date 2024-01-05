# Azure_Entra_AAD_Membership_Query
For general queries of AAD groups and memberships in Azure. 

For Credentials, use msal library. 

# Step to initiate API Call and Query: 
1. Create an MSAL instance providing the client_id, authority and client_credential parameters
2. Lookup an access token in cache.
3. If the token is available in cache, save it to a variable; If not, acquire a new one from Azure AD and save it to a variable.
4. Copy/read access_token and specify the MS Graph API endpoint you want to call, e.g. 'https://graph.microsoft.com/v1.0/groups' to get all groups in your organization.
5. Make a GET request to the provided url, passing the access token in a header.
6. Default GET request return 100 results only.
7. Loop for full dataset. Call the endpoint, if there is the @odata.nextLink property, set the url variable to it's value and continue making requests until looped through all pages.
