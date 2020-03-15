# Automatically filter all comments from a specific reddit post

## Requirements

### System Requirements

Tried and tested on:

Windows 10 and Python 3.7.4
Raspberry Pi 3B+ running Raspian

### filter_comments.py
The script runs from this file. Edit the following variables with your own details

BOT_AUTHOR      = 'epicmindwarp'

SUB_NAME        = ''    
USER_AGENT_NAME = f'{SUB_NAME} Comments Filter Bot v0.01_alpha'    
TXT_FILE        = 'redditors_messaged.txt'

POST_TITLE      = 'post_title'

MSG_SUBJECT     = 'message_subject'    
MSG_BODY        = '''multi_line_msg_body'''

Bot Author = This is the person the bot will message in the event of an error during run time (but not a login error).

Sub Name - The sub it will look over - multireddits should be okay (untested, but easy to verify)

User Agent Name - Edit this slightly to indicate what this bot will do (reddit will see this)

Text File - This is the file that usernames are stored in, so the bot doesn't reply to people constantly

Post Title - This is the post title that the bot is looking for. I could've used Post ID - but it makes no difference as the bot just removes and nothing else (so anyone imitating this post won't benefit from doing so).

Message Subject - Subject of the message when the bot responds to a user who just commented for the first time in the post

Message Body - Body of the message when the bot responds to a user who just commented for the first time in the post

The details in the above are used in the script to ensure it runs smoothly. The post title is used to identify from which post the comments should automatically be removed from.

### config.py
A file in the same folder, that is used in the main script as parameters, containing:

username = 'username'    
password = 'password'    
client_id = 'client_id'    
client_secret = 'client_secret'


### redditors_messaged.txt
An empty text file in the same folder, used to store users messaged already (to stop spamming the same user sending multiple messages)

___

## Errors

There are two pieces of error handling, one for login and subreddit connection, and another for the entire loop; the latter sends a message to the BOT_AUTHOR when an error occurs, with the error message produced by reddit.

The script will continue to run again after 60 seconds.
