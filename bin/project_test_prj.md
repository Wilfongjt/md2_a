# Project: test_prj

## Claims:

| name      | aud                 | iss                       | sub        | user       | scope     | key |
|-----------|---------------------|---------------------------|------------|------------|-----------|-----|
| api_admin | test_org | test_prj_api_client | client_api | client_api | api_admin | ?   |
| api_guest | test_org | test_prj_api_client | client_api | client_api | api_guest | 0   |
| api_user  | test_org | test_prj_api_client | client_api | client_api | api_user  | ?   |

* ? means value is unknown until runtime
* table name is dependent on project name

## Resources

### Account
Default resource

1. version: 1.0.0

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

| id        | type    | owner                    | username                | displayname | password | scope     |
|-----------|---------|--------------------------|-------------------------|-------------|----------|-----------|
| api_admin | ACCOUNT | api_admin@lyttlebit.com  | api_admin@lyttlebit.com | Admin       | a1A!aaa  | api_admin |
| api_guest | ACCOUNT | api_guest@lyttlebit.com  | api_guest@lyttlebit.com | Guest       | a1A!aaa  | api_guest |
| api_user  | ACCOUNT | api_user@lyttlebit.com   | api_user@lyttlebit.com  | User        | a1A!aaa  | api_user  |

* Do not use same passwords in production
* Set type to capitalized(resource)
* \- means not applicable
  