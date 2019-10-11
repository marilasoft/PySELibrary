#!/bin/sh
mkdir -p PySELibrary_0.0.1-r0.4-BETA_all//DEBIAN
cp BuildDEB/* PySELibrary_0.0.1-r0.4-BETA_all//DEBIAN
mkdir -p PySELibrary_0.0.1-r0.4-BETA_all/usr/lib/python3/dist-packages/PySELibrary/core/
mkdir PySELibrary_0.0.1-r0.4-BETA_all/usr/lib/python3/dist-packages/PySELibrary/net/
mkdir PySELibrary_0.0.1-r0.4-BETA_all/usr/lib/python3/dist-packages/PySELibrary/utils/
cp PySELibrary/__init__.py PySELibrary_0.0.1-r0.4-BETA_all/usr/lib/python3/dist-packages/PySELibrary/__init__.py
cp PySELibrary/core/exceptions.py PySELibrary_0.0.1-r0.4-BETA_all/usr/lib/python3/dist-packages/PySELibrary/core/exceptions.py
cp PySELibrary/core/__init__.py PySELibrary_0.0.1-r0.4-BETA_all/usr/lib/python3/dist-packages/PySELibrary/core/__init__.py
cp PySELibrary/core/templates.py PySELibrary_0.0.1-r0.4-BETA_all/usr/lib/python3/dist-packages/PySELibrary/core/templates.py
cp PySELibrary/net/__init__.py PySELibrary_0.0.1-r0.4-BETA_all/usr/lib/python3/dist-packages/PySELibrary/net/__init__.py
cp PySELibrary/utils/__init__.py PySELibrary_0.0.1-r0.4-BETA_all/usr/lib/python3/dist-packages/PySELibrary/utils/__init__.py
chmod 775 -R PySELibrary_0.0.1-r0.4-BETA_all//DEBIAN/
dpkg-deb -b PySELibrary_0.0.1-r0.4-BETA_all/
rm -r PySELibrary_0.0.1-r0.4-BETA_all/
