import credentials as c
import requests
import json


# I've largely based this code on Twitter's API v2 Python sample code

# bearer token
bearer_token = c.BEARER_TOKEN


def create_first_url(user):
    """Create and return a url using the passed Twitter username."""

    url = f"https://api.twitter.com/2/tweets/search/recent?query=from:{user}"
    return url


def create_second_url(ids):
    """Get an individual tweet's egagement data."""

    # I wouldn't normally do it like this, but we know the `ids` list will have 10 elements for a typical account
    url = f"https://api.twitter.com/2/tweets?tweet.fields=public_metrics&ids={ids[0]},{ids[1]},{ids[2]},{ids[3]},{ids[4]},{ids[5]},{ids[6]},{ids[7]},{ids[8]},{ids[9]}"
    return url


# honestly, I don't know what this does. I just copied it from the sample.
def bearer_oauth(r):
    """Method required by bearer token authentication."""
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r


def connect_to_endpoint(url):
    """Authenticate the request and return a JSON object."""
    
    # authenticate
    response = requests.request("GET", url, auth=bearer_oauth)
    
    # print the status code
    print(response.status_code)

    # throw an error if the request is anything other than 200
    if response.status_code != 200:
        raise Exception(f"Request returned an error: {response.status_code} {response.text}")

    # return the JSON object
    return response.json()


# this is NOT permanent
def make_it_pretty(user, data_list, id_list, json_obj):
    """A temporary (and hacky) way to print a formatted list of 10 tweet engagement stats."""
    print(
        f"""
        Note: These are listed as the 10 most recent tweets.
        First is the most recent, while the last is the least recent.

        Engagement stats for @{user}'s recent tweets:

        For tweet {id_list[0]}:
        Text: {json_obj["data"][0]["text"]}
        Likes:        {data_list[0]["like_count"]}
        Replies:      {data_list[0]["reply_count"]}
        Retweets:     {data_list[0]["retweet_count"]}
        Quote Tweets: {data_list[0]["quote_count"]}

        For tweet {id_list[1]}:
        Text: {json_obj["data"][1]["text"]}
        Likes:        {data_list[1]["like_count"]}
        Replies:      {data_list[1]["reply_count"]}
        Retweets:     {data_list[1]["retweet_count"]}
        Quote Tweets: {data_list[1]["quote_count"]}

        For tweet {id_list[2]}:
        Text: {json_obj["data"][2]["text"]}
        Likes:        {data_list[2]["like_count"]}
        Replies:      {data_list[2]["reply_count"]}
        Retweets:     {data_list[2]["retweet_count"]}
        Quote Tweets: {data_list[2]["quote_count"]}

        For tweet {id_list[3]}:
        Text: {json_obj["data"][3]["text"]}
        Likes:        {data_list[3]["like_count"]}
        Replies:      {data_list[3]["reply_count"]}
        Retweets:     {data_list[3]["retweet_count"]}
        Quote Tweets: {data_list[3]["quote_count"]}

        For tweet {id_list[4]}:
        Text: {json_obj["data"][4]["text"]}
        Likes:        {data_list[4]["like_count"]}
        Replies:      {data_list[4]["reply_count"]}
        Retweets:     {data_list[4]["retweet_count"]}
        Quote Tweets: {data_list[4]["quote_count"]}

        For tweet {id_list[5]}:
        Text: {json_obj["data"][5]["text"]}
        Likes:        {data_list[5]["like_count"]}
        Replies:      {data_list[5]["reply_count"]}
        Retweets:     {data_list[5]["retweet_count"]}
        Quote Tweets: {data_list[5]["quote_count"]}

        For tweet {id_list[6]}:
        Text: {json_obj["data"][6]["text"]}
        Likes:        {data_list[6]["like_count"]}
        Replies:      {data_list[6]["reply_count"]}
        Retweets:     {data_list[6]["retweet_count"]}
        Quote Tweets: {data_list[6]["quote_count"]}

        For tweet {id_list[7]}:
        Text: {json_obj["data"][7]["text"]}
        Likes:        {data_list[7]["like_count"]}
        Replies:      {data_list[7]["reply_count"]}
        Retweets:     {data_list[7]["retweet_count"]}
        Quote Tweets: {data_list[7]["quote_count"]}

        For tweet {id_list[8]}:
        Text: {json_obj["data"][8]["text"]}
        Likes:        {data_list[8]["like_count"]}
        Replies:      {data_list[8]["reply_count"]}
        Retweets:     {data_list[8]["retweet_count"]}
        Quote Tweets: {data_list[8]["quote_count"]}

        For tweet {id_list[9]}:
        Text: {json_obj["data"][9]["text"]}
        Likes:        {data_list[9]["like_count"]}
        Replies:      {data_list[9]["reply_count"]}
        Retweets:     {data_list[9]["retweet_count"]}
        Quote Tweets: {data_list[9]["quote_count"]}
        """
    )


# main function
def main():
    # get the username to retreive tweets from
    user = input("What is your Twitter username? > ")

    # create the url
    initial_tweets_url = create_first_url(user)

    # connect to an endpoint
    json_response = connect_to_endpoint(initial_tweets_url)

    # get a list of the relevant tweet IDs
    tweet_ids = []
    for tweet in json_response["data"]:
        tweet_ids.append(tweet["id"])

    # get each tweet's corresponding public data
    tweet_data_url = create_second_url(tweet_ids)

    # connect to an endpoint for a second time
    json_response_2 = connect_to_endpoint(tweet_data_url)

    # grab the public metrics from each tweet and put them in a list
    public_data = []
    for tweet in json_response_2["data"]:
        public_data.append(tweet["public_metrics"])

    # format and make it all look pretty
    make_it_pretty(user, public_data, tweet_ids, json_response_2)

if __name__ == "__main__":
    main()
