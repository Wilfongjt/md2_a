
# project --> Data
from source.component.markdown.copyable import Copyable

class Data(dict,Copyable):
    def __init__(self, project_dict, resource_name, test_name):
        self.deep_copy(project_dict['project']['tests'][resource_name],key=test_name,inclusive=False)

def test_data(status):
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD
    from pprint import pprint

    status.addTitle('Data test')
    project_dict = TierMD(ProjectStringDefault())
    actual = Data(project_dict, 'account', 'api_guest')
    #pprint(actual)
    status.addLine('api_guest')
    status.assert_test('Data not None', actual)
    status.assert_test ('"id" in data', 'id' in actual)
    status.assert_test ('"type" in data', 'type' in actual)
    status.assert_test ('"owner" in data', 'owner' in actual)
    status.assert_test ('"username" in data', 'username' in actual)
    status.assert_test ('"displayname" in data', 'displayname' in actual)
    status.assert_test ('"password" in data', 'password' in actual)
    status.assert_test ('"scope" in data', 'scope' in actual)

    status.assert_test('scope is api_guest', actual['scope'] == 'api_guest')

    actual = Data(project_dict, 'account', 'api_admin')
    #pprint(actual)
    status.addLine('api_admin')
    status.assert_test('Data not None', actual)
    status.assert_test('scope is api_admin', actual['scope'] == 'api_admin')

    actual = Data(project_dict, 'account', 'api_user')
    #pprint(actual)
    status.addLine('api_user')
    status.assert_test('Data not None', actual)
    status.assert_test('scope is api_user', actual['scope'] == 'api_user')

def main(status):
    test_data(status)

if __name__ == "__main__":
    # execute as docker
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))