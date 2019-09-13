from setuptools import setup

setup(
    # App name
    name="boyce_astro_research_tool",

    # Version
    version="0.1.0",

    # Author Details
    author="Alex Hewett",
    author_email="alexander.hewett93@gmail.com",

    # Packages
    packages=['tool'],

    # Include additional files into package
    include_package_data=True,

    # Dependencies
    install_requires=[
        'flask',
        'flask-wtf',
        'gunicorn',
        'pandas',
        'pyinstaller',
    ],

    entry_points={"console_scripts": ['boyce-astro-ra=run:run']}
)
