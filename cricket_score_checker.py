import pandas as pd
import numpy as np
import requests
import lxml.html as lh

englandUrl = 'https://www.espncricinfo.com/team/england-1/match-schedule-fixtures'

page = requests.get(englandUrl)
content = page.content
doc = lh.fromstring(content)

#Finding the status of the game
elements = doc.xpath("//div[@class='ds-px-4 ds-py-3']/a/div/div/div/div/span[@class='ds-text-tight-xs ds-font-bold ds-uppercase ds-leading-5']")
matchStatus = elements[0].text_content()

#Check if the game is ongoing, possibly incomplete - need exhaustive list
validGameStates = ['Live','Stumps','Lunch','Tea']
liveMatch = False
for state in validGameStates:
    liveMatch = liveMatch or state == matchStatus
    if liveMatch:
        break
#Check if delayed
liveMatch = liveMatch or 'delayed' in matchStatus or 'Delayed' in matchStatus

if(liveMatch):
    #Finding the URL of top game
    elements = doc.xpath("//div[@class='ds-px-4 ds-py-3']/a")
    matchUrl = 'https://www.espncricinfo.com/'+elements[0].attrib['href']
    print(matchStatus)

    
