#!/usr/bin/env python

# This script extracts the 250 top movies from IMDb, process
# and insert each of them as a document in a mongo database.
import imdb
from humbledb import Mongo, Document

class MovieDoc(Document):
    config_database = 'emdb'
    config_collection = 'movies'

def _nameAndRole(personList, joiner=u', '):
    nl = []
    for person in personList:
        n = person.get('name', u'')
        if person.currentRole: n += u' (%s)' % person.currentRole
        nl.append(n)
    return joiner.join(nl)

# Access channel
ia = imdb.IMDb()
print 'Connecting to IMDb...'

print 'Retrieving information about movies, this might take a while'
# Get the full information of each movie
top250 = ia.get_top250_movies()
i = 0
for movie in top250:
    i = i + 1
    ia.update(movie)

    values = MovieDoc()
    values['Title'] = movie['long imdb canonical title']
    values['Genres'] = ', '.join(movie['genres'])
    values['Director'] = _nameAndRole(movie['director'])
    movie['cast'] = movie['cast'][:5]
    values['Cast'] = _nameAndRole(movie['cast'])
    values['Runtime'] = ', '.join(movie['runtime'])
    values['Country'] = ', '.join(movie['country'])
    if i != 156:
        values['Language'] = ', '.join(movie['language'])
    values['Rating'] = movie['rating']
    values['Plot'] = movie['plot'][0]

    with Mongo:
        MovieDoc.insert(values)

print 'Done.'
