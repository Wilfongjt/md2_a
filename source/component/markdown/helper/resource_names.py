class ResourceNames(list):
    def __init__(self, project_dict):
        ##* Extract Resource names from project-dictionary
        for r in project_dict['project']['resources']:
            #print('Resource Names', r)
            self.append(r)

def test_resource_names():
    from source.component.markdown.tier_md import TierMD
    from source.component.markdown.project_string_default import ProjectStringDefault

    actual = ResourceNames(TierMD(ProjectStringDefault()))
    print('      resource_names:', actual)
    assert (actual == ['account', 'sample_resource'])

def main():
    test_resource_names()

if __name__ == "__main__":
    # execute as docker
    main()
