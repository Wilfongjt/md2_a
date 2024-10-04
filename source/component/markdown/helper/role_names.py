class RoleNames(list):
    def __init__(self, project_dict):
        lst = []

        for r in project_dict['project']['resources']:
            for f in project_dict['project']['resources'][r]['model']:
                for s in project_dict['project']['resources'][r]['model'][f]:
                    if s.startswith('api_'):
                        lst.append(s)

        lst = set(lst)  # get rid of duplicates
        for r in lst:
            self.append(r)

def test_role_names():
    from source.component.markdown.tier_md import TierMD
    from source.component.markdown.project_string_default import ProjectStringDefault

    actual = RoleNames(TierMD(ProjectStringDefault()))
    print('          role_names:', actual)
    assert ('api_admin' in actual)
    assert ('api_guest' in actual)
    assert ('api_user' in actual)

def main():
    test_role_names()


if __name__ == "__main__":
    # execute as docker
    main()
