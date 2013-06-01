"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from main import bot

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class GooBoTest(TestCase):
    def test_get_message_info(self):
        """
        Tests that _get_message_info is working
        """
        # channel message
        raw_channel_message = ":jjaammiiee!~jjaammiie@c-76-124-176-27.hsd1.nj.comcast.net PRIVMSG #jamie-test :GooBo: help!"
        sender, command, recipient, message = bot._get_message_info(raw_channel_message)
        self.assertEqual(sender, "jjaammiiee", "parse raw message does not get right sender")
        self.assertEqual(command, "PRIVMSG", "parse raw message does not get right command")
        self.assertEqual(recipient, "#jamie-test", "parse raw message does not get right recipient")
        self.assertEqual(message, "GooBo: help!", "parse raw message does not get right message")
        # private message
        raw_private_message = ":jjaammiiee!~jjaammiie@c-68-57-16-51.hsd1.pa.comcast.net PRIVMSG GooBo :hello"
        sender, command, recipient, message = bot._get_message_info(raw_private_message)
        self.assertEqual(sender, "jjaammiiee", "parse raw message does not get right sender")
        self.assertEqual(recipient, "GooBo", "parse raw message does not get right recipient")
        self.assertEqual(message, "hello", "parse raw message does not get right message")


