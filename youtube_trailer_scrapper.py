#Willl Bowditch
#Updates views, likes and dislikes on the movie data set.
#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd

DEVELOPER_KEY = "INSERT_KEY_HERE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def update_movie_data():
    data_table = pd.read_csv("data_set.csv",index_col=0)
    film_titles = data_table.index  # list of all of our movie titles in the dataset.



    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
    for title in film_titles:
        video_search = youtube.search().list(
            q=title+" trailer",
            part="id",
            maxResults=1, #only want one result
            type="video" #and we want that one result to be a video, not a channel.
          ).execute().get("items", [])[0]


        id1 = video_search["id"]["videoId"]  #grab the id of the video

        video_result = youtube.videos().list(
            id=id1,
            part='snippet, statistics'
          ).execute().get("items", [])[0]

        print "%s, %s (%s,%s)" % (video_result["snippet"]["title"],
                         video_result["statistics"]["viewCount"],
                         video_result["statistics"]["likeCount"],
                         video_result["statistics"]["dislikeCount"])

        data_table.set_value(title,'YouTube Trailer Views',video_result["statistics"]["viewCount"])
        data_table.set_value(title,'YouTube Like',video_result["statistics"]["likeCount"])
        data_table.set_value(title,'YouTube Dislike',video_result["statistics"]["dislikeCount"])

    data_table.to_csv("csv_output", encoding='utf-8')





if __name__ == "__main__":
  try:
    update_movie_data()
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
