import urllib2
import urllib
from HTMLParser import HTMLParser
import sys
import re

if len(sys.argv) != 2:
    print("Usage: python getMovie.py [num_of_movies]")
    exit(1)
baseUrl = "http://www.imdb.com/search/title?title_type=feature&count=100&view=simple"
outputFile = open('movieList.txt', 'w+')
numMovies = int(sys.argv[1])


class MyHTMLParser(HTMLParser):
    def __init__(self, score, outputFile, numMoviesToRead):
        HTMLParser.__init__(self)
        self.flag = False
        self.numMoviesPrinted = 0
        self.score = score
        self.parser = re.compile("/title/*", re.IGNORECASE)
        self.outputFile = outputFile
        self.numMoviesToRead = numMoviesToRead

    def handle_starttag(self, tag, attrs):
        if tag == 'a' and self.numMoviesPrinted < self.numMoviesToRead:
            for k, v in attrs:
                if k == 'href' and self.parser.match(v) and len(attrs) == 1:
                    self.flag = True
                    self.numMoviesPrinted += 1

    def handle_data(self, data):
        if self.flag is True:
            title = data
            outputFile.write(title + '\t' + str(score) + '\n')
            self.flag = False


for score in range(2, 10):
    scoreLowerBound = score - 0.5
    scoreUpperBound = score + 0.4
    numMoviesToRead = numMovies

    # We can only get 100 movies for each request so we need to do it multiple times
    for i in range(1 + numMovies / 100):
        queryParameters = {'user_rating': str(scoreLowerBound) + ',' + str(scoreUpperBound),
                           'start': i * 100 + 1}
        url = baseUrl + '&' + urllib.urlencode(queryParameters)
        rawHTML = urllib2.urlopen(url).read()
        htmlParser = MyHTMLParser(score, outputFile, numMoviesToRead)
        htmlParser.feed(rawHTML)
        numMoviesToRead -= 100

outputFile.close()
