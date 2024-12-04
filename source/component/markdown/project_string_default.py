class ProjectStringDefault(str):
    def __new__(cls):

        contents = '''
    # Project: 
    
    1. name: sample
    
    ## Claims:
    Claims(project_dict, scope=None) --> {api_admin: {...}, api_guest: {...}, api_user: {...}}
    Claims(project_dict, scope=api_admin) --> {api_admin: {...}}
    
    1. type: jwt
    
    | name      | aud       | iss                | sub        | user       | scope     | key |
    |-----------|-----------|--------------------|------------|------------|-----------|-----|
    | api_admin | lyttlebit | sample_api_client  | client_api | client_api | api_admin | ?   |
    | api_guest | lyttlebit | sample_api_client  | client_api | client_api | api_guest | 0   |
    | api_user  | lyttlebit | sample_api_client  | client_api | client_api | api_user  | ?   |
    
    * ? means value is unknown until runtime
    * table name is dependent on project_dict name

    ## Resources
    Resources(project_dict) --> {account: {active: 1, schema: api, major: 00, minor: 00, patch:00}, resource1: {...},...}
    Resources(project_dict, account) --> {account: {active: 1, schema: api, major: 00, minor: 00, patch:00}}
    
    ### Account
        User accounts
    1. active: Y
    1. schema: api
    1. major: 00
    1. minor: 00
    1. patch: 00
    
    ## Models:
    ### Account:
    | name        | type | size   | validate | encrypt | default  | required |
    |-------------|------|--------|----------|---------|----------|----------|
    | id          | C    | 3-330  | R        | N       | ?        | 1        |
    | type        | C    | 3-330  | R        | N       | ?        | 1        |
    | owner       | C    | 3-330  | R        | N       | ?        | 1        |
    | username    | C    | 3-330  | R        | N       | ?        | 1        |  
    | displayname | C    | 3-330  | R        | N       | ?        | 1        |
    | password    | C    | 10-330 | R        | Y       | ?        | 1        |
    | scope       | C    | 3-330  | R        | N       | api_user | 1        |
    | active      | L    | 1-1    | R        | N       | 1        | 1        |
    
    
    Types
    * C is character, any keyboard character
    * L is logical aka boolean, eg ‘True', ‘False', ’T', ‘F', ‘Y', ’N', ‘1', ‘0' 
    * N is numeric, eg ‘1' or ‘1.1' or ‘-1.1' 
    * D is datetime, eg '2024-06-23' or '2024-06-23 18:30:00'
    
    ## Privileges:
    ### Account:
    | name      | id  | type | owner | username | displayname | password | scope | active |
    |-----------|-----|------|-------|----------|-------------|----------|-------|--------|
    | api_admin | R   | R    | R     | R        | R           | -        | R     | R      |
    | api_guest | CR  | CR   | CR    | CR       | CR          | CR       | CR    | CR     |
    | api_user  | RUD | RUD  | RUD   | RUD      | RUD         | UD      | RUD   | RUD    |  
    
    Privileges
    * C is Create
    * R is Read
    * U is Update
    * D is Delete
    * - is None

    ## Tests:
    ### Account:
  
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

def main(status):
    status.addTitle('Project String Default test')
    from pprint import pprint
    from source.component.markdown.tier_md import TierMD
    from source.component.markdown.helper.project_name import ProjectName
    from source.component.markdown.helper.project_claim_type import ProjectClaimType

    actual = TierMD(ProjectStringDefault())
    pprint(actual)
    status.assert_test("'project' in {}".format(actual), 'project' in actual)

    status.assert_test("'claims' in {}".format(actual['project']), 'claims' in actual['project'])
    status.assert_test("'models' in {}".format(actual['project']), 'models' in actual['project'])

    status.assert_test("'privileges' in {}".format(actual['project']), 'privileges' in actual['project'])
    status.assert_test("'resources' in ".format(actual['project']), 'resources' in actual['project'])

    #status.assert_test("".format(actual), ProjectName(actual)=='sample')
    #status.assert_test("".format(actual), ProjectClaimType(actual,'sample')=='jwt')


if __name__ == "__main__":
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))
