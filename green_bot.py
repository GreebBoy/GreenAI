import os
import time
import openai
import tweepy
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
bot_username = os.getenv("BOT_USERNAME")

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

def get_ai_reply(tweet_text):
    prompt = f"""You are a degen meme bot hyping $GREEN coin. Reply in witty, humorous style: "{tweet_text}" """
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a meme-coin promoter bot."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=120,
        temperature=0.9
    )
    return resp["choices"][0]["message"]["content"]

def reply_to_mentions():
    mentions = api.mentions_timeline(count=5, tweet_mode='extended')
    for tweet in mentions:
        txt = tweet.full_text.lower()
        if bot_username.lower() not in txt:
            continue
        user = tweet.user.screen_name
        reply = get_ai_reply(tweet.full_text)
        api.update_status(status=f"@{user} {reply}", in_reply_to_status_id=tweet.id)
        print(f"Replied to @{user}")

if __name__ == "__main__":
    while True:
        try:
            reply_to_mentions()
        except Exception as e:
            print("Error:", e)
        time.sleep(300)
