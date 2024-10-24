from source.component.markdown.pattern import Pattern

class ResourcePatterns(dict):
    def __init__(self, project_dict, project_name, resource_name):
        # return {'account': {'id': {'pattern': '^.{3,330}$'}, 'type': {'pattern': '^.{3,330}$'}, ...}}
        resource_list = project_dict['project'][project_name]['resources']

        if resource_name:
            resource_list = {r: resource_list[r] for r in resource_list if r == resource_name}
        for r in project_dict['project'][project_name]['resources']:
            # {account: {}, ...}
            self[r] = {}
            for m in project_dict['project'][project_name]['resources'][r]['model']:
                #print('m',m,project_dict['project']['resources'][r]['model'])
                for fld in project_dict['project'][project_name]['resources'][r]['model']:

                    if fld not in self[r]:
                        self[r][fld]={}
                    self[r][fld]['pattern']=Pattern(project_dict['project'][project_name]['resources'][r]['model'][fld])
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

def test_resource_patterns(status):
    from source.component.markdown.tier_md import TierMD
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.helper.project_name_first import ProjectNameFirst
    from pprint import pprint
    # Trunk
    #pprint(TierMD(ProjectStringDefault())) #['project']['resources']
    status.addTitle('Resource Patterns test')
    project = TierMD(ProjectStringDefault()) #['project']['resources']
    #pprint(project_dict)
    actual = ResourcePatterns(project, ProjectNameFirst(project),'account')
    #print('   resource_patterns:', actual)
    status.assert_test("'account' in {}".format(actual),'account' in actual)

    #print('actual', actual)
    status.assert_test ("'id' in {}".format(actual['account']), 'id' in actual['account'])
    status.assert_test ("'pattern' in {}".format(actual['account']['id']), 'pattern' in actual['account']['id'])

def main(status):
    test_resource_patterns(status)


if __name__ == "__main__":
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))