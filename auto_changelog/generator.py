from jinja2 import FileSystemLoader, Environment


def generate_changelog(template_dir, title, description, count, unreleased, tags):
    tags = sorted(tags, key=lambda t: t.date)

    # Set up the templating engine
    loader = FileSystemLoader(template_dir)
    env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('base.jinja2')

    if count == 0:
        changelog = template.render(
            title=title,
            description=description,
            unreleased=unreleased,
            tags=reversed(tags))
    else:
        if unreleased:
            count -= 1

        if count > 0:
            changelog = template.render(
                title=title,
                description=description,
                unreleased=unreleased,
                tags=tags[-1::-1][:count])
        else:
            changelog = template.render(
                title=title,
                description=description,
                unreleased=unreleased,
                tags=[])

    return changelog.encode('utf-8') if isinstance(changelog, unicode) else changelog
