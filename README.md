# Gist Scanner


Using the Github API query user’s publicly available github gists and
create activity in Pipedrive for each gist. Application periodically
checks for a user's publicly available gists. 

Application has two web endpoints
* First shows all users that have been scanned.
* Second shows the gists for that user that were added since the last visit.

### Stack:
 * 🐍 Python 3.10 for scanning gists
 * Flask 2.1.3 for simple server
 * 🐋 Docker + Docker Compose


### How to run the application
1. Specify the `USER_LIST_TYPE` environment variable to either `env` or `file`
   - If `USER_LIST_TYPE` is `env` then specify users in the `USER_LIST` environment variable as comma seperated list. For example `USER_LIST: user1,user2,user3`
   - If `USER_LIST_TYPE` is `file` then add users to the `scanner/input/users.txt` file.
2. Set the `GITHUB_TOKEN` environment variable to the github token for the user.
3. Set the `PIPEDRIVE_TOKEN` environment variable to the pipedrive token for the user.
4. Run the application with `docker-compose up` 🚀
5. Check the application logs 📜 and your Pipedrive activities list 📝

### Endpoints

There are Bearer Token Authorization.

Default token is `token`. You can set your own token by setting the `BEARER_TOKEN` environment variable for the server.
* `/users` - Shows all users that have been scanned.
* `/user/<username>` - Shows the gists for that user that were added since the last visit.


### Docker environment variables
#### Scanner
* `PIPEDRIVE_API_KEY` - Pipedrive API key
* `GITHUB_API_KEY` - Github API key
* `USER_LIST_TYPE` - env or file
  * if `USER_LIST_TYPE` is env you can use `USER_LIST`
  * `USER_LIST` - comma separated list of users to scan
  * if `USER_LIST_TYPE` is file you can use `USER_LIST_FILE`
  * `USER_LIST_FILENAME` text file with list of users to scan. if not specified, it will be `users.txt`
* `SCANNER_HOUR_INTERVAL` - period of time in hours to scan for new gists. if not specified, it will be `3`
* `SCANNER_MINUTE_INTERVAL` - period of time in minutes to scan for new gists. if not specified, it will be `0`

#### Server
* `SERVER_PORT` - port to run the server on. if not specified, it will be `5000`
* `APP_ENV` - environment to run the application. if not specified, it will be `development`
* `BEARER_TOKEN` - bearer token to use for authentication. if not specified, it will be `token`