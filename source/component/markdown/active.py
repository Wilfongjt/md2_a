from able import ClassNameable

class Active(int):
    ## Active
    # bool cannot be used as base class, so int is substitute
    # from resource_dict is {major: '', minor:'', patch:'', schema:'', active:1}
    def __new__(cls, project_dict, resource_name):

        contents = False
        if 'active' in project_dict['project']['resources'][resource_name]:
            if project_dict['project']['resources'][resource_name]['active'] in [1, True, '1', 'TRUE', 'true', 'True', 'T', 't', 'Yes', 'yes','YES','Y', 'y']:
                contents = True
        instance = super().__new__(cls, contents)
        return instance

def test_active(status):
    from pprint import pprint
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD

    project_dict = TierMD(ProjectStringDefault())
    status.addTitle('Active Test')
    #pprint(project_dict)
    #{'project': {'resources':}}
    status.assert_test('account is active', Active(project_dict, 'account'))

    '''
    status.assert_test('True is True', Active({'active': True}))
    status.assert_test('"False" is False', not Active({'active': 'False'}))
    status.assert_test('"True" is True', Active({'active': 'T'}))
    status.assert_test('"F" is False', not Active({'active': 'F'}))
    status.assert_test('"T" is True', Active({'active': 'T'}))
    status.assert_test('"N" is False', not Active({'active': 'N'}))
    status.assert_test('"Y" is True', Active({'active': 'Y'}))
    status.assert_test('"No" is False', not Active({'active': 'No'}))
    status.assert_test('"Yes" is True', Active({'active': 'Yes'}))

    status.assert_test('0 is False', not Active({'active': 0}))
    status.assert_test('1 is True', Active({'active': 1}))
    '''
def main(status):
    test_active(status)

if __name__ == "__main__":
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))