# reddit-mail-notify

Status bar icon and popup notification for new reddit messages. Completely unofficial.

## Features

* Mail icon on your status bar, just like on the website
* Icon changes color when you have new messages
* Tooltip shows how many new messages there are, and reminds you who you're logged in as
* Left click icon to take you to your mailbox. Right click to go to your user page

## Usage

Simple run the program. It takes no parameters.

By default it will prompt you for a username and password, or you can make a `praw.ini` file that looks like this:

	[DEFAULT]
	user=<username>
	pswd=<password>

## Dependancies

(Versions indicate what it was developed with.)

* PRAW for reddit interaction (2.1.1)
* PyGTK for status bar icon (2.24.0)
* PyNotify for popup messages (0.1.1)
