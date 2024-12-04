import os

class TemplateFileLatest(list):
    # template files always in "/latest" template_folder
    # template files alway end with ".tmpl"
    def __init__(self, template_folder=None, subfolder=None):
        #print('template_folder', template_folder)

        if not template_folder:
            template_folder = os.getcwd().replace('/component', '/template').replace('/bin','/source/template')

        if subfolder:
            template_folder= '{}/{}'.format(template_folder, subfolder)

        #print('template_folder', template_folder)

        for root, dirs, files in os.walk(template_folder):
            if str(root).endswith('latest'):
                #print('root', root)
                for file in files:
                    if str(file).endswith('.tmpl'):
                        self.append('{}/{}'.format(root,file))


def test_template_files(status):
    status.addTitle('TemplateFileLatest test')
    status.addLine('default folder')

    actual = TemplateFileLatest() # get all from default template folder
    status.assert_test('TemplateFileLatest is not []', actual != [])

    actual= TemplateFileLatest(subfolder='docker') # limit to default template folder and the docker subfolderr
    status.assert_test("TemplateFileLatest(subfolder='docker') is not []", actual != [])

def main(status):
    from pprint import pprint
    #from able import StringReader
    test_template_files(status)

    #template_folder = os.getcwd().replace('/component', '/template/github')
    #print('template_folder',template_folder)


if __name__ == "__main__":
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))