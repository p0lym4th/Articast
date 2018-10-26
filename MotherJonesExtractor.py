#This is an article extrctor for MotherJones.com
#
#Steven Large
#October 24th 2018

from urllib import urlopen
import numpy as np
#import matplotlib.pyplot as plt
import os
from bs4 import BeautifulSoup
import re

def GetArticleContent(soup_Article):
	pass

def WriteArticleText(WritePath,WriteName,Content):
	pass

def DeleteRepeatedEntries(LinkList):

	NewList = []
	for index1 in range(len(LinkList)):
		RepCond = False
		for index2 in range(len(NewList)):
			for index3 in range(len(LinkList)):
				if(NewList[index2]==LinkList[index3]):
					RepCond = True
		if(RepCond==True):
			NewList.append(LinkList[index1])

	return NewList

def GetArticleURLs_Main(soup_Directory):

	LinkList = []
	LinksEmbedded = soup_Directory.findAll("a",{"data-ga-category":"Homepage"})
	for index in range(len(LinksEmbedded)):
		LinkList.append(LinksEmbedded[index].get('href').encode("UTF-8"))
	LinkList = DeleteRepeatedEntries(LinkList)

	return LinkList

def UpdateDictionary(ReadPath,DictName,ArticleURLs):
	pass

def WriteHTMLCode(WritePath,WriteName,soup):

	CompleteName = os.path.join(WritePath,WriteName)
	file1 = open(CompleteName,'w')
	file1.write(str(soup))
	file1.close()

def WriteHTMLCode_Pretty(WritePath,WriteName,soup):
	
	CompleteName = os.path.join(WritePath,WriteName)
	file1 = open(CompleteName,'w')
	file1.write(str(soup.prettify().encode("UTF-8")))
	file1.close()


writePath_html = "htmlCode/MotherJones/"

MainPage = "https://www.motherjones.com"

#URL Extensions for relevant subcategory pages

PoliticsExt = "/politics/"
EnvironmentExt = "/environment/"
FoodExt = "/food/"
MediaExt = "/media/"
CrimeJusticeExt = "/crime-justice/"
InvestigationExt = "/topics/investigations/"
Election2018Ext = "/topics/2018-elections/"

#Read in HTML code for main and subcategory pages

htmlCode_Main = urlopen(MainPage)
htmlCode_Politics = urlopen(MainPage + PoliticsExt)
#htmlCode_Environment = urlopen(MainPage + EnvironmentExt)
#htmlCode_Food = urlopen(MainPage + FoodExt)
#htmlCode_Media = urlopen(MainPage + MediaExt)
htmlCode_Crime = urlopen(MainPage + CrimeJusticeExt)
#htmlCode_Investigation = urlopen(MainPage + InvestigationExt)
htmlCode_Election2018 = urlopen(MainPage + Election2018Ext)

#Create the BeautifulSoup objects

soup_Main = BeautifulSoup(htmlCode_Main,'html.parser')
soup_Politics = BeautifulSoup(htmlCode_Politics,'html.parser')
#soup_Environment = BeautifulSoup(htmlCode_Environment,'html.parser')
#soup_Food = BeautifulSoup(htmlCode_Food,'html.parser')
#soup_Media = BeautifulSoup(htmlCode_Media,'html.parser')
soup_Crime = BeautifulSoup(htmlCode_Crime,'html.parser')
#soup_Investigation = BeautifulSoup(htmlCode_Investigation,'html.parser')
soup_Election = BeautifulSoup(htmlCode_Election2018,'html.parser')

WriteHTMLCode_Pretty(writePath_html,'MainPage.dat',soup_Main)
WriteHTMLCode_Pretty(writePath_html,'PoliticsPage.dat',soup_Politics)
WriteHTMLCode_Pretty(writePath_html,'CrimePage.dat',soup_Crime)
WriteHTMLCode_Pretty(writePath_html,'ElectionPage.dat',soup_Election)

