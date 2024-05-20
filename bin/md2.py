##
### MD2 Script
##
## __Goal__: Make what is not there
##
## __Strategy__: break down process into tasks and code those tasks in classes. Run the classes in order.

import os
import sys
import datetime
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
                 DiagramString, \
                 RuntimeLogger

from functions import get_bin_folder, \
    get_template_folder, \
    get_env_variable_values_string
    #get_env_var,\

from source.component import ProcessProject, Application

# Terms

##
##__Terms__
##* __NF__ means Not Found
##* __\<root>__ refers to the current repo's root folder
##* __\<repo>__ refers to a target or new repository
##* __configure__ refers to the setting of values which alter the outcome of a process
##* __initiate__ means to start/execute a process
##* __initialize__ refers to the creation of something when nothing was there previously
##* __template__ refers to a file of content, complete with template-keys and/or default values


def main():

    MultiLogger('df').set_msg('start').runtime().terminal()
    app = Application('md2').load_environment()

    ##
    #### MD2 Process
    ##
    ##### Tasks
    ##1. [Initialize MD2](#initialize-md2)

    Auto(TaskMd2().set_application(app))

    ##1. [Configure MD2 Environment Values](#configure-md2-environment-values)

    # load env from file

    Auto(TaskConfigure().set_application(app)) #(env_file_content_string, app)

    ##1. [Clone GitHub Repository](#clone-github-repository)

    Auto(TaskGithub().set_application(app))

    # #1. [Initialize GitHub Repository](#initialize-github-repository)
    ##1. [Patch Clone](#patch-clone)

    Auto(TaskGithubPatch().set_application(app))

    ##1. [Update Environment Values](#update-md2-environment-variables)

    Auto(TaskUpdateEnvironment().set_application(app))

    xx = 'Summary {} {}'.format(app.get_name(), DiagramString(app))
    MultiLogger().set_msg(xx).runtime().terminal()
    MultiLogger().set_msg('end').runtime().terminal()

# Steps

class TaskMd2(ProcessProject):
    ##
    ##### Initialize MD2
    ##
    ## Make the md2.env file
    def __init__(self):
        ProcessProject.__init__(self)

    def initialize_md2(self):

        if not self.get_application():
            MultiLogger().set_msg('Application Not Found!').runtime().terminal()
            raise Exception('Application Not Found!')

        ##* __Create__ '\<root>/bin/md2.env' __From__ template __When__ file NF

        env_name = self.get_application().get_environment_filename().split('/')[-1]
        if not os.path.isfile(self.get_application().get_environment_filename()):

            MultiLogger().set_msg('    Create ({})'.format(env_name)).runtime().terminal()

            # init from template
            env_file_content_string = self.get_application().isStringNone(StringReader(self.get_application().get_environment_template_filename()))
            assert(env_file_content_string)
            StringWriter(self.get_application().get_environment_filename(),env_file_content_string)

        self.get_application().add('initialize ({})'.format(env_name))
        return self

    def process(self):
        # print('1. Initialize MD2')
        MultiLogger().set_msg('1. Initialize Environment {}'.format(self.get_application().get_name())).runtime().terminal()

        self.initialize_md2()

        return self

class TaskConfigure(ProcessProject):
    ##
    ##### Configure MD2 Environment Values
    def __init__(self): #, env_file_content_string): # , recorder):
        ProcessProject.__init__(self)
        # package is {nv_list, repo_folder, template_folder}
        #
        self.env_file_content_string=None #env_file_content_string

    def configure_environment(self):
        if not self.get_application():
            raise Exception('Application Not Found!')

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
        env_file_content_string = StringReader(self.get_application().get_environment_filename())

        self.env_file_content_string = UpserterString(env_file_content_string,
                                                 settings={'dup': True, 'hard_fail': True}) \
            .upsert(EnvVarString())
        return self

    def process(self):
        MultiLogger().set_msg('2. Configure {}'.format(self.get_application().get_name())).runtime().terminal()

        self.configure_environment()

        return self

