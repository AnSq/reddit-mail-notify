#!/usr/bin/python -u
# -u for unbuffered output

import webbrowser
import praw
import gtk
import gobject
import pynotify
import sys


version = "1.1"
user_agent = "reddit-mail-notify v%s by /u/AnSq" % version
poll_time = 60000


def make_message(new_messages, name, mode):
	if mode == "mod":
		if new_messages:
			return "New modmail for /u/%s" % name
		else:
			return "No new modmail for /u/%s" % name
	else:
		msgCount = "No" if new_messages==0 else str(new_messages)
		plural = "" if new_messages==1 else "s"
		return "%s new message%s for /u/%s" % (msgCount, plural, name)


def poll(reddit, icon, mailIcon, nomailIcon, errorIcon, prev, notify, mode):
	try:
		#print "polling...",

		new_messages = 0
		if mode == "mod":
			new_messages = reddit.get_redditor(reddit.user.name).has_mod_mail
		else:
			new_messages = len(list(reddit.get_unread()))

		message = make_message(new_messages, reddit.user.name, mode)
		print message
		icon.set_tooltip(message)

		if new_messages > 0:
			icon.set_from_pixbuf(mailIcon)
		else:
			icon.set_from_pixbuf(nomailIcon)
		if new_messages > prev.count:
			try:
				notify.show()
			except Exception as e:
				print "Notification error: %s: %s" % (type(e).__name__, e)
		prev.count = new_messages

	except Exception as e:
		print "Polling error: %s: %s" % (type(e).__name__, e)
		icon.set_from_pixbuf(errorIcon)
		icon.set_tooltip("Polling error\n(%s on last successful poll)" % make_message(prev.count, reddit.user.name, mode))

	finally:
		return True


def click(ob, ev, reddit, icon, mailIcon, nomailIcon, errorIcon, prev, notify, mode):
	if ev.button == 1:
		#print "left click"
		if mode == "mod":
			webbrowser.open("http://www.reddit.com/message/moderator")
		else:
			if prev.count == 0:
				webbrowser.open("http://www.reddit.com/message/inbox")
			else:
				webbrowser.open("http://www.reddit.com/message/unread")
	elif ev.button == 3:
		#print "right click"
		webbrowser.open("http://www.reddit.com/user/%s" % reddit.user.name)
	prev.count = 0
	icon.set_from_pixbuf(nomailIcon)
	icon.set_tooltip(make_message(0, reddit.user.name, mode))


class PrevCount:
	def __init__(self):
		self.count = 0


def get_praw_handler():
	handler = None
	if len(sys.argv) > 1 and "--multi" in sys.argv[1:]:
		handler = praw.handlers.MultiprocessHandler()
		print "Multiprocess mode active."
	else:
		handler = praw.handlers.DefaultHandler()
	return handler


def setup():
	mode = "normal"
	if len(sys.argv) > 1 and "--mod" in sys.argv[1:]:
		mode = "mod"
		print "Modmail mode active."

	#print "loading icons...",
	loadImage = gtk.Image()

	mail_fname = ""
	if mode == "mod":
		mail_fname = "modmail.png"
	else:
		mail_fname = "mail.png"
	loadImage.set_from_file(mail_fname)
	mailIcon = loadImage.get_pixbuf()

	nomail_fname = ""
	if mode == "mod":
		nomail_fname = "nomodmail.png"
	else:
		nomail_fname = "nomail.png"
	loadImage.set_from_file(nomail_fname)
	nomailIcon = loadImage.get_pixbuf()

	error_fname = ""
	if mode == "mod":
		error_fname = "moderror.png"
	else:
		error_fname = "error.png"
	loadImage.set_from_file(error_fname)
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

	notify_msg = ""
	if mode == "mod":
		notify_msg = "New modmail for /u/%s" % reddit.user.name
	else:
		notify_msg = "New reddit mail for /u/%s" % reddit.user.name
	notify = pynotify.Notification(notify_msg)

	notify.set_timeout(5000)
	#print "done"

	prev = PrevCount()

	#print "connecting events...",
	icon.connect("button-press-event", click, reddit, icon, mailIcon, nomailIcon, errorIcon, prev, notify, mode)
	#print "done"

	#print "registering polling function...",
	gobject.timeout_add(poll_time, poll, reddit, icon, mailIcon, nomailIcon, errorIcon, prev, notify, mode)
	#print "done"

	#first poll
	poll(reddit, icon, mailIcon, nomailIcon, errorIcon, prev, notify, mode)


if __name__ == "__main__":
	try:
		print user_agent
		setup()
		#print "entering main loop"
		gtk.main()
	except KeyboardInterrupt:
		print "\nclosing..."
		exit()
