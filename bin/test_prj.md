# Project: sample
    1. schema: api
    1. version: 1.0.0

## Claim:

| name      | aud       | iss                | sub        | user       | scope     | key |
|-----------|-----------|--------------------|------------|------------|-----------|-----|
| api_admin | lyttlebit | sample_api_client  | client_api | client_api | api_admin | ?   |
| api_guest | lyttlebit | sample_api_client  | client_api | client_api | api_guest | 0   |
| api_user  | lyttlebit | sample_api_client  | client_api | client_api | api_user  | ?   |

## Resources
### Account
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
* C is Create
* R is Read
* U is Update
* D is Delete
* - is None

#### Data:

| id        | type    | owner                    | username                | displayname | password | scope     |
|-----------|---------|--------------------------|-------------------------|-------------|----------|-----------|
| api_admin | ACCOUNT | api_admin@lyttlebit.com  | api_admin@lyttlebit.com | Admin       | a1A!aaa  | api_admin |
| api_guest | ACCOUNT | api_guest@lyttlebit.com  | api_guest@lyttlebit.com | Guest       | a1A!aaa  | api_guest |
| api_user  | ACCOUNT | api_user@lyttlebit.com   | api_user@lyttlebit.com  | User        | a1A!aaa  | api_user  |

* Do not use same passwords in production
* Set type to capitalized(resource)
* ? means value is unknown until runtime
* - means not applicable


### Sample_resource
1. version: 1.0.0

#### Model:

| field       | type | size   | validate | encrypt | api_admin | api_guest | api_user |
|-------------|------|--------|----------|---------|-----------|-----------|----------|
| id          | C    | 3-330  | R        | N       | R         | CR        | RUD      |
| type        | C    | 3-330  | R        | N       | R         | CR        | RUD      |
| owner       | C    | 3-330  | R        | N       | R         | CR        | RUD      |
| s_integer   | C    | 3-330  | R        | N       | R         | CR        | RUD      |
| s_character | C    | 3-330  | R        | N       | R         | CR        | RUD      |
| s_number    | C    | 10-330 | R        | Y       | -         | CR        | UD       |
| s_datetime  | C    | 3-330  | R        | N       | R         | CR        | RUD      |

server_ext.js
+ ------------------------ +
+ require(route_const.js)  + <-- route_const.js
+                          +
+ require(route_list.js)   + <-- route_list.js
+ ------------------------ +