# Gist Scanner
[![Build Status](https://app.travis-ci.com/zicdamasta/gist_scanner.svg?token=1U5QxytYfua1YWiB3p5J&branch=main)](https://app.travis-ci.com/zicdamasta/gist_scanner)

Using the Github API query user’s publicly available github gists and
create activity in Pipedrive for each gist. Application periodically
checks for a user's publicly available gists. 

Application has two web endpoints
* First shows all users that have been scanned.
* Second shows the gists for that user that were added since the last visit.

Server and scanner run in seperated containers for clearer log and better scalability options.<br>
For simplicity there is no database and data is stored as .txt files. <br>
Server see generated .txt files via bind mount `./scanner/output/user:/server/api/user`.

### Stack:
Application:
 * 🐍 Python 3.10 for scanning gists
 * Flask 2.1.3 for endpoints and local dev server
 * Gunicorn for prod server
 
Infrastructure:
 * 🐳  Docker + Docker Compose
 * Terraform
 * Ansible

CI/CD
 * Travis CI


### How to run the application
1. Specify the `USER_LIST_TYPE` environment variable to either `env` or `file`
   - If `USER_LIST_TYPE` is `env` then specify users in the `USER_LIST` environment variable as comma seperated list. For example `USER_LIST: user1,user2,user3`
   - If `USER_LIST_TYPE` is `file` then add users to the `scanner/input/users.txt` file.
2. Set the `GITHUB_TOKEN` environment variable to the github token for the user.
3. Set the `PIPEDRIVE_TOKEN` environment variable to the pipedrive token for the user.
4. Run the application with `docker-compose up --build` 🚀
5. Check the application logs 📜 and your Pipedrive activities list 📝

### Endpoints

There are Bearer Token Authorization.

Default token is `token`. You can set your own token by setting the `BEARER_TOKEN` environment variable for the server.
* `GET /users` - Shows all users that have been scanned.
* `GET /user/<username>` - Shows the gists for that user that were added since the last visit.



### Docker environment variables
#### Scanner
* `PIPEDRIVE_API_KEY` - Pipedrive API key
* `GITHUB_API_KEY` - Github API key
* `USER_LIST_TYPE` - env or file
  * if `USER_LIST_TYPE` is env you can use `USER_LIST`
  * `USER_LIST` - comma separated list of users to scan
  * if `USER_LIST_TYPE` is file you can use `USER_LIST_FILENAME`
  * `USER_LIST_FILENAME` text file with list of users to scan. Default value `users.txt`
* `SCANNER_HOUR_INTERVAL` - period of time in hours to scan for new gists. Default value `3`
* `SCANNER_MINUTE_INTERVAL` - period of time in minutes to scan for new gists. Default value `0`
* `SCANNER_DEBUG_LEVEL` - set debug level for logs. Default value `DEBUG`

#### Server
* `SERVER_PORT` - port to run the server on. Default value `5000`
* `APP_ENV` - environment to run the application. Default value `development`
* `BEARER_TOKEN` - bearer token to use for authentication. Default value `token`

## CI /CD
CI/CD is done using Travis CI.

Stages:
* Testing
* Build and push to docker hub
* Deploy to production by running deployment script on the server.


## The Cloud

Application is deployed to the Google Cloud Platform.
Provisioning is done using Terraform with Ansible.

Application is running in a container.
nginx proxy is used to serve the application.

`GET /users` - Shows all users that have been scanned.

**NB: Host in headers is important!**
```bash
curl --location --request GET 'http://34.88.192.29/users' \
--header 'Host: gist-scanner' \
--header 'Authorization: Bearer token'
```

`GET /user/<username>` -Shows the gists for that user that were added since the last visit.
```bash
curl --location --request GET 'http://34.88.192.29/user/choco-bot' \
--header 'Host: gist-scanner' \
--header 'Authorization: Bearer token'
```

### Server setup
* install Terraform
* install Ansible

Generate Google key.json and save it as infrastructure/key.json

Run terraform script to provision the infrastructure.
```bash
cd infrastructure
terraform init
terraform apply
```

## What can be improved?
* Add database support.
* Add more tests.
* Add more endpoints.
* Run application in K8s.
* Refactor IoC part.
* Ideally IoC, scanner and server should be in seperate repositories.

