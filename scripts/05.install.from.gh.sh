#!/bin/sh
export DISTUTILS_DEBUG=ok
cd ..
## Syntax: pip install "ProcessPackage" @ git+"URL of the repository"
# run this script in the client project_dict
pip install able@git+https://github.com/Wilfongjt/abilities#egg=able-1.15.2
