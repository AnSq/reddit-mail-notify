#!/usr/bin/python -u
# -u for unbuffered output

import time
import threading
import webbrowser

import praw
import gtk
import gobject
import pynotify


def poll(reddit, icon, mailIcon, nomailIcon, prev):
	try:
		#print "polling...",
		new_messages = len(list(reddit.get_unread()))
		string = "%d new message%s for /u/%s" % (new_messages, "" if new_messages==1 else "s", reddit.user.name)
		print string
		icon.set_tooltip(string)
		if new_messages > 0:
			icon.set_from_pixbuf(mailIcon)
		else:
			icon.set_from_pixbuf(nomailIcon)
		if new_messages > prev.count:
			notify.show()
		prev.count = new_messages
	except Exception as e:
		print "Polling error: %s: %s" % (type(e).__name__, e)
	finally:
		return True


def click(ob, ev, reddit, icon, mailIcon, nomailIcon, prev):
	if ev.button == 1:
		#print "left click"
		if prev.count == 0:
			webbrowser.open("http://www.reddit.com/message/inbox")
		else:
			webbrowser.open("http://www.reddit.com/message/unread")
	elif ev.button == 3:
		#print "right click"
		webbrowser.open("http://www.reddit.com/user/%s" % reddit.user.name)
	prev.count = 0
	icon.set_from_pixbuf(nomailIcon)


class PrevCount:
	def __init__(self):
		self.count = 0


def setup():
	#print "loading icons...",
	loadImage = gtk.Image()

	loadImage.set_from_file("mail.png")
	mailIcon = loadImage.get_pixbuf()

	loadImage.set_from_file("nomail.png")
	nomailIcon = loadImage.get_pixbuf()
	#print "done"

	#print "setting up status bar...",
	icon = gtk.StatusIcon()
	icon.set_from_pixbuf(nomailIcon)
	icon.set_visible(True)
	icon.set_tooltip("loading...")
	#print "done"

	print "logging in...",
	try:
		reddit = praw.Reddit(user_agent="reddit-mail-notify v1.0.4 by /u/AnSq")
		reddit.login()
		print "logged in as /u/%s" % reddit.user.name
	except Exception as e:
		print "\nCould not log in: %s: %s" % (type(e).__name__, e)
		print "closing..."
		exit()

	#print "setting up popup...",
	pynotify.init("reddit-mail-notify")
	notify = pynotify.Notification("New reddit mail for /u/%s" % reddit.user.name)
	notify.set_timeout(60000)
	#print "done"

	prev = PrevCount()

	#print "connecting events...",
	icon.connect("button-press-event", click, reddit, icon, mailIcon, nomailIcon, prev)
	#print "done"

	#print "registering polling function...",
	gobject.timeout_add(60000, poll, reddit, icon, mailIcon, nomailIcon, prev)
	#print "done"

	#first poll
	poll(reddit, icon, mailIcon, nomailIcon, prev)


if __name__ == "__main__":
	try:
		setup()
		#print "entering main loop"
		gtk.main()
	except KeyboardInterrupt:
		print "\nclosing..."
		exit()
