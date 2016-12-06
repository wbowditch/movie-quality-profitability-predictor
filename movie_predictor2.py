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