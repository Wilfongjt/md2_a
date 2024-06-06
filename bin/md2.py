##
### MD2 Script
##
## __Goal__: Make what is not there
##
## __Strategy__: break down process into tasks and code those tasks in classes. Run the classes in order.

import os
import sys
#SCRIPT_DIR = os.path.dirname(str(os.path.abspath(__file__)).replace('/bin','/source/component'))
#sys.path.append(os.path.dirname(SCRIPT_DIR))
#print('SCRIPT_DIR',SCRIPT_DIR)
from able import StringReader, \
                 StringWriter, \
                 UpserterString, \
                 EnvVarString,\
                 CloneRepo,\
                 DiagramString,\
                 RuntimeLogger

from functions import get_bin_folder, \
    get_template_folder, \
    get_env_variable_values_string
    #get_env_var,\

from source.component import ProcessProject, Application, MultiLogger

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
    print('runtime',RuntimeLogger())
    ##
    #### MD2 Process
    ##
    MultiLogger('df').set_msg('start').runtime().terminal()
    app = ApplicationMD2().load_environment()

    ##### Process

    ##1. [Initialize MD2](#initialize-md2)
    Auto(TaskMd2().set_application(app))

    ##1. [Configure MD2 Environment Values](#configure-md2-environment-values)
    Auto(TaskConfigure().set_application(app)) #(env_file_content_string, app)

    ##1. [Clone GitHub Repository](#clone-github-repository)
    Auto(TaskGithub().set_application(app))

    ##1. [Patch Clone](#patch-clone)
    Auto(TaskGithubPatch().set_application(app))

    ##1. [Initialize ProjectSpace](#initialize-projectspace)
    Auto(TaskInitializeProjectSpace().set_application(app))

    ##1. [Initialize Docker](#initialize-docker)
    Auto(TaskInitializeDocker().set_application(app))

    ##1. [Initialize Heroku](#initialize-heroku)
    Auto(TaskInitializeHeroku().set_application(app))

    ##1. [Initialize Node](#initialize-node)
    Auto(TaskInitializeNode().set_application(app))

    ##1. [Initialize JWT](#initialize-jwt)
    Auto(TaskInitializeJWT().set_application(app))

    ##1. [Initialize Nodemon](#initialize-nodemon)
    Auto(TaskInitializeNodemon().set_application(app))

    ##1. [Initialize Hapi](#initialize-hapi)
    Auto(TaskInitializeHapi().set_application(app))


    print('app_starter', ConvertMd2Json(StringReader('{}/{}'.format(get_bin_folder(), 'app_starter.md'))))

    Auto(TaskInitializeHapiCRUD().set_application(app))

    ##1. [Initialize Postgres](#initialize-postgres)
    Auto(TaskInitializePostgres().set_application(app))

    ##1. [Initialize Model](#initialize-model)
    Auto(TaskInitializeModel().set_application(app))

    ##1. [Update Environment Values](#update-md2-environment-variables)
    Auto(TaskUpdateEnvironment().set_application(app))

    xx = 'Summary {} {}'.format(app.get_name(), DiagramString(app))
    MultiLogger().set_msg(xx).runtime().terminal()
    MultiLogger().set_msg('end').runtime().terminal()


##### Coversion
class ConvertMd2Json(str):
    def __new__(cls, md_text):
        # ProcessProject.__init__(self)
        print('ConvertMd2Json', md_text)
        md_text = str(md_text).split('\n')
        contents = []
        tbl_cols = []
        tbl_rows = []
        tbl_spacer = False
        tbl_type = ''
        resource = ''

        for ln in md_text:
            # print('md2json ln', ln)
            if len(ln.strip()):
                contents.append('')
            if ln.startswith('# '):
                contents.append(ln)
            elif ln.startswith('## '):
                contents.append(ln)
            elif ln.startswith('1.'):
                contents.append(ln)
            elif ln.startswith('| resource'):
                tbl_cols = ln.replace(' ', '').split('|')
                tbl_cols = [c for c in tbl_cols if c != '']
                tbl_type = tbl_cols[0]
                #contents.append('### {}:'.format(tbl_type))
                #contents.append('### {}'.format())

                # print('cols', tbl_cols)
            elif ln.startswith('| data') and not tbl_spacer:
                tbl_cols = ln.replace(' ', '').split('|')
                tbl_cols = [c for c in tbl_cols if c != '']
                tbl_type = tbl_cols[0]
                # print('cols', tbl_cols)
            elif ln.startswith('|-'):
                tbl_spacer = True
                # print('spacer')
            elif ln.startswith('|') and tbl_spacer:
                tbl_row = ln.replace(' ', '').split('|')
                tbl_row = [r for r in tbl_row if r != '']
                if tbl_spacer:
                    tbl_spacer = False
                    print('here', tbl_row[0], tbl_row)
                    contents.append('### {}:'.format(tbl_row[0]))

                # print('c', len(tbl_cols), tbl_cols)
                print('r', len(tbl_row), tbl_row)
                # print('range', range(len(tbl_row)))
                tbl_row = ['1. {}: {}'.format(tbl_cols[i], tbl_row[i]) for i in range(len(tbl_row))]
                # print('row\n', '\n'.join(tbl_row))
                tbl_rows.append('\n'.join(tbl_row))

            else:
                tbl_spacer = False

        print('tbl_type', tbl_type)
        print('rows', '\n'.join(tbl_rows))
        print('contents', contents)
        # contents = '\n'.join(contents)
        instance = super().__new__(cls, contents)
        print('instance', instance)
        return instance


