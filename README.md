# Create GitHub Enterprise Organization

### Prerequisites
- Create settings.py from settings.template.py
- Install package `pip install -r requirements.txt`
- Prepare GitHub Token (admin:org and admin:enterprise scope)
- Set GitHub Token as environment variable
```
export GITHUB_TOKEN=your_github_token
or
set GITHUB_TOKEN=your_github_token
```

### Target
This script works for;
- GitHub Enterprise Cloud
- GitHub Enteprise Cloud Enterprise Managed Users (EMU)

### Execution
`python create.py`

### Settings.py
- ENTERPRISE_SLUG = slug of the enterprise
- LOG_FILE = log file name

- ORG_ADMIN_LOGIN = The logins for the administrators of the new organization.
- ORG_BILLING_EMAIL = The email used for sending billing receipts.
- ORG_PROFILE_NAME = The profile name of the new organization.
- ORG_LOGIN = The login of the new organization.
<br>
[ORG_* Reference](https://docs.github.com/en/graphql/reference/input-objects#createenterpriseorganizationinput)
<br>Enterprise ID will be taken from the slug via API.

### API References
https://docs.github.com/en/graphql/reference/mutations#createenterpriseorganization

### Log Sample
yyyy-mm-dd HH:MM:ss,sss [INFO] Get Enteprise Info: ENTERPRISE_SLUG<br>
yyyy-mm-dd HH:MM:ss,sss [INFO] Eterprise Info: {'slug': 'ENTERPRISE_SLUG', 'id': 'E_enterpriseid'}<br>
yyyy-mm-dd HH:MM:ss,sss [INFO] Creating GitHub Organization: ORG_PROFILE_NAME<br>
yyyy-mm-dd HH:MM:ss,sss [INFO] Created Organization Info: {'id': 'O_neworgid', 'name': 'ORG_PROFILE_NAME ', 'url': 'https://github.com/ORG_PROFILE_NAME'}<br>

