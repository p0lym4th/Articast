#This is an article extractor for the Quillette web page
#
#Steven Large
#August 15ht 2018

from urllib import urlopen
import numpy as np
import matplotlib.pyplot as plt
import os
from bs4 import BeautifulSoup
	

def GetArticleContent(soup_Article):

	Content = []
	Paragraphs = soup_Article.find_all('p')
	Condition = -1

	for index in range(len(Paragraphs)):
		#if(Paragraphs[index]==u'\xa0'):
		if(Paragraphs[index].text.encode("UTF-8") == '\xc2\xa0'):
			Condition = index
			break

	if Condition==-1:
		print("\n\nSorry, the parsing routine cannot locate the end-of-article signature\n\n")
		print("\t\t\t---> " + str(soup_Article.title.text) + "\n\n")
		Content.append("Error")
	else:
		for index in range(Condition):
			if(Paragraphs[index].img==None):
				Content.append(Paragraphs[index].text)

	return Content

def WriteArticleText(Path,Filename,ArticleContent):
	
	CompleteName = os.path.join(Path,Filename)
	file1 = open(CompleteName,'w')
	for index in range(len(ArticleContent)):
		if(str(ArticleContent[index]) != "Error"):
			file1.write(ArticleContent[index].encode("UTF-8") + "\n")
		else:
			file1.write("HTML Parsing Error\n")
	file1.close()

def GetArticleURLs_Quillette(soup_TS):

	AllLinks = soup_TS.find_all('a')
	ArticleIdentifier = 'rel=\"bookmark\"' 				#HTML Code indicator for article links
	ArticleURLS = []
	ArticleTitles = []

	NullCounter = 0
	ArticleCounter = 0

	for index in range(len(AllLinks)):
		if ArticleIdentifier not in str(AllLinks[index]):
			NullCounter += 1
		else:
			ArticleCounter += 1
			ArticleURLS.append(AllLinks[index]['href'])
			Title = AllLinks[index].text.encode("UTF-8")
			CollapsedTitle = Title.replace(" ","")
			ArticleTitles.append(CollapsedTitle + ".txt")

	return ArticleURLS,ArticleTitles


def UpdateDictionary(WritePath,DictName,ArticleURLs):

	CompleteName = os.path.join(WritePath,DictName)

	if(os.path.exists(CompleteName)==True):
		file1 = open(CompleteName,'r')
		GlossaryData = file1.readlines()
		#PreviousURLs = file1.readlines()
		file1.close()
		PreviousURLs = []

		for index in range(len(GlossaryData)):
			Parsed = GlossaryData[index].split()
			PreviousURLs.append(Parsed[0])


	else:
		PreviousURLs = ["ArticleGlossary"]


	RepCheck = []

	for indexOuter in range(len(ArticleURLs)):

		Cond = False

		for indexInner in range(len(PreviousURLs)):

			#print PreviousURLs[indexInner]
			#print ArticleURLs[indexOuter]
			#print str(PreviousURLs[indexInner]==ArticleURLs[indexOuter])

			if(PreviousURLs[indexInner] == ArticleURLs[indexOuter]):
				#print PreviousURLs[indexInner] + "\n"
				#print ArticleURLs[indexOuter] + "\n"
				RepCheck.append(1)
				Cond = True

		if(Cond==False):
			RepCheck.append(0)

	file1 = open(CompleteName,'a')
	for index in range(len(RepCheck)):
		if(RepCheck[index]==0):
			file1.write(ArticleURLs[index] + "\n")
	file1.close()

	return RepCheck


MainPage = "https://quillette.com"
TopStoriesPage = MainPage + "/category/top-stories/"
SpotlightPage = MainPage + "/category/spotlight/"

DictName = "ArticleGlossary.dat"

BasePath = "Articles"
SubPath = "Quillette"
if(os.path.exists(BasePath)==False):
	os.mkdir(WritePath)
	os.chdir(WritePath)
	if(os.path.exsits(SubPath)==False):
		os.mkdir(WritePath)
	os.chdir("..")

WritePath = BasePath + "/" + SubPath

htmlCode_Main = urlopen(MainPage)
htmlCode_TS = urlopen(TopStoriesPage)
htmlCode_SL = urlopen(SpotlightPage)

#soup_Main = BeautifulSoup(htmlCode_Main,'html.parser')
soup_TS = BeautifulSoup(htmlCode_TS,'html.parser')

print("Top story page extracted...\n\t...")

soup_SL = BeautifulSoup(htmlCode_SL,'html.parser')

print("Spotlight articles extracted...\n\t...")

ArticleURLs_TS,ArticleTitles_TS = GetArticleURLs_Quillette(soup_TS)
ArticleURLs_SL,ArticleTitles_SL = GetArticleURLs_Quillette(soup_SL)

print("Article URLS Extracted\n\n")

RepCheck = UpdateDictionary(WritePath,DictName,ArticleTitles_TS)
print("\t\tFound --> " + str(len(RepCheck) - sum(RepCheck)) + " <-- new articles at " + TopStoriesPage + "\n\n")

for index in range(len(ArticleURLs_TS)):
	
	if(RepCheck[index]==0):
		htmlCode_Temp = urlopen(ArticleURLs_TS[index].encode("UTF-8"))
		soup_Temp = BeautifulSoup(htmlCode_Temp,'html.parser')
		ArticleContent = GetArticleContent(soup_Temp)

		WriteName = ArticleTitles_TS[index]
		WriteArticleText(WritePath,WriteName,ArticleContent)

RepCheck = UpdateDictionary(WritePath,DictName,ArticleTitles_SL)
print("\t\tFound --> " + str(len(RepCheck) - sum(RepCheck)) + " <-- new articles at " + SpotlightPage + "\n\n")

for index in range(len(ArticleURLs_SL)):

	if(RepCheck[index]==0):
		htmlCode_Temp = urlopen(ArticleURLs_SL[index].encode("UTF-8"))
		soup_Temp = BeautifulSoup(htmlCode_Temp,'html.parser')
		ArticleContent = GetArticleContent(soup_Temp)

		WriteName = ArticleTitles_SL[index]
		WriteArticleText(WritePath,WriteName,ArticleContent)

print("\n\n\t\t----- Quillette Extraction Finished -----\n\n\n")

