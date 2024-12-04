from pprint import pprint

'''
class DDD(dict, Copyable):
    def __init__(self, dt):
        #Copyable.__init__(self)
        self.deep_copy(dt)

def test_ddd(status):
    from pprint import pprint
    dictionary = {
        'a': 'A',
        'b': {'b1': 1, 'b2': '2'},
        'c': [{'c1': 'C1', 'c2':['C2',{'c22': 'C22'}]},{'c1': 'C1', 'c2': 'C2'}],
        'd': ['d1','d2','d3']
    }

    actual = DDD(dictionary)
    actual = DDD(dictionary['b'])
    dictionary['b']= 'bad'
    dictionary['c']='bad'
    print('actual', actual)

def read_dict_recursive(d, indent=0):
    """
    Recursively reads a dictionary and prints its keys and values.

    Parameters:
    d (dict): The dictionary to read.
    indent (int): Used to format the output with indentation.
    """
    for key, value in d.items():
        print(' ' * indent + f"Key: {key}")
        if isinstance(value, dict):
            print(' ' * indent + "Value: (nested dictionary)")
            # Recursively call the function to process the nested dictionary
            read_dict_recursive(value, indent + 4)
        else:
            print(' ' * indent + f"Value: {value}")

def test_branch(status):
    from pprint import pprint

    dictionary = {
        'a': 'A',
        'b': {'b1': 'BB'},
        'c': {'c1': {'cc': 'CC'}}
    }
    actual = Copyable()
    pprint(actual)
    status.assert_test('init', actual)
    print('data', actual.copy(dictionary))
    #pprint(actual)
'''
from source.component.markdown.copyable import Copyable

class Claims(dict,Copyable):
    # all scopes claims
    # a single scope claims

    def __init__(self, project_dict, scope_name):
        #pprint(project_dict)
        self.deep_copy(project_dict['project']['claims'], key=scope_name,inclusive=False)

    #def getNV(self):
    #    nv = []
    #    for n in self:
    #        nv.append({'{}'.format('<<CLAIM_{}>>'.format(str(n).upper())): self[n]})
    #    return nv

def test_claim(status):
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD
    from source.component.markdown.scalars import Scalars
    status.addTitle('Claims test')
    project_dict = TierMD(ProjectStringDefault())

    actual = Claims(project_dict, 'api_guest')
    print('claims', actual)
    status.assert_test('Model not None',actual)
    status.assert_test('"aud" in model','aud' in actual)
    status.assert_test('"iss" in model','iss' in actual)
    status.assert_test('"sub" in model','sub' in actual)
    status.assert_test('"user" in model','user' in actual)
    status.assert_test('"scope" in model','scope' in actual)
    status.assert_test('"key" in model','key' in actual)
    print('claims', actual)
    #print('getNV', actual.getNV())
    Scalars(actual)
    #pprint(actual.getNV())

def main(status):
    #test_branch(status)
    #test_ddd(status)

    test_claim(status)

if __name__ == "__main__":
    # execute as docker
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))
