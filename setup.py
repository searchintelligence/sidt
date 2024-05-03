from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='sidt',
    license='MIT',
    packages=find_packages(),
    install_requires=['tls_client', 'tqdm', 'beautifulsoup4'],
)