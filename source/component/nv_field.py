from source.component.nv_list import NVList
from pprint import pprint
import os

class NVField(NVList):  # name value field
    # NV an individual resource field
    # apply to a template
    def __init__(self, project_dict, project_name, resource_name, field_name):
        # must have an existing resource

        if not resource_name in project_dict['project'][project_name]['resources']:
            raise Exception('Resource Name Not Found: {}'.format(resource_name))

        if not field_name in project_dict['project'][project_name]['resources'][resource_name]['model']: # row_dict:
            raise Exception('Resource Field Name Not Found: {}'.format(field_name))

        # fields are stored in resource model
        pprint(project_dict)
        # project_dict: {sample: {resources: {account:{ model: {}}}}
        fld_atts = project_dict['project'][project_name]['resources'][resource_name]['model'][field_name]
        att =[f for f in fld_atts]
        print('fld_atts',fld_atts)

        flds =[{'name': '<<{}_{}>>'.format(field_name.upper(),key.upper()), 'value': value, 'resource': resource_name} for key, value in fld_atts.items()]

        self.extend(flds)

def test_nv_field(status):
    from pprint import pprint
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD

    status.addTitle('NVField test')
    actual = NVField(TierMD(ProjectStringDefault()), 'sample', 'account', 'id')
    #print('            nv_field ->', actual)
    assert ({'name': '<<ID_NAME>>', 'value': 'id', 'resource': 'account'} in actual)
    status.addBullet('<<ID_NAME>> in nvField ok')
    assert ({'name': '<<ID_SIZE_MIN>>', 'value': 3, 'resource': 'account'} in actual)
    status.addBullet('<<ID_SIZE_MIN>> in nvField ok')

    assert ({'name': '<<ID_SIZE_MAX>>', 'value': 330, 'resource': 'account'} in actual)
    status.addBullet('<<ID_SIZE_MAX>> in nvField ok')

    assert ({'name': '<<ID_RESOURCE>>', 'value': 'account', 'resource': 'account'} in actual)
    status.addBullet('<<ID_RESOURCE>> in nvField ok')

    assert ({'name': '<<ID_PATTERN>>', 'value': '^.{3,330}$', 'resource': 'account'} in actual)
    status.addBullet('<<ID_PATTERN>> in nvField ok')

    actual = NVField(TierMD(ProjectStringDefault()), 'sample', 'account', 'owner')
    # print('            nv_field ->', actual)
    assert ({'name': '<<OWNER_NAME>>', 'value': 'owner', 'resource': 'account'} in actual)
    status.addBullet('<<OWNER_NAME>> in nvField ok')

    assert ({'name': '<<OWNER_SIZE_MIN>>', 'value': 3, 'resource': 'account'} in actual)
    status.addBullet('<<OWNER_SIZE_MIN>> in nvField ok')

    assert ({'name': '<<OWNER_SIZE_MAX>>', 'value': 330, 'resource': 'account'} in actual)
    status.addBullet('<<OWNER_SIZE_MAX>> in nvField ok')

    assert ({'name': '<<OWNER_RESOURCE>>', 'value': 'account', 'resource': 'account'} in actual)
    status.addBullet('<<OWNER_RESOURCE>> in nvField ok')

    assert ({'name': '<<OWNER_PATTERN>>', 'value': '^.{3,330}$', 'resource': 'account'} in actual)
    status.addBullet('<<OWNER_PATTERN>> in nvField ok')



def main(status):
    #if 'PY_TEST' in os.environ and eval(os.environ['PY_TEST']):
    #    print('NVField test')

    test_nv_field(status)

if __name__ == "__main__":
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))