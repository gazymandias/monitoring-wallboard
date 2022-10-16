# monitoring-wallboard
Monitoring Wallboard REST API with Flask, Docker Compose and Postgres

Prerequisites
-------------
1. install docker
1. install docker-compose
1. install git
1. clone repository: `git clone --recursive https://github.com/gazymandias/monitoring-wallboard.git`

Getting Started
---------------
1. run service locally: `docker compose up -d db`
1. check status  `docker ps`
1. check db status (optional) `docker exec -it db psql -U postgres` `\dt` 
1. exit `exit` OR `\q`
1. run the python wallboard app `docker compose up --build monitoring-wallboard`
1. remove dangling images if required (optional) `docker image prune`
1. check container status (optional) `docker ps -a`
1. test the endpoints
1. visit http://localhost/home and run the generate_mock_data.py to start wallboard simulation
1. command & c to quit
1. remove service `docker-compose down`
1. remove service and all data `docker-compose down --volumes`

