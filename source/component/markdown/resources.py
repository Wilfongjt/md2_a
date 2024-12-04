# Version(project_dict, resource_name) -> 00.00.00
# Schema(project_dict, resource_name) -> api
# Active(project_dict, resource_name) -> True/False
# project
from source.component.markdown.copyable import Copyable
class Resources(dict, Copyable):
    # all resources and their attributes
    # single resource's attributes
    def __init__(self, project_dict, resource_name):
        self.deep_copy(project_dict['project']['resources'], key=resource_name)

    '''    
    def __init__(self, project_dict, resource_name=None):
        if not resource_name: # all resources and thier attributes
            for resource in project_dict['project']['resources']:
                for x in project_dict['project']['resources'][resource_name]:
                    if x == 'major':
                        self['resource_version'] = project_dict['project']['resources'][resource_name][x]
                    elif x == 'minor':
                        self['resource_version'] += '.' + project_dict['project']['resources'][resource_name][x]
                    elif x == 'patch':
                        self['resource_version'] += '.' + project_dict['project']['resources'][resource_name][x]
                    else:
                        self['resource_{}'.format(x)] = project_dict['project']['resources'][resource_name][x]
        else: # single resource's attributes
            for x in project_dict['project']['resources'][resource_name]:
                if x == 'major':
                    self['resource_version']=project_dict['project']['resources'][resource_name][x]
                elif x == 'minor':
                    self['resource_version']+='.'+project_dict['project']['resources'][resource_name][x]
                elif x == 'patch':
                    self['resource_version']+='.'+project_dict['project']['resources'][resource_name][x]
                else:
                    self['resource_{}'.format(x)]=project_dict['project']['resources'][resource_name][x]
    '''
    '''
    def getNV(self):
        nv = []
        for n in self:
            nv.append({'{}'.format('<<{}>>'.format(str(n).upper())): self[n]})
        return nv
    '''

def test_resources(status):
    from pprint import pprint
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD
    status.addTitle('Resources test')
    project_dict = TierMD(ProjectStringDefault())

    actual = Resources(project_dict, 'account')
    pprint(actual)
    #status.assert_test('Model not None', actual)
    #status.assert_test('"aud" in model', 'aud' in actual)
    #status.assert_test('"iss" in model', 'iss' in actual)
    #status.assert_test('"sub" in model', 'sub' in actual)
    #status.assert_test('"user" in model', 'user' in actual)
    #status.assert_test('"scope" in model', 'scope' in actual)
    #status.assert_test('"key" in model', 'key' in actual)

    #print('getNV', actual.getNV())


def main(status):
    test_resources(status)


if __name__ == "__main__":
    # execute as docker
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))
