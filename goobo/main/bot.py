import socket
import string
from django.conf import settings
# 
HOST="irc.freenode.net"
PORT=6667
NICK="GooBo"
IDENT="UserName"
CHANNEL = "jamie-test"
REALNAME="getRealName "


GREETING_MESSAGE = "Hey, my name is GooBo, powered by eytoss, igonor me will be your best choice but if you don't, you will be surprised."
# global socket variable
s = None

def _get_typed_message(message):
    """
        This is used to return only the user typed part of the message, i.e. discarding the part that generated by IRC automatically.
        # an example 
         message = ":jjaammiiee!~jjaammiie@c-76-124-176-27.hsd1.nj.comcast.net PRIVMSG #jamie-test :goobo help!"
         print _get_typed_message(message)
         >>goobo help!
    """
    return " ".join(message.split()[3:])[1:]
    
def _parse_command(message):
    """
        This is used to return only the user typed part of the message, i.e. discarding the part that generated by IRC automatically.
        # an example 
         message = ":jjaammiiee!~jjaammiie@c-76-124-176-27.hsd1.nj.comcast.net PRIVMSG #jamie-test :goobo help!"
         print _get_typed_message(message)
         >>goobo help!
    """
    return message.split()
    

def generate_GH_url(issue_id):
    """"""
    message = "https://github.com/DramaFever/www/issues/{}".format(issue_id)
    s.send ( 'PRIVMSG #%s :%s\r\n' % (CHANNEL, message))

def send_message(message):
    """
        This is the basic function of sending a one line message to IRC
    """
    s.send ( 'PRIVMSG #%s :%s\r\n' % (CHANNEL, message))
    
def repeat_message(message=None, repeat_time=3, interval=0, start_immediately=True):
    """"""
    if not message:
        s.send ( 'PRIVMSG #%s :%s\r\n' % (CHANNEL, "You did not specify what to repeat, so I will just repeat my favorite quote:"))
        message = "Who dares wins"
    for i in range(0, repeat_time):
        s.send ( 'PRIVMSG #%s :%s\r\n' % (CHANNEL, message))

# service list. Before DB is introduced here.
SERVICE_TUPLE_LIST = (
                      ("lunchdoc", send_message, "Narberth Lunch Doc: http://goo.gl/vs8RB"),
                      ("google", send_message, "http://www.google.com"),
                      ("repeat", repeat_message, ""),
                      ("GH", generate_GH_url, ""),
                     )

stop_goobo = False
def start_goobo():
    """
    Start GooBo
    """
    global s 
    global stop_goobo 
    s = socket.socket( )
    stop_goobo = False

    s.connect((HOST, PORT))
    
    # MUST send NICK and USER commands before any other commands 
    s.send("NICK %s\r\n" % NICK)
    s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))    

    #identify nickname
    s.send("NICKSERV IDENTIFY {} {}\r\n".format(NICK, settings.FREENODE_NICKNAME_PASSWORD))

    #join the channel and say hello!
    s.send ( 'JOIN #%s\r\n' % CHANNEL) # YOU MUST CHANGE THE CHANNEL HERE AND BELOW!!
    s.send ( 'PRIVMSG #%s :%s\r\n' % (CHANNEL, GREETING_MESSAGE))
        
    readbuffer=""
    while not stop_goobo:
        readbuffer=readbuffer+s.recv(1024)
        temp=string.split(readbuffer, "\n")
        readbuffer=temp.pop( )
        
        for line in temp:
            print line
            message = _get_typed_message(line)
            if message == "GooBo:":
                s.send ( 'PRIVMSG #%s :%s\r\n' % (CHANNEL, "YES Sir! Check out my service list: GooBo: help"))
            elif message == "GooBo: !quit":
                s.close()
                stop_goobo = True
                break
            elif message.startswith("GooBo:"):
                for service in SERVICE_TUPLE_LIST:
                    command, function, parameter = service
                    if message.split()[1] == command:
                        function(parameter if parameter else message.split()[2])

def stop_goobo():
    """
    Stop GooBo
    """
    global stop_goobo
    stop_goobo = True

if __name__ == "__main__":
    start_goobo()

