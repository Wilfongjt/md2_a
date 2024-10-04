from source.component.markdown.project_string_default import ProjectStringDefault
class ProjectName(str):
    def __new__(cls, project_dict):
        first_key = next(iter(project_dict['project']))
        contents = first_key

        instance = super().__new__(cls, contents)
        return instance

def test_project_name():
    from source.component.markdown.tier_md import TierMD

    actual = ProjectName(TierMD(ProjectStringDefault()))


    print('        project_name:', actual)
    assert (actual == 'sample')

def main():
    test_project_name()

if __name__ == "__main__":
    # execute as docker
    main()
