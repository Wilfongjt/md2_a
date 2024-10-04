
class TestToken(str):
    def __new__(cls, project_dict):

        contents = 'Implement Me'
        instance = super().__new__(cls, contents)
        return instance

def main(status):
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD
    status.addTitle('TestToken test')
    status.addBullet('NOT implemented')
    project_dict = TierMD(ProjectStringDefault())
    actual = TestToken(project_dict)
    #print('', actual)
    status.assert_test("'Implement Me' in TestToken(project_dict)", 'Implement Me' in actual)

if __name__ == "__main__":
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))