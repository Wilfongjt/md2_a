import os
import sys
#SCRIPT_DIR = os.path.dirname(str(os.path.abspath(__file__)).replace('/bin','/source/component'))
#sys.path.append(os.path.dirname(SCRIPT_DIR))
#print('SCRIPT_DIR',SCRIPT_DIR)
from able import StringReader, \
                 StringWriter, \
                 UpserterString, \
                 EnvVarString,\
                 Recorder,\
                 NameValuePairs,\
                 TemplateString, \
                 CloneRepo,\
                 DiagramString

from functions import get_bin_folder, \
    get_template_folder, \
    get_env_variable_values_string
    #get_env_var,\
#from source.component import ProcessGithub
from source.component import ProcessProject

class Application(Recorder):
    def __init__(self, name='md2'):
        Recorder.__init__(self)
        #self.name = name
        self['name']=name

    def get_name(self):
        return self['name']

    def set_name(self, name):
        self['name']=name
        return self

    def get_bin_folder(self):
        return os.getcwd()

    def get_template_folder(self):
        return os.getcwd().replace('/bin', '/source/template')

    def get_environment_filename(self):
        # env is stored in the bin folder bin/md2
        return '{}/{}.env'.format(self.get_bin_folder(), self.get_name())

    def get_environment_template_filename(self):
        return '{}/{}.env.tmpl'.format(self.get_template_folder(), self.get_name())

    def get_environment_varable_names(self, prefix):

        rc = [item for item in os.environ
                if item.startswith(prefix)]
        return ', '.join(rc)

#def isStringNone(str_object):
#    rc = str_object
#    if str_object == None:
#        rc = None
#    elif str_object == 'None':
#        rc = None
#    return rc



#def get_template_name_value_pairs():
#    nv_list = NameValuePairs(multi_line_string=EnvVarString())
#    nv_list = [{'name': '<<{}>>'.format(itm['name']), 'value': itm['value']} for itm in nv_list]
#    return nv_list

#def get_branch_folder():
#    nv_list = get_template_name_value_pairs()
#    return TemplateString('{}/Development/<<WS_ORGANIZATION>>/<<WS_WORKSPACE>>/<<WS_PROJECT>>/<<GH_BRANCH>>'.format(os.environ['HOME']), nv_list=nv_list)

#def get_repo_folder():
#    nv_list = get_template_name_value_pairs()
#    return TemplateString('{}/Development/<<WS_ORGANIZATION>>/<<WS_WORKSPACE>>/<<WS_PROJECT>>/<<GH_BRANCH>>/<<GH_REPO>>'.format(os.environ['HOME']), nv_list=nv_list)

#def output_name(folder_file):
#    everyother = str(folder_file).split('/')[::2]
#    print('everyother',everyother)
#    return folder_file
##
### MD2 Script
##
##__Terms__
##* __NF__ means Not Found
##* __\<root>__ refers to the current repo's root folder
##* __\<repo>__ refers to a target or new repository
##* __configure__ refers to the setting of values which alter the outcome of a process
##* __initiate__ means to start/execute a process
##* __initialize__ refers to the creation of something when nothing was there previously
##* __template__ refers to a file of content, complete with template-keys and/or default values

class Auto():
    def __init__(self, process):
        process.run()


def main():
    #recorder = Recorder()
    app = Application('md2')
    ##
    #### MD2 Process
    ##
    ## Make what is not there

    ##1. [__Initialize__ md2](#initialize~md2)

    # initialize_md2(recorder)
    Auto(ProcessMd2().set_application(app))

    ##1. [__Configure__ Environment Values](#configure~environment~values)

    # load env from file

    Auto(ProcessConfigure().set_application(app)) #(env_file_content_string, app)

    ##1. [__Initialize__ Repository](#clone~process)

    # clone_github_repository(recorder)
    Auto(ProcessGithub().set_application(app))

    # #1. [__Initialize__ GitHub Repository](#initialize~clone)

    #initialize_github(recorder)

    # #1. __Commit__ Environment Values __To__ '\<root>/bin/md2.env'

    ##1. __Commit__ Environment Values
    Auto(ProcessCommit().set_application(app))
    exit(0)
    #commit_environment(recorder)

    #print('recorder: {}'.format(recorder))
    print(DiagramString().set_application(app))

