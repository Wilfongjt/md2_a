from source.component.markdown.project_string_default import ProjectStringDefault
from source.component.markdown.tier_md import TierMD
class Finder(dict):
    def __init__(self, project, findkey_list):
        self.project = project

        # self.findkey_list = findkey_list

        if type(findkey_list) is str:
            self.findkey_list = [findkey_list]
            print('finder', self.findkey_list)
        else:
            self.findkey_list = findkey_list

        print('self.findkey_list',self.findkey_list)

    def read_dict_recursive(self, project, findkey_list=None, rc={}):
        """
        Recursively reads a dictionary and prints its keys and values.

        Parameters:
        d (dict): The dictionary to read.
        indent (int): Used to format the output with indentation.
        """
        #print('key',key, 'value', value)
        if not findkey_list:
            findkey_list = self.findkey_list
            #print('findkey_list', findkey_list)

        for key, value in project.items():
            #print('key', findkey_list, key)
            if findkey_list[0] == key:
                if len(findkey_list) > 1:
                    #print('A')
                    findkey_list = [k for k in findkey_list[1:]]
                    rc = self.read_dict_recursive(value,findkey_list, rc)

                else:
                    #print('B',key)
                    rc[key]=value

            elif isinstance(value, dict):
                #print('C')
                # Recursively call the function to process the nested dictionary
                rc = self.read_dict_recursive(value, findkey_list, rc)

        return rc

class Artemis(Finder):
    def __init__(self, project, findlist):
        Finder.__init__(self, project, findlist)
        #print('artemis findlist', self.findkey_list)
        rc = self.read_dict_recursive(project)
        for k in rc:
            self[k] = rc[k]
        #print('rc',self)


def main():
    from pprint import pprint

    project = TierMD(ProjectStringDefault())
    #pprint(project)
    # every other

    # claims
    claims = Artemis(project, ['claim', 'api_admin'])
    #claims = Find(project, ['claim','api_admin'])

    account = Artemis(project, ['resources','account','model'])

    pprint(claims)
    print('')
    pprint(account)

if __name__ == "__main__":
    # execute as docker
    main()
