from source.component.markdown.tier_md import TierMD
from source.component.markdown.helper.project_name_first import ProjectNameFirst
from source.component.markdown.data import Data
from source.component.markdown.claims import Claims
from source.component.markdown.model import Model
from source.component.markdown.scopes import Scopes
from source.component.markdown.privileges import Privileges


class ProjectMD(TierMD):
    # setResourceName to limit config to given resource
    # setScope to limit config to given scope
    # contains configuration for all resources and scopes
    # setScopeName to limit config to given scope
    def __init__(self, md_text, resource_name=None, scope_name=None, echo=False):
        TierMD.__init__(self, md_text, echo)
        #self.project_name=project_name
        self.project_name=self['project']['name']
        self.resource_name=resource_name
        self.scope_name=scope_name

        #if not project_name: self.project_name = self['project'][ProjectNameFirst(self)]
        if not resource_name: self.resource_name = 'account'
        if not scope_name: self.scope_name = 'api_guest'

    def getProjectName(self):
        return self.project_name

    def setResourceName(self, resource_name):
        self.resource_name = resource_name
        return self
    def getResourceName(self):
        return self.resource_name

    def setScopeName(self,scope_name):
        self.scope_name = scope_name
        return self
    def getScopeName(self):
        return self.scope_name

    def getScopes(self):
        return Scopes(self, self.getResourceName())

    def getClaim(self): #, scope='api_guest', key=None):
        # get claim keys for a scope and resource in a project_dict
        # dependencies, project_name, resource_name, scope_name
        claim = Claims(self, self.getScopeName())
        return claim

    def getData(self):
        # dependencies, project_name, resource_name, scope_name
        return Data(self, self.getResourceName(), self.getScopeName())

    def getModel(self):
        # dependencies, project_name, resource_name, scope_name
        return Model(self, self.getResourceName())

    def getPrivileges(self): #project_dict, resource_name, scope_name
        return Privileges(self,self.getResourceName(), self.getScopeName())

def test_project_md(status):
    from source.component.markdown.project_string_default import ProjectStringDefault
    from pprint import pprint

    status.addTitle('Project MD test')
    actual = ProjectMD(ProjectStringDefault())
    status.assert_test('ProjectMD not None', actual)

    status.assert_test ('.getProjectName() == "sample"', actual.getProjectName() == 'sample')
    status.assert_test ('.getResourceName() == "account"', actual.getResourceName() == 'account')
    status.assert_test ('.getScopeName() == "api_guest"', actual.getScopeName() == 'api_guest')

    status.assert_test('.getClaim() not None', actual.getClaim() != None)
    status.assert_test('.getData() not None', actual.getData() != None)

    status.assert_test('.getPrivileges() not None', actual.getPrivileges() != None)
    status.assert_test('.getScopes() not None', actual.getScopes() != None)

def main(status):
    test_project_md(status)

if __name__ == "__main__":
    # execute as docker
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))