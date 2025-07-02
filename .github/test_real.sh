#!/bin/bash
set -e

# Test building the baseclasses docs
TEST_REPO=baseclasses

git clone https://github.com/mdolab/$TEST_REPO.git
cd $TEST_REPO/doc
pip install -r requirements.txt
make html
cd ../../
rm -rf $TEST_REPO
