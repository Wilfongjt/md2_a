
class Claim(dict):
    def __init__(self, project_dict, project_name, resource_name, scope_name):
        for x in project_dict['project'][project_name]['claim'][scope_name]:
            if x != 'name':
                self[x]=project_dict['project'][project_name]['claim'][scope_name][x]

def test_claim(status):
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD
    status.addTitle('Claim test')
    project_dict = TierMD(ProjectStringDefault())

    actual = Claim(project_dict, 'sample', 'account', 'api_guest')

    status.assert_test('Model not None',actual)
    status.assert_test('"aud" in model','aud' in actual)
    status.assert_test('"iss" in model','iss' in actual)
    status.assert_test('"sub" in model','sub' in actual)
    status.assert_test('"user" in model','user' in actual)
    status.assert_test('"scope" in model','scope' in actual)
    status.assert_test('"key" in model','key' in actual)

def main(status):
    test_claim(status)

if __name__ == "__main__":
    # execute as docker
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))