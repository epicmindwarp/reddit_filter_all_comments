# reddit_filter_all_comments
Filter all comments in a specific post automatically

# Requirements

## filter_comments.py
The script runs from this file. Edit the following variables with your own details

BOT_AUTHOR      = 'epicmindwarp'

SUB_NAME        = ''
USER_AGENT_NAME = f'{SUB_NAME} Bot to Moderate COVID-19 Discussion'
TXT_FILE        = 'redditors_messaged.txt'

POST_TITLE      = 'post_title'

MSG_SUBJECT     = 'message_subject'
MSG_BODY        = '''message_body'''

The details in the above are used in the script to ensure it runs smoothly. The post title is used to identify from which post the comments should automatically be removed from.

## config.py
A file in the same folder, that is used in the main script as parameters, containing:

username = 'username'
password = 'password'
client_id = 'client_id'
client_secret = 'client_secret'


## redditors_messaged.txt
An empty text file in the same folder, used to store users messaged already (to stop spamming the same user sending multiple messages)
