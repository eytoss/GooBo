import socket
import string
import threading
import time
from django.conf import settings
from django.db import IntegrityError
from main.models import Jiyi

# global socket variable
s = None
stop_goobo = False
CP = settings.COMMAND_PREFIX


def _send_email(reply_to, message):
    """send email functionality"""
    _send_email_or_txt(reply_to, message, is_txt=0)


def _send_txt(reply_to, message):
    """send txt functionality"""
    _send_email_or_txt(reply_to, message, is_txt=1)


def _send_email_or_txt(reply_to, message, is_txt=1):
    """send_email functionality"""
    # Import smtplib for the actual sending function
    import smtplib
    # Import the email modules we'll need
    from email.mime.text import MIMEText
    # Create a text/plain message
    msg = MIMEText(message)

    destination = settings.EMAIL_TO
    if is_txt:
        destination = settings.EMAIL_TO_TXT_GATEWAY
    msg['Subject'] = 'Message from {}'.format(reply_to)
    msg['From'] = settings.EMAIL_FROM
    msg['To'] = destination

    s = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    # this is needed if you want to do login authentication with gmail
    s.starttls()
    s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    s.sendmail(settings.EMAIL_FROM, [destination], msg.as_string())
    s.quit()


def _is_channel(name):
    """determine if a name represents a channel"""
    return name.startswith("#")


def _get_message_info(raw_message):
    """
        return (sender, command, recipient, message),
        i.e. discarding the part that generated by IRC automatically.
        An message example:
         ":yournick!~yournick@reverse_ip PRIVMSG #yournick-test :goobo help!"
         print _get_message_info(message)
         >>("yournick", "PRIVMSG", "#yournick-test", "goobo help!")
    """
    try:
        parts = raw_message.split()
        sender = parts[0].split("!")[0][1:]
        command = parts[1]
        recipient = parts[2]
        message = " ".join(parts[3:])[1:]
    except:
        return (None, None, None, None)
    return (sender, command, recipient, message)


def _parse_command(message):
    """
        This is used to return only the user typed part of the message
        i.e. discarding the part that generated by IRC automatically.
        # an message example:
          ":tim!~time@c-76-124-176-27.hsd1.nj.comcast.net PRIVMSG #test !help"
         print _get_typed_message(message)
         >>goobo help!
    """
    return message.split()


def generate_GH_url(issue_id, repo="www"):
    """"""
    return "https://github.com/DramaFever/{repo}/issues/{issue_id}" \
        .format(issue_id=issue_id, repo=repo)


def send_message(recipient, message):
    """
        Sends a one line message to channel/nick in IRC
    """
    time.sleep(settings.MESSAGE_DELAY_TIME)
    s.send('PRIVMSG %s :%s\r\n' % (recipient, message))


def repeat_message(channel, message=None, repeat_time=3,
                   interval=0, start_immediately=True):
    """
        Repeat message for certain times with intervals
    """
    for i in range(0, repeat_time):
        if not start_immediately:
            time.sleep(interval)
        send_message(channel, message)
        time.sleep(interval)


def echo(msg_str):
    """echo whatever in the msg part to the specified channel or user"""
    channel_str = msg_str.split()[0]
    channel = channel_str.replace(":", "", 1)
    msg = msg_str.replace(channel, "", 1)
    send_message(channel, msg)


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

# service list. Before DB is introduced here.
SERVICE_LIST = (
    ("help", send_message, "Command List: \
        {}hint {}txt {}email".format(CP, CP, CP)),
    ("hint", hint, ""),
    ("txt", _send_txt, ""),
    ("email", _send_email, ""),
    ("repeat", repeat_message, ""),
    ("GH", generate_GH_url, ""),
)


def _set_up_goobo():
    """
        Initialize goobo for all the channels
    """
    global s
    global stop_goobo
    s = socket.socket()
    stop_goobo = False

    s.connect((settings.HOST, settings.PORT))

    # MUST send NICK and USER commands before any other commands
    s.send("NICK %s\r\n" % settings.NICK)
    s.send("USER %s %s bla :%s\r\n" %
           (settings.IDENT, settings.HOST, settings.REALNAME))

    #identify nickname
    s.send("NICKSERV IDENTIFY {nick} {password}\r\n"
           .format(nick=settings.NICK,
                   password=settings.FREENODE_NICKNAME_PASSWORD))

    #join the CHANNELs
    for channel in settings.CHANNEL_LIST:
        time.sleep(1)
        s.send('JOIN #%s\r\n' % channel)


def _quit_goobo(channel):
    """
        quit goobo
    """
    send_message(channel, "Who dare to kill me?")
    time.sleep(2)
    send_message(channel, "Well, who dares wins.")
    time.sleep(1)
    s.close()


def _tear_down_goobo():
    """
        Tear down goobo after quiting
    """
    pass


def _keyword_react(channel, message):
    """
        react upon listened any keywords in LISTEN_KEYWORDS
    """
    for name in settings.AUTO_REPLY_KEYWORDS:
        if name in message:
            send_message(channel, "{name} is currently not available."
                         .format(name=name))
            return
    for keyword in settings.LISTEN_KEYWORDS:
        if keyword in message:
            send_message(channel, "Command List: {}help".format(CP))


def _ping_pong(line):
    """PONG message back upon receiving PING"""
    #  Ping message sent by server irc.funet.fi example:
    #      PING :irc.funet.fi
    print line
    if line.startswith("PING :"):
        s.send("PONG {}\r\n".format(line.split()[1][1:]))
        return True
    return False


def start_goobo():
    """
    Start GooBo
    """
    listen_IRC_thread = threading.Thread(target=_listen_IRC)
    listen_IRC_thread.start()


def _listen_IRC():
    """
        make GooBo keep listening on IRC
    """
    _set_up_goobo()

    global stop_goobo
    # keep listening and acting to commands until receiving QUIT_COMMAND
    readbuffer = ""
    while not stop_goobo:
        readbuffer = readbuffer+s.recv(1024)
        temp = string.split(readbuffer, "\n")
        readbuffer = temp.pop()

        for line in temp:
            if _ping_pong(line):
                continue
            sender, command, recipient, message = _get_message_info(line)
            # only reacts on private messages(from channel or nick)
            if command != "PRIVMSG":
                continue

            if _is_channel(recipient) and not message.startswith(CP):
                _keyword_react(recipient, message)
                continue

            # channel message started with GooBo: or private message to GooBo.
            reply_to = sender
            # channel message need to reply to receipt normally
            if _is_channel(recipient):
                reply_to = recipient
            # NOTE: GooBo: is not necessary prefix as private message
            command_str = message.replace(settings.COMMAND_PREFIX, "", 1)
            command_parts = command_str.split()
            if not command_parts:
                send_message(recipient, "Command List: {}help".format(CP))
                continue
            if command_parts[0] == settings.QUIT_COMMAND:
                _quit_goobo(reply_to)
                stop_goobo = True
                break
            if command_parts[0] == "echo":
                echo(command_str.replace("echo", "", 1))
                break
            try:
                for service in SERVICE_LIST:
                    command, function, parameter = service
                    if command_parts[0] == command:
                        function(reply_to, parameter if parameter else
                                 command_str.replace(command, "", 1).strip())
            except:
                pass

    _tear_down_goobo()


def stop_goobo():
    """
    Stop GooBo
    """
    global stop_goobo
    stop_goobo = True

if __name__ == "__main__":
    start_goobo()
