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
    if mode:
        if new_messages:
            return "New modmail for /u/%s" % name
        else:
            return "No new modmail for /u/%s" % name
    else:
        msgCount = "No" if new_messages==0 else str(new_messages)
        plural = "" if new_messages==1 else "s"
        return "%s new message%s for /u/%s" % (msgCount, plural, name)


def poll(users, icons):
    for user in users:
        try:
            #print "polling...",

            new_messages = 0
            if user.mod:
                new_messages = user.reddit.get_redditor(user.reddit.user.name).has_mod_mail
            else:
                new_messages = len(list(user.reddit.get_unread()))

            message = make_message(new_messages, user.reddit.user.name, user.mod)
            print message
            user.icon.set_tooltip(message)

            if new_messages > 0:
                user.icon.set_from_pixbuf(icons[user.mod][0])
            else:
                user.icon.set_from_pixbuf(icons[user.mod][1])
            if new_messages > user.prev.count:
                try:
                    user.notify.show()
                except Exception as e:
                    print "Notification error: %s: %s" % (type(e).__name__, e)
            user.prev.count = new_messages

        except Exception as e:
            print "Polling error: %s: %s" % (type(e).__name__, e)
            user.icon.set_from_pixbuf(icons[user.mod][2])
            tip = "Polling error\n(%s on last successful poll)" % make_message(user.prev.count, user.reddit.user.name, user.mod)
            user.icon.set_tooltip(tip)

    return True


def click(ob, ev, user, icons):
    if ev.button == 1:
        #print "left click"
        if user.mod:
            webbrowser.open("http://www.reddit.com/message/moderator")
        else:
            if user.prev.count == 0:
                webbrowser.open("http://www.reddit.com/message/inbox")
            else:
                webbrowser.open("http://www.reddit.com/message/unread")
    elif ev.button == 3:
        #print "right click"
        webbrowser.open("http://www.reddit.com/user/%s" % user.reddit.user.name)
    user.prev.count = 0
    user.icon.set_from_pixbuf(icons[user.mod][1])
    user.icon.set_tooltip(make_message(0, user.reddit.user.name, user.mod))


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


class User (object):
    def __init__(self, mod, username, password):
        self.mod = mod
        self.username = username
        self.password = password
        self.icon = None
        self.reddit = None
        self.notify = None
        self.prev = None


def load_users():
    f = open("accounts.cfg", "r")

    users = []

    for line in f:
        if "=" in line:
            username, password = line.split("=", 1)
            if password[-1] == "\n":
                password = password[:-1]
            mod = False
            if username[0] == "!":
                mod = True
                username = username[1:]
            users.append(User(mod, username, password))

    f.close()
    return users


def setup(users):
    #print "loading icons...",
    loadImage = gtk.Image()

    modmail_fname = "modmail.png"
    loadImage.set_from_file(modmail_fname)
    modmailIcon = loadImage.get_pixbuf()

    mail_fname = "mail.png"
    loadImage.set_from_file(mail_fname)
    mailIcon = loadImage.get_pixbuf()

    nomodmail_fname = "nomodmail.png"
    loadImage.set_from_file(nomodmail_fname)
    nomodmailIcon = loadImage.get_pixbuf()

    nomail_fname = "nomail.png"
    loadImage.set_from_file(nomail_fname)
    nomailIcon = loadImage.get_pixbuf()

    moderror_fname = "moderror.png"
    loadImage.set_from_file(moderror_fname)
    moderrorIcon = loadImage.get_pixbuf()

    error_fname = "error.png"
    loadImage.set_from_file(error_fname)
    errorIcon = loadImage.get_pixbuf()

    icons = (
        (mailIcon, nomailIcon, errorIcon),
        (modmailIcon, nomodmailIcon, moderrorIcon)
    )
    #print "done"

    #print "setting up status bar...",
    for user in users:
        icon = gtk.StatusIcon()
        icon.set_from_pixbuf(icons[user.mod][1])
        icon.set_visible(True)
        icon.set_tooltip("loading...")
        user.icon = icon
    #print "done"

    print "logging in...",
    for user in users:
        try:
            reddit = praw.Reddit(user_agent=user_agent, handler=get_praw_handler())
            reddit.login(user.username, user.password)
            user.reddit = reddit
            print "logged in as /u/%s" % reddit.user.name
        except Exception as e:
            print "\nCould not log in: %s: %s" % (type(e).__name__, e)
            print "closing..."
            exit()

    #print "setting up popup...",
    pynotify.init("reddit-mail-notify")

    for user in users:
        notify_msg = ""
        if user.mod:
            notify_msg = "New modmail for /u/%s" % user.reddit.user.name
        else:
            notify_msg = "New reddit mail for /u/%s" % user.reddit.user.name
        user.notify = pynotify.Notification(notify_msg)
        user.notify.set_timeout(5000)
    #print "done"

    for user in users:
        user.prev = PrevCount()

    #print "connecting events...",
    for user in users:
        user.icon.connect("button-press-event", click, user, icons)
    #print "done"

    #print "registering polling function...",
    gobject.timeout_add(poll_time, poll, users, icons)
    #print "done"

    #first poll
    poll(users, icons)


if __name__ == "__main__":
    try:
        print user_agent
        users = load_users()
        setup(users)
        #print "entering main loop"
        gtk.main()
    except KeyboardInterrupt:
        print "\nclosing..."
        exit()
