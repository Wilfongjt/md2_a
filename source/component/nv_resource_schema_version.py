from source.component.nv_list import NVList
from source.component.markdown.helper.project_name_first import ProjectNameFirst
class NVResourceSchemaVersion(NVList):
    def __init__(self, project_dict, project_name, resource_name):
        schema = 'api'
        #print('project_dict',project_dict)
        #print('resource_name',resource_name)
        project_name = ProjectNameFirst(project_dict)
        if 'schema' in project_dict['project'][project_name]['resources'][resource_name]:  # schema:
            schema = project_dict['project'][project_name]['resources'][resource_name]['schema']
        version = '0.0.1'
        if 'version' in project_dict['project'][project_name]['resources'][resource_name]:  # schema:
            version = project_dict['project'][project_name]['resources'][resource_name]['version']

        self.add({'name': '<<API_SCHEMA>>', 'value': '{}_{}'.format(schema, version.replace('.', '_'))})

def test_nv_resource_schema_version(status):
    status.addTitle('NV resource schema version')
    from source.component.markdown.tier_md import TierMD
    from source.component.markdown.project_string_default import ProjectStringDefault
    default_md = ProjectStringDefault()
    #print('default_md', default_md)
    project_dict = TierMD(default_md)
    project_name = ProjectNameFirst(project_dict)
    actual = NVResourceSchemaVersion(project_dict, project_name, 'account')

    #print('nv resource schema version', actual)
    expected = [{'name': '<<API_SCHEMA>>', 'value': 'api_1_0_0'}]
    #assert(actual == expected)
    status.assert_test("{} == {}".format(actual, expected), actual == expected)


def main(status):
    test_nv_resource_schema_version(status)


if __name__ == "__main__":
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))