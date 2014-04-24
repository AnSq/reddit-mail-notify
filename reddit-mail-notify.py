#!/usr/bin/python

import praw


reddit = praw.Reddit(user_agent="reddit-mail-notify v0.1 by /u/AnSq")
reddit.login()
new_messages = len(list(reddit.get_unread()))
print "New messages for %s: %d" % (reddit.user.name, new_messages)
