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

    def getClassifiers(self):
        return [self.imdb_rating,self.profitability]



data_table = pd.read_csv("data_set.csv",index_col=0)
film_titles = data_table.index  # list of all of our movie titles in the dataset.

data =


