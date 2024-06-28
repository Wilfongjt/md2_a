import os, stat
from pprint import pprint
from source.component import ProcessPackage, MultiLogger, Permissions
from able import TemplateString, \
                 EnvVarString, \
                 NameValuePairs, \
                 CloneRepo, \
                 StringWriter, \
                 TemplateList_Latest,\
                 StringReader, \
                 UpserterString,\
                 Recorder, \
                 DiagramString,\
                 Inputable, \
                 UpdaterString


class ProcessProject(ProcessPackage):
    ##
    ##### Process Project
    ##
    ## Base class for project methods

    def __init__(self):

        #def __init__(self, template_folder_key, application=None):
        ProcessPackage.__init__(self)
        ##* optional recorder
        # convert recorder to application
        self.application = None # application
        ##* template_folder_key, eg 'github'
        self.template_folder_key = None # template_folder_key # eg 'github'

        self.e_var = []

    def get_application(self):
        return self.application

    def set_application(self, application):

        self.application = application
        return self

    ##
    def get_env_var(self, env_name, default_value=None):
        ##* __get_env_var__
        rc = None
        if env_name in os.environ:
            rc = os.environ[env_name]
        elif default_value:
            rc = default_value
        return rc

    def set_env_var(self, name, value):
        ##* __set_env_var__, eg

        self.e_var.append({'name': name, 'value': value})
        return self

    def get_template_key_list(self):
        ##* __get_template_key_list__, list of template formated env vars, eg. [{\<\<GH_A>>:'abc'}, ...]

        return [{'name': '<<{}>>'.format(itm['name']),
                            'value': itm['value']}
                            for itm in NameValuePairs(multi_line_string=EnvVarString())]

    def get_template_folder_key(self):
        ##* __get_template_folder_key__, eg 'github'
        return self.template_folder_key

    def set_template_folder_key(self,template_folder_key):
        self.template_folder_key=template_folder_key
        return self
    #def get_template_name_value_pairs(self):
    #    ##* get_template_name_value_pairs
    #    nv_list = NameValuePairs(multi_line_string=EnvVarString())
    #    nv_list = [{'name': '<<{}>>'.format(itm['name']), 'value': itm['value']} for itm in nv_list]
    #    return nv_list
    def get_template_folder(self):
        if not self.get_template_folder_key():
            raise Exception('Unset template_folder_key')
        ##* __get_template_folder__, location of templates
        template_folder = os.getcwd()\
                            .replace('/component', '/template/{}'
                                     .format(self.get_template_folder_key()))\
                            .replace('/bin',
                                     '/source/template/{}'.format(self.get_template_folder_key()))

        return template_folder

    def get_branch_folder(self):
        ##* __get_branch_folder__, location of git branch
        #nv_list = self.get_template_name_value_pairs()
        return TemplateString('{}/Development/<<WS_ORGANIZATION>>/<<WS_WORKSPACE>>/<<WS_PROJECT>>/<<GH_BRANCH>>'.format(
            os.environ['HOME']), nv_list=self.get_template_key_list())

    def get_repo_folder(self):
        ##* __get_repo_folder__, location of github repo
        #nv_list = self.get_template_name_value_pairs()
        return TemplateString(
            '{}/Development/<<WS_ORGANIZATION>>/<<WS_WORKSPACE>>/<<WS_PROJECT>>/<<GH_BRANCH>>/<<GH_REPO>>'.format(
                os.environ['HOME']), nv_list=self.get_template_key_list())

    def configure_environment(self):
        ##* __configure_environment__, manually set or confirm env vars
        # set environment variables before configuring
        #if self.e_var == []:
        #    raise Exception('Environment keys are undefined!')
        # print('e_var', self.e_var)
        for v in self.e_var:
            if self.get_application(): self.get_application().add('configure')
            os.environ[v['name']] = Inputable().get_input(v['name'],
                                                          self.get_env_var(v['name'], v['value']),
                                                          hardstop=True)
        return self

    def makedirs(self, folder_file):
        ##* __makedirs__, make folders from a folder file name
        # end with / then folder
        # end without / then file
        if not str(folder_file).endswith('/'):
            # remove filename
            folder_file = '/'.join(str(folder_file).split('/')[0:-1])
        os.makedirs(folder_file, exist_ok=True)
        return self

    def templatize(self, nv_list=None, output_folder=None):
        ##* __templatize__ convert templates to code
        # #* generate templates
        #template_folder = os.getcwd().replace('/component', '/template/{}'.format(self.get_template_subfolder()))
        #template_folder = template_folder.replace('/bin', '/source/template/{}'.format(self.get_template_subfolder()))
        print('templatize 1')
        template_folder = self.get_template_folder()
        print('templatize 1.1')

        # #* Convert Templates to Code
        # print('template_folder', template_folder)
        print('templatize template_folder',template_folder)
        template_list = TemplateList_Latest(folder_path=template_folder)
        print('templatize 1.2 template_list', template_list)

        # make list of template-keys and values
        if not nv_list: nv_list = self.get_template_key_list() # self.get_template_name_value_pairs()
        print('templatize 1.3 nv_list',nv_list)

        # process list of specific templates
        for tmplt in template_list:
            print('templatize 2')

            if self.get_application(): self.get_application().add('templatize')
            # handle multiple templates of the same name
            for template_folderfile in template_list[tmplt]['template']:
                print('templatize 2.1')

                # make input and output file names
                if not output_folder:
                    output_subfolder = template_list[tmplt]['output_subfolder']
                    repo_folderfile = '{}/{}'.format(self.get_repo_folder(), output_subfolder)
                    repo_folderfile = repo_folderfile.replace('root/', '')
                    #repo_folderfile = TemplateString(repo_folderfile,nv_list)
                    #print('repo_folderfile',repo_folderfile)
                else:
                    repo_folderfile = output_folder

                cmd = str(template_folderfile).split('/')[-1].split('.')[-2]
                #print('template_folderfile',template_folderfile)
                #print('repo_folderfile    ', repo_folderfile)
                # make templatized-content from template
                #new_content = TemplateString(StringReader(template_folderfile), nv_list)
                target_content = ''
                template_content = ''
                # make target-file from templatized-content
                self.makedirs(repo_folderfile) # make output folder
                template_name = '/'.join(self.get_template_folder().split('/')[0:-1])
                print('template_name',template_name)
                MultiLogger().set_msg('   template({}) -> actual({})'.format(str(template_folderfile).replace(template_name,''), repo_folderfile.replace(self.get_branch_folder(),''))).runtime()
                if 'd' in cmd or 'D' in cmd:  # delete target
                    print('templatize 2.2')

                    if os.path.exists(repo_folderfile): os.remove(repo_folderfile)

                if 'c' in cmd or 'C' in cmd:  # create from template
                    print('templatize 2.3  ', repo_folderfile)

                    if not os.path.exists(repo_folderfile):
                        print('templatize 2.3.1')

                        #template_content = StringReader(template_folderfile)
                        template_content = TemplateString(StringReader(template_folderfile), nv_list)
                        print('write', repo_folderfile)
                        print('write', template_content)
                        StringWriter(repo_folderfile, template_content)

                if 'r' in cmd or 'R' in cmd:  # read from target
                    print('templatize 2.4')

                    target_content = TemplateString(StringReader(repo_folderfile), nv_list)
                    template_content = TemplateString(StringReader(template_folderfile), nv_list)

                if 'u' in cmd or 'U' in cmd:  # update
                    print('templatize 2.5')

                    # read template
                    # read target
                    tmp = UpdaterString(target_content).updates(template_content)
                    #print('file {} nv-list {}'.format(repo_folderfile,nv_list), nv_list)
                    StringWriter(repo_folderfile, TemplateString(tmp, nv_list))
                    #print('tmp', tmp)
                if repo_folderfile.endswith('.sh'):
                    # make file runable
                    # Change the mode of path
                    Permissions(repo_folderfile, verbose=False)
        #import subprocess

        #subprocess.run(["ls", "-l"])
        print('templatize out')

        return self

    def process(self):
        print('Hi process')
        return self

    def run(self):
        return self.process()


