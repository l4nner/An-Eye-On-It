# An Eye On It
Script to check for Jira tickets updates every minute.

## Python versions
(This script was created for Python 2 because everybody has it by default. It comes with Mac OS)
You you happen to have Python 3 installed, don't worry. Just create a "jump" script to call the script.
For example, if you cloned the git repo to your home folder:
`
$ pwd
/Users/flcardos
$ git clone http://www.github.com/l4nner/aeoi
Cloning into 'aeoi'...
$ ls -lisa aeoi/aeoi.py 
16281003 16 -rw-r--r--  1 flcardos  staff  4146 Jan 28 07:49 aeoi/aeoi.py
$ chmod u+x aeoi/aeoi.py 
$ cat > /usr/local/bin/aeoi <<EOF
> python ~/aeoi/aeoi.py
> EOF
$ ls -lisa /usr/local/bin/aeoi 
16281236 8 -rw-r--r--  1 flcardos  wheel  22 Jan 28 07:52 /usr/local/bin/aeoi
$ chmod u+x /usr/local/bin/aeoi 
`

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
