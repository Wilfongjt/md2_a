# Project: sample

## Claims:

1. name: starter-api
1. iss: lyttlebit
1. aud: starter-api_client
1. sub: client_api  

## Resource:

| resource | field       | type     | api_admin | api_guest | api_user |
|----------|-------------|----------|-----------|-----------|----------|
| account  | id          | string   | R         | C         | RUD      |
| account  | type        | ACCOUNT  | R         | C         | RUD      |
| account  | owner       | string   | R         | C         | RUD      |
| account  | username    | string   | R         | C         | RUD      |
| account  | displayname | string   | R         | C         | RUD      |
| account  | password    | password |           | C         | UD       |
| account  | scope       | string   | R         | C         | RUD      |

### Data:

| data    | id | type    | owner                    | username                | displayname | password | scope     |
|---------|----|---------|--------------------------|-------------------------|-------------|----------|-----------|
| account | #  | ACCOUNT | api_admin@lyttlebit.com  | api_admin@lyttlebit.com | Admin       | a1A!aaa  | api_admin |
| account | #  | ACCOUNT | api_guest@lyttlebit.com  | api_guest@lyttlebit.com | Guest       | a1A!aaa  | api_guest |
| account | #  | ACCOUNT | api_user@lyttlebit.com   | api_user@lyttlebit.com  | User        | a1A!aaa  | api_user  |