def main():
    from able import DiagramString
    os.environ['GH_TEST'] = 'TEST'
    #print ('ProcessProject',ProcessProject('github', recorder=Recorder()))
    #print('ProcessProject', ProcessProject().set_application('github').get_application() )
    #assert (ProcessProject().set_application('github').get_application() == 'github')
    #assert (ProcessProject('github', application=None) == {})

    assert (ProcessProject().assign(ProcessPackage().set('A', 'a')).get('A') == 'a')
    print ('xxx',ProcessProject().get_template_folder_key() )

    assert (ProcessProject().set_template_folder_key('github').get_template_folder_key() == 'github')

    assert (ProcessProject().get_template_key_list() == [{'name': '<<GH_TEST>>', 'value': 'TEST'}])
    assert (ProcessProject().get_branch_folder() == '/Users/jameswilfong/Development/<<WS_ORGANIZATION>>/<<WS_WORKSPACE>>/<<WS_PROJECT>>/<<GH_BRANCH>>')
    assert (ProcessProject().get_repo_folder() == '/Users/jameswilfong/Development/<<WS_ORGANIZATION>>/<<WS_WORKSPACE>>/<<WS_PROJECT>>/<<GH_BRANCH>>/<<GH_REPO>>')

    ProcessProject().set_env_var('GH_TEST', 'TEST').configure_environment()

    ProcessProject().set_template_folder_key('__project__').templatize()

if __name__ == "__main__":
    # execute as docker
    main()