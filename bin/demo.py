from source.component.markdown.project_string_default import ProjectStringDefault
from source.component.markdown.tier_md import TierMD
from source.component.markdown.helper import route_scopes
from able.string_reader import StringReader
import re

from pprint import pprint

class TemplateKeyList(list):
    # Make list of keys from template string
    # List is unique
    # [{"name": "<<A>>"},{"name":"<<B>>"},...{"name": "<<N">>}]

    def __init__(self, template_string=None):
        if template_string:
            pattern = r"<<[A-Z_]+>>"
            #print('text', template_string)

            matches = re.findall(pattern, template_string)
            #print('matches', matches)
            matches = set(matches)
            #print('matches', matches)
            for x in matches:
                if x not in self:
                    self.append(x)

def main(status):
    from source.component.template_files import TemplateFileLatest
    status.addTitle('Test ')
    from pprint import pprint
    #subfolder = 'docker'
    #template_files = TemplateFileLatest(subfolder=subfolder)
    template_files = TemplateFileLatest()
    print('template_files',template_files)
    keylist = [] # KeyList()
    keylist = TemplateKeyList(StringReader(template_files))

    #for file_name in template_files:
    #    keylist.extend(TemplateKeyList(StringReader(file_name)))
    keylist = sorted(keylist)
    #keylist = sorted(set(keylist))

    keylist = [{'name': key, 'value': 'uk'} for key in keylist]
    print('keylist', keylist)
    pprint(keylist)

if __name__ == "__main__":
    # execute as docker
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))

