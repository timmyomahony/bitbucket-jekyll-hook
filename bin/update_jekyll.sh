#!/bin/bash
cd /path/to/jekyll/
sudo -u admin git pull origin master
chown -R admin:admin ./*
jekyll build
