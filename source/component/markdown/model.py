from source.component.markdown.scopes import Scopes

class Model(dict):
    def __init__(self, project_dict, project_name, resource_name, scope_name):
        self.project_name = project_name
        self.resource_name = resource_name
        self.scope_name = scope_name

        # get model keys for a scope and resource in a project_dict
        model = project_dict['project'][self.project_name]['resources'][self.resource_name]['model']
        scopes = Scopes()
        for m in model:
            item = {}
            for x in model[m]:
                if x == self.scope_name: # convert scope name to role and permissions
                    item['role']=self.scope_name
                    item['permissions']=model[m][x]
                elif x == 'size':
                    item['size_min']= int(str(model[m][x]).split('-')[0])
                    item['size_max']= int(str(model[m][x]).split('-')[1])
                else:
                    if x not in scopes:
                        item[x] = model[m][x]

            self[m]=item

def test_model(status):
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD
    status.addTitle('Mode test')
    project_dict = TierMD(ProjectStringDefault())

    status.addBullet('Instantiated model not None')

    actual = Model(project_dict, 'sample', 'account', 'api_guest')
    status.assert_test('Model not None',actual != None)
    status.assert_test ('"id" in model','id' in actual)
    status.assert_test ('"type" in model','type' in actual)
    status.assert_test ('"owner" in model', 'owner' in actual)
    status.assert_test ('"username" in model','username' in actual)
    status.assert_test ('"displayname" in model','displayname' in actual)
    status.assert_test ('"password" in model','password' in actual)
    status.assert_test ('"scope" in model','scope' in actual)

def main(status):
    test_model(status)

if __name__ == "__main__":
    # execute as docker
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))