class ParseMd2Json_1(str):
    def __new__(cls, md_text):
        #ProcessProject.__init__(self)
        print('ParseMd2Json', md_text)
        md_text = str(md_text).split('\n')
        contents = {}
        tbl_cols = []
        tbl_rows = []
        tbl_spacer = False
        for ln in md_text:
            #print('md2json ln', ln)
            if ln.startswith('| field'):
                tbl_cols = ln.replace(' ','').split('|')
                tbl_cols = [c for c in tbl_cols if c != '']
                print('cols', tbl_cols)
            elif ln.startswith('| id') and not tbl_spacer:
                tbl_cols = ln.replace(' ','').split('|')
                tbl_cols = [c for c in tbl_cols if c != '']
                print('cols', tbl_cols)
            elif ln.startswith('|-'):
                tbl_spacer = True
                print('spacer')

            elif ln.startswith('|') and tbl_spacer:
                tbl_row = ln.replace(' ', '').split('|')
                tbl_row = [r for r in tbl_row if r != '']
                #print('c', len(tbl_cols), tbl_cols)
                #print('r', len(tbl_row), tbl_row)
                tbl_row = {tbl_cols[i]: tbl_row[i] for i in range(len(tbl_row))}
                tbl_rows.append(tbl_row)

            else:
                tbl_spacer = False
                #tbl_start = True
                #print('ParseMd2Json C {}'.format(ln))

            #if ln.startswith('#'):
            #    print('ParseMd2Json A {}'.format(ln))
            #elif ln.startswith('1.'):
            #    print('ParseMd2Json B {}'.format(ln))

        print('rows', tbl_rows)
        #contents = '\n'.join(contents)
        instance = super().__new__(cls, contents)
        return instance




##### Tasks

class TaskMd2(ProcessProject):
    ##
    ###### Initialize MD2
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
    ###### Configure MD2 Environment Values
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
    ###### Clone GitHub Repository
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
    ###### Patch Clone
    ##
    ## Make sure that runtime files don't get included in the repo
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
        ##  * add "*.env" line when NF
        ##  * add "*.idea" line when NF
        ##
        #self.makedirs(temp_file)
        StringWriter(temp_file, temp_contents)
        return self

    def process(self):

        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('4. GitHub Patch: {}'.format(repo_name)).runtime().terminal()

        self.patch()

        return self

