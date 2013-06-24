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
        raw_channel_msg = ":jxu!~jxu@c-76-124-176-27.hsd1.nj.comcast.net \
            PRIVMSG #test :GooBo: help!"
        sender, cmd, recipient, msg = bot._get_message_info(raw_channel_msg)
        self.assertEqual(sender, "jxu", " parse out wrong sender")
        self.assertEqual(cmd, "PRIVMSG", " parse out wrong command")
        self.assertEqual(recipient, "#test", " parse out wrong recipient")
        self.assertEqual(msg, "GooBo: help!", " parse out wrong message")
        # private message
        raw_private_msg = ":jxu!~jxu@c-68-57-16-51.hsd1.pa.comcast.net \
            PRIVMSG GooBo :hello"
        sender, cmd, recipient, msg = bot._get_message_info(raw_private_msg)
        self.assertEqual(sender, "jxu", " parse out wrong sender")
        self.assertEqual(recipient, "GooBo", " parse out wrong recipient")
        self.assertEqual(msg, "hello", " parse out wrong message")
