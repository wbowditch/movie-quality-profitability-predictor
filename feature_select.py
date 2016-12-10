from sklearn import svm
import pandas as pd
import optunity
import optunity.metrics
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import SelectKBest, chi2, f_classif


def compute_cross_fold(data, target):
     data_table = pd.read_csv("total_set.csv",index_col=0)

     scaler = preprocessing.StandardScaler().fit(data)
     data_scaled = scaler.transform(data)

     #clf_profit = svm.SVC(kernel='rbf',C=0.8, gamma=5,verbose=True)
     clf_profit = svm.LinearSVC(C=0.001,verbose=True,tol=.1)
     clf_profit.fit(data_scaled, target)
     scores = cross_val_score(clf_profit, data_scaled, target, cv=10)

     #print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
     return (scores.mean(), scores.std() * 2)

def main():
     data_table = pd.read_csv("total_set.csv",index_col=0)
     film_titles = data_table.index  # list of all of our movie titles in the dataset.
     #print film_titles
     lst = [   'Sequel',
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
               ]

     data = data_table[lst]
     target = data_table['Profitable']

     print data.shape
     data_new = SelectKBest(f_classif, k=10).fit_transform(data, target)
     print data_new.shape

     no_select=compute_cross_fold(data, target)
     with_select=compute_cross_fold(data_new, target)

     print no_select
     print with_select


"""
     error_lst = []
     for item in lst:
          data = data_table[[i for i in lst if i != item]]
          error_lst.append(compute_cross_fold(data)[0])

     data = data_table[lst]
     all_par=compute_cross_fold(data)
     zpd = [('All', all_par[0])] + zip(lst, error_lst)
     print zpd

     plt.scatter(range(len(lst)+1), [all_par[0]]+error_lst)
     plt.show()
     """

main()
