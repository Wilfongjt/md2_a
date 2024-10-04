import os
from able import EnvVarString, \
                 NameValuePairs
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
    ##
    ##### Process Package
    ##

    def set(self, key, value):
        ##* __set__
        self[key]=value
        return self

    def get(self, key):
        ##* __get__
        return self[key]

    def assign(self, package):
        ##* __assign__
        for dp in package:
            self[dp] = package[dp]
        return self

    def show(self):
        ##* __show__
        print('show', self)
        return self

    def isStringNone(self, str_object):

        rc = str_object

        if str_object == None:
            rc = None
        elif str_object == 'None':
            rc = None

        return rc

    #def getNVList(self):
    #    ##* get name-value pair list
    #    return [{'name': '<<{}>>'.format(itm['name']),
    #                        'value': itm['value']}
    #                        for itm in NameValuePairs(multi_line_string=EnvVarString())]


def process_package_test(status):
    from able import DiagramString
    #if 'PY_TEST' in os.environ and eval(os.environ['PY_TEST']):
    #    print('Process Package test')
    status.addTitle('Process Package test')
    os.environ['GH_TEST'] = 'TEST'

    #print('ProcessPackage',ProcessPackage().set('A','a') )

    status.assert_test("ProcessPackage() == {}",ProcessPackage() == {})
    status.addBullet('init ProcessPackage() to {}')
    assert('A' in ProcessPackage().set('A', 'a'))
    status.addBullet("'A' in ProcessPackage().set('A', 'a') ok")

def main(status):
    process_package_test(status)

if __name__ == "__main__":
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))