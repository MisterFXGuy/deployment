#!/bin/bash

mkdir -p ~/swamp
cd ~/swamp

git clone git@swa-scm-1.mirsam.org:swamp/db-config.git db
git clone git@swa-scm-1.mirsam.org:swamp/service.git services
git clone git@swa-scm-1.mirsam.org:vendor/deployment-dependencies.git deployment

git clone git@swa-scm-1.mirsam.org:swamp/swamp-web-server.git swamp-web-server
git clone git@swa-scm-1.mirsam.org:swamp/www-front-end.git www-front-end