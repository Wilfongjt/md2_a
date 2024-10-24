from source.component.markdown.tier_md import TierMD
from source.component.markdown.helper.project_name_first import ProjectNameFirst
from source.component.markdown.data import Data
from source.component.markdown.claim import Claim
from source.component.markdown.model import Model

class ProjectMD(TierMD):
    def __init__(self, md_text, echo=False):
        TierMD.__init__(self, md_text, echo)
        self.project_name = ProjectNameFirst(self)
        print('project_name', ProjectNameFirst(self))
        self.resource_name = 'account'
        self.scope_name = 'api_guest'

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

    def getClaim(self, scope='api_guest', key=None):
        # get claim keys for a scope and resource in a project_dict
        claim = Claim(self, self.getProjectName(), self.getResourceName(), self.getScopeName())
        return claim

    def getData(self):
        return Data(self, self.getProjectName(), self.getResourceName(), self.getScopeName())

    def getModel(self):
        return Model(self, self.getProjectName(),self.getResourceName(), self.getScopeName())

def test_project_md(status):
    from source.component.markdown.project_string_default import ProjectStringDefault

    status.addTitle('Project MD test')
    actual = ProjectMD(ProjectStringDefault())
    status.assert_test('ProjectMD not None', actual)
    status.assert_test ('.getProjectName() == "sample"', actual.getProjectName() == 'sample')
    status.assert_test ('.getResourceName() == "account"', actual.getResourceName() == 'account')
    status.assert_test ('.getScopeName() == "api_guest"', actual.getScopeName() == 'api_guest')

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