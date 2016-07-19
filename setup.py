from setuptools import setup, find_packages


setup(
        name='auto_changelog',
        version='0.1.4',
        description='A quick script to generate changelogs from git commit messages',
        long_description=open('README.rst').read(),
        author='Michael F Bryan',
        author_email='michaelfbryan@gmail.com',
        url='https://github.com/Michael-F-Bryan/auto-changelog',
        license='MIT',
        packages=find_packages(),

        package_data={
            'auto_changelog': ['templates/*.jinja2'],
            },
        include_package_data=True,
        entry_points={
            'console_scripts': ['auto-changelog=auto_changelog.__main__:main'],
            },

        install_requires=[
            'jinja2',
            'gitpython',
            'docopt',
            ],

        classifiers=[
            'Development Status :: 3 - Alpha',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',

            'Environment :: Console',
            'Operating System :: POSIX :: Linux',
            'Topic :: Software Development :: Documentation',

            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: MIT License',

            # The python versions actively being supported
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            ],
        keywords='git changelog generator',

)

