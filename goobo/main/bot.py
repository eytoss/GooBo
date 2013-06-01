import socket, string, time
from django.conf import settings

# global socket variable
s = None

def _is_channel(name):
    """determine if a name represents a channel"""
    return name.startswith("#")

def _get_message_info(raw_message):
    """
        return (sender, recipient, message), i.e. discarding the part that generated by IRC automatically.
        An example: 
         message = ":jjaammiiee!~jjaammiie@c-76-124-176-27.hsd1.nj.comcast.net PRIVMSG #jamie-test :goobo help!"
         print _get_message_info(message)
         >>("#jamie-test", "goobo help!")
    """
    parts = raw_message.split()
    sender = parts[0].split("!")[0][1:]
    recipient = parts[2]
    message = " ".join(parts[3:])[1:]
    return (sender, recipient, message)
    
def _parse_command(message):
    """
        This is used to return only the user typed part of the message, i.e. discarding the part that generated by IRC automatically.
        # an example 
         message = ":jjaammiiee!~jjaammiie@c-76-124-176-27.hsd1.nj.comcast.net PRIVMSG #jamie-test :goobo help!"
         print _get_typed_message(message)
         >>goobo help!
    """
    return message.split()
    

def generate_GH_url(issue_id, repo="www"):
    """"""
    return "https://github.com/DramaFever/{repo}/issues/{issue_id}".format(issue_id=issue_id, repo=repo)

def send_message(channel, message):
    """
        This is the basic function of sending a one line message to a channel in IRC
    """
    s.send ( 'PRIVMSG #%s :%s\r\n' % (channel, message))
    
def repeat_message(channel, message=None, repeat_time=3, interval=0, start_immediately=True):
    """"""
    for i in range(0, repeat_time):
        if not start_immediately:
            time.sleep(interval)
        send_message(channel, message)
        time.sleep(interval)

# service list. Before DB is introduced here.
SERVICE_TUPLE_LIST = (
                      ("lunchdoc", send_message, "Narberth Lunch Doc: http://goo.gl/vs8RB"),
                      ("google", send_message, "http://www.google.com"),
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
    s.send("USER %s %s bla :%s\r\n" % (settings.IDENT, settings.HOST, settings.REALNAME))    

    #identify nickname
    s.send("NICKSERV IDENTIFY {nick} {password}\r\n".format(nick=settings.NICK, password=settings.FREENODE_NICKNAME_PASSWORD))

    #join the CHANNELs and say hello!
    for channel in settings.CHANNEL_LIST:
        s.send ( 'JOIN #%s\r\n' % channel) # YOU MUST CHANGE THE CHANNEL HERE AND BELOW!!

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
            send_message(channel, "{name} is currently not available.".format(name=name))
            return
    for keyword in settings.LISTEN_KEYWORDS:
        if keyword in message:
            send_message(channel, "What's up!")
    
stop_goobo = False
def start_goobo():
    """
    Start GooBo
    """
    _set_up_goobo()
    global stop_goobo 

    # keep listening and acting to commands until receiving QUIT_COMMAND
    readbuffer=""
    while not stop_goobo:
        readbuffer=readbuffer+s.recv(1024)
        temp=string.split(readbuffer, "\n")
        readbuffer=temp.pop( )
        
        for line in temp:
            print line
            sender, recipient, message = _get_message_info(line)
            if _is_channel(recipient): # channel message need to reply to receipt normally
                if not message.startswith("GooBo:"):
                    _keyword_react(recipient, message)
                    break
                command_str = message.replace("GooBo:", "", 1)
                command_parts = command_str.split()
                if not command_parts:
                    send_message(recipient, "YES Sir! Check out my service list: GooBo: help")
                    break      
                if command_parts[0] == settings.QUIT_COMMAND:
                    _quit_goobo(recipient)
                    stop_goobo = True
                    break
                try:
                    for service in SERVICE_TUPLE_LIST:
                        command, function, parameter = service
                        if command_parts[0] == command:
                            function(recipient, parameter if parameter else command_parts[1])
                except:
                    pass
            else: # private or system message need to reply to sender NOTE: never send_message w/o any checking, or you will be trapped in infinite loop!
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

