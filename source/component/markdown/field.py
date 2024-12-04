from source.component.markdown.model import Model
#DeprecationWarning()
from source.component.markdown.copyable import Copyable
class Field(dict, Copyable):
    def __init__(self, project_dict, resource_name, field_name):
        self.deep_copy(project_dict['project']['models'][resource_name], key=field_name, inclusive=False)
        self.field_name=field_name
    '''    
    def __init__(self, model_dict, field_name):
        self.field_name = field_name
        for att in model_dict[field_name]:
            self[att]=model_dict[field_name][att]
        #print('self', self)
    '''
    '''
    def getNV(self):
        rc = []
        for item in self:
            if type(item) is dict:
                #print('Field', item)
                raise Exception('Field cannot handle nested objects {}'.format(item))
            else:
                #print('item', item)
                rc.append({'name': '<<{}_{}>>'.format(self.field_name.upper(), item.upper()), 'value': self[item]})
                #'{}: {}'.format(item, self[item])

        return rc
    '''
def test_model_field(status):
    from pprint import pprint
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD
    from source.component.markdown.model import Model

    status.addTitle('Field test')
    project_dict = TierMD(ProjectStringDefault())

    actual = Field(project_dict, 'account', 'id')
    pprint(actual)
    status.assert_test('name in model', 'name' in Field(project_dict, 'account', 'id'))
    status.assert_test('type in model', 'type' in Field(project_dict, 'account', 'id'))
    #status.assert_test('size_min in model', 'size_min' in Field(project_dict, 'account', 'id'))
    #status.assert_test('size_max in model', 'size_max' in Field(project_dict, 'account', 'id'))
    status.assert_test('pattern in model', 'pattern' in Field(project_dict, 'account', 'id'))
    status.assert_test('encrypt in model', 'encrypt' in Field(project_dict, 'account', 'id'))
    status.assert_test('default in model', 'default' in Field(project_dict, 'account', 'id'))
    status.assert_test('required in model', 'required' in Field(project_dict, 'account', 'id'))

    #print('getNV',actual.getNV())

def main(status):
    test_model_field(status)

if __name__ == "__main__":
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport
    status=Status()
    main(status)
    print(StatusReport(status))
