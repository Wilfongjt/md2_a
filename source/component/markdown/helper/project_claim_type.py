from source.component.markdown.project_string_default import ProjectStringDefault
class ProjectClaimType(str):
    def __new__(cls, project_dict, project_name):
        print('project_dict',project_dict['project'])
        contents = project_dict['project'][project_name]['claim']['type']

        instance = super().__new__(cls, contents)
        return instance
def test_project_name():
    from source.component.markdown.tier_md import TierMD

    actual = ProjectClaimType(TierMD(ProjectStringDefault()),'sample')
    # print('        project_claim_name:', actual)
    assert (actual == 'jwt')

def main():
    test_project_name()

if __name__ == "__main__":
    # execute as docker
    main()
