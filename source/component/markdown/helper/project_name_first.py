from source.component.markdown.project_string_default import ProjectStringDefault

class ProjectNameFirst(str):
    def __new__(cls, project_dict):
        #print('keys', list(project_dict['project'].keys()))
        if 'project' in project_dict:
            first_key = list(project_dict['project'].keys())[0]
        else:
            first_key = list(project_dict.keys())[0]
        #print('first_key', first_key)
        contents = first_key

        instance = super().__new__(cls, contents)
        return instance

def test_project_name_last(status):
    from pprint import pprint
    status.addTitle('Project Name First test')
    from source.component.markdown.tier_md import TierMD

    actual = ProjectNameFirst(TierMD(ProjectStringDefault()))
    #pprint(actual)
    #print('        project_name:', actual)
    status.assert_test ("actual == 'sample'", actual == 'sample')

def main(status):
    test_project_name_last(status)

if __name__ == "__main__":
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))
