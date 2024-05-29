# -*- coding: utf_8 -*-
'''create.py: Create GitHub Enterprise Organization'''
import logging
import os
import settings
import util.util as util

def main():
    """main"""
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s [%(levelname)s] %(message)s",
        handlers = [
            logging.FileHandler(settings.LOG_FILE),
            logging.StreamHandler()
        ])

    # Token from environment variable
    token = os.getenv('GITHUB_TOKEN')
    if token is None:
        logging.error("GITHUB_TOKEN is not set.")
        raise SystemExit("GITHUB_TOKEN is not set.")

    # Get Enterprise ID
    enterprise_info = util.get_github_enterprise_id(token)
    if enterprise_info is None or "id" not in enterprise_info:
        logging.error("Failed to get GitHub Enterprise ID.")
        raise SystemExit("Failed to get GitHub Enterprise ID.")
    enterprise_id = enterprise_info["id"]
    logging.info("Enterprise Info: %s", enterprise_info)

    # Create GitHub Enterprise Organization
    organization_info = util.create_github_organization(token, enterprise_id)
    if organization_info is not None:
        logging.info("Created Organization Info: %s", organization_info)


if __name__ == "__main__":
    main()
