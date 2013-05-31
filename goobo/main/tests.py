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
        raw_message = ":jjaammiiee!~jjaammiie@c-76-124-176-27.hsd1.nj.comcast.net PRIVMSG #jamie-test :GooBo: help!"
        channel_name, real_message = bot._get_message_info(raw_message)
        self.assertEqual(channel_name, "jamie-test", "parse raw message does not get right channel name")
        self.assertEqual(real_message, "GooBo: help!", "parse raw message does not get right real message")


