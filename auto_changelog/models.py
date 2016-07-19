"""
The basic data structures used in the project.
"""

import datetime
import re
from collections import defaultdict


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

