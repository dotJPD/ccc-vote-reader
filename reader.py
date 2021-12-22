# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
import re
import googleapiclient.discovery

def getVotes(video_id):
    # users_to_votes is a dictionary mapping user IDs to the vote they made.
    # I might want to turn this into a list later down the road since it isn't needed
    # to handle duplicates like it was in my first implementation
    users_to_votes = {}

    # candidates is a String->Int dictionary. Keys are in the format [x], where x is any letter,
    # so a set of our keys in candidates could be [A], [B], and [C]. This stores the critical
    # information for this program, since we want to know who got how many votes.
    candidates = {}

    # page_token represents the ID of the page we're loading up, since Youtube's API doesn't let us just
    # load all the comments in one go. We have to go in batches of 100. Every batch we load tells us the
    # ID of the next page of comments, so we update this with each batch until we reach the last page.
    page_token = None

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "devkeyhere"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    # Getting the raw data in the form of a dictionary from the API. video_id is whatever the video ID the user gave us is
    # The highest number we can put in maxResults is 100, so I set it to that instead of loading the default 20 comments per call
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100
    )
    response = request.execute()

    # If the video overall has <= 100 comments, page_token will still be None.
    # This works with the while loop since page_token is set to None when we're
    # at the end there, too
    if 'nextPageToken' in response:
        page_token = response['nextPageToken']

    # I could say "while response" but this is more readable imo
    # Have to do this in a loop because youtube API only lets you load up to 100 comments at a time
    while response is not None:

        # indiv_item represents an individual top-level comment
        for indiv_item in response['items']:
            
            # comment_text is the original text of the comment that we'll process
            # I don't know why the data has so many layers of keys lmao what a mess 
            comment_text = indiv_item['snippet']['topLevelComment']['snippet']['textOriginal']

            # user is the ID of the user who made this comment. This helps us deal with duplicates
            user = indiv_item['snippet']['topLevelComment']['snippet']['authorChannelId']['value']

            # This finds every match of string in the format "[x]" where x is any letter
            vote = re.findall("\[[a-zA-Z]\]", comment_text)

            # If there are no votes in the comment we can just do nothing this iteration.
            # If the comment does have a vote, we'll retrieve it. If there are multiple votes, we'll
            # just take the last vote in the comment
            if len(vote) > 0:
                vote = vote[-1].upper()

                # If this candidate hasn't had a vote yet, we start it off at 0
                if vote not in candidates:
                    candidates[vote] = 0
                # If this user has not already voted we add their vote to the system.
                # If they have already voted, we can safely ignore it. If they changed
                # their mind, we already got their updated vote since this is reading comments
                # in newest to oldest
                if user not in users_to_votes:
                    users_to_votes[user] = vote
                    candidates[vote] += 1
        
        # If we have a next page to go to, load up the next page. If there is no next
        # page, page_token will just be None
        if page_token is not None:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken = page_token
            )

            response = request.execute()

            # If we have a token for the next page, set up page_token to be that
            if 'nextPageToken' in response: 
                page_token = response['nextPageToken']
            # If we don't that means we've loaded up our last page and can set
            # page_token to None. The next loop iteration will process that last page
            # and end the loop
            else:
                page_token = None

        # If page_token is None, that means we've just read the last page of votes and can exit
        # the loop.
        else:
            response = None

    return candidates

if __name__ == "__main__":
    # Getting the video ID through user input so the code doesn't have to be changed
    # for every new video
    video_id = input("Enter the video ID (the part after \"watch?v=\"): ")
    all_votes = getVotes(video_id)

    # Printing out all the vote results in alphabetical order
    for candidate in sorted(all_votes):
        print(candidate + " got " + str(all_votes[candidate]) + " votes")