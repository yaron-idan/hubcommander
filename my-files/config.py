from hubcommander.auth_plugins.enabled_plugins import AUTH_PLUGINS


ONLY_LISTEN = [
    "C800CA22C"
]

# Define the organizations that this Bot will examine.
ORGS = {
    "soluto-private": {
        "aliases": [
            "solutoprivate"
        ],
        "public_only": False,   # False means that your org supports Private repos, True otherwise.
        "new_repo_teams": [  # This is a list, so add all the teams you want to here...
            {
                "id": "2500898",        # The team ID for the team that you want new repos to be attached to
                "perm": "push",         # The permission, either "push", "pull", or "admin"...
                "name": "Developers"    # The name of the team here...
            },
            {
                "id": "2774000",        # The team ID for the team that you want new repos to be attached to
                "perm": "admin",        # The permission, either "push", "pull", or "admin"...
                "name": "ci-bot"        # The name of the team here...
            }
        ]
    }
}

# github API Version
GITHUB_VERSION = "application/vnd.github.v3+json"   # Is this still needed?

# GITHUB API PATH:
GITHUB_URL = "https://api.github.com/"

# You can use this to add/replace fields from the command_plugins dictionary:
USER_COMMAND_DICT = {
    # This is an example for enabling Duo 2FA support for the "!SetDefaultBranch" command:
    "!SetRepoPermissions": {
        "enabled": True,
        "permitted_permissions": ["push", "pull", "admin"]
    },
    "!AddKey": {
		"enabled": False
    },
    "!ListKeys": {
		"enabled": False
    },
    "!DeleteKey": {
		"enabled": False
    },
    "!AddUserToTeam": {
		"enabled": False
    },
    "!DeleteRepo": {
		"enabled": False
    },
    "!SetDescription": {
		"enabled": False
    },
    "!SetDefaultBranch": {
		"enabled": True
    },
    "!SetHomepage": {
		"enabled": False
    },
    "!GetKey": {
		"enabled": False
    },
    "!AddCollab": {
		"enabled": False
    },
    "!ListPRs": {
		"enabled": False
    },
    "!SetTopics": {
		"enabled": False
    }
}

