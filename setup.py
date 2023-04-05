"""THis is the setup.py file for whatpack.py"""
import os
from setuptools import setup

dir_path = os.path.dirname(os.path.realpath(__file__))


def readme_str() -> str:
    """This will return the readme file"""
    with open(r"README.md", encoding='UFT-8') as file:
        readme = file.read()
        return readme


def reqs():
    """This will return the requirements file"""
    print(dir_path)
    with open((dir_path + "//requirements.txt"), "r", encoding="UTF-8") as file:
        requirements = [line.strip() for line in file]
        return requirements


setup(
    name="whatpack.py",
    packages=['whatpack', 'whatpack.async', 'whatpack.sync', 'whatpack.headless'],
    version="1.0.0.0",
    maintainer="SigireddyBalasai",
    maintainer_email="SigireddyBalasai@gmail.com",
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    license="MIT",
    description="""About whatpack.py is a Python package that
    allows you to automate WhatsApp and YouTube tasks in an asynchronous
    and headless way. It uses asyncpywhatkit and headlesspywhatkit libraries
    under the hood to provide fast and easy-to-use features. With whatpack.py,
    you can send messages on WhatsApp without opening the app""",
    author="SigireddyBalasai",
    author_email="sigireddybalasai@gmail.com",
    url="https://github.com/SigireddyBalasai/whatpack.py",
    download_url="https://github.com/SigireddyBalasai/whatpack.py",
    keywords=["send_what_msg", "whatpack"],
    install_requires=reqs(),
    include_package_data=True,
    long_description=readme_str(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
