#!/usr/bin/env python
import webbrowser
import os
from string import Template

# We are using `urlparse` instead of `re` to find out youtube id.
try:
	import urlparse # python >2.6
except ImportError:
	import urllib.parse as urlparse #python >3.0	


output_filename = 'movies.html'


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
	trailer_youtube_url = "None"
	poster_image = "no_poster.png"
	release_year = ""
	category = ""
	
	def __init__(self, **entries):
		self.__dict__.update(entries) # An elegant way to set the object variables
		
	def html(self):
		''' Generate html code '''
		movie_tile_template = """
			<div class="col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="${trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
				<img src="${poster_image_url}" width="220" height="342" class="movie-poster">
				<h2>${movie_title} <span class="movie-category">${category}</span></h2>
				<p><strong>${release_year}</strong></p>
			</div>
			"""
		
		placeholders = {
			'trailer_youtube_id': get_youtube_id(self.trailer_youtube_url),
			'movie_title': self.title,
			'poster_image_url': self.poster_image,
			'release_year': self.release_year,
			'category': self.category,
			}
		template = Template(movie_tile_template)
		return template.safe_substitute(placeholders)


# A better way is to use json or yaml to store the data, but to simplify things we just create a list of python dictionaries.
movie_data = [
	{
		'title': "Fight Club",
		'trailer_youtube_url': "http://www.youtube.com/watch?v=J8FRBYOFu2w",
		'poster_image': "https://www.movieposter.com/posters/archive/main/4/MPW-2244",
		'release_year': " 15 October 1999",
		'category': 'R',
	},
	{
		'title': "Run Lola Run",
		'trailer_youtube_url': "http://www.youtube.com/watch?v=3ea0mG4ahRk",
		'poster_image': "https://www.movieposter.com/posters/archive/main/12/A70-6235",
		'release_year': "1998",
		'category': 'R',
	},
	{
		'title': "Leon: The Professional",
		'trailer_youtube_url': "http://www.youtube.com/watch?v=DcsirofJrlM",
		'poster_image': "https://www.movieposter.com/posters/archive/main/8/A70-4120",
		'category': 'R',
	},
	{
		'title': "The Shawshank Redemption",
		'trailer_youtube_url': "http://www.youtube.com/watch?v=6hB3S9bIaco",
		'poster_image': "https://www.movieposter.com/posters/archive/main/42/MPW-21321",
		'release_year': "1994",
	},
	{
		'title': "Forrest Gump",
		'trailer_youtube_url': "http://www.youtube.com/watch?v=uPIEn0M8su0",
		'poster_image': "https://www.movieposter.com/posters/archive/main/38/MPW-19355",
		'release_year': "6 July 1994",
		'category': 'PG-13',
	},
]


# Create a list of Movie objects in cycle
movies = []

for idx, md in enumerate(movie_data):
	try:
		movies.append( Movie(**md) ) # '**' unpacks dictionary into keyword arguments
		
	except TypeError:
		raise ValueError("Movie data item #%d is not a dictionary: %s given."	% (idx, type(md)) )
	

def generate_movies_page(movies):
	''' Generate a movies webpage file.'''
	
	with open(output_filename,'w') as output_file, \
		 open('main.tpl', 'r') as template_file, \
		 open('head.htm', 'r') as header_file:
		
		template = Template(template_file.read())
		tiles_html = '\n'.join( [m.html() for m in movies])
		head_html = header_file.read()
		
		content = template.substitute(movie_tiles=tiles_html, head=head_html)  #fill page template with contents
		output_file.write(content)
		
		
def open_movies_page():
	''' Show a browser window with movies webpage.'''
	generate_movies_page(movies)
	url = os.path.abspath(output_filename)
	webbrowser.open('file://' + url, new=2) # open in a new tab, if possible

open_movies_page()	

