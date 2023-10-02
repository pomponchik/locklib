from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf8') as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name='locklib',
    version='0.0.9',
    author='Evgeniy Blinov',
    author_email='zheni-b@yandex.ru',
    description='A wonderful life without deadlocks',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/pomponchik/locklib',
    packages=find_packages(exclude='tests'),
    install_requires=requirements,
    classifiers=[
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
    ],
)
