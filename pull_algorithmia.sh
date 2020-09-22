#!/bin/bash

ALGO_NAME=demo_gh
ALGO_REPO=https://git.algorithmia.com/git/asli/demo_gh.git

git clone --depth=1 $ALGO_REPO
cd $ALGO_NAME
rm -rf .git