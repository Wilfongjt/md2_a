import os
from source.component.markdown.scalars import Scalars

class NVList(list):
    # [{"name": "A"},{"name":"B"},...{"name": "N"}]
    def add(self, nv, upsert=False):
        #print('A')
        ##* Validate nv before adding
        if not upsert:
            #print('B')
            if not self.validate(nv):
                #print('C')
                return self

        ##* ensure nv not in NVList
        for nv_ in self:
            if nv['name'] == nv_['name']:
                if upsert:
                    #print('D')
                    nv_['value'] = nv['value']
                    return self
                else:
                    #print('E')
                    raise Exception('Attempt to update existing key "{}" with value "{}"'.format(nv['name'], nv['value']))
                    return self
        self.append(nv)
        return self

    def extend(self, nv_list, upsert=False):
        for nv in nv_list:
            self.add(nv, upsert)
        return self

    def find(self, name):
        for nv_ in self:
            if nv_['name'] == name:
                return nv_
        return False

    def validate(self, nv):
        if 'name' not in nv:
            return False
            # raise Exception('Name Value Pair is missing "name".')
        if 'value' not in nv:
            return False
            # raise Exception('Name Value Pair is missing "value".')
        return True

    def scalars_nv(self, dictionary, parent_name):
        # print('scalars_nv 1')
        print('scalar_nv', parent_name)
        print('scalar_nv', dictionary)
        for key, value in dictionary.items():
            # print('scalars_nv 2',type(value))
            if type(value) not in [dict, list]:
                # print('scalars_nv 3', '{}_{}'.format(parent_name, key).upper() )
                self.append({'{}_{}'.format(parent_name.upper(), key.upper()): value})
        return self



def nv_list_test(status):
    #if 'PY_TEST' in os.environ and eval(os.environ['PY_TEST']):
    #    print('NVList test')
    from pprint import pprint
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD
    from source.component.markdown.claims import Claims
    from source.component.markdown.model import Model
    status.addTitle('Resources test')
    project_dict = TierMD(ProjectStringDefault())

    status.addTitle('NVList test')
    #actual = NVList().scalars_nv(project_dict['project'], 'project')
    #actual.scalars_nv(project_dict['project']['models']['account']['id'],'id')
    #actual.scalars_nv(project_dict['project']['privileges']['account']['id'],'id')
    print('project', project_dict)
    print('claims', Claims(project_dict, scope_name='api_admin'))
    print('scalars', Scalars(Claims(project_dict, 'api_admin')))
    actual = NVList().extend(Scalars(Claims(project_dict, 'api_admin')))
    #actual = NVList().scalars_nv(Claims(project_dict, 'api_admin'),'claim')
    #actual = actual.scalars_nv(Model(project_dict, 'account'),'model')

    #actual.scalars_nv(project_dict['project']['resources']['account'],'resource')
    pprint(actual)
    #actual = NVList()
    #exit(0)
    assert (not actual.validate({'a': 'b'}))
    status.addBullet('not actual.validate({\'a\': \'b\'}')

    assert (not actual.validate({'name': 'b'}))
    status.addBullet("validate({'name': 'b', 'value': 'c'})")

    assert (actual.validate({'name': 'b', 'value': 'c'}))
    status.addBullet("validate({'name': 'b', 'value': 'c'})")

    assert (actual.add({'name': 'b', 'value': 'c'}) == [{'name': 'b', 'value': 'c'}])
    status.addBullet("add({'name': 'b', 'value': 'c'})")

    #assert (actual.add({'name': 'b', 'value': 'c'}) == [{'name': 'b', 'value': 'c'}])
    #status.addBullet("add({'name': 'b', 'value': 'c'})")

    assert (actual.add({'name': 'x', 'value': 'y'}) == [{'name': 'b', 'value': 'c'}, {'name': 'x', 'value': 'y'}])
    status.addBullet("add({'name': 'x', 'value': 'y'})")

    #print(actual.add({'name': 'x', 'value': 'z'}))
    #assert (actual.add({'name': 'x', 'value': 'z'}) == [{'name': 'b', 'value': 'c'}, {'name': 'x', 'value': 'z'}])
    #status.addBullet("add({'name': 'x', 'value': 'z'})")

    #print('NVList:', actual)

    d = {
        'a': 'A',
        'b': {'name': 'B1', 'type': 'C'},
        'c': {'name': 'B2', 'type': 'C'}
    }
    d= {
        'a': {
            'b': 'b',
            'c': 'c',
            'd': {
                'e': 'e',
                'f1': {'f': 'f1', 'g': 'g1', 'h': 'h1'},
                'f2': {'f': 'f2', 'g': 'g2', 'h': 'h2'},
                'f3': {'f': 'f3', 'g': 'g3', 'h': 'h3'}
            }
        }
    }

    x=[
        {'name': 'a',  'value': 'A'},
        {'name': 'b#name', 'value': 'B1'},
        {'name': 'b#type', 'value': 'C'},
        {'name': 'c#name', 'value': 'B2'},
        {'name': 'c#type', 'value': 'C'}
    ]

def main(status):
    nv_list_test(status)

if __name__ == "__main__":
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))