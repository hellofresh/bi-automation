import os


def set_repo(repo, egg, branch='master'):
    """
    Creates proper GitHub repo URL depending if we are in automation
    or running locally.
    """
    token_variable = os.getenv("HELLOFRESH_GITTOKEN", False)

    if not token_variable:
        return "git+ssh://git@github.com/{0}.git@{2}#egg={1}".format(repo, egg, branch)

    return "https://{0}@github.com/{1}/tarball/{3}#egg={2}".format(
        token_variable, repo, egg, branch)
