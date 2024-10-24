from source.component.markdown.project_string_default import ProjectStringDefault
class ProjectNameLast(str):
    def __new__(cls, project_dict):
        if 'project' in project_dict:
            last_key = list(project_dict['project'].keys())[-1]
        else:
            last_key = list(project_dict.keys())[-1]

        contents = last_key

        instance = super().__new__(cls, contents)
        return instance

def test_project_name_last(status):
    status.addTitle('Project Name Last test')
    from source.component.markdown.tier_md import TierMD

    actual = ProjectNameLast(TierMD(ProjectStringDefault()))

    print('        project_name:', actual)
    status.assert_test ("actual == 'sample'",actual == 'sample')

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
