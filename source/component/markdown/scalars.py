class RecursiveScalar():
    #print('recersive')

    def getScalars(self, dictionary,pkey=None):
        # print('section', self.getClassName())
        scalars = []
        #if not self.pa:
        #    self.setScalarParent(self)
        #print('getScalars', dictionary)
        if not pkey:
            #print('A')
            pkey = self.__class__.__name__

        # used by NVList
        for k, v in dictionary.items():
            if isinstance(v, dict):
                #print('B',k)
                scalars.extend(self.getScalars(v,pkey=k))
                #scalars.extend(self.getScalars(dictionary=v, pkey=k))
            else:
                #print('C')
                s = {'{}{}_{}{}'.format(self.lwrapper, pkey.upper(), k.upper(), self.rwrapper): v}
                scalars.append(s)

        return scalars
    '''
        def getScalars(self, dictionary=None, pkey=None):
        # print('section', self.getClassName())
        scalars = []
        if not self.parent:
            self.setScalarParent(self)
        if not dictionary:
            dictionary = self
        if not pkey:
            pkey = self.__class__.__name__
        # used by NVList
        for k, v in dictionary.items():
            if isinstance(v, dict):
                scalars.extend(self.getScalars(dictionary=v, pkey=k))
            else:
                s = {'{}{}_{}{}'.format(self.lwrapper, pkey.upper(), k.upper(), self.rwrapper): v}
                scalars.append(s)

        # print('scalar', scalars)
        return scalars
    '''

class Scalars(list, RecursiveScalar):

    def __init__(self, dictionary, pkey=None):
        self.parent = pkey
        self.lwrapper = '<<'
        self.rwrapper = '>>'
        self.extend(self.getScalars(dictionary,pkey=pkey))

    def setScalarParent(self, key):
        self.parent = key
        return self

def test_scalars(status):

    from pprint import pprint
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD
    from source.component.markdown.model import Model
    from source.component.markdown.claims import Claims

    status.addTitle('Scalars test')

    status.addTitle('model scalars')
    project_dict = TierMD(ProjectStringDefault())

    #model = Model(project_dict=project_dict, resource_name='account')
    print('model ', Scalars(Model(project_dict=project_dict, resource_name='account')))
    print('claims', Scalars(Claims(project_dict,'api_admin'),pkey='api_admin'))
    #print('count', len(actual))
    #print('Scalars',actual)
    #pprint(actual)


def main(status):
    test_scalars(status)

if __name__ == "__main__":
    # execute as docker
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))
