from source.component.markdown.project_string_default import ProjectStringDefault
class ProjectName(str):
    def __new__(cls, project_dict):
        first_key = next(iter(project_dict['project']))
        contents = first_key

        instance = super().__new__(cls, contents)
        return instance

def test_project_name(status):
    status.addTitle('Project Name test')
    from source.component.markdown.tier_md import TierMD

    actual = ProjectName(TierMD(ProjectStringDefault()))


    status.addTitle('        project_name: {}'.format(actual))
    status.assert_test("actual == 'sample'", actual == 'sample')


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
