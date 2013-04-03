soxbot
======

Updates baseball standings on a Reddit subreddit.

Usage
-----

Setup a developer account at http://sportsdatallc.org/ and create a trial key for usage with this bot. Please be aware of the data usage limitations or you risk your key being throttled and deactivated.

Enter all your user information into rlogin.py. You'll need your Reddit username, password, and subreddit. You'll also need to define a reddit user agent. MAKE SURE THIS IS UNIQUE. If it is not unique you risk the account being banned by Reddit. See here: https://github.com/reddit/reddit/wiki/API

Subreddit Configuration
-------------------------------------------

I've currently setup the script to look for the string **Standings** in your subreddit description and then truncate it and replace it with the new standings. It is very important that the subreddit description places the **Standings** header at the bottom of the description so it doesn't cut off anything you don't want to lose. I know this is rudimentary currently and maybe with more time and development I can make a smarter solution. But for now this works and gets the job done.

Cron
---------
Once your data is entered into rlogin.py you'll need setup a cronjob on your server to have the main.py file run nightly to update your settings. This is assuming you are using a Linux server. Either way the script needs to be run once a day to update the standings on your Subreddit.

Future Additions
-----------------------------

Eventually this bot will also create your Game Threads so you don't have to. I plan on having that done by the end of April 2013.
