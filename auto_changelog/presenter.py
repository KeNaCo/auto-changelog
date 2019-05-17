import os

from jinja2 import FileSystemLoader, Environment

from auto_changelog.domain_model import Changelog, PresenterInterface


default_template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')
default_template_name = 'default.jinja2'


class MarkdownPresenter(PresenterInterface):
    def __init__(self, template_path=None):
        if template_path:
            template_dir, template_name = os.path.split(template_path)
        else:
            template_dir = default_template_dir
            template_name = default_template_name

        env = Environment(loader=FileSystemLoader(template_dir))

        self.template = env.get_template(template_name)

    def present(self, changelog: Changelog) -> str:
        return self.template.render(changelog=changelog)
