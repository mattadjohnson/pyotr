from flask import Flask
from flask import render_template
import ConfigParser
import praw

app = Flask(__name__)

"""Load config file to get Reddit API connection info"""
Config = ConfigParser.ConfigParser()
Config.read('config.ini')


def get_praw_config():
    """Return a dict of Reddit API connection config:
    UserAgent, ClientID, and ClientSecret
    """
    praw_info = {}
    options = Config.options('PrawInfo')
    for option in options:
        try:
            praw_info[option] = Config.get('PrawInfo', option)
            if praw_info[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            praw_info[option] = None
    return praw_info

praw_config = get_praw_config()

my_user_agent = praw_config['useragent']
my_client_id = praw_config['clientid']
my_client_secret = praw_config['clientsecret']

"""Setup Reddit API connection"""
reddit = praw.Reddit(user_agent=my_user_agent,
                     client_id=my_client_id,
                     client_secret=my_client_secret)

query = '''nsfw:no title:giraffes OR title:pyotr OR selftext:giraffes OR selftext:pyotr
           OR url:giraffes OR url:pyotr'''


def get_giraffes(post_limit):
    """Return a list (len=post_limit) of submissions from Reddit matching query"""
    submissions = []

    for submission in reddit.subreddit('all').search(query,
                                                     sort='new',
                                                     syntax='lucene',
                                                     limit=post_limit):
        submissions.append(submission)

    return submissions


@app.route('/')
def hello_pyotr():
    """Return HTML template, with submissions from get_giraffes(post_limit)"""
    submissions = get_giraffes(5)

    return render_template('pyotr.html', submissions=submissions)
