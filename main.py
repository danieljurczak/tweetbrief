import datetime
import os
from copy import copy
from typing import List

import pytz
import twitter
from emoji import UNICODE_EMOJI
from twitter import Status, User
from weasyprint import HTML, CSS

from variables import STYLE


class TweetBrief:
    api = twitter.Api(consumer_key=os.environ['BOT_CONSUMER_KEY'],
                      consumer_secret=os.environ['BOT_CONSUMER_SECRET'],
                      access_token_key=os.environ['BOT_TOKEN_KEY'],
                      access_token_secret=os.environ['BOT_TOKEN_SECRET'],
                      tweet_mode='extended')

    NUMBER_OF_LINES = 60
    LINE_LENGTH = 38

    @staticmethod
    def get_filename() -> str:
        return f"tweetbrief_{datetime.datetime.now(tz=pytz.utc).strftime('%Y%m%d')}.pdf"

    @staticmethod
    def sort_tweets_by_retweet_count(tweets: List[Status]) -> List[Status]:
        tweets.sort(key=lambda x: x.retweet_count, reverse=True)
        return tweets

    @classmethod
    def get_best_tweets_for_user(cls, user: User, from_days: int) -> List[Status]:
        now = datetime.datetime.now(tz=pytz.utc)
        week_ago = now - datetime.timedelta(days=from_days)
        user_tweets = []
        for status in cls.api.GetUserTimeline(user_id=user.id, exclude_replies=True):
            created_at = datetime.datetime.strptime(status.created_at, '%a %b %d %X %z %Y')
            if created_at > week_ago:
                user_tweets.append(status)
        return cls.sort_tweets_by_retweet_count(user_tweets)

    @classmethod
    def get_tweets(cls, screen_name: str, from_days: int) -> List[Status]:
        users = cls.api.GetFriends(screen_name=screen_name)
        final_tweets = []

        for user in users:
            final_tweets += cls.get_best_tweets_for_user(user, from_days)[:3]

        return cls.sort_tweets_by_retweet_count(final_tweets)

    @staticmethod
    def generate_html_layout(first_column: str, second_column: str) -> str:
        html = f"""
        <html>
            <head>
                <meta charset="UTF-8">
            </head>
            <body>
                <div class="row">
                  <div class="column">
                      {first_column}
                  </div>
                  <div class="column">
                      {second_column}
                  </div>
                </div>
            </body>
        </html>
        """
        return html

    @classmethod
    def count_number_of_lines_in_pdf(cls, content: str) -> int:
        content = content.split()
        len_of_line = 0
        num_of_lines = 1
        for word in content:
            len_of_word = len(word)
            for char in copy(word):
                if char in UNICODE_EMOJI:
                    len_of_word += 1
            if len_of_line + len_of_word < cls.LINE_LENGTH:
                len_of_line += len_of_word + 1  # +1 beacause of space at the end
            else:
                len_of_line = len_of_word + 1
                num_of_lines += 1
        num_of_lines += 1
        return num_of_lines

    @classmethod
    def generate_html_for_status(cls, status: Status) -> str:
        html = f"""
            <p><b>{status.user.screen_name}</b> ({status.created_at[:-11]}):
            {status.full_text}</p>
            <br>
        """
        return html

    @classmethod
    def generate_html_for_tweet_brief(cls, statuses: List[Status]) -> str:
        first_column = ""
        second_column = ""
        number_of_lines = 0
        for status in statuses:
            tweet_content = f"{status.user.screen_name} ({status.created_at[:-11]}): {status.full_text}"
            tweet_lines = cls.count_number_of_lines_in_pdf(tweet_content)

            html = cls.generate_html_for_status(status)
            number_of_lines += tweet_lines

            if number_of_lines < cls.NUMBER_OF_LINES:
                first_column += html
            elif cls.NUMBER_OF_LINES <= number_of_lines < cls.NUMBER_OF_LINES * 2:
                second_column += html
            else:
                break

        return cls.generate_html_layout(first_column, second_column)

    @classmethod
    def generate_pdf(cls, statuses: List[Status]) -> None:
        html = cls.generate_html_for_tweet_brief(statuses)
        filename = cls.get_filename()
        HTML(string=html).write_pdf(target=filename, stylesheets=[CSS(string=STYLE)])

    @classmethod
    def run(cls, screen_name: str, from_days: int) -> None:
        tweets = cls.get_tweets(screen_name, from_days)
        cls.generate_pdf(tweets)


if __name__ == "__main__":
    TweetBrief.run(os.environ['TARGET_USERNAME'], os.environ['BRIEF_PERIOD'])
