# Project: 
1. name: test_prj
1. schema: api
1. version: 1.0.0

process
p#r#m#f#
[r for r in project]
[m for m in resource]
[f for f in model]
project#<project>
project#<project>#schema#<schema>
project#<project>#version#<version>

## Claim:
1. name: jwt

project#<project>#claim#jwt#name#<name>
????

| name      | aud                 | iss                       | sub        | user       | scope     | key |
|-----------|---------------------|---------------------------|------------|------------|-----------|-----|
| api_admin | test_org | test_prj_api_client | client_api | client_api | api_admin | ?   |
| api_guest | test_org | test_prj_api_client | client_api | client_api | api_guest | 0   |
| api_user  | test_org | test_prj_api_client | client_api | client_api | api_user  | ?   |

* ? means value is unknown until runtime
* table name is dependent on project name

## Resources
### Account
    User accounts

1. active: y

#### Model:

| field       | type | size   | validate | encrypt | api_admin | api_guest | api_user |
|-------------|------|--------|----------|---------|-----------|-----------|----------|
| id          | C    | 3-330  | R        | N       | R         | CR        | RUD      |
| type        | C    | 3-330  | R        | N       | R         | CR        | RUD      |
| owner       | C    | 3-330  | R        | N       | R         | CR        | RUD      |
| username    | C    | 3-330  | R        | N       | R         | CR        | RUD      |
| displayname | C    | 3-330  | R        | N       | R         | CR        | RUD      |
| password    | C    | 10-330 | R        | Y       | -         | CR        | UD       |
| scope       | C    | 3-330  | R        | N       | R         | CR        | RUD      |

account_del(Token, Owner, Id),  DELETE, U
account(Token, Owner, Id),      GET,    AUG
account(Token, Owner, Form),    POST,   U
account(Token, Owner, Id, Form),PUT,    U

Types
* C is character, any keyboard character
* L is logical aka boolean, eg ‘True', ‘False', ’T', ‘F', ‘Y', ’N', ‘1', ‘0' 
* N is numeric, eg ‘1' or ‘1.1' or ‘-1.1' 
* D is datetime, eg '2024-06-23' or '2024-06-23 18:30:00'

Roles
* C is Create in the db
* R is Read from the db
* U is Update in the db
* D is Delete from the db
* \- is None, space holder

#### Data:
Default account data

##### Test:

| id        | type    | owner                    | username                | displayname | password | scope     |
|-----------|---------|--------------------------|-------------------------|-------------|----------|-----------|
| api_admin | ACCOUNT | api_admin@lyttlebit.com  | api_admin@lyttlebit.com | Admin       | a1A!aaaa | api_admin |
| api_guest | ACCOUNT | api_guest@lyttlebit.com  | api_guest@lyttlebit.com | Guest       | a1A!aaaa | api_guest |
| api_user  | ACCOUNT | api_user@lyttlebit.com   | api_user@lyttlebit.com  | User        | a1A!aaaa | api_user  |

* Do not use same passwords in production
* Set type to capitalized(resource)
* ? means value is unknown until runtime
* - means not applicable

### Drain

1. active: y

#### Model:

| field | type | size | validate | encrypt | api_admin | api_guest | api_user |
|-------|-----|--|---------|--------|----------|---------|-------|
| id    | C   | 3-330 | R       | N      | R        | CR      | RUD   |
| type  | C   | 3-330 | R       | N      | R        | CR      | RUD   |
| owner | C   | 3-330 | R       | N      | R        | CR      | RUD   |
| lat   | N   | 14,6 | R       | N      | R        | CR      | RUD   |
| lon   | N   | 14,6 | R       | N      | R        | CR      | RUD   |
| alt   | N   | 10,4 | R       | N      | R        | CR      | RUD   |
