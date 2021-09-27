#!/bin/bash
"""virtualenv workspace
cd workspace
source bin/activate"""
cd Python
pip3 install boto3
pip3 install requests
pip3 install argparse
pip3 install pytest
pip3 install Appium-Python-Client
find tests/

py.test --collect-only tests/

## Remove cached files
find . -name '__pycache__' -type d -exec rm -r {} +
find . -name '*.pyc' -exec rm -f {} +
find . -name '*.pyo' -exec rm -f {} +
find . -name '*~' -exec rm -f {} +

## Write installed packages to requirements.txt
pip3 freeze > requirements.txt

## Package your tests and pip requirements into a zip file:
zip -r test_bundle.zip tests/ requirements.txt
echo $(pwd)/test_bundle.zip