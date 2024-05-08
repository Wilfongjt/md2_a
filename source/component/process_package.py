import os
'''
from able import TemplateString, \
                 EnvVarString, \
                 NameValuePairs, \
                 CloneRepo, \
                 StringWriter, \
                 TemplateList_Latest,\
                 StringReader, \
                 UpserterString,\
                 Recorder, DiagramString
'''
class ProcessPackage(dict):

    def set(self, key, value):
        self[key]=value
        return self

    def get(self, key):
        return self[key]

    def assign(self, package):
        for dp in package:
            self[dp] = package[dp]
        return self
    def show(self):
        print('show', self)
        return self

def main():
    from able import DiagramString
    os.environ['GH_TEST'] = 'TEST'

    #print('ProcessPackage',ProcessPackage().set('A','a') )

    assert(ProcessPackage() == {})
    assert('A' in ProcessPackage().set('A', 'a'))


if __name__ == "__main__":
    # execute as docker
    main()