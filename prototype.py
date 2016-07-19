
# coding: utf-8

# In[1]:

import datetime
import re
from collections import namedtuple, defaultdict
from pprint import pprint
import os
import subprocess
import shlex

import git
from jinja2 import Environment, FileSystemLoader


# In[35]:

class Tag:
    def __init__(self, name, date, commit):
        self.name = 'Version ' + name if not name.lower().startswith('v') else name
        self._commit = commit
        self.date = datetime.datetime.fromtimestamp(date)
        self.commits = []
        self.groups = defaultdict(list)
        
    def add_commit(self, commit):
        self.commits.append(commit)
        commit.tag = self
        self.groups[commit.category].append(commit)
        
    def __repr__(self):
        return '<{}: {!r}>'.format(
                self.__class__.__name__,
                self.name)
    
class Unreleased:
    def __init__(self, commits):
        self.name = 'Unreleased'
        self.groups = defaultdict(list)
        self.commits = commits
        
        for commit in commits:
            self.add_commit(commit)
            
    def add_commit(self, commit):
        self.groups[commit.category].append(commit)

    def __repr__(self):
        return '<{}: {!r}>'.format(
                self.__class__.__name__,
                self.name)        
        
class Commit:
    def __init__(self, commit):
        self._commit = commit
        self.date = datetime.datetime.fromtimestamp(commit.committed_date)
        self.commit_hash = commit.hexsha
        
        first_line = commit.message.splitlines()[0].strip()
        self.first_line = first_line
        self.message = commit.message
        self.tag = None
        
        self.category, self.specific, self.description = self.categorize()
        
    def categorize(self):
        match = re.match(r'(\w+)(\(\w+\))?:\s*(.*)', self.first_line)
        
        if match:
            category, specific, description = match.groups()
            specific = specific[1:-1]  if specific else None # Remove surrounding brackets
            return category, specific, description
        else:
            return None, None, None
        
        
    def __repr__(self):
        return '<{}: {} "{}">'.format(
                self.__class__.__name__,
                self.commit_hash[:7],
                self.date.strftime('%x %X'))


# In[36]:

def group_commits(tags, commits):
    tags = sorted(tags, key=lambda t: t.date)
    commits = sorted(commits, key=lambda c: c.date)
    
    commits = list(filter(lambda c: c.category, commits))
    
    for index, tag in enumerate(tags):
        # Everything is sorted in ascending order (earliest to most recent), 
        # So everything before the first tag belongs to that one
        if index == 0:
            children = filter(lambda c: c.date <= tag.date, commits)
        else:
            prev_tag = tags[index-1]
            children = filter(lambda c: prev_tag.date < c.date <= tag.date, commits)
            
        for child in children:
            commits.remove(child)
            tag.add_commit(child)
            
    left_overs = list(filter(lambda c: c.date > tags[-1].date, commits))
    return left_overs


# In[37]:

base_dir = '/tmp/cz-cli'
repo = git.Repo(base_dir)
tags = repo.tags

my_tags = []
for tagref in tags:        
    t = Tag(
        name=tagref.name, 
        date=tagref.commit.committed_date, 
        commit=tagref.commit)
    my_tags.append(t)
    
commits = list(repo.iter_commits('master'))
commits = map(Commit, commits) # Convert to Commit objects
left_overs = group_commits(my_tags, commits)

if left_overs:
    unreleased = Unreleased(left_overs)
else:
    unreleased = None


# In[40]:

loader = FileSystemLoader('./templates')
env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
template = env.get_template('base.jinja2')

title = 'My Awesome Project'
description = 'My awesome project is a project that is awesome'
stuff = template.render(
    title=title,
    description=description,
    unreleased=unreleased,
    tags=reversed(my_tags))

print(stuff)
#display(Markdown(stuff))


# In[ ]:




# In[ ]:



