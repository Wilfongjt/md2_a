class RoleNames(list):
    def __init__(self, project_dict):
        lst = []
        for r in project_dict['project']['privileges']:
            for p in project_dict['project']['privileges'][r]:
                if p.startswith('api_'):
                    lst.append(p)

        lst = set(lst)  # get rid of duplicates
        for r in lst:
            self.append(r)

def test_role_names(status):
    status.addTitle('Role Names test')
    from source.component.markdown.tier_md import TierMD
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.helper.project_name_first import ProjectNameFirst

    project = TierMD(ProjectStringDefault())
    actual = RoleNames(project)
    print('          role_names:', actual)

    status.assert_test ("'api_admin' in {}".format(actual), 'api_admin' in actual)
    status.assert_test ("'api_guest' in {}".format(actual), 'api_guest' in actual)
    status.assert_test ("'api_user' in {}".format(actual), 'api_user' in actual)

def main(status):
    test_role_names(status)


if __name__ == "__main__":
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))
