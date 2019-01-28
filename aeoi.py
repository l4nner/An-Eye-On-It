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

if len(sys.argv) >= 3:
    print "Number of parameters is invalid"
    sys.exit()

requests.packages.urllib3.disable_warnings()

configFile = 'aeoiconfig.txt'
homeFolder = os.environ['HOME']
jiraSrvFqdn = 'jira-sd.mc1.oracleiaas.com'
pro = 'https'
listAware = [False for _ in range(1,40)]
validParameters = ["reporter", "r", "watcher", "w"]

def linkPrint(pro, server, issue):
    uri = '{}://{}/browse/{}'.format(pro, server, issue)
    print(uri)

def alertSound(audioFile,external,internal):
    if os.path.exists(audioFile):
        for _ in range(0, external):
            for _ in range(0, internal):
                subprocess.call("afplay " + audioFile, shell=True)
            time.sleep(0.5)

if not os.path.exists(homeFolder + "/" + configFile):
    userName = raw_input("Enter your Oracle SSO account (Full.Name@Oracle.com): ")
    if re.match(r"\w+\.\w+@oracle.com", userName):
        os.system("echo " + userName + " > " + homeFolder + "/" + configFile)
    else:
        print ("You haven't entered a valid Oracle e-mail address")
        sys.exit()
userName = (subprocess.check_output('grep -i "@oracle.com" ~/aeoiconfig.txt', shell=True)).rstrip()

try:
    jitToken = popen('ssh webadm-jit-01001.node.ad1.mc1 -p 22222 "generate --mode password"').read()
except KeyboardInterrupt:
    sys.exit()

jira = JIRA(server=pro+'://'+jiraSrvFqdn, basic_auth=(userName,jitToken), options={'verify': False})

if (len(sys.argv) == 1) or (len(sys.argv) == 2 and sys.argv[1] in validParameters ):
    if len(sys.argv) == 1:
        jiraField = "reporter"
    else:
        if sys.argv[1] in ["reporter", "r"]: jiraField="reporter"
        elif sys.argv[1] in ["watcher", "w"]: jiraField="watcher"
    listInitialComments=[]
    try:
        for issue in jira.search_issues( jiraField +' = currentUser() AND status not in (Resolved, Closed) order by created desc'):
            listInitialComments.append(len(jira.comments(issue)))
    except BaseException:
        print "Parameter invalid"
        sys.exit()
    try:
        while True:
            os.system('clear')
            print "\nLast check: ",datetime.datetime.now().strftime("%-I:%M"),"\t*",(jiraField.upper()),"*\n"
            index=0
            listIssue=[]
            listSummary=[]
            listComments=[]
            for issue in jira.search_issues(jiraField + ' = currentUser() AND status not in (Resolved, Closed) order by created desc'):
                listIssue.append(str(issue.key))
                listSummary.append(str(issue.fields.summary))
                listComments.append(len(jira.comments(issue)))
                if listComments[index] > listInitialComments[index]:
                    print "\033[46m",listIssue[index],"\t", listSummary[index],"\033[0m"
                    linkPrint(pro, jiraSrvFqdn, str(issue.key))
                    if listAware[index] == False:
                        alertSound("/System/Library/Sounds/Glass.aiff", 2, 2)
                        listAware[index] = True
                else:
                    print listIssue[index],"\t", listSummary[index]
                index += 1
            print "\n^C to cancel"
            sleep(120)
    except KeyboardInterrupt:
        print ""
        pass
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
                print "\033[34m* * TICKET UPDATED * *\033[0m\n\t\t"
                print "\t\t"
                linkPrint(pro , jiraSrvFqdn , jiraIssue)
                break
    except BaseException:
        print "Invalid issue number"
