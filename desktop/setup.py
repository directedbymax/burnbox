#!/usr/bin/env python3
# This file is used to build the Snapcraft and Flatpak packages
import setuptools

# The version must be hard-coded because Snapcraft won't have access to ../cli
version = "2.6.3"

setuptools.setup(
    name="burnbox",
    version=version,
    long_description="Securely and anonymously share files, host websites, and chat with friends using the Tor network",
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
        "burnbox",
        "burnbox.tab",
        "burnbox.tab.mode",
        "burnbox.tab.mode.share_mode",
        "burnbox.tab.mode.receive_mode",
        "burnbox.tab.mode.website_mode",
        "burnbox.tab.mode.chat_mode",
    ],
    package_data={
        "burnbox": [
            "resources/*",
            "resources/images/*",
            "resources/images/countries/*",
            "resources/locale/*",
            "resources/countries/*",
        ]
    },
    entry_points={
        "console_scripts": [
            "burnbox = burnbox:main",
            "burnbox-cli = burnbox_cli:main",
        ],
    },
)
