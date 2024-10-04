
'''
{project: {
        claim: {<user-name>},
        resource: {<resource-name>: {}},
        name: <project-name>
    }
}
'''


class Tier(dict):
    '''

# project: <prj-nm>

                                           update            update
ln[0]  ln[1]   ln[2]      dict             stack             dict
#      <cat1>: <cat-va1>  d[<cat1>] = {}   push(d[<cat1>])   {project: {<category-value1>:{}}}
#      <cat2>: <cat-va2>  d[<cat2>] = {}   push(d[<cat2>)    {project: {<category-value2>:{}}}



    # <key>: <key-value>
    {
        "<category1>": {
            "<key>": {
                "category2": {
                    "key": {
                        "category3": "",
                        "category4": "",
                        ...
                    }
                }
            }
        }
    }
    '''
    def __init__(self, dictionary):
        # make refernce to the dictionary
        # dictionary should stay in memory
        # use like a copy, without copying
        for a in dictionary:
            self[a] =  dictionary[a]

    def find(self, key, dictionary=None):
        if not dictionary:
            dictionary = self

        if key in dictionary: return dictionary[key]
        for k, v in dictionary.items():
            if isinstance(v, dict):
                #print('parent', k)
                v['parent']=k
                item = self.find(key,v)
                if item is not None:
                    return item


