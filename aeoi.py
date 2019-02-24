#!/usr/bin/python
# Beta 2.0

import os
import sys
import requests
import datetime
import time
import re
from jira import JIRA
from time import sleep
from os import popen
import subprocess

# we didn't have a budget for multiple parameters

if len(sys.argv) >= 3:
    print "Number of parameters is invalid"
    sys.exit()

requests.packages.urllib3.disable_warnings()

# variables

configFile = 'aeoiconfig.txt'
homeFolder = os.environ['HOME']
jiraSrvFqdn = 'jira-sd.mc1.oracleiaas.com'
protocol = 'https'
listAware = [False for _ in range(1,40)]
validParameters = ["reporter", "r", "watcher", "w"]
listIssue=[]
listSummary=[]
listComments=[]
colorcode={
    "mediumblue": "\033[94m",
    "bluebackground": "\033[44;96m",
    "gray": "\033[90m",
    "auto": "\033[0m"}
maxNumberHours = 730

# to print an URI

def linkPrint(protocol, server, issue):
    uri = ' {}://{}/browse/{}'.format(protocol, server, issue)
    print(uri)

# to play a sound file

def alertSound(audioFile,externalLoop,internalLoop):
    if os.path.exists(audioFile):
        for _ in range(0, externalLoop):
            for _ in range(0, internalLoop):
                subprocess.call("afplay " + audioFile, shell=True)
            time.sleep(0.5)

# If email/login still not available, asks for input

if not os.path.exists(homeFolder + "/" + configFile):
    userName = raw_input("Enter your Oracle SSO account (Full.Name@Oracle.com): ")
    if re.match(r"\w+\.\w+@oracle.com", userName):
        os.system("echo " + userName + " > " + homeFolder + "/" + configFile)
    else:
        print ("You haven't entered a valid Oracle e-mail address")
        sys.exit()
userName = (subprocess.check_output('grep -i "@oracle.com" ~/aeoiconfig.txt', shell=True)).rstrip()

# Getting a tocken from our jit server

try:
    jitToken = popen('ssh webadm-jit-01001.node.ad1.mc1 -p 22222 "generate --mode password"').read()
except KeyboardInterrupt:
    sys.exit()

jira = JIRA(server=protocol+'://'+jiraSrvFqdn, basic_auth=(userName,jitToken), options={'verify': False})

# if no parameters or a valid parameter, other than the ticket number

if (len(sys.argv) == 1) or (len(sys.argv) == 2 and sys.argv[1] in validParameters ) or (sys.argv[1]).isdigit():
    if not ( 1 <= int(sys.argv[1]) <= maxNumberHours ):
        print "Maximum number of ours is",maxNumberHours
        sys.exit()
    if len(sys.argv) == 1:
        jiraField = "reporter"
    else:
        if sys.argv[1] in ["reporter", "r"]: jiraField="reporter"
        elif sys.argv[1] in ["watcher", "w"]: jiraField="watcher"
        elif int(sys.argv[1]) in range(1,maxNumberHours,1):
            numberOfHours = sys.argv[1]
            for issue in jira.search_issues(' reporter = currentUser() and updatedDate > -'+numberOfHours+'h'):
                listIssue.append(str(issue.key))
                listSummary.append(str(issue.fields.summary))
                listComments.append(len(jira.comments(issue)))
            if len(listIssue) == 0:
                print colorcode["mediumblue"],"No ticket updates within the last ",numberOfHours," hours.",colorcode["auto"]
            else:
                index=0
                while index < len(listIssue):
                    print colorcode["mediumblue"],listIssue[index],"\t",listSummary[index],colorcode["auto"]
                    index += 1
            sys.exit()
    listCommentsWatermark=[]
    try:
        for issue in jira.search_issues( jiraField +' = currentUser() AND status not in (Resolved, Closed) order by created desc'):
            listCommentsWatermark.append(len(jira.comments(issue)))
    except BaseException:
        print "Parameter invalid"
        sys.exit()
    try:

        # creates ticket list

        for issue in jira.search_issues(jiraField + ' = currentUser() AND status not in (Resolved, Closed) order by created desc'):
            listIssue.append(str(issue.key))
            listSummary.append(str(issue.fields.summary))
            listComments.append(len(jira.comments(issue)))
        
        # initial number of issues

        numberIssuesWatermark = (len(listIssue))
        
        # enters the loop until number of tickets change or user interrupts 

        while True:
            os.system('clear')
            print "\nLast check: ",datetime.datetime.now().strftime("%-I:%M"),"\t*",(jiraField.upper()),"*\n"
            index=0

            # goes over active tickets
            
            while index < numberIssuesWatermark:

                # If the ticket changed

                if listComments[index] != listCommentsWatermark[index]:
                    print colorcode["bluebackground"],listIssue[index],"\t", listSummary[index],colorcode["auto"]
                    linkPrint(protocol, jiraSrvFqdn, str(listIssue[index]))
                    if listAware[index] == False:
                        alertSound("/System/Library/Sounds/Glass.aiff", 2, 2)
                        listAware[index] = True
                else:
                    print colorcode["mediumblue"],listIssue[index],"\t",listSummary[index],colorcode["auto"]
                index += 1

            print "\n^C to cancel"
            sleep(120)

            listIssue=[]
            listSummary=[]
            listComments=[]
            for issue in jira.search_issues(jiraField + ' = currentUser() AND status not in (Resolved, Closed) order by created desc'):
                listIssue.append(str(issue.key))
                listSummary.append(str(issue.fields.summary))
                listComments.append(len(jira.comments(issue)))
            
            # if the number of tickets changed, just list all of them and leave
            if len(listIssue) != numberIssuesWatermark:
                print "\n\n* * Number of active items changed to:\n"
                index=0
                alertSound("/System/Library/Sounds/Glass.aiff", 2, 2)
                while index < len(listIssue):
                    print colorcode["gray"],listIssue[index],"\t",listSummary[index],colorcode["auto"]
                    index += 1
                print "\n\n"
                break             
    except KeyboardInterrupt:
        print ""
        pass

# if a ticket number was provided 

else:
    jiraIssue = sys.argv[1]
    try:
        initialCounter = currentCounter = len(jira.comments(jiraIssue)) 
        while True:
            os.system('clear')
            print(jiraIssue)
            print ("Last check: " + datetime.datetime.now().strftime("%-I:%M"))
            currentCounter = len(jira.comments(jiraIssue))
            if currentCounter <= initialCounter:
			    sleep(60)
            else:
                alertSound("/System/Library/Sounds/Morse.aiff", 1, 3)
                print colorcode["bluebackground"], "* * TICKET UPDATED * *\n\t\t",colorcode["auto"]
                print "\t\t"
                linkPrint(protocol , jiraSrvFqdn , jiraIssue)
                break
    except BaseException:
        print "Invalid issue number"
