# An Eye On It
Script to check for Jira tickets updates every minute.

## Python versions
Follow this example and you won't be facing Python version hell issues:
[Step by step](https://github.com/l4nner/aeoi/blob/master/Step-by-step.txt)

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
      
* Tickets updated within the last x hours
      
      $ aeoi -h|--hour|--hours <x>
      
Note: no parameter defaults to reported issues
