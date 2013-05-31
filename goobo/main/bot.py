import socket, string, time
from django.conf import settings

# global socket variable
s = None

def _get_message_info(raw_message):
    """
        return (channel_name, message), i.e. discarding the part that generated by IRC automatically.
        An example: 
         message = ":jjaammiiee!~jjaammiie@c-76-124-176-27.hsd1.nj.comcast.net PRIVMSG #jamie-test :goobo help!"
         print _get_message_info(message)
         >>("jamie-test", "goobo help!")
    """
    parts = raw_message.split()
    channel_name = parts[2][1:]
    real_message = " ".join(parts[3:])[1:]
    return (channel_name, real_message)
    
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

def send_channel_message(channel, message):
    """
        This is the basic function of sending a one line message to a channel in IRC
    """
    s.send ( 'PRIVMSG #%s :%s\r\n' % (channel, message))
    
def repeat_message(channel, message=None, repeat_time=3, interval=0, start_immediately=True):
    """"""
    for i in range(0, repeat_time):
        if not start_immediately:
            time.sleep(interval)
        send_channel_message(channel, message)
        time.sleep(interval)

# service list. Before DB is introduced here.
SERVICE_TUPLE_LIST = (
                      ("lunchdoc", send_channel_message, "Narberth Lunch Doc: http://goo.gl/vs8RB"),
                      ("google", send_channel_message, "http://www.google.com"),
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
        s.send ( 'PRIVMSG #%s :%s\r\n' % (channel, settings.GREETING_MESSAGE))

def _quit_goobo(channel):
    """
        quit goobo
    """
    send_channel_message(channel, "Who dare to kill me?")
    time.sleep(2)
    send_channel_message(channel, "Well, who dares wins.")
    time.sleep(1)
    s.close()

def _tear_down_goobo():
    """
        Tear down goobo after quiting
    """
    pass
            
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
            channel, message = _get_message_info(line)

            if not message.startswith("GooBo:"):
                break
            command_str = message.replace("GooBo:", "", 1)
            command_parts = command_str.split()
            if not command_parts:
                send_channel_message(channel, "YES Sir! Check out my service list: GooBo: help")
                break      
            if command_parts[0] == settings.QUIT_COMMAND:
                _quit_goobo(channel)
                stop_goobo = True
                break
            try:
                for service in SERVICE_TUPLE_LIST:
                    command, function, parameter = service
                    if command_parts[0] == command:
                        function(channel, parameter if parameter else command_parts[1])
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

