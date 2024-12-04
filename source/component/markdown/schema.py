
class Schema(str):
    ## Schema
    # bool cannot be used as base class, so int is substitute
    # from resource_dict is {major: '', minor:'', patch:'', schema:'', active:1}
    def __new__(cls, project_dict, resource_name):
        schema = project_dict['project']['resources'][resource_name]['schema']
        major = project_dict['project']['resources'][resource_name]['major']
        minor = project_dict['project']['resources'][resource_name]['minor']
        patch = project_dict['project']['resources'][resource_name]['patch']

        contents = '{}_{}_{}_{}'.format(schema, major, minor, patch)

        instance = super().__new__(cls, contents)
        return instance

def test_schema(status):
    from pprint import pprint
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD

    project_dict = TierMD(ProjectStringDefault())

    status.addTitle('Schema Test')
    status.assert_test('Schema is api_00_00_00', Schema(project_dict, 'account')=='api_00_00_00')


def main(status):
    test_schema(status)

if __name__ == "__main__":
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))