from source.component.markdown.project_string_default import ProjectStringDefault
from source.component.markdown.tier_md import TierMD
from source.component.markdown.helper import route_scopes
from pprint import pprint

def main(status):
    status.addTitle('Test ')
    from pprint import pprint
    # project_dict = TierMD(ProjectStringDefault())

    #print('data', data)

if __name__ == "__main__":
    # execute as docker
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))

