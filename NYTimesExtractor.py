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

def CheckDirStructure(htmlPath,WritePath):
	html_basePath = htmlPath.replace("/"," ").split() 			#Spilt directories into their indifivual folder paths

	write_basePath = WritePath.replace("/"," ").split() 		#Again

	if(os.path.exists(html_basePath[0])==False): 				#Check if outer directory exists, if not then make it
		os.mkdir(html_basePath[0])
	os.chdir(html_basePath[0])									#Navigate into to outer directory
	if(os.path.exists(html_basePath[1])==False): 				#Check if inner directory exists, if not then make it
		os.mkdir(html_basePath[1])
	os.chdir("..")

	if(os.path.exists(write_basePath[0])==False): 				#Same goes for the write directories
		os.mkdir(write_basePath[0])
	os.chdir(write_basePath[0])
	if(os.path.exists(write_basePath[1])==False):
		os.mkdir(write_basePath[1])
	os.chdir("..")


def GetArticleContent(soup_Article): 						
	ArticleName = soup_Article.title.text
	ArticleName = ArticleName.replace(" ","-")
	ArticleName = ArticleName.replace(".","")

	Content_Temp = soup_Article.find("section",{"itemprop":"articleBody"}).findAll("p")
	Content = []

	for index in range(len(Content_Temp)):
		Content.append(Content_Temp[index].text.encode("unicode-escape"))
		Content[index].replace("\u2019","")
		Content[index].replace("\u201c","")
		Content[index].replace("\u201d","")

	return Content,ArticleName

def WriteArticleText(WritePath,WriteName,Content):
	CompleteName = os.path.join(WritePath,WriteName)
	file1 = open(CompleteName,'w')
	for index in range(len(Content)):
		file1.write(Content[index])
	file1.close()

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
WritePath = "Articles/NYTimes/"
HTMLWritePath = "htmlCode/NYTimes/"

CheckDirStructure(WritePath,HTMLWritePath)

htmlCode_Politics = urlopen(MainPage_NYT + Politics_NYT)
soup_Politics = BeautifulSoup(htmlCode_Politics,'html.parser')
ArticleURLs = GetArticleURLs(soup_Politics)

for index in range(len(ArticleURLs)):
	htmlCode_Article = urlopen(ArticleURLs[index])
	soup_Article = BeautifulSoup(htmlCode_Article,'html.parser')
	
	#if(index<=10):
	#	print("Article name --> " + str(ArticleURLs[index]))
	#	WriteHTMLCode_Pretty(HTMLWritePath,"Article_"+str(index)+".dat",soup_Article)
	
	ArticleContent,ArticleName = GetArticleContent(soup_Article)
	WriteName = ArticleName + ".dat"
	print("WritePath --> " + WritePath)
	print("WriteName --> " + WriteName)
	WriteArticleText(WritePath,WriteName,ArticleContent)

print("\n\n\t\t-----Article content finished scraping-----\n\n")


