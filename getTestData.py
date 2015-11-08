from subprocess import call
from threading import Thread

def getTweets(movieName, rating):
	outFileName = "testTweets/{}.txt".format(movieName+rating)
	query = "\\\"{}\\\" movie".format(movieName)
	call(["java", "-jar", "GetTweets-1.0-SNAPSHOT-jar-with-dependencies.jar", "querysearch={}".format(query), "maxtweets=3000", outFileName])

def readList():
	threadList = []
	with open('list.txt','r') as f:
		for line in f:
			words = line.split()
			if len(words) == 0:
					break;
			movieName = " ".join(words[0:len(words)-1])
			rating = words[len(words)-1]
			t = Thread(target=getTweets, args=(movieName, rating))
			threadList.append(t)
			t.start()
			print "start {}".format(words[0])
	for item in threadList:
		item.join()
	print "finish"


if __name__ == '__main__':
	readList()
	