from setuptools import setup, find_packages


setup(
        name='auto_changelog',
        version='0.1.0',
        description='A quick script to generate changelogs from git commit messages',
        long_description=open('README.rst').read(),
        author='Michael F Bryan',
        author_email='michaelfbryan@gmail.com',
        url='https://github.com/Michael-F-Bryan/auto-changelog',
        license='MIT License',
        packages=find_packages(),

        data_files=[
            ('templates', ['templates/base.jinja2', 'templates/tag_format.jinja2']),
            ],
        entry_points={
            'console_scripts': ['auto-changelog=auto_changelog.__main__:main'],
            },

        install_requires=[
            'jinja2',
            'gitpython',
            'docopt',
            ],
)

