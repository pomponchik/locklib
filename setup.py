from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="locklib",
    version="0.0.2",
    author="Evgeniy Blinov",
    author_email="zheni-b@yandex.ru",
    description="A wonderful life without deadlocks",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/pomponchik/locklib",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
)
