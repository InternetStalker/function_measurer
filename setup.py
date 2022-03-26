from setuptools import setup
from measurer import __version__
import os

def read(path: str):
    with open(path, "r", encoding = "utf-8") as file:
        return file.read()

scriptFolder = os.path.dirname(__file__)
ReadmePath = os.path.join(scriptFolder, "README.html")

projectUrls = {
    "Homepage": "https://github.com/InternetStalker/function_measurer",
}

classifiers = [
    'License :: OSI Approved :: MIT License',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities'
]

setup(name = 'function_measurer',
    version = __version__,
    description = 'Python utility for compairing functions and other callable objects.',
    packages = ['measurer'],
    author = "InternetStalcker",
    author_email = 'internetstalcker@yandex.ru',
    include_package_data = True,
    zip_safe = False,
    long_description = read(ReadmePath),
    long_description_content_type = 'text/markdown',
    project_urls = projectUrls,
    keywords = 'test tests testing runtime memory',
    classifiers = classifiers,
    license = 'MIT'
)