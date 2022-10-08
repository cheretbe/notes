#!/usr/bin/env python3

import sys
import os

if sys.argv[1].lower().startswith("username for "):
    print(os.environ["CUSTOM_GIT_USERNAME"])
elif sys.argv[1].lower().startswith("password for "):
    print(os.environ["CUSTOM_GIT_PASSWORD"])
