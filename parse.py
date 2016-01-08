#
# @title : Crawl question
# @author : PhungHV
# @date : 01072015
#

import re
import time
import urllib2

startTime = time.time()
proxyHandler = urllib2.ProxyHandler({"http": "http://user:pass@proxy.com.vn:3128"})
opener = urllib2.build_opener(proxyHandler)
urllib2.install_opener(opener)
listRootSites = []
listRootSites.append("http://www.sanfoundry.com/1000-database-management-system-questions-answers/")
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
numQuestion = 0
outputFile = open("list_question.html", 'w')
outputFile.truncate()
for site in listRootSites:
    req = urllib2.Request(site, headers=hdr)
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e :
        print(e.fp.read())
    content = page.read()
    lines = content.splitlines()

    listQuestionUrls = []
    for line in lines:
        if re.match("^<a href=.*(</a>|<br />)$", line):
            url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
            if len(url) == 1:
                listQuestionUrls+=url
    questionReading = False
    for url in listQuestionUrls:
        print("\tReading: " + url)
        req = urllib2.Request(url, headers=hdr)
        try:
            page = urllib2.urlopen(req)
        except urllib2.HTTPError, e :
            print(e.fp.read())
        content = page.read()
        lines = content.splitlines()
        rootQuestion = []
        for line in lines:
            questionRegex = "(^<p>\d{1,3}\. .*>$)|(^\t\d{1,3}\..*>$)"
            questionPattern = re.compile(questionRegex)
            answerPattern = re.compile('(^<span class="collapseomatic.*?)|(.*?View Answer.*?)')
            if questionPattern.match(line):
                questionReading=True
                numQuestion += 1
                subLine=re.sub(r'(^<p>\d{1,3})|(^\t\d{1,3})',str(numQuestion),line)
                line = re.sub(r'<br.*>$','',subLine)
                rootQuestion.append("<p>")
                rootQuestion.append(line)
                rootQuestion.append("<br/>")
                rootQuestion.append("\n")
    
            elif questionReading:
                if answerPattern.match(line):
                    subLine = re.sub(r'^<span class="collapseomati.*?</span>','' ,line)
                    line = re.sub(r'<div.*?id="target.*?">','' ,subLine)
                    subLine = re.sub(r'<div.*>','' ,line)
                    line = re.sub(r'<script.*?>','' ,subLine)
                    temp=line
                    subLine = re.sub(r'.*?Answer:','' ,line)
                    line=subLine
                    subLine = re.sub(r'.*?:','',line)
                    line = re.sub(r'or','',subLine)
                    subLine = re.sub(r'and','',line)
                    line = re.sub(r',','',subLine)
                    subLine = re.sub(r'<br />','',line)
                    line = re.sub(r' ','',subLine)
                    for quest in rootQuestion :
                        checked = 0
                        for a in line :
                            aa= []
                            aa.append('^')
                            aa.append(a)
                            aa.append('[\.|)].*?')
                            rex_check = ''.join(aa)
                            if re.match(rex_check,quest) :
                                outputFile.write("<font color='red'><b>")
                                outputFile.write(quest)
                                outputFile.write("</b></font>")
                                checked =1
                        if checked ==0 :
                            outputFile.write(quest)
                    outputFile.write(temp)
                    questionReading = False
                    rootQuestion = []
                else :
                    subLine = re.sub(r'<br.*>$','',line)
                    rootQuestion.append(subLine)
                    rootQuestion.append("<br/>")
                    rootQuestion.append("\n")
            else:
                continue

print ("Total question: ", numQuestion)
print("Time execution: ", (time.time() - startTime))

