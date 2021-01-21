from bs4 import BeautifulSoup
import json
import requests
import csv
'''
I'M NOT FAMILIAR WITH PANDAS SO THE WAY I TRIED TO DO THIS TASK IS PRETTY STRAIGHTFORWARD
'''

if __name__ == '__main__':

    # creating list to store every movie as a dict
    all_movies = []
    # opening local html file to use BeatifulSoap
    with open('imdb_most_popular_movies_dump.html', encoding='utf-8') as html_file:
        soaped_info = BeautifulSoup(html_file, features='html.parser')
    # a loop finding every td-field with class attr titleColumn
    for row in soaped_info.find_all('td',  attrs={'class':'titleColumn'}):
        #creating variables which contains parsed data from html page
        title_html = row.a.text
        year_html = row.span.text
        velocity_html = row.div.text
        velocity_html = ''.join(velocity_html.split())
        #creating dict with parsed values
        movie = {
            'title': title_html,
            'year': year_html,
            'velocity': velocity_html,
        }
        #append every dict to the list
        all_movies.append(movie)

    #emty str variable which will be used to edit omdapi base link
    name = ''
    #loop in which i will get all inforamtion about every film parsed from html file
    # and stored insid list of dicts var (all_movies)
    for elem in all_movies:
        #replcaing spaces in title with "+"  to use it in the url
        name = elem['title'].replace(' ','+')
        base_url = f'http://www.omdbapi.com/?t={name}&apikey=9e810e39'
        response = requests.get(base_url)
        #converting string into dict to access jason data from omdb
        dict_values = json.loads(response.text)
        #loop for updating var (all_movies) by adding information from omdbapi
        for value in dict_values.keys():
            elem[f'{value}'] = dict_values[f'{value}']

    # straightforward way for creating columns in final csv file
    csv_columns = [ 'title', 'year', 'velocity', 'Country', 'Language', 'Website', 'imdbVotes', 'Ratings', 'Production',
                    'Type', 'Plot', 'Year', 'Poster', 'Title', 'imdbRating', 'imdbID', 'Writer', 'Runtime', 'Metascore',
                    'DVD', 'Rated', 'Released', 'Actors', 'Genre', 'Awards', 'Director', 'BoxOffice', 'Response',
                    'totalSeasons']

    csv_file = "movies.csv"
    #openning cav file
    with open(csv_file, 'w', encoding='utf-8') as file:
        #converting data from var(all_movies) into table
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(all_movies)


