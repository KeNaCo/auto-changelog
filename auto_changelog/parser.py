"""
The parser module will traverse a git repository, gathering all the commits
that follow the AngularJS commit message convention, and linking them with
the releases they correspond to.
"""

import git

from .models import Commit, Tag, Unreleased



def group_commits(tags, commits):
    tags = sorted(tags, key=lambda t: t.date)

    # Adding the tag's commit manually because those seem to be skipped
    commits.extend([Commit(t._commit) for t in tags])

    # Sort the commits and filter out those not formatted correctly
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


def traverse(base_dir):
    repo = git.Repo(base_dir)
    tags = repo.tags

    wrapped_tags = []
    for tagref in tags:        
        t = Tag(
            name=tagref.name, 
            date=tagref.commit.committed_date, 
            commit=tagref.commit)
        wrapped_tags.append(t)
        
    commits = list(repo.iter_commits('master'))
    commits = list(map(Commit, commits)) # Convert to Commit objects

    # Iterate through the commits, adding them to a tag's commit list
    # if it belongs to that release
    left_overs = group_commits(wrapped_tags, commits)

    # If there are any left over commits (i.e. commits created since 
    # the last release
    if left_overs:
        unreleased = Unreleased(left_overs)
    else:
        unreleased = None

    return wrapped_tags, unreleased

