#!/usr/bin/python

import time
import threading
import webbrowser

import praw
import gtk
import gobject
import pynotify

print "loading icons...",
loadImage = gtk.Image()

loadImage.set_from_file("mail.png")
mailIcon = loadImage.get_pixbuf()

loadImage.set_from_file("nomail.png")
nomailIcon = loadImage.get_pixbuf()
print "done"

print "setting up status bar...",
icon = gtk.StatusIcon()
icon.set_from_pixbuf(nomailIcon)
icon.set_visible(True)
icon.set_tooltip("loading...")
print "done"

print "logging in...",
reddit = praw.Reddit(user_agent="reddit-mail-notify v1.0 by /u/AnSq")
reddit.login()
print "done"
print "logged in as %s" % reddit.user.name

print "setting up popup...",
pynotify.init("reddit-mail-notify")
notify = pynotify.Notification("New reddit mail for /u/%s" % reddit.user.name)
notify.set_timeout(5000)
print "done"


class PrevCount:
	def __init__(self):
		self.count = 0


prev = PrevCount()


def poll(prev):
	new_messages = len(list(reddit.get_unread()))
	print "New messages for %s: %d" % (reddit.user.name, new_messages)
	icon.set_tooltip("%d new message%s for %s" % (new_messages, "" if new_messages==1 else "s", reddit.user.name))
	if new_messages > 0:
		icon.set_from_pixbuf(mailIcon)
	else:
		icon.set_from_pixbuf(nomailIcon)
	if new_messages > prev.count:
		notify.show()
	prev.count = new_messages
	return True


def click(ob, ev, prev):
	prev.count = 0
	if ev.button == 1:
		"left click"
		if prev.count == 0:
			webbrowser.open("http://www.reddit.com/message/inbox")
		else:
			webbrowser.open("http://www.reddit.com/message/unread")
	elif ev.button == 3:
		"right click"
		webbrowser.open("http://www.reddit.com/user/%s" % reddit.user.name)


print "connecting events...",
icon.connect("button-press-event", click, prev)
print "done"

print "registering polling function...",
gobject.timeout_add(60000, poll, prev)
print "done"

print "entering main loop"
gtk.main()
