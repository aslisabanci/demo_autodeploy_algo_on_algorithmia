#!/bin/bash

ALGO_NAME=demo_jameskenny
ALGO_REPO=https://git.algorithmia.com/git/asli/demo_jameskenny.git

git clone --depth=1 $ALGO_REPO
cd $ALGO_NAME
rm -rf .git