# An Eye On It
Script to check for Jira tickets updates every minute.

## Python versions
(This script was created for Python 2 because everybody has it by default. It comes with Mac OS)
You you happen to have Python 3 installed, don't worry. Just create a "jump" script to call the script.
For example, if you cloned the git repo to your home folder, here is are the commands you will run, and the results:

## Requirements
- Python 2
- Python's library for Jira API. To install it: $ pip install jira
- Permissions to run the file ($ sudo chmod u+x aeoi.sh)

## How to monitor

* A specific ticket:

       $ aeoi <jira ticket name>
* Active tickets you reported

      $ aeoi r
      $ aeoi reporter
* Active tickets you are watching
      
      $ aeoi w
      $ aeoi watcher
