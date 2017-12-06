"""
The parser module will traverse a git repository, gathering all the commits
that follow the AngularJS commit message convention, and linking them with
the releases they correspond to.
"""
import git

from .models import Commit, Tag, Unreleased


def group_commits(tags, commits):
    tags = sorted(tags, key=lambda t: t.date)

    # Sort the commits and filter out those not formatted correctly
    commits = [
        c for c in sorted(set(commits), key=lambda c: c.date)
        if c.category
    ]

    for prev_tag, this_tag in zip([None] + tags[:-1], tags):
        commits_this_tag = (
            c for c in commits
            if prev_tag is None or prev_tag.date < c.date
            if c.date <= this_tag.date
        )
        for commit in commits_this_tag:
            this_tag.add_commit(commit)

    unreleased = [c for c in commits if c.date > tags[-1].date]
    return unreleased


def traverse(base_dir):
    repo = git.Repo(base_dir)
    tags = repo.tags

    if len(tags) < 1:
        raise ValueError('Not enough tags to generate changelog')

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
