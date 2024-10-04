class ProjectStringDefault(str):
    def __new__(cls):

        contents = '''
    # Project: 
    ## sample:
    1. name: sample
    
    ### Claim:
    1. type: jwt
    
    | name      | aud       | iss                | sub        | user       | scope     | key |
    |-----------|-----------|--------------------|------------|------------|-----------|-----|
    | api_admin | lyttlebit | sample_api_client  | client_api | client_api | api_admin | ?   |
    | api_guest | lyttlebit | sample_api_client  | client_api | client_api | api_guest | 0   |
    | api_user  | lyttlebit | sample_api_client  | client_api | client_api | api_user  | ?   |
    
    * ? means value is unknown until runtime
    * table name is dependent on project name

    ### Resources
    #### Account
        User accounts
    1. schema: api
    1. version: 1.0.0
    1. active: y

    ##### Model:
    resource.model 
    
    | name        | type | size   | validate | encrypt |
    |-------------|------|--------|----------|---------|
    | id          | C    | 3-330  | R        | N       |
    | type        | C    | 3-330  | R        | N       |
    | owner       | C    | 3-330  | R        | N       |
    | username    | C    | 3-330  | R        | N       |  
    | displayname | C    | 3-330  | R        | N       |
    | password    | C    | 10-330 | R        | Y       |
    | scope       | C    | 3-330  | R        | N       |
    
    Types
    * C is character, any keyboard character
    * L is logical aka boolean, eg ‘True', ‘False', ’T', ‘F', ‘Y', ’N', ‘1', ‘0' 
    * N is numeric, eg ‘1' or ‘1.1' or ‘-1.1' 
    * D is datetime, eg '2024-06-23' or '2024-06-23 18:30:00'
    
    ##### Scope:
    resource.scope
     
    | name        | api_admin | api_guest | api_user |
    |-------------|-----------|-----------|----------|
    | id          | R         | CR        | RUD      |
    | type        | R         | CR        | RUD      |
    | owner       | R         | CR        | RUD      |
    | username    | R         | CR        | RUD      |    
    | displayname | R         | CR        | RUD      |
    | password    | -         | CR        | UD       |
    | scope       | R         | CR        | RUD      |
    
    Privileges
    * C is Create
    * R is Read
    * U is Update
    * D is Delete
    * - is None

    ##### Data:
    ###### Test:
    
    | id        | type    | owner                    | username                | displayname | password | scope     |
    |-----------|---------|--------------------------|-------------------------|-------------|----------|-----------|
    | api_admin | ACCOUNT | api_admin@lyttlebit.com  | api_admin@lyttlebit.com | Admin       | a1A!aaa  | api_admin |
    | api_guest | ACCOUNT | api_guest@lyttlebit.com  | api_guest@lyttlebit.com | Guest       | a1A!aaa  | api_guest |
    | api_user  | ACCOUNT | api_user@lyttlebit.com   | api_user@lyttlebit.com  | User        | a1A!aaa  | api_user  |

    * Do not use same passwords in production
    * Set type to capitalized(resource)
    * ? means value is unknown until runtime
    * - means not applicable

    '''.replace('    ', '')

        instance = super().__new__(cls, contents)
        return instance

def main():
    from pprint import pprint
    from source.component.markdown.tier_md import TierMD
    from source.component.markdown.helper.project_name import ProjectName
    from source.component.markdown.helper.project_claim_type import ProjectClaimType

    actual = TierMD(ProjectStringDefault())
    pprint(actual)
    assert ('project' in actual)
    assert ('sample' in actual['project'])
    assert ('resources' in actual['project']['sample'])

    assert ('claim' in actual['project']['sample'])

    assert (ProjectName(actual)=='sample')
    assert (ProjectClaimType(actual,'sample')=='jwt')


if __name__ == "__main__":
    # execute as docker
    main()