"""
hint.py - Hint Module
"""
from django.conf import settings
from django.db import IntegrityError
from main.bot import send_message
from main.module import command
from main.models import Jiyi


@command("hint")
def hint(reply_to, command_str):
    """
        Given a hint, return the mapping message in Jiyi model
        If --add is provided, then create the message for the hint.
    """
    # usage note.
    print "s{}s".format(command_str)
    if not command_str:
        send_message(reply_to, "{}hint <hint> For example: {}hint lunchdoc."
                     .format(settings.COMMAND_PREFIX, settings.COMMAND_PREFIX))
        return
    # add hint
    if command_str.startswith("--add "):
        hint_and_message = command_str.replace("--add ", "", 1)
        jiyi = Jiyi()
        hint = hint_and_message.split()[0]
        jiyi.hint = hint
        jiyi.message = hint_and_message.replace(hint, "", 1).strip()
        try:
            jiyi.save()
            send_message(reply_to, "Hint '{}' has been created. \
                        To check message: {}hint {}"
                         .format(hint, settings.COMMAND_PREFIX, hint))
        except IntegrityError:
            send_message(reply_to, "Hint '{}' has already exist, \
                        please be creative. \
                        Use {}hint {} to check the message out."
                         .format(hint, settings.COMMAND_PREFIX, hint))
        return
    # query hint
    hint = command_str
    try:
        msg = Jiyi.objects.get(hint=hint)
    except Jiyi.DoesNotExist:
        send_message(reply_to, "No such hint, to add: {}hint --add {} <msg>"
                     .format(settings.COMMAND_PREFIX, hint))
    send_message(reply_to, msg.message)
