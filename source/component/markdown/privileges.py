
from source.component.markdown.copyable import Copyable

class Privileges(dict, Copyable):
    # all resources and their attributes
    # single resource's attributes
    def __init__(self, project_dict, resource_name, scope_name):
        self.deep_copy(project_dict['project']['privileges'][resource_name], key=scope_name)

def test_privileges(status):
    from pprint import pprint
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD
    status.addTitle('Resources test')
    project_dict = TierMD(ProjectStringDefault())

    actual = Privileges(project_dict, 'account', 'api_admin')
    pprint(actual)
    actual = Privileges(project_dict, 'account', 'api_guest')
    pprint(actual)
    actual = Privileges(project_dict, 'account', 'api_user')
    pprint(actual)
    #status.assert_test('Model not None', actual)
    #status.assert_test('"aud" in model', 'aud' in actual)
    #status.assert_test('"iss" in model', 'iss' in actual)
    #status.assert_test('"sub" in model', 'sub' in actual)
    #status.assert_test('"user" in model', 'user' in actual)
    #status.assert_test('"scope" in model', 'scope' in actual)
    #status.assert_test('"key" in model', 'key' in actual)

    #print('getNV', actual.getNV())


def main(status):
    test_privileges(status)


if __name__ == "__main__":
    # execute as docker
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))
