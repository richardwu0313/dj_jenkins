## introduction
Jenkins is a very useful tool for CI/CD, but Jenkins store build results using files and have limited summary functions.
dj_jenkins is a Django app to store build results in mysql, and provide lots of functions for user to view Jenkins build results.

## pre-condition
### setup mysql
`
docker run -d --name mysql-docker -e MYSQL_ROOT_USER=root -e MYSQL_ROOT_PASSWORD=password -e MYSQL_USER=jenkins -e MYSQL_PASSWORD=password -p 13306:3306 -v /deploy/dj-data/mysql:/var/lib/mysql mysql:8.0
`
### setup jenkins
`
docker run -d --name jenkins-docker --privileged -v /deploy/dj-data/jenkins:/var/jenkins_home -p 18080:8080 -p 50000:50000 jenkins:2.387.3-alpine
`

set username to **root**, password to **password**

## setup dj_jenkins
clone code and run cmds `cd dj_jenkins && poetry install`

## run dj_jenkins
`python3 manage.py runserver 0.0.0.0:18000`

## API Docs
### redoc
http://0.0.0.0:18000/redoc/
### swagger
http://0.0.0.0:18000/swagger/

## Notes
1. only tested on Jenkins 2.375, get_build_stages of latest Jenkins version return None.