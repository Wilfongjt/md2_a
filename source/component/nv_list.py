
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

def main():
    actual = NVList()
    assert (not actual.validate({'a': 'b'}))
    assert (not actual.validate({'name': 'b'}))
    assert (actual.validate({'name': 'b', 'value': 'c'}))
    assert (actual.add({'name': 'b', 'value': 'c'}) == [{'name': 'b', 'value': 'c'}])
    assert (actual.add({'name': 'b', 'value': 'c'}) == [{'name': 'b', 'value': 'c'}])
    assert (actual.add({'name': 'x', 'value': 'y'}) == [{'name': 'b', 'value': 'c'}, {'name': 'x', 'value': 'y'}])
    assert (actual.add({'name': 'x', 'value': 'z'}) == [{'name': 'b', 'value': 'c'}, {'name': 'x', 'value': 'z'}])

    print('NVList:', actual)


if __name__ == "__main__":
    # execute as docker
    main()