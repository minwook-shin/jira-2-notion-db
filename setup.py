import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jira-2-notion-db",
    version="1.1.1",
    author="minwook-shin",
    author_email="minwook0106@gmail.com",
    description="Jira to Notion-database Migration Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/minwook-shin/jira-2-notion-db",
    project_urls={
        "Bug Tracker": "https://github.com/minwook-shin/jira-2-notion-db/issues",
    },
    install_requires=[
        "jira==3.4.1",
        "notion-database==20220628.3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=("venv", "*.sh")),
    python_requires=">=3.7",
    scripts=['bin/jira-2-notion-db'],
)