class ProcessMd2(ProcessProject):

    def __init__(self): # , recorder):
        ProcessProject.__init__(self)
        # self.set_application(recorder)

    def initialize_md2(self):

        ##
        ##### Initialize md2
        ##
        ## Make the md2.env file
        #print('A application', not self.get_application())
        if not self.get_application():
            raise Exception('Application Not Found!')
        #recorder.add('initialize')
        #print('B')
        ##* __Create__ '\<root>/bin/md2.env' __From__ template __When__ file NF

        env_name = self.get_application().get_environment_filename().split('/')[-1]
        #print('C')

        if not os.path.isfile(self.get_application().get_environment_filename()):
            #    print('D')

            # init from template
            env_file_content_string = self.get_application().isStringNone(StringReader(self.get_application().get_environment_template_filename()))
            assert(env_file_content_string)
            StringWriter(self.get_application().get_environment_filename(),env_file_content_string)
        #print('E')

        self.get_application().add('initialize ({})'.format(env_name))
        return self

    def process(self):
        print('1. Initialize md2')
        self.initialize_md2()
        print('    step {} {}'.format(self.get_application().get_name(),DiagramString(self.get_application())))
        return self

class ProcessConfigure(ProcessProject):
    def __init__(self): #, env_file_content_string): # , recorder):
        ProcessProject.__init__(self)
        #def __init__(self, env_file_content_string, recorder=None):
        #super().__init__(template_folder_key='github', recorder=recorder)
        # package is {nv_list, repo_folder, template_folder}
        #
        #self.recorder = recorder
        self.env_file_content_string=None #env_file_content_string

    def configure_environment(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        ##
        ##### Configure Environment Values
        ##1. Project Values
        ##    * __Configure__ WS_ORGANIZATION
        self.set_env_var('WS_ORGANIZATION', 'test-org')
        ##    * __Configure__ WS_WORKSPACE
        self.set_env_var('WS_WORKSPACE', 'test-ws')
        ##    * __Configure__ WS_PROJECT
        self.set_env_var('WS_PROJECT', 'test-prj')
        ##    * __Configure__ WS_REPO
        self.set_env_var('WS_REPO', 'py_test')

        ##
        ##2. GitHub Values
        ##    * __Configure__ GH_TRUNK
        self.set_env_var('GH_TRUNK','main')
        ##    * __Configure__ GH_PROJECT
        self.set_env_var('GH_PROJECT','test-prj')
        ##    * __Configure__ GH_BRANCH
        self.set_env_var('GH_BRANCH','first')
        ##    * __Configure__ GH_REPO
        self.set_env_var('GH_REPO','py_test')
        ##    * __Configure__ GH_USER
        self.set_env_var('GH_USER','x')
        ##    * __Configure__ GH_MESSAGE
        self.set_env_var('GH_MESSAGE','init')
        ##    * __Configure__ GH_TOKEN
        self.set_env_var('GH_TOKEN','x')

        super().configure_environment()
        # env_file_content_string = ''
        print('2. Configure Environment:')
        env_file_content_string = StringReader(self.get_application().get_environment_filename())

        self.env_file_content_string = UpserterString(env_file_content_string,
                                                 settings={'dup': True, 'hard_fail': True}) \
            .upsert(EnvVarString())
        #return env_file_content_string
        return self

    def process(self):
        self.configure_environment()
        print('    step {} {}'.format(self.get_application().get_name(),DiagramString(self.get_application())))
        return self

class ProcessGithub(ProcessProject):
    def __init__(self): # , recorder=None ):
        ProcessProject.__init__(self)
        #super().__init__(template_folder_key='github', recorder=recorder)

        # package is {nv_list, repo_folder, template_folder}
        #
        #self.recorder=recorder
        self.set_template_folder_key('github')

    def clone(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        #if self.recorder: self.recorder.add('clone')
        repo_name = os.environ['GH_REPO']
        self.get_application().add('clone ({})'.format(repo_name))

        ##
        ##### Initialize Repository
        ## Create and Configure a Project Repository.

        ##* __Create__ Branch Folder __When__ folder is NF
        branch_folder = self.get_branch_folder()
        os.makedirs(branch_folder, exist_ok=True)

        ##* __Clone__ '\<repo>' __When__ repo is NF
        repo_folder = '{}/{}'.format(branch_folder, repo_name)

        if not os.path.isdir(repo_folder):
            repo_name = repo_folder.split('/')[-1]
            # if self.recorder: self.recorder.add('clone ({})'.format(repo_name))
            if 'GH_TEST' not in os.environ:
                CloneRepo(repo_folder=repo_folder, username_gh=os.environ['GH_USER'])
            else:
                self.makedirs(repo_folder)
        #else:
        #    repo_name = repo_folder.split('/')[-1]
            # if self.recorder: self.recorder.add('cloned ({})'.format(repo_name))

        return self

    def patch(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        ##* __Patch__ .gitignore

        self.get_application().add('patch(.gitignore)')

        repo_folder = self.get_repo_folder()
        repo_name = repo_folder.split('/')[-1]
        ##
        ##* Fix the .gitignore file
        temp_file = '{}/.gitignore'.format(repo_folder)

        if not os.path.isfile(temp_file):
            if 'GH_TEST' not in os.environ:
                raise Exception('Uninitialized file ({})'.format(temp_file.split('/')[-1]))
        temp_contents = ''
        if os.path.isfile(temp_file):
            temp_contents = StringReader(temp_file)
        temp_contents = UpserterString(temp_contents, settings={'dup': True, 'hard_fail': True}, recorder=self.get_application()) \
            .upsert('*.env') \
            .upsert('.idea/')
        self.makedirs(temp_file)
        StringWriter(temp_file, temp_contents)
        return self

    def process(self):
        print('3. GitHub:')

        self.clone()
        self.patch()
        self.templatize()
        print('    step {} {}'.format(self.get_application().get_name(),DiagramString(self.get_application())))

        return self

class ProcessCommit(ProcessProject):
    def __init__(self): #, env_file_content_string, recorder=None):
        ProcessProject.__init__(self) #(template_folder_key='github', recorder=recorder)
        # package is {nv_list, repo_folder, template_folder}
        #
        #self.recorder = recorder
        #self.env_file_content_string=env_file_content_string

    def commit_environment(self):

        if not self.get_application():
            raise Exception('Application Not Found!')

        env_name = str(self.get_application().get_environment_filename()).split('/')[-1]
        self.get_application().add('commit ({})'.format(env_name))
        ##
        ##### Commit Environment Values
        ##
        ## Save user's environment changes.
        env_file_content_string = StringReader(self.get_application().get_environment_filename())
        env_file_content_string = UpserterString(env_file_content_string, settings={'dup': True, 'hard_fail': True},
                                                 recorder=self.get_application()).upsert(get_env_variable_values_string())
        ##1. __Commit__ Environment Values __To__ '\<root>/bin/md2.env'

        StringWriter(self.get_application().get_environment_filename(),
                     env_file_content_string,
                     self.get_application())

        print('    step {} {}'.format(self.get_application().get_name(),DiagramString(self.get_application())))

        assert (self.get_application().get_environment_filename())
        return self

    def process(self):
        print('4. Commit:')

        self.commit_environment()
        return self

#### Classes
if __name__ == "__main__":
    # execute as docker
    main()