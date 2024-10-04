import os

class NVList(list):

    def add(self, nv, upsert=True):
        ##* Validate nv before adding
        if not upsert:
            if not self.validate(nv):
                return self

        ##* ensure nv not in NVList
        for nv_ in self:
            if nv['name'] == nv_['name']:
                if upsert:
                    nv_['value'] = nv['value']
                    return self
                else:
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

def nv_list_test(status):
    #if 'PY_TEST' in os.environ and eval(os.environ['PY_TEST']):
    #    print('NVList test')
    status.addTitle('NVList test')
    actual = NVList()

    assert (not actual.validate({'a': 'b'}))
    status.addBullet('not actual.validate({\'a\': \'b\'}')

    assert (not actual.validate({'name': 'b'}))
    status.addBullet("validate({'name': 'b', 'value': 'c'})")

    assert (actual.validate({'name': 'b', 'value': 'c'}))
    status.addBullet("validate({'name': 'b', 'value': 'c'})")

    assert (actual.add({'name': 'b', 'value': 'c'}) == [{'name': 'b', 'value': 'c'}])
    status.addBullet("add({'name': 'b', 'value': 'c'})")

    assert (actual.add({'name': 'b', 'value': 'c'}) == [{'name': 'b', 'value': 'c'}])
    status.addBullet("add({'name': 'b', 'value': 'c'})")

    assert (actual.add({'name': 'x', 'value': 'y'}) == [{'name': 'b', 'value': 'c'}, {'name': 'x', 'value': 'y'}])
    status.addBullet("add({'name': 'x', 'value': 'y'})")
    assert (actual.add({'name': 'x', 'value': 'z'}) == [{'name': 'b', 'value': 'c'}, {'name': 'x', 'value': 'z'}])
    status.addBullet("add({'name': 'x', 'value': 'z'})")

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