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
        return text

    @staticmethod
    def _link(url, pattern, text: str) -> str:
        """ Replaces all occurrences of pattern in text with markdown links based on url template """
        if not url or not pattern:
            return text

        def replace(match):
            matching_text = match.group(1)
            ticket_id = match.group(2) or match.group(1)
            ticket_url = url.format(id=ticket_id)
            return "[{matching_text}]({ticket_url})".format(matching_text=matching_text, ticket_url=ticket_url)

        return re.sub(pattern, replace, text)
