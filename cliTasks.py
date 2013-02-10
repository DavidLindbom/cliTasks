#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Get todo items from Google Tasks
# 
# Help: 
# If getting encoding errors when doing output redirection in the terminal
# add 'export PYTHONIOENCODING=utf-8' to your .bash_profile
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

api_key = ''
tasklist_id = ''
client_id=''
client_secret=''
scope='https://www.googleapis.com/auth/tasks.readonly'
app_name='cliTasks/v1'

# Set up a Flow object to be used if we need to authenticate.
FLOW = OAuth2WebServerFlow(
    client_id=client_id,
    client_secret=client_secret,
    scope=scope,
    user_agent=app_name)

# Looks if there is accepted cridentials.
# If not, make the user accept through the browser
storage = Storage('.todo-gtasks.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
  credentials = run(FLOW, storage)

# Authorize our credentials
http = httplib2.Http()
http = credentials.authorize(http)

# Build a service object for interacting with the API.
service = build(serviceName='tasks', version='v1', http=http,
                developerKey=api_key)

# Do request to Google
tasks = service.tasks().list(tasklist=tasklist_id, showCompleted=False).execute()

# Print all todo items
for task in tasks['items']:
  print ' * %s' % task['title']
