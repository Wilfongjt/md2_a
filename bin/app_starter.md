# project:
1. name: starter-api
1. issuer: lyttlebit
1. audience: starter-api_client
1. subject: client_api

## owner:
### api_admin:
1. id: api_admin@lyttlebit.com
1. type: ACCOUNT
1. username: api_admin@lyttlebit.com
1. displayname: J
1. password: a1A!aaaa
1. scope: api_admin

### api_guest:
1. id: api_guest@lyttlebit.com
1. type: ACCOUNT
1. username: api_guest@lyttlebit.com
1. displayname: J
1. password: a1A!aaaa
1. scope: api_guest

### api_user:
1. id: api_user@lyttlebit.com
1. type: ACCOUNT
1. username: api_user@lyttlebit.com
1. displayname: J
1. password: a1A!aaaa
1. scope: api_user

## resource:
### account:
##### account_delete_kop:
1. resource: account
1. method: delete
1. key: account_delete_kop
1. active: 1
1. description: describe me
1. test_type: single
1. scope: [api_user, api_admin, api_guest]
1. project_name: starter-api
parameter: [{name:token_id,type:TOKEN},{name:owner_id,type:OWNERID},{name:primary_key,type:PRIMARYKEY}]
source: generate
version:000
method: delete
return: JSONB
type: account
###### name:
group:account
name:account_del
kind:api
version:0_0_1
###### test_data:
1. id: replace_id
1. type: replace_type
1. owner: replace_owner

##### account_get_kop:
1. resource: account
1. key:account-get_kop
1. active: 1
1. description: describe me
1. source: generate
1. version:000
1. method: get
1. return: JSONB
1. type: account
1. test_type: single
1. scope: [api_user, api_admin, api_guest]
1. parameter: [{name:token_id,type:TOKEN},{name:owner_id,type:OWNERID},{name:primary_key,type:PRIMARYKEY}]
1. project_name: starter-api
###### name:
1. group:account
1. name:account
1. kind:api
1. version:0_0_1
###### test_data:
1. id: replace_id
1. type: replace_type_id
1. owner: replace_owner_id

##### account_get_km:
1. resource: account
1. key:account_get_km
1. active: 1
1. description: describe me
1. source: generate
1. version:000
1. method: get
1. return: JSONB
1. type: account
1. test_type: single
1. scope: [api_guest]
1. parameter: [{name:token_id,type:TOKEN},{name:m_b_r,type:MBR}]
1. project_name: starter-api
1. mbr: {north: 2.0,south: 0.0,west: 0.0,east: 2.0}
###### name:
1. group:account
1. name:account
1. kind:api
1. version:0_0_1
###### test_data:
1. id: replace_id
1. type: replace_type_id
1. owner: replace_owner_id

##### account_post_tor:
1. resource: account
1. key:account_post_tor
1. active: 1
1. description: describe me
1. source: generate
1. version:000
1. method: post
1. return: JSONB
1. type: account
1. test_type: single
1. scope: [api_user, api_admin, api_guest]
1. parameter: [{name:token_id,type:TOKEN},{name:owner_id,type:OWNERID},{name:trip,type:TRIPLE}]
1. project_name: starter-api
###### name:
1. group:account
1. name:account
1. kind:api
1. version:0_0_1
###### test_data:
1. id: replace_id
1. type: replace_type_id
1. owner: replace_owner_id

##### account_put_topt:
1. resource: account
1. key:account_put_topt
1. active: 1
1. description: describe me
1. source: generate
1. version:000
1. method: put
1. return: JSONB
1. type: account
1. test_type: single
1. scope: [api_user, api_admin, api_guest]
1. parameter: [{name:token_id,type:TOKEN},{name:owner_id,type:OWNERID},{name:primary_key,type:PRIMARYKEY},{name:trip,type:TRIPLE}]
1. project_name: starter-api
###### name:
1. group:account
1. name:account
1. kind:api
1. version:0_0_1
###### test_data:
1. id: replace_id
1. type: replace_type_id
1. owner: replace_owner_id

er