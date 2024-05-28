# -*- coding: utf_8 -*-
import logging
import requests
import settings
import os

# Get Enteprise ID
def get_github_enterprise_id(token):
    query = '''
    query {
      enterprise(slug: {slug}") {
        id
      }
    }
    '''.format(slug=settings.ENTERPRISE_SLUG)
    variables = ''
    result = run_query(query, variables, token)
    if is_error(result):
        return None
    return result["data"]["enterprise"]["id"]

# Create GitHub Enterprise Organization
def create_github_organization(token, enterprise_id):
    '''Create GitHub Enterprise Organization'''
    query = '''
mutation CreateEnterpriseOrg(
	$adminLogin: String!
	$billingEmail: String!
	$enterpriseId: ID!
	$login: String!
	$profileName: String!
) {
	createEnterpriseOrganization(
		input: {
			adminLogins: [$adminLogin]
			billingEmail: $billingEmail
			enterpriseId: $enterpriseId
			login: $login
			profileName: $profileName
		}
	) {
		organization {
			id
			name
			url
		}
	}
}
'''
    variables = '''
{{
	"adminLogin": {adminLogin},
	"billingEmail": {billingEmail},
	"enterpriseId": {enterpriseId},
	"login": {login},
	"profileName": {profileName}
}}'''.format(adminLogin=settings.ORG_ADMIN_LOGIN,   
             billingEmail=settings.ORG_BILLING_EMAIL,
             enterpriseId=enterprise_id, 
             login=settings.ORG_LOGIN, 
             profileName=settings.ORG_PROFILE_NAME)
    
    result = run_query(query, variables, token)
    if is_error(result):
        return None
    return result["data"]["createEnterpriseOrganization"]["organization"]

# Run Query
def run_query(query, variables, token):
    """run query"""
    try:
        headers = {"Authorization": f"bearer {token}"}
        request = requests.post('https://api.github.com/graphql',
          json={'query': query, "variables": variables},
          headers=headers)
        request.raise_for_status()
        return request.json()
    except (requests.exceptions.ConnectionError,
      requests.exceptions.Timeout,
      requests.exceptions.HTTPError) as exception:
        logging.error("Request failed. %s", exception)
        logging.debug("Failed Query: %s", query)
        raise SystemExit(exception) from exception

# Error Check
def is_error(result):
    """is error"""
    try:
        error = result["errors"]
        logging.error(error)
        return True
    except KeyError:
        return False
    
def main():
    """main"""
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s [%(levelname)s] %(message)s",
        handlers = [
            logging.FileHandler("create-enterprise-org.log"),
            logging.StreamHandler()
        ])
    
    # Token from environment variable
    token = os.getenv('GITHUB_TOKEN')
    if token is None:
        logging.error("GITHUB_TOKEN is not set.")
        raise SystemExit("GITHUB_TOKEN is not set.")
    
    # Get Enterprise ID
    enterprise_Id = get_github_enterprise_id(token)

    # Create GitHub Enterprise Organization
    organization_Info = create_github_organization(token, enterprise_Id)
    logging.log(logging.INFO, organization_Info)

