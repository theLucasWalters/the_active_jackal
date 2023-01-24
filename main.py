import credentials as c
import requests
import json
import os


# I've largely based this code on Twitter's API v2 Python sample code

# bearer token
# bearer_token = c.BEARER_TOKEN # only if `os.environ.get()` doesn't work
bearer_token = os.environ.get("BEARER_TOKEN")


# honestly, I don't know what this does, I just copied it from Twitter's code samples.
def bearer_oauth(r):
    # don't mess with this lest things break
    """Method required by bearer token authentication."""
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r


def connect_to_endpoint(url, params):
    # don't mess with this lest things break
    """Authenticate the request and return a JSON object."""

    # authenticate
    response = requests.request("GET", url, auth=bearer_oauth, params=params)

    # print the status code
    print(response.status_code)

    # throw an error if the request is anything other than 200
    if response.status_code != 200:
        raise Exception(f"Request returned an error: {response.status_code} {response.text}")

    # return the JSON object
    return response.json()


def rts_reps():
    # ask if the user wants to include retweets in the results
    rts = input("Do you want to include retweets? y/N > ").lower()
    while not (rts == 'y' or rts == 'n'):
        rts = input("Must be 'y' or 'n' > ")
    if rts == 'y':
        rts_bool = True
    else:
        rts_bool = False

    # as if the user wants to include replies in the results
    reps = input("Do you want to include replies? y/N > ").lower()
    while not (reps == 'y' or reps == 'n'):
        reps = input("Must be 'y' or 'n' > ")
    if reps == 'y':
        reps_bool = True
    else:
        reps_bool = False

    return rts_bool, reps_bool


def make_it_pretty(tweet_dict, user):
    for tweet in tweet_dict["data"]:
        date_published = tweet["created_at"].split('T')
        print(
            f"""
            \n
For tweet 'https://twitter.com/{user}/status/{tweet['id']}':
Text: \"{tweet['text']}\"
Published on: {date_published[0]} at {date_published[1]}
Metrics:
    Views:        {tweet['public_metrics']['impression_count']}
    Likes:        {tweet['public_metrics']['like_count']}
    Replies:      {tweet['public_metrics']['reply_count']}
    Retweets:     {tweet['public_metrics']['retweet_count']}
    Quote Tweets: {tweet['public_metrics']['quote_count']}
            """
        )

    print(f"Total tweets found: {tweet_dict['meta']['result_count']}")


# main function
def main():
    # get the account to look up
    user = input("What's the Twitter account you want to look at? > ")
    print(f"Retreiving tweets for account: @{user}")

    rts, reps = rts_reps()

    # our search url
    search_url = "https://api.twitter.com/2/tweets/search/recent"

    # query parameters
    # All recent tweets from the passed account, including or excluding retweets and/or replies depending on previous inputs
    # The maximum number of tweets that can be returned is 100
    # The default time period is within the last 7 days
    if rts and reps:
        query_params = {
            'query': f'(from:{user})',
            'tweet.fields': 'public_metrics,created_at',
            'max_results': 100
        }
    elif not rts and reps:
        query_params = {
            'query': f'(from:{user} -is:retweet)',
            'tweet.fields': 'public_metrics,created_at',
            'max_results': 100
        }
    elif rts and not reps:
        query_params = {
            'query': f'(from:{user} -is:reply)',
            'tweet.fields': 'public_metrics,created_at',
            'max_results': 100
        }
    elif not rts and not reps:
        query_params = {
            'query': f'(from:{user} -is:retweet -is:reply)',
            'tweet.fields': 'public_metrics,created_at',
            'max_results': 100
        }
    else:
        raise Exception(f"Invalid 'rts' and/or 'reps' value: {rts}, {reps}")

    # get the json response
    json_response = connect_to_endpoint(search_url, query_params)

    # and print it all out
    make_it_pretty(json_response, user)


if __name__ == "__main__":
    main()
