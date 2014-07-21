# reddit-mail-notify

Status bar icon and popup notification for new reddit messages. Completely unofficial.

## Features

* Polls for new mail every minute
* Mail icon on your status bar, just like on the website
* Icon changes color when you have new messages
* Tooltip shows how many new messages there are, and reminds you who you're logged in as
* Left click icon to take you to your mailbox. Right click to go to your user page

## Usage

`python reddit-mail-notify.py [--multi]`

The `--multi` flag turns on multiprocess support, in case you want to run other PRAW programs alongside it. Run `praw-multiprocess` to start the PRAW request server.

To specify accounts to check you need to make an `accounts.cfg` file. Each line in the file represents one user. First you put the username, then an equals sign (`=`), then the password (which may safely contain more equals signs). If you want modmail checked instead of regular messages, put an exclamation mark (`!`) before the username.

The complete file might look something like this:

    !modguy123445=this-is-my-password
    modguy123445=this-is-my-password
    some_other_acnt=logmeinplox

This will check both modmail and normal mail of /u/modguy123445 and normal mail of /u/some_other_acnt.

## Dependencies

(Versions indicate what it was developed with.)

* Python (2.7.3)
* PRAW for reddit interaction (2.1.16)
* PyGTK for status bar icon (2.24.0)
* PyNotify for popup messages (0.1.1)
