import copy


class Copyable():
    def deep_copy(self, d, key='project', inclusive=True):
        # when branch_name is None then copy entire dictionary
        # inclusive == True, keeps the key name {'project': {'a': 'A'}}
        # inclusive == false, discards key name ... {'a': 'A'}
        if inclusive:
            self[key] = copy.deepcopy(d[key])
        else:
            d=copy.deepcopy(d[key])
            for k in d:
                self[k]=d[k]

        return self
'''
    def deep_copy(self, d):
        # when branch_name is None then copy entire dictionary
        tmp = {}
        for key, value in d.items():
            if isinstance(value, dict):
                #self.deep_copy(value)
                tmp[key]  = self.deep_copy(value)
                #print('value', value)
                #print('rc   ', rc)
                #self[key] = rc

            else:
                #if isinstance(self, dict):
                #    self[key] = value
                tmp[key] = value

                #print('default {}: {}'.format(key, value))
            print('tmp',tmp)
        return tmp
'''
def test_copyable(status):
    from pprint import pprint
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD
    from source.component.markdown.model import Model

    class Test(dict, Copyable):
        def __init__(self, dictionary, key, inclusive):
            #Copyable.__init__()
            self.deep_copy(dictionary, key=key, inclusive=inclusive)

    status.addTitle('Scalars test')

    status.addTitle('model scalars')
    project_dict = TierMD(ProjectStringDefault())
    #project_dict = {'project': {'name': 'sample'}}
    #print(project_dict)
    status.addTitle('Copyable test')
    #actual = Copyable().deep_copy(project_dict)
    actual = Test(project_dict['project'],key='claims',inclusive=False)
    # pprint(actual)
    status.assert_test('copyable', 'claims' not in actual)
    #print('copyable', actual)
    #pprint(actual)

def main(status):

    test_copyable(status)

if __name__ == "__main__":
    # execute as docker
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))
