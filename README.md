# reddit-mail-notify

Status bar icon and popup notification for new reddit messages. Completely unofficial.

## Features

* Polls for new mail every minute
* Mail icon on your status bar, just like on the website
* Icon changes color when you have new messages
* Tooltip shows how many new messages there are, and reminds you who you're logged in as
* Left click icon to take you to your mailbox. Right click to go to your user page

## Usage

`python reddit-mail-notify.py [OPTIONS]`

The `--mod` flag turns on modmail mode. This checks for modmail instead of regular messages, and changes the icon to match. Unfortunately, the program cannot count the number of new modmail messages at this time.

The `--multi` flag turns on multiprocess support, in case you want to run other PRAW programs alongside it. Run `praw-multiprocess` to start the PRAW request server.

By default the program will prompt you for a username and password, or you can make a `praw.ini` file that looks like this:

	[DEFAULT]
	user=<username>
	pswd=<password>

If you have multiple accounts that you want to check mail for, simply start the program multiple times, once for each account. You will need to log in manually each time, not using `praw.ini` in this case.

## Dependencies

(Versions indicate what it was developed with.)

* Python (2.7.3)
* PRAW for reddit interaction (2.1.16)
* PyGTK for status bar icon (2.24.0)
* PyNotify for popup messages (0.1.1)
