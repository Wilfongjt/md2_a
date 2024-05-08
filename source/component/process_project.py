import os
from pprint import pprint
#from process_package import ProcessPackage
from source.component import ProcessPackage

#from source.component.process_package import ProcessPackage

from able import TemplateString, \
                 EnvVarString, \
                 NameValuePairs, \
                 CloneRepo, \
                 StringWriter, \
                 TemplateList_Latest,\
                 StringReader, \
                 UpserterString,\
                 Recorder, DiagramString,Inputable


class ProcessProject(ProcessPackage):
    ##
    ##### Process Project
    ##
    ## Base class for common methods
    def __init__(self, template_subfolder_name, recorder):
        ##* optional recorder
        self.recorder = recorder
        ##* template_subfolder_name, eg 'github'
        self.template_subfolder_name = template_subfolder_name # eg 'github'

        self['nv_list'] = [{'name': '<<{}>>'.format(itm['name']),
                            'value': itm['value']}
                        for itm in NameValuePairs(multi_line_string=EnvVarString())]

        repo_folder_template='{}/Development/<<WS_ORGANIZATION>>/<<WS_WORKSPACE>>/<<WS_PROJECT>>/<<GH_BRANCH>>/<<GH_REPO>>'
        self['repo_folder']= TemplateString(repo_folder_template.format(os.environ['HOME']), nv_list=self['nv_list'])

        # environment variable names with default values

        self.e_var = []

    def get_env_var(self, env_name, default_value=None):
        ##* get_env_var
        rc = None
        if env_name in os.environ:
            rc = os.environ[env_name]
        elif default_value:
            rc = default_value
        return rc

    def set_env_var(self, name, value):
        ##* set_env_var

        if self.recorder: self.recorder.add('configure')

        self.e_var.append({'name': name, 'value': value})
        return self

    def configure_environment(self):
        ##* configure_environment

        for v in self.e_var:
            self.recorder.add('configure')
            os.environ[v['name']] = Inputable().get_input(v['name'],
                                                          self.get_env_var(v['name'], v['value']),
                                                          hardstop=True)
        return self

    def get_template_subfolder(self):
        ##* get_template_subfolder
        return self.template_subfolder_name

    def get_template_name_value_pairs(self):
        ##* get_template_name_value_pairs
        nv_list = NameValuePairs(multi_line_string=EnvVarString())
        nv_list = [{'name': '<<{}>>'.format(itm['name']), 'value': itm['value']} for itm in nv_list]
        return nv_list

    def get_branch_folder(self):
        ##* get_branch_folder
        nv_list = self.get_template_name_value_pairs()
        return TemplateString('{}/Development/<<WS_ORGANIZATION>>/<<WS_WORKSPACE>>/<<WS_PROJECT>>/<<GH_BRANCH>>'.format(
            os.environ['HOME']), nv_list=nv_list)

    def get_repo_folder(self):
        ##* get_repo_folder
        nv_list = self.get_template_name_value_pairs()
        return TemplateString(
            '{}/Development/<<WS_ORGANIZATION>>/<<WS_WORKSPACE>>/<<WS_PROJECT>>/<<GH_BRANCH>>/<<GH_REPO>>'.format(
                os.environ['HOME']), nv_list=nv_list)

    def makedirs(self, folder_file):
        ##* makedirs
        # end with / then folder
        # end without / then file
        if not str(folder_file).endswith('/'):
            # remove filename
            folder_file = '/'.join(str(folder_file).split('/')[0:-1])
        os.makedirs(folder_file, exist_ok=True)
        return self

    def templatize(self):
        ##* templatize
        # #* locate templates
        template_folder = os.getcwd().replace('/component', '/template/{}'.format(self.get_template_subfolder()))
        template_folder = template_folder.replace('/bin', '/source/template/{}'.format(self.get_template_subfolder()))

        # #* Convert Templates to Code
        template_list = TemplateList_Latest(folder_path=template_folder)

        # make list of template-keys and values
        nv_list = self.get_template_name_value_pairs()

        # process list of specific templates
        for tmplt in template_list:

            if self.recorder: self.recorder.add('templatize')
            # handle multiple templates of the same name
            for template_folderfile in template_list[tmplt]['template']:
                # make output folder

                # make input and output file names
                repo_folderfile = '{}/{}'.format(self.get_repo_folder(), template_list[tmplt]['output_subfolder'])
                repo_folderfile = repo_folderfile.replace('root/', '')

                # make templatized-content from template
                new_content = TemplateString(StringReader(template_folderfile), nv_list)

                # make target-file from templatized-content
                self.makedirs(repo_folderfile)
                StringWriter(repo_folderfile, new_content)

        return self

    def process(self):
        print('Hi process')
        return self

    def run(self):
        return self.process()


def main():
    from able import DiagramString
    os.environ['GH_TEST'] = 'TEST'

    assert (ProcessProject('github', recorder=Recorder()) != {})

    assert (ProcessProject('github', recorder=Recorder()).assign(ProcessPackage().set('A', 'a')).get('A') == 'a')
    assert (ProcessProject('github', recorder=Recorder()).get_template_subfolder() == 'github')
    assert (ProcessProject('github', recorder=Recorder()).get_template_name_value_pairs() == [{'name': '<<GH_TEST>>', 'value': 'TEST'}])
    assert (ProcessProject('github', recorder=Recorder()).get_branch_folder() == '/Users/jameswilfong/Development/<<WS_ORGANIZATION>>/<<WS_WORKSPACE>>/<<WS_PROJECT>>/<<GH_BRANCH>>')
    assert (ProcessProject('github', recorder=Recorder()).get_repo_folder() == '/Users/jameswilfong/Development/<<WS_ORGANIZATION>>/<<WS_WORKSPACE>>/<<WS_PROJECT>>/<<GH_BRANCH>>/<<GH_REPO>>')

    ProcessProject('github', recorder=Recorder()).configure_environment()
if __name__ == "__main__":
    # execute as docker
    main()