'''
    The Setup.py is an essential part of Packaging and Distribution of Python Packages.
    It is used by Setuptools(or distutils in older python versions) to define the coonfiguration 
    of your package.Such as metadata,dependencies,scripts,etc
    
'''
from setuptools import setup, find_packages # type: ignore
from typing import List


def get_requirements(file_path: str) -> List[str]:
    ''' This function will return the list of requirements '''
    requirement_list=[]
    try :
        with open(file_path) as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                # ignore the -e . in requirements.txt
                if requirement and requirement != "-e .":
                    requirement_list.append(requirement)
    except FileNotFoundError as e:
        print("requirements.txt not found")

    return requirement_list

print(get_requirements("requirements.txt"))

setup(
    name= "Network_security",
    version="0.0.1",
    author="Sumit",
    author_email="sumit13thakur124@gmail.com",
    packages=find_packages(),
    install_requires= get_requirements("requirements.txt")
)