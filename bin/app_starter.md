# Project: sample

## Claims:

| name      | aud       | iss                | sub        | user       | scope     | key |
|-----------|-----------|--------------------|------------|------------|-----------|-----|
| api_admin | lyttlebit | sample_api_client  | client_api | client_api | api_admin | ?   |
| api_guest | lyttlebit | sample_api_client  | client_api | client_api | api_guest | 0   |
| api_user  | lyttlebit | sample_api_client  | client_api | client_api | api_user  | ?   |

## Resources

### Account
1. version: 1.0.0

#### Model:

| field       | type | size   | validate | pattern       | encrypt | api_admin | api_guest | api_user |
|-------------|------|--------|----------|---------------|---------|-----------|-----------|----------|
| id          | C    | 3-330  | R        | '^.{3,330}$'  | N       | R         | CR        | RUD      |
| type        | C    | 3-330  | R        | '^.{3,330}$’  | N       | R         | CR        | RUD      |
| owner       | C    | 3-330  | R        | '^.{3,330}$'  | N       | R         | CR        | RUD      |
| username    | C    | 3-330  | R        | '^.{3,330}$'  | N       | R         | CR        | RUD      |
| displayname | C    | 3-330  | R        | '^.{3,330}$'  | N       | R         | CR        | RUD      |
| password    | C    | 10-330 | R        | '^.{10,330}$' | Y       | -         | CR        | UD       |
| scope       | C    | 3-330  | R        | '^.{3,330}$'  | N       | R         | CR        | RUD      |

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
