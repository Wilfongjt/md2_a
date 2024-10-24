

class Data(dict):
    def __init__(self, project_dict, project_name, resource_name, scope_name):
        test_data = project_dict['project'][project_name]['resources'][resource_name]['data']['test'][scope_name]

        for x in test_data:
            self[x]=test_data[x]



def test_data(status):
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD

    status.addTitle('Data test')
    project_dict = TierMD(ProjectStringDefault())
    actual = Data(project_dict, 'sample', 'account', 'api_guest')

    status.assert_test('Data not None', actual)
    status.assert_test ('"id" in data', 'id' in actual)
    status.assert_test ('"type" in data', 'type' in actual)
    status.assert_test ('"owner" in data', 'owner' in actual)
    status.assert_test ('"username" in data', 'username' in actual)
    status.assert_test ('"displayname" in data', 'displayname' in actual)
    status.assert_test ('"password" in data', 'password' in actual)
    status.assert_test ('"scope" in data', 'scope' in actual)

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