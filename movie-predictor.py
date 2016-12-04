#Will Bowditch, Tom O'Boyle, JP Scaduto
from sklearn import svm
import pandas as pd

class Movie:
    def __init__(self,sequel,budget,youtube_views,youtube_likes,
                youtube_dislikes,youtube_ratio,reddit_ups,reddit_ratio,
                reddit_comments,genre,release_date,star_oscar,star_rating,star_gross):
        self.sequel = sequel
        self.budget = budget
        self.youtube_views = youtube_views
        self.youtube_likes = youtube_likes
        self.youtube_dislikes = youtube_dislikes
        self.youtube_ratio = youtube_ratio
        self.reddit_ups = reddit_ups
        self.reddit_ratio =reddit_ratio
        self.reddit_comments = reddit_comments
        self.genre = genre
        self.release_date = release_date
        self.star_oscar = star_oscar
        self.star_rating = star_rating
        self.star_gross = star_gross

    def getFeatures(self):
        return [self.sequel,
                self.budget,
                self.youtube_views,
                self.youtube_likes,
                self.youtube_dislikes,
                self.youtube_ratio,
                self.reddit_ups,
                self.reddit_ratio,
                self.reddit_comments,
                self.genre,
                self.release_date,
                self.star_oscar,
                self.star_rating,
                self.star_gross]


    def addClassifiers(self,imdb_rating,profitability):
        self.imdb_rating = imdb_rating
        self.profitability = profitability

    def getRating(self):
        return [self.imdb_rating]

    def getProfitability(self):
        return [self.profitability]



data_table = pd.read_csv("data_set.csv",index_col=0)
film_titles = data_table.index  # list of all of our movie titles in the dataset.

data = data_table[['Sequel',
                    'Production Budget',
                    'YouTube Trailer Views',
                    'YouTube Likes',
                    'YouTube Dislike',
                    'YouTube Like:Dislike',
                    'YouTube Ratio',
                    'Reddit UpVotes',
                    'Reddit Ratio',
                    'Reddit Comments',
                    'Genre',
                    'Release Date',
                    'Star Oscar',
                    'Star Rating',
                    'Star Gross']]

profitability_target = data_table['Profitable']
rating_target = data_table['IMDB Rating']

clf_profit = svm.SVC()
clf_proft.fit(data,profitability_target)

clf_rating = svm.SVC()
clf_rating.fit(data,rating_target)



training_table = pd.read_csv("training_set.csv",index_col=0)

film_titles = training_table.index

training_data = training_table[['Sequel',
                    'Production Budget',
                    'YouTube Trailer Views',
                    'YouTube Likes',
                    'YouTube Dislike',
                    'YouTube Like:Dislike',
                    'YouTube Ratio',
                    'Reddit UpVotes',
                    'Reddit Ratio',
                    'Reddit Comments',
                    'Genre',
                    'Release Date',
                    'Star Oscar',
                    'Star Rating',
                    'Star Gross']]


actual_profitability = data_table['Profitable']
actual_rating = data_table['IMDB Rating']


profit_predictions = clf_profit.predict(training_data)
rating_predictions = clf_rating.predict(training_data)

for film,profit,rating,true_rating,true_profit in zip(film_titles,profit_predictions,rating_predictions,actual_rating,actual_profitability):
    print film
    print "Predicted Rating",rating, "Actual Rating", true_rating
    print "Predicted Profit",profit, "Actual Profit", true_profit
    print







