"""
repeat.py
"""
import  time
from main.bot import send_message


def repeat(channel, command_str):
    """
        Repeat message for certain times with intervals
    """
    command_parts = command_str.split()
    message = command_parts[0]
    repeat_time = 2
    interval = 0
    start_immediately = 1

    if len(command_parts) > 1:
        repeat_time = int(command_parts[1])
    if len(command_parts) > 2:
        interval = int(command_parts[2])
    if len(command_parts) > 3:
        start_immediately = int(command_parts[3])

    for i in range(0, repeat_time):
        if start_immediately != 1:
            time.sleep(interval)
        send_message(channel, message)
        time.sleep(interval)
