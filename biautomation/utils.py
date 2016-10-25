import os


def set_repo(repo, egg):
    """
    Creates proper GitHub repo URL depending if we are in automation
    or running locally.
    """
    token_variable = os.getenv("HELLOFRESH_GITTOKEN", False)

    if not token_variable:
        return "git+ssh://git@github.com/{0}.git#egg={1}".format(repo, egg)

    return "https://{0}@github.com/{1}/tarball/master#egg={2}".format(
        token_variable, repo, egg)
