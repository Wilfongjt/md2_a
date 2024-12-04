# privileges -> scopes
from pprint import pprint
class Scopes(list):
    def __init__(self,project_dict, resource_name):
        #print('scope', project_dict['project']['privileges'][resource_name])
        #pprint(project_dict['project']['privileges'][resource_name])
        for x in project_dict['project']['privileges'][resource_name]:#['privileges'][resource_name]:
            self.append(x)

def test_scopes(status):
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD
    status.addTitle('Scopes test')
    status.addTitle('Model tests')
    project_dict = TierMD(ProjectStringDefault())
    actual = Scopes(project_dict, 'account')
    expected = ['api_admin', 'api_guest', 'api_user']
    status.addBullet('Instantiated {}'.format(actual))
    #print('scopes', actual)
    status.assert_test('Expected Scopes = {}'.format(actual), actual == expected)

def main(status):
    test_scopes(status)

if __name__ == "__main__":
    # execute as docker
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))