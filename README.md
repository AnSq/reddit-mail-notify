# reddit-mail-notify

Status bar icon and popup notification for new reddit messages. Completely unofficial.

## Features

* Polls for new mail every minute
* Mail icon on your status bar, just like on the website
* Icon changes color when you have new messages
* Tooltip shows how many new messages there are, and reminds you who you're logged in as
* Left click icon to take you to your mailbox. Right click to go to your user page

## Usage

`python reddit-mail-notify.py [-m]`

The optional `-m` flag turns on multiprocess support, in case you want to run other PRAW programs alongside it. Run `praw-multiprocess` to start the PRAW request server.

By default the progtam will prompt you for a username and password, or you can make a `praw.ini` file that looks like this:

	[DEFAULT]
	user=<username>
	pswd=<password>

## Dependancies

(Versions indicate what it was developed with.)

* Python (2.7.3)
* PRAW for reddit interaction (2.1.15)
* PyGTK for status bar icon (2.24.0)
* PyNotify for popup messages (0.1.1)
