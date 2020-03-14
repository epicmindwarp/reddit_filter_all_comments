import sys
import time
import praw
import datetime as dt
import config as config

BOT_AUTHOR      = 'epicmindwarp'

SUB_NAME        = ''
USER_AGENT_NAME = f'{SUB_NAME} Bot v0.01_alpha'
TXT_FILE        = 'redditors_messaged.txt'

POST_TITLE      = 'post_title'  # This post title is used to identify which post is being filtered for comments

MSG_SUBJECT     = 'message_subject'
MSG_BODY        = '''multi_line_msg_body'''

def current_time():
    return dt.datetime.today().replace(microsecond=0)

def bot_login():

    print(f'\nLogging in as {config.username}...')     # LOGIN USING CREDENTIALS FROM CONFIG FILE (SEPERATE FILE)

    # Login with oAuth2
    try:
        r = praw.Reddit(username = config.username,
                        password = config.password,
                        client_id = config.client_id,
                        client_secret = config.client_secret,
                        user_agent = USER_AGENT_NAME)
    except:
        print('### ERROR - Could not log into reddit.')

    # Try logging in 
    try:
        r.read_only = False
    except Exception as e:
        print('\t### ERROR - Reddit login failed!\n\n\t{0}'.format(e))
        return False

    # Confirm it's not in read only mode to continue                
    if r.read_only == False:
        print(f'Logged in at {current_time()}')
        print(f'Subreddits: {SUB_NAME}'+ '\n'*3 )

        # Send the logged in variable back
        return r
    else:
        print('Error logging in - not non-read only mode!!')
        return False



def check_username_in_file(username):

    f = open(TXT_FILE, 'r')

    # Loop through all lines
    for x in f:
        
        # If username in file
        if x == username.name:
            
            # Already messaged
            return True
    
    return False


def add_username_in_file(username):

    f = open(TXT_FILE, 'a')

    f.write('\n'+username.name)

    f.close()

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------


try:
    reddit = bot_login()

    if type(reddit) is bool:
        sys.exit(1)

    # Connect to the sub we're interested in
    subreddit = reddit.subreddit(SUB_NAME)

except Exception as e:
    print('\t### ERROR - Could not login to reddit!')

while True:

    try:

        for comment in subreddit.stream.comments(skip_existing=True):

            # Get the title to compare against            
            title = comment.submission.title

            # Is the sub title what we're looking for
            if title == POST_TITLE:

                # Get the author
                author = comment.author
                body = '\t' + comment.body.replace('\n', '\n\t')

                try:
                    print('\n', comment, ' - ', author ,' - ', title)
                    print(body)
                except Exception as e:
                    print(f'\t# Error - {e}')

                # Remove the comment
                comment.mod.remove(spam=False)

                # If their username is not already in the messaged file
                if not check_username_in_file(author):

                    # Send the author a message
                    author.message(MSG_SUBJECT, MSG_BODY)    
                    print('\tMessage sent.')
                    add_username_in_file(author)

                print('\n', '*'*50)

    except Exception as e:

        print(f'\t###ERROR - {e}')
        reddit.redditor(BOT_AUTHOR).message('Bot Error', f'The bot just errored out.\n\n{e}')
        time.sleep(60)
