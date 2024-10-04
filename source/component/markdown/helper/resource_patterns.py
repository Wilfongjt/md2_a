from source.component.markdown.pattern import Pattern

class ResourcePatterns(dict):
    def __init__(self, project_dict, resource_name):
        # return {'account': {'id': {'pattern': '^.{3,330}$'}, 'type': {'pattern': '^.{3,330}$'}, ...}}
        resource_list = project_dict['project']['resources']

        if resource_name:
            resource_list = {r: resource_list[r] for r in resource_list if r == resource_name}
        for r in project_dict['project']['resources']:
            # {account: {}, ...}
            self[r] = {}
            for m in project_dict['project']['resources'][r]['model']:
                #print('m',m,project_dict['project']['resources'][r]['model'])
                for fld in project_dict['project']['resources'][r]['model']:

                    if fld not in self[r]:
                        self[r][fld]={}
                    self[r][fld]['pattern']=Pattern(project_dict['project']['resources'][r]['model'][fld])
                    #print('fld', fld, project_dict['project']['resources'][r]['model'][fld])

                '''
                for row in project_dict['project']['resources'][r]['model']['rows']:

                    for fld in row:
                        if fld == 'field':
                            # {account: {id: {}, ...}, ...}
                            self[r][row[fld]] = {}
                            # fld_key= fld

                        # {account: {id: {pattern: ^.{3,330}$, ... }, ...}, ...}
                        self[r][row['field']]['pattern'] = Pattern(row)
                '''

def test_resource_patterns():
    from source.component.markdown.tier_md import TierMD
    from source.component.markdown.project_string_default import ProjectStringDefault
    from pprint import pprint
    # Trunk
    #pprint(TierMD(ProjectStringDefault())) #['project']['resources']


    project = TierMD(ProjectStringDefault()) #['project']['resources']
    pprint(project)
    actual = ResourcePatterns(project, 'account')
    print('   resource_patterns:', actual)
    assert ('account' in actual)
    #print('actual', actual)
    assert ('id' in actual['account'])
    assert ('pattern' in actual['account']['id'])

def main():
    test_resource_patterns()


if __name__ == "__main__":
    # execute as docker
    main()
