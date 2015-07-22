#!/usr/bin/env python
import webbrowser
import os
from string import Template

movie_tile_template = '''
<div class="col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="${trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <img src="${poster_image_url}" width="220" height="342">
    <h2>${movie_title}</h2>
</div>
'''


# We are using urlparse instead of re to find out youtube id
try:
	import urlparse # python >2.6
except ImportError:
	from urllib.parse import urlparse #python >3.0	

def get_youtube_id(url):
	''' Parse youtube url (http://www.youtube.com/watch?v=ID) and return the ID'''
	query = urlparse.urlparse(url).query
	try:
		youtube_id = urlparse.parse_qs(query)['v'][0]
	except KeyError:
		youtube_id = None
		
	return youtube_id


class Movie():
	''' A movie with default properties. '''

	title = "No title"
	trailer_youtube_url = "about:blank"
	poster_image = "default_poster.gif"
	
	def __init__(self, **entries):
		self.__dict__.update(entries) # An elegant way to set the object variables
		
	def html(self):
		placeholders = {
			'trailer_youtube_id': get_youtube_id(self.trailer_youtube_url),
			'movie_title':self.title,
			'poster_image_url': self.poster_image,
			}
		template = Template(movie_tile_template)
		return template.safe_substitute(placeholders)


# A better way is to use json or yaml to store the data, but to simplify things we just create a list of python dictionaries.
movie_data = [
	{
		'title': "Zombies",
		'trailer_url': "http://sdaff",
		'poster_image': "poster1.gif",
	},
	{
		'title': "Fight Club",
		'trailer_youtube_url': "http://www.youtube.com/watch?v=J8FRBYOFu2w",
	},
]


# Create a list of Movie objects in cycle
movies = []

for idx, md in enumerate(movie_data):
	try:
		movies.append( Movie(**md) ) # '**' unpacks dictionary into keyword arguments
		
	except TypeError:
		raise ValueError("Movie data item #%d is not a dictionary: %s given."	% (idx, type(md)) )
	
	
for m in movies:
	print(m.html())