def tier_test(status):

    #from source.component.markdown.project_string_default import ProjectStringDefault
    from pprint import pprint
    status.addTitle('Tier test')
    # filename_md = 'project_test_prj.md'
    # folderfilename_md = '{}/{}'.format(os.getcwd(), filename_md)
    # print('folderfilename_md', folderfilename_md)
    # resource_string = getProjectMDString(Tier(getProjectString())) # StringReader(folderfilename_md)
    # print('resource_string',resource_string)
    # project_dict = Tier(getProjectString())

    '''
    ?? Tree Stack ??
    # a:
    ## a1:
    # b:
    ## b1:

                lv  sz  pop     action                                         stack                           D
    l0 l1               sz-lv
                                                                                []                          {}
     # a:       1   0   -1      pop(-1)                                         []                          {}
                                lv==1 and len(D) == 0: D[L1]={a}                []                          {a:{<a>}}
                                                       push(D[L1])              [{<a>}]                     {a:{<a>}}
                                otherwise: Exception('Unknown Command')
    ## <a1>:    2   1   -1      pop(-1)                                         [{<a>}]                     {a:{<a>}}
                                lv>1 and len(D) == 0: Exception('Bad Tree')     
                                lv>1 and L1 in peek(): Exception('Duplicate')   
                                lv>1 and L1 not in peek(): peek()[L1]={<a1>}    [{1'a1':{<a1>}}]            {a:{1'a1':{<a1>}}}
                                lv>1 and sz == 0: Exception('Line out of order')
                                lv>1 and sz != 0: push(peek()[L1])              [{1'a1':{<a1>}},{<a1>}]     {a:{1'a1':{<a1>}}}
                                otherwise: Exception('Unknown Command')
    #  a:       1   2   1       pop(1)                                          [{1'a1':{<a1>}}]            {a:{1'a1':{<a1>}}}
                                lv==1 and len(D) > 0: ignore

    ## <a2>:    2   1   -1      pop(-1)                                         [{1<a1>:{<a1>}}]            {a:{1<a1>:{<a1>}}}
                                L1 in peek(): Exception('Duplicate')
                                L1 not in peek(): peek()[L1]={<a2>}                                         {a:{1<a1>:{<a1>},<a2>:{<a2>}}}
                                                  push(peek()[L1])              [{1<a1>:{<a1>}}]


    '''
    #print('A')

    #md_string = ProjectStringDefault()
    #print('md_string')
    #print(md_string)
    #print('B')

    dictionary = {'project': {'claim': {'api_admin': {'aud': 'lyttlebit',
                                                     'iss': 'sample_api_client',
                                                     'key': '?',
                                                     'name': 'api_admin',
                                                     'scope': 'api_admin',
                                                     'sub': 'client_api',
                                                     'user': 'client_api'},
                                       'api_guest': {'aud': 'lyttlebit',
                                                     'iss': 'sample_api_client',
                                                     'key': '0',
                                                     'name': 'api_guest',
                                                     'scope': 'api_guest',
                                                     'sub': 'client_api',
                                                     'user': 'client_api'},
                                       'api_user': {'aud': 'lyttlebit',
                                                    'iss': 'sample_api_client',
                                                    'key': '?',
                                                    'name': 'api_user',
                                                    'scope': 'api_user',
                                                    'sub': 'client_api',
                                                    'user': 'client_api'},
                                       'type': 'jwt'},
             'name': 'sample',
             'resources': {'account': {'active': 'y',
                                       'data': {'test': {'api_admin': {'displayname': 'Admin',
                                                                       'id': 'api_admin',
                                                                       'owner': 'api_admin@lyttlebit.com',
                                                                       'password': 'a1A!aaa',
                                                                       'scope': 'api_admin',
                                                                       'type': 'ACCOUNT',
                                                                       'username': 'api_admin@lyttlebit.com'},
                                                         'api_guest': {'displayname': 'Guest',
                                                                       'id': 'api_guest',
                                                                       'owner': 'api_guest@lyttlebit.com',
                                                                       'password': 'a1A!aaa',
                                                                       'scope': 'api_guest',
                                                                       'type': 'ACCOUNT',
                                                                       'username': 'api_guest@lyttlebit.com'},
                                                         'api_user': {'displayname': 'User',
                                                                      'id': 'api_user',
                                                                      'owner': 'api_user@lyttlebit.com',
                                                                      'password': 'a1A!aaa',
                                                                      'scope': 'api_user',
                                                                      'type': 'ACCOUNT',
                                                                      'username': 'api_user@lyttlebit.com'}}},
                                       'model': {'displayname': {'api_admin': 'R',
                                                                 'api_guest': 'CR',
                                                                 'api_user': 'RUD',
                                                                 'encrypt': 'N',
                                                                 'field': 'displayname',
                                                                 'size': '3-330',
                                                                 'type': 'C',
                                                                 'validate': 'R'},
                                                 'id': {'api_admin': 'R',
                                                        'api_guest': 'CR',
                                                        'api_user': 'RUD',
                                                        'encrypt': 'N',
                                                        'field': 'id',
                                                        'size': '3-330',
                                                        'type': 'C',
                                                        'validate': 'R'},
                                                 'owner': {'api_admin': 'R',
                                                           'api_guest': 'CR',
                                                           'api_user': 'RUD',
                                                           'encrypt': 'N',
                                                           'field': 'owner',
                                                           'size': '3-330',
                                                           'type': 'C',
                                                           'validate': 'R'},
                                                 'password': {'api_admin': '-',
                                                              'api_guest': 'CR',
                                                              'api_user': 'UD',
                                                              'encrypt': 'Y',
                                                              'field': 'password',
                                                              'size': '10-330',
                                                              'type': 'C',
                                                              'validate': 'R'},
                                                 'scope': {'api_admin': 'R',
                                                           'api_guest': 'CR',
                                                           'api_user': 'RUD',
                                                           'encrypt': 'N',
                                                           'field': 'scope',
                                                           'size': '3-330',
                                                           'type': 'C',
                                                           'validate': 'R'},
                                                 'type': {'api_admin': 'R',
                                                          'api_guest': 'CR',
                                                          'api_user': 'RUD',
                                                          'encrypt': 'N',
                                                          'field': 'type',
                                                          'size': '3-330',
                                                          'type': 'C',
                                                          'validate': 'R'},
                                                 'username': {'api_admin': 'R',
                                                              'api_guest': 'CR',
                                                              'api_user': 'RUD',
                                                              'encrypt': 'N',
                                                              'field': 'username',
                                                              'size': '3-330',
                                                              'type': 'C',
                                                              'validate': 'R'}},
                                       'schema': 'api',
                                       'version': '1.0.0'},
                           'sample_resource': {'active': 'y',
                                               'model': {'id': {'api_admin': 'R',
                                                                'api_guest': 'CR',
                                                                'api_user': 'RUD',
                                                                'encrypt': 'N',
                                                                'field': 'id',
                                                                'size': '3-330',
                                                                'type': 'C',
                                                                'validate': 'R'},
                                                         'owner': {'api_admin': 'R',
                                                                   'api_guest': 'CR',
                                                                   'api_user': 'RUD',
                                                                   'encrypt': 'N',
                                                                   'field': 'owner',
                                                                   'size': '3-330',
                                                                   'type': 'C',
                                                                   'validate': 'R'},
                                                         's_character': {'api_admin': 'R',
                                                                         'api_guest': 'CR',
                                                                         'api_user': 'RUD',
                                                                         'encrypt': 'N',
                                                                         'field': 's_character',
                                                                         'size': '3-330',
                                                                         'type': 'C',
                                                                         'validate': 'R'},
                                                         's_datetime': {'api_admin': 'R',
                                                                        'api_guest': 'CR',
                                                                        'api_user': 'RUD',
                                                                        'encrypt': 'N',
                                                                        'field': 's_datetime',
                                                                        'size': '3-330',
                                                                        'type': 'C',
                                                                        'validate': 'R'},
                                                         's_integer': {'api_admin': 'R',
                                                                       'api_guest': 'CR',
                                                                       'api_user': 'RUD',
                                                                       'encrypt': 'N',
                                                                       'field': 's_integer',
                                                                       'size': '3-330',
                                                                       'type': 'C',
                                                                       'validate': 'R'},
                                                         's_number': {'api_admin': '-',
                                                                      'api_guest': 'CR',
                                                                      'api_user': 'UD',
                                                                      'encrypt': 'Y',
                                                                      'field': 's_number',
                                                                      'size': '10-330',
                                                                      'type': 'C',
                                                                      'validate': 'R'},
                                                         'type': {'api_admin': 'R',
                                                                  'api_guest': 'CR',
                                                                  'api_user': 'RUD',
                                                                  'encrypt': 'N',
                                                                  'field': 'type',
                                                                  'size': '3-330',
                                                                  'type': 'C',
                                                                  'validate': 'R'}},
                                               'name': 'Sample_resource',
                                               'version': '0.0.0'}}}}
    '''
    project#<project_name1>
    project#<project_name2>
    project#<project_name2>#claim#<claim_name1>
    project#<project_name2>#claim#<claim_name2>
    project#<project_name2>#resource#<resource_name1>
    project#<project_name2>#resource#<resource_name1>#model...
    project#<project_name2>#resource#<resource_name1>#data...
    project#<project_name2>#resource#<resource_name2>
    project#<project_name2>#resource#<resource_name2>#model...
    project#<project_name2>#resource#<resource_name2>#data...
    '''
    actual = Tier(dictionary)
    # actual = Tier(ProjectStringDefault())
    #print('actual')
    #pprint(actual)
    #print('actual', actual)
    status.assert_test ("'project' in actual", 'project' in actual)

    #print('actual find',actual.find('claim'))
    #print('actual find',actual.find('resources'))
    #claims = Tier1(actual.find('claim'))
    #print('claims', claims)

    status.assert_test ("'resources' in Tier(dictionary)", 'resources' in actual['project'])

    status.assert_test ("'account' in project_dict['project']['resources']", 'account' in actual['project']['resources'])
    status.assert_test ("'model' in project_dict['project']['resources']['account']", 'model' in actual['project']['resources']['account'])
    #status.assert_test ("'rows' in project_dict['project']['resources']['account']['model']", 'rows' in actual['project']['resources']['account']['model'])
    status.assert_test ("'sample_resource' in project_dict['project']['resources']", 'sample_resource' in actual['project']['resources'])
    status.assert_test ("'model' in project_dict['project']['resources']['sample_resource']", 'model' in actual['project']['resources']['sample_resource'])
    #status.assert_test ("'rows' in project_dict['project']['resources']['sample_resource']['model']", 'rows' in actual['project']['resources']['sample_resource']['model'])

    #print(status)


def main(status):

    tier_test(status)


if __name__ == "__main__":
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))