#This is an article content extraction script for the New York Times
#
#Steven Large
#October 25th 2018

from urllib import urlopen
import numpy as np
import os
#import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import re

def GetArticleContent(soup_Article):
	pass

def WriteArticleText(WritePath,WriteName,Content):
	pass

def GetArticleURLs(soup_Directory):
	
	ArticleSections = soup_Directory.findAll("h2",{"class":"css-l2vidh e4e4i5l1"})
	ArticleURLs = []
	for index in range(len(ArticleSections)):
		ArticleURLs.append("https://www.nytimes.com" + ArticleSections[index].find("a").get("href").encode("UTF-8"))

	return ArticleURLs

def UpdateDictionary(ReadPath,DictName,ArticleURLs):
	pass

def WriteHTMLCode_Pretty(Path,Filename,soup):
	CompleteName = os.path.join(Path,Filename)
	file1 = open(CompleteName,'w')
	file1.write(str(soup.prettify().encode("UTF-8")))
	file1.close()

def WriteHTMLCode(Path,Filename,soup):
	CompleteName = os.path.join(Path,Filename)
	file1 = open(CompleteName,'w')
	file1.write(str(soup))
	file1.close()


MainPage_NYT = "https://www.nytimes.com"
Politics_NYT = "/section/politics"

htmlCode_Politics = urlopen(MainPage_NYT + Politics_NYT)
soup_Politics = BeautifulSoup(htmlCode_Politics,'html.parser')




