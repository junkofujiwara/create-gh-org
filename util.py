# -*- coding: utf_8 -*-
'''util.py: Utility Functions'''
import logging
import requests
import settings

# Get Enteprise ID
def get_github_enterprise_id(token):
    '''Get GitHub Enterprise ID'''
    logging.info("Get Enterprise Info: %s", settings.ENTERPRISE_SLUG)
    query = '''query GetEnterprise($slug: String!){ enterprise(slug: $slug) {slug, id}}'''
    variables = f'''{{"slug": "{settings.ENTERPRISE_SLUG}"}}'''
    result = run_query(query, variables, token)
    if is_error(result):
        return None
    return result["data"]["enterprise"]

# Create GitHub Enterprise Organization
def create_github_organization(token, enterprise_id):
    '''Create GitHub Enterprise Organization'''
    logging.info("Creating GitHub Organization: %s", settings.ORG_PROFILE_NAME)
    query = '''mutation CreateEnterpriseOrg(
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
    variables = f'''{{
        "adminLogin": "{settings.ORG_ADMIN_LOGIN}",
        "billingEmail": "{settings.ORG_BILLING_EMAIL}",
        "enterpriseId": "{enterprise_id}",
        "login": "{settings.ORG_LOGIN}",
        "profileName": "{settings.ORG_PROFILE_NAME}"}}
    '''

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
