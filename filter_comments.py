import sys
import time
import praw
import datetime as dt
import config as config

BOT_AUTHOR      = ''

SUB_NAME        = ''
USER_AGENT_NAME = f'{SUB_NAME} Bot v0.01_alpha'
TXT_FILE        = 'redditors_messaged.txt'

POST_TITLE      = 'post_title'  # This post title is used to identify which post is being filtered for comments

MSG_SUBJECT     = 'message_subject'
MSG_BODY        = '''multi_line_msg_body'''

# Created by /u/epicmindwarp
# Designed to filter all comments automatically from a single post defined by name
# Created in response to a rising number of unsubstantiated comments around COVID-19 on /r/AskUK
# By focusing discussion on this topic to one thread, it gives control to moderators to filter threads more easily

def current_time():
    
    # Returns the current date and time in a more readable format
    
    return dt.datetime.today().replace(microsecond=0)

def bot_login():

    # Login to reddit using credentials from config file
    # You can also use the credentials from environment variables or other places
    
    print(f'\nLogging in as {config.username}...')     

    # Login with oAuth2
    try:
        r = praw.Reddit(username = config.username,
                        password = config.password,
                        client_id = config.client_id,
                        client_secret = config.client_secret,
                        user_agent = USER_AGENT_NAME)
    except:
        print('### ERROR - Could not log into reddit.')
        return False

    # After logging in, ensure it's not read only (so we can make changes)
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

    # Opens a seperate text file which contains a list of usernames
    # If a user's name is in that file, the bot won't message them again
    
    f = open(TXT_FILE, 'r')

    # Loop through all lines
    for x in f:

        # Remove the line break tag, to allow for comparison
        x = x.replace('\n', '')

        # If username in file
        if x == username.name:
            
            # Already messaged
            return True
    
    return False


def add_username_in_file(username):

    # When the bot messages someone for the first time, it records their username in this file
    # This stops the user from being messaged again by the bot, if they comment again
    
    # Open in append mode
    f = open(TXT_FILE, 'a')

    # Add a new line break before adding their name
    f.write('\n'+username.name)

    f.close()

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------

# Code starts running here

try:
    # Ensure you can connect to reddit
    reddit = bot_login()

    # It will only return FALSE if the login failed in any way
    if type(reddit) is bool:
        raise ConnectionError("Could not connect to reddit!")

    # Connect to the sub we're interested in
    subreddit = reddit.subreddit(SUB_NAME)

except Exception as e:
    # If any of the above have failed, then you'll see it on screen anyway
    # So no point sending a message, just quit
    print('\t### ERROR - Could not login to reddit!')
    sys.exit(1)

while True:

    try:
        # Being a streaming comments instance on the sub already connected to
        # Use skip_existing, otherwise the bot will remove the last 100 comments
        for comment in subreddit.stream.comments(skip_existing=True):

            # Get the title to compare against            
            title = comment.submission.title

            # Is the sub title what we're looking for
            if title == POST_TITLE:

                # Get the author
                author = comment.author

                # Tab and new line tags added for ease of viewing when printing
                body = '\t' + comment.body.replace('\n', '\n\t')

                try:
                    print('\n', comment, ' - ', author ,' - ', title)
                    print(body)
                except Exception as e:
                    # This will handle unicode errors or other print errors (that shouldn't stop the bot)
                    print(f'\t# Error - {e}')

                # Remove the comment
                comment.mod.remove(spam=False)

                # If their username is not already in the messaged file
                if not check_username_in_file(author):

                    # Send the author a message
                    author.message(MSG_SUBJECT, MSG_BODY)    
                    print('\tMessage sent.')

                    # Log we've messaged them
                    add_username_in_file(author)

                # Visual seperator
                print('\n', '*'*50)

    except Exception as e:

        print(f'\t###ERROR - {e}')

        # In the event of an error, message the author with the error message
        try:
            reddit.redditor(BOT_AUTHOR).message('Bot Error', f'The bot just errored out.\n\n{e}')
        except Exception as e:
            # This may also fail in the event of the host's internet going down
            # So ensure the bot doesn't go down, so do nothing
            pass

        # Wait 60 seconds before trying again in the event of an error
        # This won't stop an infinite loop, but it'll stop any hit rate issues (hopefully)
        time.sleep(60)
