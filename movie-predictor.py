#Will Bowditch, Tom O'Boyle, JP Scaduto
from sklearn import svm
import pandas as pd
import optunity
import optunity.metrics
import matplotlib.pyplot as pyplot


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



data_table = pd.read_csv("total_set.csv",index_col=0)
film_titles = data_table.index  # list of all of our movie titles in the dataset.
#print film_titles
data = data_table[['Sequel',
                    'Budget',
                    'YouTube Trailer Views',
                    'YouTube Like',
                    'YouTube Dislike',
                    'YouTube Like:Dislike',
                    'Reddit UpVotes',
                    'Distributor',
                    'Reddit Ratio',
                    'Reddit Comments',
                    'Date',
                    'Runtime',
                    'MPAA',
                    'Comedy',
                    'Action/Adventure',
                    'Animated',
                    'Drama'
                    ]]
data_norm = (data - data.mean()) / (data.max() - data.min())

profitability_target = data_table['Profitable']
gross_target = data_table['Domestic Gross']
tomato = data_table['Rotten']


normalized_target_gross = (gross_target - gross_target.mean()) / (gross_target.max() - gross_target.min())
#tomato = (tomato - tomato.mean()) / (tomato.max() - tomato.min())


clf_profit = svm.SVC(kernel='linear',C=1000,verbose=True)
clf_profit.fit(data_norm,profitability_target)

clf_rating = svm.SVR(C=1000)
clf_rating.fit(data_norm,normalized_target_gross)

clf_tomato = svm.SVR()
clf_tomato.fit(data_norm,tomato)


print clf_profit.coef_

print "done"

#profit1 = clf_profit.predict(data)
#rating1 = clf_rating.predict(data)

# for film,profit,rating,true_rating,true_profit in zip(film_titles,profit1,rating1,rating_target,profitability_target):
#     print film
#     print "Predicted Rating",rating, "Actual Rating", true_rating
#     print "Predicted Profit",profit, "Actual Profit", true_profit
#     print

testing_table = pd.read_csv("testing_set.csv",index_col=0)

film_titles = testing_table.index
#print film_titles

testing_data = testing_table[['Sequel',
                    'Budget',
                    'YouTube Trailer Views',
                    'YouTube Like',
                    'YouTube Dislike',
                    'YouTube Like:Dislike',
                    'Reddit UpVotes',
                    'Distributor',
                    'Reddit Ratio',
                    'Reddit Comments',
                    'Date',
                    'Runtime',
                    'MPAA',
                    'Comedy',
                    'Action/Adventure',
                    'Animated',
                    'Drama'
                    ]]
testing_norm = (testing_data - testing_data.mean()) / (testing_data.max() - testing_data.min())


actual_profitability = testing_table['Profitable']
actual_growth = testing_table['Domestic Gross']
actual_tomato = testing_table['Rotten']

normalized_test_gross = (actual_growth - actual_growth.mean()) / (actual_growth.max() - actual_growth.min())
actual_tomato = (actual_tomato - actual_tomato.mean()) / (actual_tomato.max() - actual_tomato.min())


profit_predictions = clf_profit.predict(testing_norm)
growth_predictions = clf_rating.predict(testing_norm)
tomato_predictions = clf_tomato.predict(testing_norm)
#print profit_predictions

print clf_profit.score(testing_norm,actual_profitability)
print clf_rating.score(testing_norm,normalized_test_gross)
print clf_tomato.score(testing_norm,actual_tomato)

#print testing_data
#print clf_profit.score(testing_data,actual_profitability)
#print clf_rating.score(testing_data,actual_rating)
y = abs(growth_predictions-normalized_test_gross)
print y
pyplot.plot(range(len(growth_predictions)),y)
pyplot.show()
for film,profit,rating,true_rating,true_profit,tomato,actual_t in zip(film_titles,profit_predictions,growth_predictions,normalized_test_gross,actual_profitability,tomato_predictions,actual_tomato):
    print film
    print "Predicted Rating",rating, "Actual Rating", true_rating
    print "Predicted Profit",profit, "Actual Profit", true_profit
    print "Predicted Tomato",tomato, "Actual Tomato",actual_t