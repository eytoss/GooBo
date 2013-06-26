"""
echo.py
"""
from main.module import command


@command("echo")
def echo(goobo, reply_to, command_str):
    """
        echo whatever in the msg part to the specified channel or user
        NOTE: reply_to here need to be overridden
    """
    channel_str = command_str.split()[0]
    reply_to = channel_str.replace(":", "", 1)
    msg = command_str.replace(reply_to, "", 1)
    goobo.say(reply_to, msg)
