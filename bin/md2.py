import os
import re
from able import Inputable, \
                 StringReader, \
                 StringWriter, \
                 UpserterString, \
                 EnvVarString,\
                 Recorder,\
                 NameValuePairs,\
                 TemplateString, \
                 CloneRepo

from functions import get_bin_folder, \
    get_template_folder, \
    get_data_folder, \
    get_default_input_folder,\
    get_default_output_folder,\
    get_env_var,\
    get_root_folder,\
    get_env_variable_values_string


def get_environment_filename():
    # env is stored in the bin folder bin/md2
    return '{}/md2.env'.format(get_bin_folder())
def isStringNone(str_object):

    rc = str_object

    if str_object == None:
        rc = None
    elif str_object == 'None':
        rc = None

    return rc
def get_environment_template_filename():
    return '{}/md2.env.tmpl'.format(get_template_folder())
def get_environment_varable_names(prefix):

    rc = [item for item in os.environ
            if item.startswith(prefix)]
    return ', '.join(rc)

def get_template_name_value_pairs():
    nv_list = NameValuePairs(multi_line_string=EnvVarString())
    nv_list = [{'name': '<<{}>>'.format(itm['name']), 'value': itm['value']} for itm in nv_list]
    return nv_list

def get_branch_folder():
    nv_list = get_template_name_value_pairs()
    return TemplateString('{}/Development/<<WS_ORGANIZATION>>/<<WS_WORKSPACE>>/<<WS_PROJECT>>/<<GH_BRANCH>>'.format(os.environ['HOME']), nv_list=nv_list)

## md2 new project
##
##__Terms__
##* __NF__ means Not Found
##* __\<root>__ refers to the current repo's root folder
##* __\<repo>__ refers to a target or new repository
##* __configure__ refers to the setting of values which alter the outcome of a process
##* __initiate__ means to start/execute a process
##* __initialize__ refers to the creation of something when nothing was there previously; an initialization includes suitable defaults
##* __template__ refers to a file of content, complete with template-keys and/or default values
class DiagramString(str):

    def __new__(cls, recorder=None):
        contents = recorder
        if not recorder:
            contents=''

        contents = ''
        if 'step_list' not in recorder:
            recorder['step_list'] = []

        for s in recorder['step_list']:
            if s['count'] == 1:
                contents += ' {}'.format(s['msg'])
            else:
                contents += ' {} ({})'.format(s['msg'], s['count'])

        instance = super().__new__(cls, contents)
        return instance

def initialize_md2(recorder):
    print('1. initialize_md2')
    ##
    ##### Initialize md2
    ##
    ## Make the md2.env file

    #recorder.add('initialize')

    ##* __Create__ '\<root>/bin/md2.env' __From__ template __When__ file NF
    #__Configure__ Project Default Values __To__ Memory
    #__Configure__ GitHub Default Values __To__ Memory

    env_name = get_environment_filename().split('/')[-1]

    if not os.path.isfile(get_environment_filename()):

        # init from template
        recorder.add('initialize ({})'.format(env_name))
        #print('    initialize({})'.format(env_name))

        env_file_content_string = isStringNone(StringReader(get_environment_template_filename()))
        assert(env_file_content_string)
        StringWriter(get_environment_filename(),env_file_content_string)
        # StringWriter(get_environment_filename(),env_file_content_string, recorder=recorder)
    else:
        recorder.add('initialize ({})'.format(env_name))
        #print('    initialized from ({})'.format(env_name))

    ##* __Upsert__ '\<root>/.gitignore' __Set__ '\*.env'
    gitignore_filename = '{}/.gitignore'.format(get_root_folder())
    if os.path.isfile(gitignore_filename):
        gitignore_contents = UpserterString(str_value=StringReader(gitignore_filename),
                                            settings={'dup': True, 'hard_fail': True},
                                            recorder=recorder)\
                                .upsert('*.env')

        #print('gitignore_contents',gitignore_contents)
    else:
        raise Exception('Missing .gitignore')
    #UpserterString(StringReader('{}/.gitignore'.format(get_root_folder())))

    #return env_file_content_string
