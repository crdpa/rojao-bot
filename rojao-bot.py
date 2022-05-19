#!/usr/bin/env python3

import configparser
import praw
import re
import traceback
from time import sleep


def config_read(file):
    config = configparser.ConfigParser()
    config.read(file)
    user_agent = config.get('bot', 'user_agent')
    client_id = config.get('bot', 'client_id')
    client_secret = config.get('bot', 'client_secret')
    username = config.get('bot', 'username')
    password = config.get('bot', 'password')
    return user_agent, client_id, client_secret, username, password


def check_condition(comment):
    word1 = re.compile('!rojao')
    word2 = re.compile('!rojão')
    text = comment.body
    result1 = re.search(word1, text.lower())
    result2 = re.search(word2, text.lower())
    if result1 or result2:
        return True
    else:
        return False


def main():
    sub_name = 'bottesting'
    reply_text = 'Eu \U0001F389 fico \U0001F9E8 muito triste \U0001F602 com uma notícia dessas! \U0001F9E8 \U0001F38A'
    cache = []

    user_agent, id, secret, username, password = config_read('secrets.ini')
    bot = praw.Reddit(
        client_id=id,
        client_secret=secret,
        username=username,
        password=password,
        user_agent=user_agent
    )

    while True:
        try:
            subreddit = bot.subreddit(sub_name)
            comments = subreddit.comments(limit=1000)
            for comment in comments:
                if comment.id in cache:
                    break

                cache.append(comment.id)
                condition = check_condition(comment)
                if condition:
                    comment.reply(reply_text)
        except Exception:
            traceback.print_exc()
            print("Sleeping for 60 seconds.")
            sleep(60)


if __name__ == "__main__":
    main()
