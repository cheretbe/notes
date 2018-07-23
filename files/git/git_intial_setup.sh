#!/bin/bash

echo "Setting git parameters"

git config --global user.useConfigOnly true

# [!!] This will make git to store passwords in plaintext
git config --global credential.helper store

git config --global push.default simple

echo "Done"
