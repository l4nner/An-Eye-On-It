#!/usr/bin/python
# Beta 1.0

import os
import sys
import requests
import datetime
import re
from jira import JIRA
from time import sleep
from os import popen
import subprocess

requests.packages.urllib3.disable_warnings()

configFile = 'aeoiconfig.txt'
homeFolder = os.environ['HOME']
jiraSrvFqdn = 'jira-sd.mc1.oracleiaas.com'
pro = 'https'

def printJiraUrl(pro, server, issue):
	url = '{}://{}/browse/{}'.format(pro, server, issue)
	print(url)

if not os.path.exists(homeFolder + "/" + configFile):
	userName=raw_input("Enter your Oracle SSO account (Full.Name@Oracle.com): ")
	if re.match(r"\w+\.\w+@oracle.com", userName):
		os.system("echo " + userName + " > " + homeFolder + "/" + configFile)
	else:
		print "You haven't entered a valid Oracle e-mail address"
		sys.exit()

userName=(subprocess.check_output('grep -i "@oracle.com" ~/aeoiconfig.txt',shell=True)).rstrip()
jitToken=popen('ssh webadm-jit-01001.node.ad1.mc1 -p 22222 "generate --mode password"').read()
jira=JIRA(server=pro+'://'+jiraSrvFqdn ,basic_auth=(userName,jitToken),options={'verify': False})

if len(sys.argv) == 2:
	jiraIssue=sys.argv[1]
else:
	jiraIssue=raw_input("Jira ticket: ")

try:
	jira.issue(jiraIssue)
except:
	print "Invalid issue number"
	sys.exit()

initialCounter = currentCounter = len(jira.comments(jiraIssue))

try:
	while True:
		os.system('clear')
		print (jiraIssue)
		print ("Last check: " + datetime.datetime.now().strftime("%-I:%M"))
		currentCounter = len(jira.comments(jiraIssue))
		if currentCounter <= initialCounter:
			sleep(60)
		else:
			if os.path.exists("/System/Library/Sounds/Glass.aiff"):
				for i in range(0,2): os.system("afplay /System/Library/Sounds/Glass.aiff")
			print "\033[34m* * TICKET UPDATED * *\033[0m"
			# print "To open it hit Command + click:" # this depends on the terminal application
			printJiraUrl(pro , jiraSrvFqdn , jiraIssue)
			break
except KeyboardInterrupt:
	print ""
	pass
