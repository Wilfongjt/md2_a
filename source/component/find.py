from source.component.markdown.project_string_default import ProjectStringDefault
from source.component.markdown.tier_md import TierMD
class Finder(dict):
    '''
    base class for Find
    recursive
    '''
    def __init__(self, project, findkey_list, inclusive=True):
        self.project = project
        self.idx = 0
        self.foundbranch = {}
        self.keycnt = len(findkey_list)
        if type(findkey_list) is str:
            self.find_list = [findkey_list]
        else:
            self.findkey_list = findkey_list

    def read_dict_recursive(self, project):
        """
        Recursively reads a dictionary and prints its keys and values.

        Parameters:
        project_dict (dict): The dictionary to read.

        """
        rc = {}

        for key, value in project.items():

            if self.keycnt == self.idx:
                return self.foundbranch

            if self.findkey_list[self.idx] == key:
                self.foundbranch = value
                self.idx += 1

                if self.keycnt == self.idx:
                    return self.foundbranch

            if isinstance(value, dict):
                # Recursively call the function to process the nested dictionary
                rc = self.read_dict_recursive(value)

        return rc


class Find(Finder):
    def __init__(self, project, findlist, inclusive=True):
        Finder.__init__(self, project, findlist, inclusive=True)

        rc = self.read_dict_recursive(project)
        print('findlist', findlist)
        print('rc', rc)

        if inclusive:
            me = self
            lastme = self
            for k in self.findkey_list:
                lastme = me
                me[k]={}
                me = me[k]

            if type(rc) not in [dict, list]:
                lastme[self.findkey_list[-1]] = rc

            if type(rc) in [dict, list]:
                for k in rc:
                    me[k] = rc[k]
        else:
            for k in rc:
                print('k ', k)
                print('rc', rc[k])
                if type(rc[k]) in [dict, list]:
                    print('self', self)
                    self[k] = rc[k]
                else:
                    print('self', self)
                    self[k]=rc[k]

        #if not inclusive:
        #    last = findlist[-1]


def main(status):
    from pprint import pprint
    status.addTitle('Find tests')

    project_dict = TierMD(ProjectStringDefault())

    status.assert_test("Find(project, ['models', 'account','id','size'])", Find(project_dict, ['models', 'account','id','size']) == {'models': {'account': {'id': {'size': '3-330'}}}})
    status.assert_test("Find(project, ['models', 'account','id','type'])", Find(project_dict, ['models', 'account','id','type']) == {'models': {'account': {'id': {'type': 'C'}}}})

    print('find',Find(project_dict, ['claims', 'api_admin'], inclusive=True))
    status.assert_test('Find Inclusive','claims' in Find(project_dict, ['claims', 'api_admin'], inclusive=True))
    print('find',Find(project_dict, ['claims', 'api_admin'], inclusive=False))
    status.assert_test('Find Not Inclusive','claims' not in Find(project_dict, ['claims', 'api_admin'], inclusive=False))

    #status.assert_test("Find(project, ['claims'])", Find(project_dict, ['claims']) == )

if __name__ == "__main__":
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))