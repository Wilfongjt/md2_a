from pprint import pprint
class ResourceNames(list):
    def __init__(self, project_dict, project_name):
        ##* Extract Resource names from project-dictionary
        #project = project_dict['project'][project_name]
        #print('project_name', project_name)
        #print('project')
        #pprint(project_dict)
        for r in project_dict['project'][project_name]['resources']:
            #print('Resource Names', r)
            self.append(r)

def test_resource_names(status):
    status.addTitle('Resource Names test')
    from source.component.markdown.tier_md import TierMD
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.helper.project_name_first import ProjectNameFirst

    project =TierMD(ProjectStringDefault())
    actual = ResourceNames(project, ProjectNameFirst(project))
    #print('      resource_names:', actual)
    status.assert_test ("resource names", actual == ['account'])

def main(status):
    test_resource_names(status)

if __name__ == "__main__":
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))