class TaskInitializeProjectSpace(ProcessProject):
    ##
    ###### Initialize ProjectSpace
    ##
    def __init__(self):
        ProcessProject.__init__(self)

        self.set_template_folder_key('projectspace')

    def projectspace_templates(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        self.get_application().add(self.get_template_folder_key())
        ##* Templatize Projectspace templates
        self.templatize()
        return self

    def process(self):
        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('3. ProjectSpace: {}'.format(repo_name)).runtime().terminal()

        self.projectspace_templates()

        return self

class TaskInitializeDocker(ProcessProject):
    ##
    ###### Initialize Docker
    ##

    def __init__(self): # , recorder=None ):
        ProcessProject.__init__(self)
        self.set_template_folder_key('docker')

    def docker_templates(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        self.get_application().add('docker')
        ##* Templatize Docker templates
        self.templatize()
        return self

    def process(self):

        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('5. Docker: {}'.format(repo_name)).runtime().terminal()

        self.docker_templates()

        return self

class TaskInitializeHeroku(ProcessProject):
    ##
    ###### Initialize Heroku
    ##

    def __init__(self):  # , recorder=None ):
        ProcessProject.__init__(self)
        self.set_template_folder_key('heroku')

    def heroku_templates(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        self.get_application().add('heroku')
        ##* Templatize Heroku templates
        self.templatize()
        return self

    def process(self):

        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('6. Heroku: {}'.format(repo_name)).runtime().terminal()

        self.heroku_templates()

        return self

class TaskInitializeNode(ProcessProject):
    ##
    ###### Initialize Node
    ##

    def __init__(self):
        ProcessProject.__init__(self)
        self.set_template_folder_key('node')

    def node_templates(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        self.get_application().add('node')
        ##* Templatize Node templates
        self.templatize()
        return self

    def process(self):

        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('7. Node: {}'.format(repo_name)).runtime().terminal()

        self.node_templates()

        return self

class TaskInitializeJWT(ProcessProject):
    ##
    ###### Initialize Node
    ##

    def __init__(self):
        ProcessProject.__init__(self)
        self.set_template_folder_key('jwt')

    def jwt_templates(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        self.get_application().add('jwt')
        ##* Templatize JWT templates
        self.templatize()
        return self

    def process(self):

        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('7. JWT: {}'.format(repo_name)).runtime().terminal()

        self.jwt_templates()

        return self

class TaskInitializeNodemon(ProcessProject):
    ##
    ###### Initialize Nodemon
    ##

    def __init__(self):
        ProcessProject.__init__(self)
        self.set_template_folder_key('nodemon')

    def nodemon_templates(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        self.get_application().add('nodemon')
        ##* Templatize Nodemon templates
        self.templatize()
        return self

    def process(self):

        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('8. Nodemon: {}'.format(repo_name)).runtime().terminal()

        self.nodemon_templates()

        return self

class TaskInitializeHapi(ProcessProject):
    ##
    ###### Initialize Hapi
    ##

    def __init__(self):
        ProcessProject.__init__(self)
        self.set_template_folder_key('hapi')

    def hapi_templates(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        self.get_application().add('hapi')
        ##* Templatize Hapi templates
        self.templatize()
        return self

    def process(self):

        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('9. Hapi: {}'.format(repo_name)).runtime().terminal()

        self.hapi_templates()

        return self

class TaskInitializeHapiCRUD(ProcessProject):
    def __init__(self):
        ProcessProject.__init__(self)
        self.set_template_folder_key('hapi')

    def crud_templates(self):

        return self

    def process(self):

        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('10. Fix Me Hapi CRUD: {}'.format(repo_name)).runtime().terminal()

        self.crud_templates()

        return self

class TaskInitializePostgres(ProcessProject):
    ##
    ###### Initialize Postgres
    ##

    def __init__(self):
        ProcessProject.__init__(self)
        self.set_template_folder_key('postgres')

    def postgres_templates(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        self.get_application().add(self.get_template_folder_key())
        ##* Templatize Postgres templates
        self.templatize()
        return self

    def process(self):

        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('10. Postgres: {}'.format(repo_name)).runtime().terminal()

        self.postgres_templates()

        return self

class TaskInitializeModel(ProcessProject):
    ##
    ###### Initialize Model
    ##

    def __init__(self):
        ProcessProject.__init__(self)
        self.set_template_folder_key('model')

    def db_deploy_templates(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        self.get_application().add(self.get_template_folder_key())
        ##* Templatize DB Deploy templates
        self.templatize()
        return self

    def process(self):
        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('10. Model: {}'.format(repo_name)).runtime().terminal()

        self.db_deploy_templates()

        return self

class TaskUpdateEnvironment(ProcessProject):
    ##
    ###### Update MD2 Environment Variables
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

        MultiLogger().set_msg('99. Update Environment: {}'.format(self.get_application().get_name())).runtime().terminal()

        self.commit_environment()

        return self
##<hr/>
##
#### Helper Classes

class ApplicationMD2(Application):
    ##
    ###### ApplicationMD2
    ##
    ## Custom application data and methods
    ##* Extends Application
    def __init__(self):
        Application.__init__(self, 'md2')

class Auto():
    ##
    ###### Auto
    ##
    ## Launch/run task
    def __init__(self, process):
        process.run()


##<hr/>
##
#### Parent Classes


if __name__ == "__main__":
    # execute as docker
    main()