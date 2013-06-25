"""
echo.py
"""


def echo(goobo, msg_str):
    """echo whatever in the msg part to the specified channel or user"""
    channel_str = msg_str.split()[0]
    channel = channel_str.replace(":", "", 1)
    msg = msg_str.replace(channel, "", 1)
    goobo.send_message(channel, msg)
