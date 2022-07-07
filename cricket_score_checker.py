import pandas as pd
import numpy as np
import requests
import lxml.html as lh
import time

teamUrl = 'https://www.espncricinfo.com/team/england-1/match-schedule-fixtures'

page = requests.get(teamUrl)
content = page.content
doc = lh.fromstring(content)

#Finding the status of the game
elements = doc.xpath("//div[@class='ds-px-4 ds-py-3']/a/div/div/div/div/span[@class='ds-text-tight-xs ds-font-bold ds-uppercase ds-leading-5']")
matchStatus = elements[0].text_content()

#Check if the game is ongoing, possibly incomplete - need exhaustive list
validGameStates = ['Live','Stumps','Lunch','Tea','Innings break']
liveMatch = False
for state in validGameStates:
    liveMatch = liveMatch or state == matchStatus
    if liveMatch:
        break
#Check if delayed
liveMatch = liveMatch or 'delayed' in matchStatus or 'Delayed' in matchStatus

#Finding the URL of top game
print(matchStatus)
elements = doc.xpath("//div[@class='ds-px-4 ds-py-3']/a")
matchUrl = 'https://www.espncricinfo.com/'+elements[0].attrib['href']
overs = 0
while liveMatch:
    page = requests.get(matchUrl)
    content = page.content
    doc = lh.fromstring(content)
    
    elements = doc.xpath("//div[@class = 'ds-text-compact-m ds-text-typo-title']")    
    #el = elements[0].text_content().replace(u'\xa0',u'').replace(' ','')
    #els = el.split(')')

    string1 = elements[0].text_content().replace(u'\xa0',u'').replace(' ','')
    if len(elements)>1: #If num of inns >1
        string2 = elements[1].text_content().replace(u'\xa0',u'').replace(' ','')
    else:
        string2 = ''
    #Could break during innings break or limited overs
    #Find out who's batting using overs in brackets
    if 'ov' in string1:
        batting = 1
        els = string1.split(')')
        #Check if ball bowled
        if overs != els[0].strip('( ov').split(',')[0].strip('ov'):
            #Split data up
            overs = els[0].strip('( ov').split(',')[0].strip('ov')
            scores1 = els[1].split('&')
            scores2 = string2.split('&')
    elif 'ov' in string2:
        batting = 2
        els = string2.split(')')
        if overs != els[0].strip('( ov').split(',')[0].strip('ov'):
            #split data up
            overs = els[0].strip('( ov').split(',')[0].strip('ov')
            scores2 = els[1].split('&')
            scores1 = string1.split('&')
    print(overs, scores1, scores2)

    
    
    time.sleep(5)
    

