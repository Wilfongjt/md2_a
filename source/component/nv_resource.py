
from source.component.nv_list import NVList
#from .nv_list import NVList
from source.component.nv_resource_fields import NVResourceFields
from pprint import pprint
import os

class NVResource(NVList):  # name value resource
    # NV a resource_name
    # apply to a template
    # NVResource(project_dict, resource_name)
    def __init__(self, project_dict, project_name, resource_name):
        if not project_name in project_dict['project']:
            raise Exception('Project Name Not Found: {}'.format(project_name))
        #print('NVResource')
        #pprint(project_dict)
        if not resource_name in project_dict['project'][project_name]['resources']:
            raise Exception('Resource Name Not Found: {}'.format(resource_name))

        self.add({'name': '<<API_RESOURCE>>', 'value': resource_name})
        # print('NVResource', resource_name)
        self.extend(NVResourceFields(project_dict, project_name, resource_name))

def test_nv_resource(status):
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD
    #if 'PY_TEST' in os.environ and eval(os.environ['PY_TEST']):
    #    print('NVResource test')
    status.addTitle('NVResource test')
    actual = NVResource(TierMD(ProjectStringDefault()), 'sample', 'account')
    #print('         nv_resource:', actual)
    #print('given: {}'.format(actual))
    tests=list()
    tests.append({'name': '<<API_RESOURCE>>', 'value': 'account'} )
    tests.append({'name': '<<ID_NAME>>', 'value': 'id', 'resource': 'account'})
    tests.append({'name': '<<ID_SIZE_MIN>>', 'value': 3, 'resource': 'account'})
    tests.append({'name': '<<ID_SIZE_MAX>>', 'value': 330, 'resource': 'account'})
    tests.append({'name': '<<ID_RESOURCE>>', 'value': 'account', 'resource': 'account'})
    tests.append({'name': '<<ID_PATTERN>>', 'value': '^.{3,330}$', 'resource': 'account'})
    tests.append({'name': '<<OWNER_NAME>>', 'value': 'owner', 'resource': 'account'})
    tests.append({'name': '<<OWNER_SIZE_MIN>>', 'value': 3, 'resource': 'account'})
    tests.append({'name': '<<OWNER_SIZE_MAX>>', 'value': 330, 'resource': 'account'})
    tests.append({'name': '<<OWNER_RESOURCE>>', 'value': 'account', 'resource': 'account'})
    tests.append({'name': '<<OWNER_PATTERN>>', 'value': '^.{3,330}$', 'resource': 'account'})

    for test in tests:
        assert (test in actual)
        status.addBullet('{} in actual ok'.format(test))

    #assert ({'name': '<<API_RESOURCE>>', 'value': 'account'} in actual)
    #assert ({'name': '<<ID_NAME>>', 'value': 'id', 'resource': 'account'} in actual)
    #assert ({'name': '<<ID_SIZE_MIN>>', 'value': 3, 'resource': 'account'} in actual)
    #assert ({'name': '<<ID_SIZE_MAX>>', 'value': 330, 'resource': 'account'} in actual)
    #assert ({'name': '<<ID_RESOURCE>>', 'value': 'account', 'resource': 'account'} in actual)
    #assert ({'name': '<<ID_PATTERN>>', 'value': '^.{3,330}$', 'resource': 'account'} in actual)
    #assert ({'name': '<<OWNER_NAME>>', 'value': 'owner', 'resource': 'account'} in actual)
    #assert ({'name': '<<OWNER_SIZE_MIN>>', 'value': 3, 'resource': 'account'} in actual)
    #assert ({'name': '<<OWNER_SIZE_MAX>>', 'value': 330, 'resource': 'account'} in actual)
    #assert ({'name': '<<OWNER_RESOURCE>>', 'value': 'account', 'resource': 'account'} in actual)
    #assert ({'name': '<<OWNER_PATTERN>>', 'value': '^.{3,330}$', 'resource': 'account'} in actual)

    #actual = NVResource(TierMD(ProjectStringDefault()), 'sample', 'sample_resource')
    #print('         nv_resource:', actual)
    #assert ({'name': '<<API_RESOURCE>>', 'value': 'sample_resource'} in actual)
    #assert ({'name': '<<ID_FIELD>>', 'value': 'id', 'resource': 'sample_resource'} in actual)
    #assert ({'name': '<<ID_MIN>>', 'value': 3, 'resource': 'sample_resource'} in actual)
    #assert ({'name': '<<ID_MAX>>', 'value': 330, 'resource': 'sample_resource'} in actual)
    #assert ({'name': '<<ID_RESOURCE>>', 'value': 'sample_resource', 'resource': 'sample_resource'} in actual)
    #assert ({'name': '<<ID_PATTERN>>', 'value': '^.{3,330}$', 'resource': 'sample_resource'} in actual)
    #assert ({'name': '<<OWNER_FIELD>>', 'value': 'owner', 'resource': 'sample_resource'} in actual)
    #assert ({'name': '<<OWNER_MIN>>', 'value': 3, 'resource': 'sample_resource'} in actual)
    #assert ({'name': '<<OWNER_MAX>>', 'value': 330, 'resource': 'sample_resource'} in actual)
    #assert ({'name': '<<OWNER_RESOURCE>>', 'value': 'sample_resource', 'resource': 'sample_resource'} in actual)
    #assert ({'name': '<<OWNER_PATTERN>>', 'value': '^.{3,330}$', 'resource': 'sample_resource'} in actual)

def main(status):
    test_nv_resource(status)

if __name__ == "__main__":
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))