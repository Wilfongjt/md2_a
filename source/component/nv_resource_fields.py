
from source.component.nv_list import NVList
from source.component.nv_field import NVField
from pprint import pprint
import os

class NVResourceFields(NVList):
    # NV all resource fields
    # apply to a template
    def __init__(self, project_dict, project_name, resource_name):
        # upsert = True
        # print('B resource_name', resource_name)
        if resource_name not in project_dict['project'][project_name]['resources']:
            raise Exception('Resource Fields Not Found: {}'.format(resource_name))
        #print('NVResourceFields')
        #pprint(project_dict['project'][project_name]['resources'])
        for field_name in project_dict['project'][project_name]['resources'][resource_name]['model']:
            # print('NVResourceFields', resource_name)
            self.extend(NVField(project_dict, project_name, resource_name, field_name=field_name))
        #for row in project_dict['project'][project_name]['resources'][resource_name]['model']['rows']:
        #    # print('NVResourceFields', resource_name)
        #    self.extend(NVField(project_dict, project_name, resource_name, row['field']))
def test_nv_resource_fields(status):
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD
    status.addTitle('NVResourceField test')
    #if 'PY_TEST' in os.environ and eval(os.environ['PY_TEST']):
    #    print('NVResourceFields test')
    actual = NVResourceFields(TierMD(ProjectStringDefault()), 'sample', 'account')
    #print('  nv_resource_fields:', actual)
    #pprint(actual)

    #print('given: {}'.format(actual))
    tests=list()
    #tests.append({'name': '<<API_RESOURCE>>', 'value': 'account'} )
    tests.append({'name': '<<ID_NAME>>', 'resource': 'account', 'value': 'id'})
    tests.append({'name': '<<ID_SIZE_MIN>>', 'value': 3, 'resource': 'account'})
    tests.append({'name': '<<ID_SIZE_MAX>>', 'value': 330, 'resource': 'account'})
    tests.append({'name': '<<ID_RESOURCE>>', 'value': 'account', 'resource': 'account'})
    tests.append({'name': '<<ID_PATTERN>>', 'value': '^.{3,330}$', 'resource': 'account'})
    tests.append({'name': '<<OWNER_NAME>>', 'value': 'owner', 'resource': 'account'})
    tests.append({'name': '<<OWNER_SIZE_MIN>>', 'value': 3, 'resource': 'account'})
    tests.append({'name': '<<OWNER_SIZE_MAX>>', 'value': 330, 'resource': 'account'})
    tests.append({'name': '<<OWNER_RESOURCE>>', 'value': 'account', 'resource': 'account'})
    tests.append({'name': '<<OWNER_PATTERN>>', 'value': '^.{3,330}$', 'resource': 'account'})

    # status.addLine('given: {}'.format(actual))
    for test in tests:

        assert (test in actual)
        status.addBullet('{} in actual ok'.format(test))
    '''
    assert ({'name': '<<ID_NAME>>', 'resource': 'account', 'value': 'id'} in actual)
    assert ({'name': '<<ID_SIZE_MIN>>', 'resource': 'account', 'value': 3} in actual)
    assert ({'name': '<<ID_SIZE_MAX>>', 'resource': 'account', 'value': 330} in actual)
    assert ({'name': '<<ID_RESOURCE>>', 'resource': 'account', 'value': 'account'} in actual)
    assert ({'name': '<<ID_PATTERN>>', 'value': '^.{3,330}$', 'resource': 'account'} in actual)

    assert ({'name': '<<OWNER_NAME>>', 'value': 'owner', 'resource': 'account'} in actual)
    assert ({'name': '<<OWNER_SIZE_MIN>>', 'value': 3, 'resource': 'account'} in actual)
    assert ({'name': '<<OWNER_SIZE_MAX>>', 'value': 330, 'resource': 'account'} in actual)
    assert ({'name': '<<OWNER_RESOURCE>>', 'value': 'account', 'resource': 'account'} in actual)
    assert ({'name': '<<OWNER_PATTERN>>', 'value': '^.{3,330}$', 'resource': 'account'} in actual)
    '''


def main(status):

    test_nv_resource_fields(status)

if __name__ == "__main__":
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))