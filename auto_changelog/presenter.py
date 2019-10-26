import re
import os

from jinja2 import FileSystemLoader, Environment

from auto_changelog.domain_model import Changelog, PresenterInterface

default_template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates")
default_template_name = "default.jinja2"


class MarkdownPresenter(PresenterInterface):
    def __init__(self, template_path=None, issue_url=None):
        if template_path:
            template_dir, template_name = os.path.split(template_path)
        else:
            template_dir = default_template_dir
            template_name = default_template_name

        env = Environment(loader=FileSystemLoader(template_dir))

        self.template = env.get_template(template_name)

    def present(self, changelog: Changelog) -> str:
        text = self.template.render(changelog=changelog)
        text = self._link(changelog.issue_url, changelog.issue_pattern, text)
        text = self._title(changelog.compare_url, changelog.tag_pattern, changelog.tag_prefix, text)
        return text

    @staticmethod
    def _title(url, pattern, prefix_value: str, text: str) -> str:
        """ Replaces all occurrences of pattern in text with markdown links based on tag template """
        if not url or not pattern:
            return text

        index_version = 0
        # regex to get the title format of the release
        format_regex = "(?P<format>((?m)^#{1,6}(?!#)  *))"
        # regex to get the prefix / nothing with no prefix
        prefix_regex = "(?P<prefix>%s)" % prefix_value
        # build the final regex
        pattern = "(%s%s%s)" % (format_regex, prefix_regex, pattern)
        r = re.compile(pattern)
        # get all versions in the file to use them to build compare url
        all_versions = [m.groupdict() for m in r.finditer(text)]

        # tag_pattern should contain a group named "version"
        for versions in all_versions:
            if "version" not in versions:
                return text

        def replace(match):
            nonlocal index_version

            tag = match.group(match.re.groupindex["format"])
            version = match.group(match.re.groupindex["version"])
            prefix = match.group(match.re.groupindex["prefix"])

            # this is not the last versions of the file
            if (index_version + 1) < len(all_versions):
                # get version to build compare url
                current_version = all_versions[index_version]["version"]
                previous_version = all_versions[index_version + 1]["version"]
                compare_url = url.format(previous=previous_version, current=current_version)
                index_version += 1
                return "{format}[{prefix}{version}]({url})".format(
                    format=tag, prefix=prefix, version=version, url=compare_url
                )
            # this is the last version of the file => no need to put compare url
            else:
                return "{format}{prefix}{version}".format(format=tag, prefix=prefix, version=version)

        return re.sub(pattern, replace, text)

    @staticmethod
    def _link(url, pattern, text: str) -> str:
        """ Replaces all occurrences of pattern in text with markdown links based on url template """
        if not url or not pattern:
            return text

        def replace(match):
            groups = match.groups()
            if len(groups) == 2:
                matching_text = groups[0]
                ticket_id = groups[1]
            elif len(groups) == 1:
                matching_text = ticket_id = groups[0]
            else:
                raise ValueError("Invalid pattern")
            ticket_url = url.format(id=ticket_id)
            return "[{matching_text}]({ticket_url})".format(matching_text=matching_text, ticket_url=ticket_url)

        return re.sub(pattern, replace, text)
