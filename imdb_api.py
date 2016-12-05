#
#install IMDbPY with: sudo apt-get install python-imdbpy
#also make sure you have regex
#

from datetime import datetime
import re
import pandas as pd
from imdb import IMDb
import random

ia = IMDb()


MOVIE_LST = [
'Star Wars: The Force Awakens',
'Jurassic World',
'Avengers: Age of Ultron',
'Inside Out',
'Furious 7',
'Minions',
'The Hunger Games: Mockingjay - Part 2',
'The Martian',
'Spectre',
'Mision: Impossible - Rogue Nation',
'Pitch Perfect 2',
'The Revenant',
'Ant-Man',
'Fifty Shades of Grey',
'The Spongebob Movie: Sponge Out of Water',
'Straight Outta Compton',
'San Andreas',
'Mad Max: Fury Road',
'Kingsman: The Secret Service',
'Get Hard',
'Terminator: Genisys',
'Taken 3',
'Ted 2',
'Pixels',
'Rock The Kasbah',
'The Gunman',
'Blackhat',
'Unfinished Business',
'Jem & The Holograms',
'Self/Less',
'American Ultra',
'We Are Your Friends',
'Aloha',
'Mortdecai',
'Child 44',
'Hot Tub Time Machine 2',
'In the Heart of the Sea',
'Our Brand Is Crisis',
'Pan',
'Steve Jobs',
'Strange Magic',
'Victor Frankenstein',
'Jupiter Ascending',
'Gods of Egypt',
"Legends of Oz: Dorothy's Return",
'The Finest Hours',
'Ben-Hur',
'47 Ronin',
'R.I.P.D.',
]

def get_data(title,data_table):
	mlst = ia.search_movie(title)

	#search for the film
	mlst.reverse()
	search = True
	while(search):
		if len(mlst) == 0:
			break
		movie = mlst.pop()
		print movie
		if movie['year'] >= 2013 and movie['kind']=='movie':
			search=False

	#could not find film
	if search:
		print "Cannot find film {}".format(title)
		return None

	#if we find it, pull more info
	ia.update(movie)
	ia.update(movie, 'business')
	ia.update(movie, 'release dates')
	#print sorted(movie.keys())
	biz = movie['business']

	#get budget
	if not 'budget' in biz:
		print "Could not find Budget for film {}".format(movie['title'])
		bud = None
	else:
		bud = biz['budget']
		bud = bud[0].replace(',', '')
		bud = int(re.findall('\d+', bud)[0])

	#get domestic gross
	if not 'gross' in biz:
		print "Could not find Budget for film {}".format(movie['title'])
		gross = None

	else:
		gross = [i for i in biz['gross'] if '(USA)' in i]
		gross.reverse()
		gross = gross.pop()
		gross = gross.replace(',', '')
		gross = int(re.findall('\d+', gross)[0])

	# print some datas
	print "Title: {} Gross: {}".format(movie['title'],gross)

	#get opening weekend data
	if not 'weekend gross' in biz:
		print "Could not find weekend gross for film {}".format(movie['title'])
		op_wkd = None
		screens = None
		op_per_scr = None
		mx_scr = None
	else:
		op_wkd = biz['weekend gross'][-1]
		op_wkd = op_wkd.replace(',', '')
		op_wkd, foo, foo1, screens = [int(i) for i in re.findall('\d+', op_wkd)]
		op_per_scr = op_wkd / screens
		mx_scr = 0
		for item in biz['weekend gross']:
			scr = int(re.findall('\d+',item)[-1])
			if scr > mx_scr:
				mx_scr = scr

	dates = movie['release dates']
	#print dates
	for date in dates:
		if 'USA' in date and '(' not in date:
			#print date
			date = date.split('::')
			date = datetime.strptime(date[1], '%d %B %Y')
			break

	if not 'production companies' in movie.data.keys():
		print "No production company info for film {}".format(movie['title'])
		prd = None
	else:
		prd = movie.get('production companies')[0]['name']

	if 'mpaa' not in movie.keys():
		print "Could not find mpaa info for film {}".format(movie['title'])
		mpaa = None
	else:
		mpaa = movie.get('mpaa').split(' ')[1]

	rt = int(re.findall('\d+', movie.get('runtime')[0])[0])
	genres = ', '.join(movie.get('genres'))

	print mpaa
	print rt
	data = {}
	data['title'] = title
	data['domestic gross'] = gross
	data['budget'] = bud
	data['opening weekend'] = op_wkd
	data['theaters'] = screens
	data['opening/theater'] = op_per_scr
	data['genres'] = genres
	data['rating'] = movie.get('rating')
	data['date'] = date
	data['production company'] = prd
	data['max number theaters'] = mx_scr
	data['mpaa'] = mpaa
	data['runtime'] = rt

	data_table.Genre = data_table.Genre.astype('str')
	data_table.MPAA = data_table.MPAA.astype('str')
	data_table.set_value(title, 'MPAA', mpaa)
	data_table.set_value(title, 'Runtime', rt)
	data_table.set_value(title,'Genre',genres)
	data_table.set_value(title,'IMDB Rating',data['rating'])
	#date = date.split(' ')[-2]
	#print date
	#data_table.Date = data_table.Date.astype('str')
	data_table.set_value(title,'Date',date)
	data_table.Distributor = data_table.Distributor.astype('str')
	data_table.set_value(title,'Distributor',prd)
	data_table.set_value(title,'Domestic Gross',gross)
	data_table.set_value(title,'Budget',bud)
	data_table.set_value(title,'Opening Gross',op_wkd)
	data_table.set_value(title,'Theaters',screens)
	data_table.set_value(title,'Opening/Theatre',op_per_scr)
	data_table.set_value(title,'Max Number Theaters',mx_scr)
	return data_table


def main():
	data_lst=[]
	data_table = pd.read_csv("data_output.csv",index_col=0)
	movie_lst = data_table.index
	#movie_lst = MOVIE_LST
	for movie in movie_lst:
		data_table = get_data(movie,data_table)
		#data_lst.append(get_data(movie))
	#print data_lst

	data_table.to_csv("data_output.csv",encoding = 'utf-8')

if __name__ == "__main__":
	main()
