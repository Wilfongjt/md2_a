from source.component.markdown.project_string_default import ProjectStringDefault
from source.component.markdown.tier_md import TierMD
class Finder(dict):
    '''
    base class for Find
    recursive
    '''
    def __init__(self, project, findkey_list):
        self.project = project

        if type(findkey_list) is str:
            self.findkey_list = [findkey_list]
        else:
            self.findkey_list = findkey_list

    def read_dict_recursive(self, project, findkey_list=None):
        """
        Recursively reads a dictionary and prints its keys and values.

        Parameters:
        project (dict): The dictionary to read.

        """
        rc = {}
        if not findkey_list:
            findkey_list = self.findkey_list

        for key, value in project.items():
            if findkey_list[0] == key:
                if len(findkey_list) > 1: # go again
                    findkey_list = [k for k in findkey_list[1:]] # get rid of first key
                    rc = self.read_dict_recursive(value,findkey_list)

                else: # found
                    rc[key]=value
                    return rc

            elif isinstance(value, dict):
                # Recursively call the function to process the nested dictionary
                rc = self.read_dict_recursive(value, findkey_list)

        return rc

class Find(Finder):
    def __init__(self, project, findlist):
        Finder.__init__(self, project, findlist)
        #print('artemis findlist', self.findkey_list)
        rc = self.read_dict_recursive(project)
        for k in rc:
            self[k] = rc[k]
        #print('rc',self)


def main(status):
    from pprint import pprint
    status.addTitle('Find test')

    project = TierMD(ProjectStringDefault())

    # claims
    claims = Find(project, ['claim', 'api_admin'])
    status.assert_test("'api_admin' in claims", 'api_admin' in claims)

    account = Find(project, ['account', 'model'])
    status.assert_test ("'model' in account", 'model' in account)


if __name__ == "__main__":
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))