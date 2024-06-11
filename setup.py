from setuptools import setup, find_packages

# Read the contents of the requirements file for setup reqs
with open("requirements.txt", "r", encoding="utf-16") as f:
    requirements = f.read().splitlines()

setup(
    name="sidt",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    license="MIT",
    packages=find_packages(),
    install_requires=requirements,
    package_data={
        "": ["*.json", "*.csv", "*.txt", "*.geojson", "*.md"],
        "sidt": ["data/*.*"]
    },
    include_package_data=True,
)