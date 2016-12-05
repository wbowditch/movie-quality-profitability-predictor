#Will Bowditch
import praw
import blockspring
import json
import requests
import pandas as pd
import wikipedia
from wikitables import import_tables

#tables = import_tables('List of American films of 2015')

#movies2015 = tables[0]
data_table = pd.read_csv("data_set.csv",index_col=0)
film_titles = data_table.index  # list of all of our movie titles in the dataset.

#output = pd.DataFrame(columns =["Title","Sentiment","Upvotes","Comments"])
def aggregate_analysis(movie_name):
    #print movie_name
    r = praw.Reddit(user_agent='wpb')
    #submission = r.get_submission(submission_id=id)
    #print help(r.search)
    obj = r.search(movie_name + " Trailer flair:'Trailer' ",subreddit="movies")
    #print obj
    try:
        submission = obj.next()
        print submission.title
    except StopIteration:
        return
    ratio = r.get_submission(submission.permalink).upvote_ratio

    #print dict(submission)
    #print help(submission)

    comments = submission.comments
    #print submission.get_json()
    #print submission.title,submission.ups,submission.score
    #ratio = submission.upvote_ratio
    # pos_bvs = 0
    # neg_bvs = 0
    # #print submission.title,submission.ups, submission.ratio
    # for comment in comments:
    #     try:
    #         if(type(comment)== praw.objects.MoreComments):
    #             break
    #         r = requests.post('http://sentiment.vivekn.com/api/text/',data = {"txt":comment.body })
    #         confidence = r.json()["result"]["confidence"]
    #         opinion = r.json()["result"]["sentiment"]
    #         #print opinion, comment.body
    #         if opinion == "Positive": pos_bvs+=1

    #         if opinion == "Negative" and float(confidence)> 90: neg_bvs+=1
    #     except UnicodeEncodeError:
    #         continue
    flat_comments = praw.helpers.flatten_tree(submission.comments)
    #val = pos_bvs*1.0/(pos_bvs+neg_bvs)
    #print movie_name, ratio
    #data_table.set_value(movie_name,"Reddit Sentiment",val)
    data_table.set_value(movie_name,"Reddit Comments",len(flat_comments))
    data_table.set_value(movie_name,"Reddit UpVotes",submission.ups)
    data_table.set_value(movie_name,"Reddit Ratio",ratio)
    #return {"Title":movie_name,"Sentiment":val,"Upvotes":submission.ups,"Comments":len(flat_comments)} #'+"~"+val+"~"+str(submission.ups)+"~"+comments_count+"~"+ratio

#file = open("sentiment_ups_comments_ratio.txt", "w")
#file2 = open("2015movies.txt","r")
#index = 0
#print film_titles
for title in film_titles:
        print title
        #title = str(row["Opening"])
        #print type(title), title
        aggregate_analysis(title.strip())
        #print index
        #index+=1

        #print sentiment
        #output.loc[title] = sentiment
        #print output
        #index+=1
        #output.append(sentiment)
       # file.write(sentiment)
        #file.write("\n")
#print output
data_table.to_csv("csv_output.csv", encoding='utf-8')
#file.close()



# print "Suicide Squad", aggregate_analysis("Suicide Squad")
# print "Star Wars", aggregate_analysis("Star Wars")
# print "Batman v Superman", aggregate_analysis("Batman v Superman")
# print "Mad Max", aggregate_analysis("Mad Max")
# print "Jupiter Ascending", aggregate_analysis("Jupiter Ascending")
# print "Finding Dory", aggregate_analysis("Finding Dory")

# pos_bvs = 0
# neg_bvs = 0
# for comment in bvs_comments:
#     if(type(comment)== praw.objects.MoreComments):
#         break
#     r = requests.post('http://sentiment.vivekn.com/api/text/',data = {"txt":comment.body })
#     opinion = r.json()["result"]["sentiment"]
#     if opinion == "Positive": pos_bvs+=1
#     if opinion == "Negative": neg_bvs+=1

# print "B v S Aggregated", pos_bvs*1.0/(pos_bvs+neg_bvs)


# pos_sw = 0
# neg_sw = 0
# for comment in sw_comments:
#     if(type(comment)== praw.objects.MoreComments):
#         break
#     r = requests.post('http://sentiment.vivekn.com/api/text/',data = {"txt":comment.body })
#     opinion = r.json()["result"]["sentiment"]
#     if opinion == "Positive": pos_sw+=1
#     if opinion == "Negative": neg_sw+=1

# print "SW Aggregated", pos_sw*1.0/(pos_sw+neg_sw)

    #print r.json()["result"]["sentiment"]
# for comment in submission.comments:
#     print
#     print comment.body
#     print

#print flat_comments[0].body
# for obj in dir(flat_comments[0]):
#     print obj

#print comments[0]
#print starwars_comments

# for comment in starwars_comments:
#     print
#     print comment
#     print