class TaskGithub(ProcessProject):
    ##
    ##### Clone GitHub Repository
    ## Create and Configure a Project Repository.
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

        repo_name = os.environ['GH_REPO']
        self.get_application().add('clone ({})'.format(repo_name))

        ##* __Create__ Branch Folder __When__ folder is NF
        branch_folder = self.get_branch_folder()
        os.makedirs(branch_folder, exist_ok=True)

        ##* __Clone__ '\<repo>' __When__ repo is NF
        repo_folder = '{}/{}'.format(branch_folder, repo_name)

        if not os.path.isdir(repo_folder):
            repo_name = repo_folder.split('/')[-1]
            if 'GH_TEST' not in os.environ:
                CloneRepo(repo_folder=repo_folder, username_gh=os.environ['GH_USER'])
            else:
                self.makedirs(repo_folder)

        return self

    def process(self):
        #print('3. GitHub:')
        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('3. GitHub: {}'.format(repo_name)).runtime().terminal()

        self.clone()
        self.templatize()

        return self

class TaskGithubPatch(ProcessProject):
    ##
    ##### Patch Clone
    ##
    def __init__(self): # , recorder=None ):
        ProcessProject.__init__(self)
        # package is {nv_list, repo_folder, template_folder}

    def patch(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        ##* __Patch__ .gitignore

        self.get_application().add('patch(.gitignore)')

        repo_folder = self.get_repo_folder()
        #repo_name = repo_folder.split('/')[-1]

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
        ##  * add "*.env" when NF
        ##  * add "*.idea" when NF
        ##
        #self.makedirs(temp_file)
        StringWriter(temp_file, temp_contents)
        return self

    def process(self):

        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('4. GitHub Patch: {}'.format(repo_name)).runtime().terminal()

        self.patch()

        return self

class TaskUpdateEnvironment(ProcessProject):
    ##
    ##### Update MD2 Environment Variables
    ##
    def __init__(self): #, env_file_content_string, recorder=None):
        ProcessProject.__init__(self) #(template_folder_key='github', recorder=recorder)
        # package is {nv_list, repo_folder, template_folder}
        #

    def commit_environment(self):

        if not self.get_application():
            raise Exception('Application Not Found!')

        env_name = str(self.get_application().get_environment_filename()).split('/')[-1]
        self.get_application().add('update ({})'.format(env_name))

        ## Save MD2 user's environment changes.
        env_file_content_string = StringReader(self.get_application().get_environment_filename())
        env_file_content_string = UpserterString(env_file_content_string, settings={'dup': True, 'hard_fail': True},
                                                 recorder=self.get_application()).upsert(get_env_variable_values_string())
        ##* __Commit__ Environment Values __To__ '\<root>/bin/md2.env'

        StringWriter(self.get_application().get_environment_filename(),
                     env_file_content_string,
                     self.get_application())

        #print('   * step {} {}'.format(self.get_application().get_name(),DiagramString(self.get_application())))

        assert (self.get_application().get_environment_filename())
        return self

    def process(self):

        MultiLogger().set_msg('5. Update Environment: {}'.format(self.get_application().get_name())).runtime().terminal()

        self.commit_environment()

        return self

#### Helper Classes

class Auto():
    ##
    ##### Auto
    ##
    ## Launch/run task
    def __init__(self, process):
        process.run()

class MultiLogger():
    ##
    ##### MultiLogger
    ##
    ## Application logging system

    def __init__(self,setting_string='df', log_folder=None):
        self.msg = '{}'.format(datetime.datetime.now())
        self.log_folder=log_folder
        if not self.log_folder:
            # default log folder is the current working dir
            self.log_folder = os.getcwd()
        self.setting_string=setting_string

    def set_msg(self, msg):
        self.msg = msg
        return self

    def format(self):
        rc = ''
        if 'd' in self.setting_string:
            rc += '{}'.format(datetime.datetime.now())
        if 'f' in self.setting_string :
            rc += ' {}'.format(str(__file__).split('/')[-1])

        rc += ' ' + self.msg

        return rc

    def runtime(self):
        log_foldefile = '{}/runtime.log'.format(self.log_folder)
        with open(log_foldefile, 'a') as f:
            f.write('{}\n'.format(self.format()))
        return self

    def terminal(self):
        print(self.format())
        return self

#### Base Classes


if __name__ == "__main__":
    # execute as docker
    main()