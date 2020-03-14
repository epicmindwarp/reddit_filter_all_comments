# Automatically filter all comments from a specific reddit post

### Requirements

### filter_comments.py
The script runs from this file. Edit the following variables with your own details

BOT_AUTHOR      = 'epicmindwarp'

SUB_NAME        = ''    
USER_AGENT_NAME = f'{SUB_NAME} Bot to Moderate COVID-19 Discussion'    
TXT_FILE        = 'redditors_messaged.txt'

POST_TITLE      = 'post_title'

MSG_SUBJECT     = 'message_subject'    
MSG_BODY        = '''message_body'''

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

### Errors

There are two pieces of error handling, one for login and subreddit connection, and another for the entire loop; the latter sends a message to the BOT_AUTHOR when an error occurs, with the error message produced by reddit.

The script will continue to run again after 60 seconds.
