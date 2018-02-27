import matplotlib.pyplot as plot;
import numpy as np
import urllib.request
from bs4 import BeautifulSoup
import re
import argparse

plot.rcdefaults()

url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
maxCount = 10

parser = argparse.ArgumentParser()
parser.add_argument("url", help="Add a url to scrape the text from.")
parser.add_argument("max", help="The amount of words you want on the bar chart e.g 10.")
args = parser.parse_args()
url = args.url
maxCount = int(args.max) 

commonDictionary = set()

with open('10k.txt','r') as f:
    for line in f:
        for word in line.split():
         	commonDictionary.add(word)

html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

for script in soup(["script", "style"]):
    script.extract()

text = soup.get_text()

lines = (line.strip() for line in text.splitlines())
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
text = '\n'.join(chunk for chunk in chunks if chunk)

dictionary = {}

for word in text.split():
	
	cleanWord = re.sub("[^a-zA-Z]","", word.lower())

	if(cleanWord is not "" and cleanWord not in commonDictionary):
    
		if(cleanWord in dictionary):
			x = dictionary[cleanWord]
			x = x + 1
			dictionary[cleanWord] = x
		else:
			dictionary[cleanWord] = 1

words = []
figures = []

count = 0

for w in sorted(dictionary, key=dictionary.get, reverse=True):
  if(count is maxCount):
  	break
  else:
  	words.append(w)
  	figures.append(dictionary[w])
  	count = count + 1

yPos = np.arange(len(words))
 
plot.bar(yPos, figures, align='center', alpha=0.5)
plot.xticks(yPos, words)
plot.ylabel('Word Count')
plot.title('Top 10 Words from ' + url) 
plot.show()