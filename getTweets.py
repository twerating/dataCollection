from subprocess import call
from threading import Thread

def getTweets(movieName, rating):
	outFileName = "{}.txt".format(rating+movieName)
	query = "\\\"{}\\\" movie".format(movieName)
	print query
	try:
		call(["java", "-jar", "GetTweets-1.0-SNAPSHOT-jar-with-dependencies.jar", "querysearch={}".format(query), "maxtweets=2000", outFileName])
	except:
		print 'jar problem'

def readList():
	# threadList = []
	with open('list.txt','r') as f:
		threadList = []
		for line in f:
			words = line.split()
			if len(words) == 0:
					break;
			movieName = " ".join(words[0:len(words)-1])

			rating = words[len(words)-1]
			print rating
			t = Thread(target=getTweets, args=(movieName, rating))
			threadList.append(t)
			t.start()
			if len(threadList) >= 15:
				print "waiting for workers"
				for t in threadList:
					t.join()
				threadList = []
			print "start {}".format(movieName)
	
	if len(threadList) > 0:
		for t in threadList:
			t.join()

	print "finish"


if __name__ == '__main__':
	readList()
	