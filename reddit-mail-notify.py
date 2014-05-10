#!/usr/bin/python -u
# -u for unbuffered output

import webbrowser
import praw
import gtk
import gobject
import pynotify
import sys


version = "1.0.9"
user_agent = "reddit-mail-notify v%s by /u/AnSq" % version
poll_time = 60000


def make_message(new_messages, name):
	msgCount = "No" if new_messages==0 else str(new_messages)
	plural = "" if new_messages==1 else "s"
	return "%s new message%s for /u/%s" % (msgCount, plural, name)


def poll(reddit, icon, mailIcon, nomailIcon, errorIcon, prev, notify):
	try:
		#print "polling...",
		new_messages = len(list(reddit.get_unread()))
		message = make_message(new_messages, reddit.user.name)
		print message
		icon.set_tooltip(message)
		if new_messages > 0:
			icon.set_from_pixbuf(mailIcon)
		else:
			icon.set_from_pixbuf(nomailIcon)
		if new_messages > prev.count:
			notify.show()
		prev.count = new_messages
	except Exception as e:
		print "Polling error: %s: %s" % (type(e).__name__, e)
		icon.set_from_pixbuf(errorIcon)
		icon.set_tooltip("Polling error\n(%s on last successful poll)" % make_message(prev.count, reddit.user.name))
	finally:
		return True


def click(ob, ev, reddit, icon, mailIcon, nomailIcon, errorIcon, prev, notify):
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
	icon.set_tooltip(make_message(0, reddit.user.name))


class PrevCount:
	def __init__(self):
		self.count = 0


def get_praw_handler():
	handler = None
	if len(sys.argv) > 1 and sys.argv[1] == "-m":
		handler = praw.handlers.MultiprocessHandler()
	else:
		handler = praw.handlers.DefaultHandler()
	return handler


def setup():
	#print "loading icons...",
	loadImage = gtk.Image()

	loadImage.set_from_file("mail.png")
	mailIcon = loadImage.get_pixbuf()

	loadImage.set_from_file("nomail.png")
	nomailIcon = loadImage.get_pixbuf()

	loadImage.set_from_file("error.png")
	errorIcon = loadImage.get_pixbuf()
	#print "done"

	#print "setting up status bar...",
	icon = gtk.StatusIcon()
	icon.set_from_pixbuf(nomailIcon)
	icon.set_visible(True)
	icon.set_tooltip("loading...")
	#print "done"

	print "logging in...",
	try:
		reddit = praw.Reddit(user_agent=user_agent, handler=get_praw_handler())
		reddit.login()
		print "logged in as /u/%s" % reddit.user.name
	except Exception as e:
		print "\nCould not log in: %s: %s" % (type(e).__name__, e)
		print "closing..."
		exit()

	#print "setting up popup...",
	pynotify.init("reddit-mail-notify")
	notify = pynotify.Notification("New reddit mail for /u/%s" % reddit.user.name)
	notify.set_timeout(5000)
	#print "done"

	prev = PrevCount()

	#print "connecting events...",
	icon.connect("button-press-event", click, reddit, icon, mailIcon, nomailIcon, errorIcon, prev, notify)
	#print "done"

	#print "registering polling function...",
	gobject.timeout_add(poll_time, poll, reddit, icon, mailIcon, nomailIcon, errorIcon, prev, notify)
	#print "done"

	#first poll
	poll(reddit, icon, mailIcon, nomailIcon, errorIcon, prev, notify)


if __name__ == "__main__":
	try:
		print user_agent
		setup()
		#print "entering main loop"
		gtk.main()
	except KeyboardInterrupt:
		print "\nclosing..."
		exit()
