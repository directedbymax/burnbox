#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BurnBox | https://burnbox.hideaway.chat/

Copyright (C) 2014-2022 Micah Lee, et al. <micah@micahflee.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import setuptools

with open(os.path.join("burnbox_cli", "resources", "version.txt")) as f:
    version = f.read().strip()

setuptools.setup(
    name="burnbox-cli",
    version=version,
    long_description=(
        "BurnBox lets you securely and anonymously send and receive files. It works by starting a web server, "
        "making it accessible as a Tor onion service, and generating an unguessable web address so others can "
        "download files from you, or upload files to you. It does _not_ require setting up a separate server or "
        "using a third party file-sharing service."
    ),
    author="BurnBox",
    author_email="support@burnbox.hideaway.chat",
    maintainer="BurnBox",
    maintainer_email="support@burnbox.hideaway.chat",
    url="https://burnbox.hideaway.chat",
    license="GPLv3",
    keywords="onion, share, burnbox, tor, anonymous, web server",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Flask",
        "Topic :: Communications :: File Sharing",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
    ],
    packages=[
        "burnbox_cli",
        "burnbox_cli.web",
    ],
    package_data={
        "burnbox_cli": [
            "resources/*",
            "resources/static/*",
            "resources/static/css/*",
            "resources/static/img/*",
            "resources/static/js/*",
            "resources/templates/*",
        ]
    },
    entry_points={
        "console_scripts": [
            "burnbox-cli = burnbox_cli:main",
        ],
    },
)