def configure_environment(env_file_content_string, recorder):
    print('2. Configure Environment:')
    ##### Configure Environment Values
    ##
    ## Interactively configure values

    ##1. Project Values
    ##

    recorder.add('configure')
    ##    * __Configure__ WS_ORGANIZATION
    os.environ['WS_ORGANIZATION'] = Inputable().get_input('WS_ORGANIZATION',
                                                          get_env_var('WS_ORGANIZATION', 'test-org'),
                                                          hardstop=True)
    recorder.add('configure')
    ##    * __Configure__ WS_WORKSPACE

    os.environ['WS_WORKSPACE'] = Inputable().get_input('WS_WORKSPACE',
                                                       get_env_var('WS_WORKSPACE', 'test-ws'),
                                                       hardstop=True)
    recorder.add('configure')
    ##    * __Configure__ WS_PROJECT

    os.environ['WS_PROJECT'] = Inputable().get_input('WS_PROJECT',
                                                     get_env_var('WS_PROJECT', 'test-prj'),
                                                     hardstop=True)
    print('    configured: {}'.format(get_environment_varable_names('WS_')))

    ##
    ##2. GitHub Values

    recorder.add('configure')
    ##    * __Configure__ GH_TRUNK

    os.environ['GH_TRUNK'] = Inputable().get_input('GH_TRUNK',
                                                   get_env_var('GH_TRUNK', 'main'),
                                                   hardstop=True)
    recorder.add('configure')
    ##    * __Configure__ GH_BRANCH

    os.environ['GH_BRANCH'] = Inputable().get_input('GH_BRANCH',
                                                    get_env_var('GH_BRANCH', 'first'),
                                                    hardstop=True)
    recorder.add('configure')
    ##    * __Configure__ GH_REPO

    os.environ['GH_REPO'] = Inputable().get_input('GH_REPO',
                                                  get_env_var('GH_REPO', 'py_test'),
                                                  hardstop=True)
    recorder.add('configure')
    ##    * __Configure__ GH_USER

    os.environ['GH_USER'] = Inputable().get_input('GH_USER',
                                                  get_env_var('GH_USER', 'x'),
                                                  hardstop=True)
    recorder.add('configure')
    ##    * __Configure__ GH_MESSAGE

    os.environ['GH_MESSAGE'] = Inputable().get_input('GH_MESSAGE',
                                                     get_env_var('GH_MESSAGE', 'init'),
                                                     hardstop=True)
    recorder.add('configure')
    ##    * __Configure__ GH_TOKEN

    os.environ['GH_TOKEN'] = Inputable().get_input('GH_TOKEN',
                                                   get_env_var('GH_TOKEN', 'x'),
                                                   hardstop=True)
    recorder.add('configure')
    print('    configured: {}'.format(get_environment_varable_names('GH_')))

    env_file_content_string = UpserterString(env_file_content_string,
                                             settings={'dup': True, 'hard_fail': True}) \
                                .upsert(EnvVarString())
    return env_file_content_string

def clone_repository(recorder):
    print('clone_repository')
    repo_name =  os.environ['GH_REPO']
    recorder.add('clone repository ({})'.format(repo_name))

    ##
    ##### Clone Repository
    ## Create and Configure a Project Repository

    ##* __Create__ Branch Folder __When__ folder is NF
    branch_folder = get_branch_folder()
    os.makedirs(branch_folder, exist_ok=True)

    ##* __Clone__ '\<repo>' __When__ repo is NF
    repo_folder = '{}/{}'.format(branch_folder, os.environ['GH_REPO'])

    if not os.path.isdir(repo_folder):
        repo_name = repo_folder.split('/')[-1]
        recorder.add('clone ({})'.format(repo_name))
        CloneRepo(repo_folder=repo_folder,  username_gh=os.environ['GH_USER'])
    else:
        repo_name = repo_folder.split('/')[-1]
        recorder.add('cloned ({})'.format(repo_name))

def initialize_clone(recorder):
    print('initialize_clone')
    repo_name = 'TBD'
    recorder.add('initialize clone ({})'.format(repo_name))
    ##
    ##### Initialize Clone
    ##

    ##* __Create__ '\<repo>/.gitignore' file __When__ file is NF
    ##* __Upsert__ '\<repo>/.gitignore' __Set__ line = '\*.env' __When__ '\*.env' is NF
    ##* __Upsert__ '\<repo>/.gitignore' __Set__ line = '.idea/' __When__ '.idea/' is NF

    ##* __Create__ '\<repo>/.env' file __When__ file is NF

    ##* __Create__ '\<repo>/bin/' folder __When__ folder is NF

    ##* __Create__ '\<repo>/scripts/' folder __When__ folder is NF
    ##* __Create__ '\<repo>/scripts/git.rebase.sh' file __When__ file is NF

    ##* __Create__ '\<repo>/source/' folder __When__ folder is NF

    ##* __Create__ '\<repo>/bin/md2.env' __When__ file NF
    ##* __Upsert__ '\<repo>/bin/md2.env' __Set__ line = GH_*
    ##* __Upsert__ '\<repo>/bin/md2.env' __Set__ line = WS_*

def commit_environment(recorder):
    print('commit_environment')
    env_name = 'TBD'
    recorder.add('commit environment ({})'.format(env_name))
    ##
    ##### Commit Environment
    ##

    env_file_content_string=StringReader(get_environment_filename())
    # print('env_file_content_string',env_file_content_string)
    #print('get_env_variable_values_string()',get_env_variable_values_string())
    env_file_content_string=UpserterString(env_file_content_string,settings={'dup': True, 'hard_fail': True}, recorder=recorder).upsert(get_env_variable_values_string())
    #print('env_file_content_string',env_file_content_string)
    StringWriter(get_environment_filename(),
                 env_file_content_string,
                 recorder)

    #env_file_content_string = configure_environment(env_file_content_string, recorder)

def main():
    recorder = Recorder()
    ##
    #### MD2 Process
    ##
    ## Make what is not there

    ##1. [__Initialize__ md2](#initialize~md2)

    initialize_md2(recorder)

    ##1. [__Configure__ Environment Values](#configure~environment~values)

    # load env from file
    env_file_content_string=StringReader(get_environment_filename())
    configure_environment(env_file_content_string, recorder)

    ##1. [__Clone__ Repository](#clone~process)

    clone_repository(recorder)

    ##1. [__Initialize__ Clone](#initialize~clone)

    initialize_clone(recorder)

    ##1. __Commit__ Environment Values __To__ '\<root>/bin/md2.env'

    commit_environment(recorder)

    #print('recorder: {}'.format(recorder))
    print(DiagramString(recorder=recorder))

if __name__ == "__main__":
    # execute as docker
    main()