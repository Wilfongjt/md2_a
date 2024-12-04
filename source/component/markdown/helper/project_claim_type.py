from source.component.markdown.project_string_default import ProjectStringDefault
class ProjectClaimType(str):
    def __new__(cls, project_dict):
        #print('project_dict',project_dict['project'])
        contents = project_dict['project']['claims']['type']

        instance = super().__new__(cls, contents)
        return instance

def test_project_name(status):
    from source.component.markdown.tier_md import TierMD

    status.addTitle('project_dict claim type test')
    project_dict = TierMD(ProjectStringDefault())
    #print('project_dict', project_dict)
    actual = ProjectClaimType(project_dict)
    #print('        project_claim_name:', actual)
    #assert (actual == 'jwt')
    status.assert_test("actual == 'jwt'", actual == 'jwt')

def main(status):
    test_project_name(status)

if __name__ == "__main__":
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))
