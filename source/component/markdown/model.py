from source.component.markdown.scopes import Scopes
from source.component.markdown.copyable import Copyable
from able import ClassNameable


class Model(dict, Copyable,ClassNameable):
    # grab a project resource model for a given scope
    def __init__(self, project_dict, resource_name):
        self.deep_copy(project_dict['project']['models'], resource_name, inclusive=False)

        # self.deep_copy(project_dict['project']['models'][resource_name])

    '''
        def __init__(self, project_dict, resource_name, field_name=None):
        if not field_name:
            self.deep_copy(project_dict['project']['models'][resource_name])
        else:
            self.deep_copy(project_dict['project']['models'][resource_name][field_name])
    
    '''

def test_model(status):
    from pprint import pprint
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD

    status.addTitle('Model tests')
    project_dict = TierMD(ProjectStringDefault())

    status.addBullet('Instantiated model not None')

    actual = Model(project_dict, 'account')
    #pprint(actual)

    status.addTitle('model')

    status.assert_test('Model not None', actual != None)
    status.assert_test('"id" in model', 'id' in actual)
    status.assert_test('"type" in model', 'type' in actual)
    status.assert_test('"owner" in model', 'owner' in actual)
    status.assert_test('"username" in model', 'username' in actual)
    status.assert_test('"displayname" in model', 'displayname' in actual)
    status.assert_test('"password" in model', 'password' in actual)
    status.assert_test('"scope" in model', 'scope' in actual)

    #print('field id', Model(project_dict, resource_name='account', field_name='id'))
    '''
    actual = Model(project_dict, 'sample', 'account', 'api_admin')
    status.addTitle('api_admin model')
    status.assert_test('Model not None',actual != None)
    status.assert_test ('"id" in model','id' in actual)
    status.assert_test ('"type" in model','type' in actual)
    status.assert_test ('"owner" in model', 'owner' in actual)
    status.assert_test ('"username" in model','username' in actual)
    status.assert_test ('"displayname" in model','displayname' in actual)
    status.assert_test ('"password" in model','password' in actual)
    status.assert_test ('"scope" in model','scope' in actual)

    actual = Model(project_dict, 'sample', 'account', 'api_guest')
    status.addTitle('api_guest model')
    status.assert_test('Model not None',actual != None)
    status.assert_test ('"id" in model','id' in actual)
    status.assert_test ('"type" in model','type' in actual)
    status.assert_test ('"owner" in model', 'owner' in actual)
    status.assert_test ('"username" in model','username' in actual)
    status.assert_test ('"displayname" in model','displayname' in actual)
    status.assert_test ('"password" in model','password' in actual)
    status.assert_test ('"scope" in model','scope' in actual)

    actual = Model(project_dict, 'sample', 'account', 'api_user')
    status.addTitle('api_user model')

    status.assert_test('Model not None',actual != None)
    status.assert_test ('"id" in model','id' in actual)
    status.assert_test ('"type" in model','type' in actual)
    status.assert_test ('"owner" in model', 'owner' in actual)
    status.assert_test ('"username" in model','username' in actual)
    status.assert_test ('"displayname" in model','displayname' in actual)
    status.assert_test ('"password" in model','password' in actual)
    status.assert_test ('"scope" in model','scope' in actual)
    #print('getNV', actual.getNV())
    '''
    #print('model', actual)
    #print('scalars', actual.getScalars())
    #pprint(actual.getScalars())
    # pprint(actual)

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
