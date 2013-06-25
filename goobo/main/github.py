"""
github.py
"""
from django.conf import settings
from main.module import command


@command("GH")
def generate_GH_url(goobo, reply_to, command_str):
    """
        generate corresponding issue/pull request urls
    """
    command_parts = command_str.split()
    issue_id = 1
    repo = "www"
    user = "DramaFever"
    try:
        issue_id = int(command_parts[0])
    except ValueError:
        goobo.send_message(reply_to, "Issue Id need to be integer. \
            Example: {}GH 46 goobo eytoss".format(settings.COMMAND_PREFIX))
        return
    if len(command_parts) > 1:
        repo = command_parts[1]
    if len(command_parts) > 2:
        user = command_parts[2]
    goobo.send_message(reply_to, "https://github.com/{user}/{repo}/issues/{issue_id}"
                 .format(issue_id=issue_id, repo=repo, user=user))
