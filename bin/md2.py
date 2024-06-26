##
### MD2 Script
##
## __Goal__: Make what is not there
##
## __Strategy__: break down process into tasks and code those tasks in classes. Run the classes in order.

import os
import sys
import ast
from pprint import pprint
import re
#SCRIPT_DIR = os.path.dirname(str(os.path.abspath(__file__)).replace('/bin','/source/component'))
#sys.path.append(os.path.dirname(SCRIPT_DIR))
#print('SCRIPT_DIR',SCRIPT_DIR)
from able import StringReader, \
                 StringWriter, \
                 UpserterString, \
                 EnvVarString,\
                 CloneRepo,\
                 DiagramString,\
                 RuntimeLogger,\
                 JSONString, NormalString, Stack, Level, \
                 TemplateString, \
                 TemplateList_Latest


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
    Auto(TaskInitializeEnv().set_application(app))

    ##1. [Configure MD2 Environment Values](#configure-md2-environment-values)
    Auto(TaskConfigure().set_application(app)) #(env_file_content_string, app)

    ##1. [Initialize project_<<WS_PROJECT>>.md.C---.tmpl](#configure-md2-environment-values)
    print('-----')
    Auto(TaskInitializeProjecMd().set_application(app))  # (env_file_content_string, app)
    print('-----')
    exit(0)
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
    Auto(TaskInitializeHapi().set_application(app)) # move /templates to project, apply .env nv_list
    '''
    resource_string = StringExpandMdTable(StringReader('{}/{}'.format(get_bin_folder(), 'test_prj.md')))
    # resource_string = StringExpandMdTable(StringReader('{}/{}'.format(get_bin_folder(), 'app_starter.md')))

    #print('app_starter', resource_string)
    #print('DictMd',DictMd(resource_string))
    #pprint(DictMd(resource_string))
    #print('ResourceNames', ResourceNames(DictMd(resource_string)))
    #print('RoleNames',RoleNames(DictMd(resource_string)))
    #print('ProjectName',ProjectName(DictMd(resource_string)))
    #print('permissions', ResourcePermissions(DictMd(resource_string)))
    #print('--')
    #pprint(ResourcePermissions(DictMd(resource_string)))
    #print('--')
    #print('model A', ResourceModel(DictMd(resource_string)))
    #print('model B', ResourceModel(DictMd(resource_string),'account'))
    #print('resource_string', resource_string)
    print('--fields')
    # {id:{}, owner:'' ...}
    print('fields', ResourceFields(DictMd(resource_string),'account'))
    #print('create form', ResourceFields(DictMd(resource_string),'account').getNewForm())
    print('route_list', RouteConstantsJS(DictMd(resource_string)))
    print('api_route_list', ApiRoutes(DictMd(resource_string)))
    nv_list = [
        {'<<ROUTE_CONST>>': RouteConstantsJS(DictMd(resource_string))},
        {'<<API_ROUTES>>': ApiRoutes(DictMd(resource_string))}
    ]
    print('nv_list', nv_list)
    #resource_fields = ResourceFields(DictMd(resource_string),'account')
    # file.md --> DictMd -->
    #pprint(ResourceModel(DictMd(resource_string)))
    #print('--')
    #pprint(ResourceModel(DictMd(resource_string), 'account2'))
    #print('get()',ResourceModel(DictMd(resource_string)).get('account'))
    #pprint(ResourceModel(DictMd(resource_string)).get('account'))

    #print('pattern', ResourceFields(ResourceModel(DictMd(resource_string))))

    #print('xxx',JSONString((resource_string)))
    #test_resource_fields()
    #test_pattern()
    '''
    Auto(TaskInitializeHapiRoutes().set_application(app)) # -->

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
#class TaskMdTableFlatten(str):

'''
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
'''



#####
class StringExpandMdTable(str):
    def __new__(cls, md_text):

        md_text = str(md_text).split('\n')
        contents = []
        tbl_cols = []

        table = False
        for ln in md_text:
            if len(ln.strip())==0:
                contents.append('')
            if not ln.startswith('|'):
                table = False

            if ln.startswith('|'):
                if not table:
                    table = True
                    tbl_cols = ln.replace(' ', '').split('|')
                    tbl_cols = [c for c in tbl_cols if c != '']
                elif ln.startswith('|-'):
                    pass
                else:
                    tbl_row = ln.replace(' ', '').split('|')
                    tbl_row = [r for r in tbl_row if r != '']
                    r = {tbl_cols[k]: tbl_row[k] for k in range(len(tbl_row))}
                    contents.append('1. {}: {}'.format(tbl_row[0], r))
                    # contents.append('1. {}: {}'.format(tbl_row[1], r))

            else:
                contents.append(ln)

        contents = '\n'.join(contents)
        instance = super().__new__(cls, contents)
        return instance

# with stack pointing to last and active

# Lists and Dicts

class DictMd(dict):

    def __init__(self, md_text):
        # skip spaces
        # skip *
        #stack = Stack()
        ostack = Stack()
        table = False

        for ln in str(md_text).split('\n'):

            if not ln.startswith('|'):
                table = False

            if ln.startswith('#'):
                # print('DictMd level', Level(ln))
                level = Level(ln)
                ln = ln.replace(':', '')
                ln = ln.split(' ')
                if len(ln) < 2:
                    raise Exception('Bad Line')
                #while stack.size() >= level: stack.pop()
                while ostack.size() >= level: ostack.pop()

                if ostack.size() == 0: #1:  # projecrt

                    self[ln[1].lower()] = {'name': ln[2].lower()}
                    ostack.push(self[ln[1].lower()])

                elif ostack.size() >= 1:  # project claims

                    if len(ln) ==2:
                        ostack.peek()[ln[1].lower()] = {}
                        ostack.push(ostack.peek()[ln[1].lower()])

                    elif len(ln) == 3:
                        ostack.peek()[ln[1].lower()] = {'name': ln[2].lower()}
                        ostack.push(ostack.peek()[ln[1].lower()])

            elif ln.startswith('1.'):
                ln = ln.replace('1. ','')
                ln = ln.split(':', maxsplit=1)

                line = ln[1].strip()

                if line.startswith('{'):
                    line = ast.literal_eval(line)
                ostack.peek()[ln[0]] = line

class ProjectName(str):
    def __new__(cls, project_dict):

        contents = project_dict['project']['name']

        instance = super().__new__(cls, contents)
        return instance

class ResourceNames(list):
    def __init__(self, project_dict):
        for r in project_dict['project']['resources']:
            self.append(r)

class RoleNames(list):
    def __init__(self, project_dict):

        lst = []
        for r in project_dict['project']['resources']:
            for f in project_dict['project']['resources'][r]['model']:
                for s in project_dict['project']['resources'][r]['model'][f]:
                    if s.startswith('api_'):
                        lst.append(s)

        lst = set(lst)
        for r in lst:
            self.append(r)


    # TASKS

class ResourcePermissions(dict):
    # { account: {id: {api_admin: R, api_guest:CR, api_user:RUD},...}
    def __init__(self, project_dict):
        for r in project_dict['project']['resources']:
            self[r]={}
            for f in project_dict['project']['resources'][r]['model']:
                self[r][f] = {}
                for s in project_dict['project']['resources'][r]['model'][f]:
                    if s.startswith('api_'):
                        self[r][f][s] = project_dict['project']['resources'][r]['model'][f][s]

class ResourceModel(dict):
    # { account: {id: {api_admin: R, api_guest:CR, api_user:RUD},...}
    def __init__(self, project_dict, resource_name=None):
        resource_list = project_dict['project']['resources']

        if resource_name:
            resource_list = {r: resource_list[r] for r in resource_list if r == resource_name}

        for r in resource_list:
            self[r] = {}
            for f in project_dict['project']['resources'][r]['model']:
                self[r][f] = {}
                for s in project_dict['project']['resources'][r]['model'][f]:
                    if not s.startswith('api_'):
                        self[r][f][s] = project_dict['project']['resources'][r]['model'][f][s]

# new resource\
#   account
#   given scope 'api_user' or 'CRUD'
#   given scope 'api_guest' or 'C'
#   given scope 'api_admin' or 'U'


class ResourceFields(dict):
    def __init__(self, project_dict, resource_name):
        resource_list = project_dict['project']['resources']

        if resource_name:
            resource_list = {r: resource_list[r] for r in resource_list if r == resource_name}

        for r in resource_list:
            for f in project_dict['project']['resources'][r]['model']:
                self[f] = {'resource': r}
                for s in project_dict['project']['resources'][r]['model'][f]:
                    self[f][s] = project_dict['project']['resources'][r]['model'][f][s]
                    self[f]['pattern']=Pattern(project_dict['project']['resources'][r]['model'][f])
                    # print('xxx', self.Pattern(project_dict['project']['resources'][r]['model'][f]))

    def depgetNewForm(self, default=None):
        form = {}
        for f in self:
            if not default:
                form[f]=''
            else:
                form[f]= default
        return form
    def depgetNewValidation(self, crud):
        return {}
    def depgetReadForm(self, crud):
        return {}
    def depgetUpdateForm(self, crud):
        return {}
    def depgetDelete(self, crud):
        return {}

class Pattern(str):
    def __new__(cls, resource_field):
        # resource_field is {'api_admin': 'R', 'api_guest': 'CR', 'api_user': 'RUD', 'encrypt': 'N', 'field': 'id', 'pattern': '^.{3,330}$', 'resource': 'account','size': '3-330', 'type': 'C', 'validate': 'R'}
        contents = ''
        if 'type' in resource_field:
            if resource_field['type'] == 'C':
                contents = '^<<TYPE>>{<<MIN>>,<<MAX>>}$'
                contents = contents.replace('<<TYPE>>', '.')
                min = resource_field['size'].split('-')[0]
                max = resource_field['size'].split('-')[1]
                contents = contents.replace('<<MIN>>', min).replace('<<MAX>>',max)
            elif resource_field['type'] == 'L':
                contents = '(True|False|Y|N|T|F|1|0)'
                resource_field['size']='1-5' # eg True, False, Y, N, T, F, 1, or 0
            elif resource_field['type']=='I':
                contents = '-?\d{<<MIN>>,<<MAX>>}'
                min = resource_field['size'].split('-')[0]
                max = resource_field['size'].split('-')[1]
                contents = contents.replace('<<MIN>>',min).replace('<<MAX>>',max)
            elif resource_field['type'] == 'N':
                contents = '-?\d{1,<<W>>}(\.\d{1,<<D>>})?' # .replace('<<W>',w).replace('<<D>>',d) # eg
                w = resource_field['size'].split(',')[0]
                d = resource_field['size'].replace('-', ',').split(',')[1]
                contents = contents.replace('<<W>>', w).replace('<<D>>', d)
            elif resource_field['type'] == 'D':
                contents = '(\d{4}-\d{2}-\d{2})([T ]?)(\d{2}:\d{2}:\d{2})?(\.\d+)?(Z|([+-]\d{2}:\d{2}))?'
                resource_field['size']='8-19' # eg 2024-06-23 18:30:00

        instance = super().__new__(cls, contents)
        return instance

def test_resource_fields():
    print('test_resource_fields')

def test_pattern():
    # character
    resource_field = {'size': '3-330', 'type': 'C', 'api_admin': 'R', 'api_guest': 'CR', 'api_user': 'RUD', 'encrypt': 'N', 'field': 'id', 'resource': 'account', 'validate': 'R'}
    # print('C', Pattern(resource_field))
    assert(Pattern(resource_field) == '^.{3,330}$')
    assert(re.match(Pattern(resource_field), 'abc!89'))
    # logical
    resource_field = {'size': '14,6', 'type': 'L', 'api_admin': 'R', 'api_guest': 'CR', 'api_user': 'RUD', 'encrypt': 'N', 'field': 'id', 'resource': 'account', 'validate': 'R'}
    assert(Pattern(resource_field) == '(True|False|Y|N|T|F|1|0)')
    assert(re.match(Pattern(resource_field), 'False'))
    assert(re.match(Pattern(resource_field), 'True'))
    assert(re.match(Pattern(resource_field), 'Y'))
    assert(re.match(Pattern(resource_field), 'N'))
    assert(re.match(Pattern(resource_field), 'T'))
    assert(re.match(Pattern(resource_field), 'F'))
    assert(re.match(Pattern(resource_field), '0'))
    assert(re.match(Pattern(resource_field), '1'))
    assert(not re.match(Pattern(resource_field), 'z'))
    # integer
    resource_field = {'size': '1-6', 'type': 'I', 'api_admin': 'R', 'api_guest': 'CR', 'api_user': 'RUD', 'encrypt': 'N', 'field': 'id', 'resource': 'account', 'validate': 'R'}
    #print('integer',Pattern(resource_field))
    assert(Pattern(resource_field) == '-?\d{1,6}')
    assert (not re.match(Pattern(resource_field), 'a'))
    assert (re.match(Pattern(resource_field), '1'))
    assert (re.match(Pattern(resource_field), '-1'))
    # number
    resource_field = {'size': '14,6', 'type': 'N', 'api_admin': 'R', 'api_guest': 'CR', 'api_user': 'RUD', 'encrypt': 'N', 'field': 'id', 'resource': 'account', 'validate': 'R'}
    assert (Pattern(resource_field) == '-?\d{1,14}(\.\d{1,6})?')
    assert (not re.match(Pattern(resource_field), 'a'))
    assert (re.match(Pattern(resource_field), '1'))
    assert (re.match(Pattern(resource_field), '-1'))
    assert (re.match(Pattern(resource_field), '1.1'))
    # datetime
    resource_field = {'size': '14,6', 'type': 'D', 'api_admin': 'R', 'api_guest': 'CR', 'api_user': 'RUD', 'encrypt': 'N', 'field': 'id', 'resource': 'account', 'validate': 'R'}
    assert (Pattern(resource_field) == '(\d{4}-\d{2}-\d{2})([T ]?)(\d{2}:\d{2}:\d{2})?(\.\d+)?(Z|([+-]\d{2}:\d{2}))?')
    assert (not re.match(Pattern(resource_field), 'a'))
    assert (re.match(Pattern(resource_field), '2024-06-23'))
    assert (re.match(Pattern(resource_field), '2024-06-23 18:30:00'))

class RouteConstantsJS(str):
    def __new__(cls,project_dict):
        resource_list = project_dict['project']['resources']
        lst = ['/* generated in RouteConstantsJS from {} */'.format(str(__file__))]
        for r in resource_list:
            # crud = CRUD_Collective(project_dict, r)
            # if 'C' in crud:
            lst.append('const {}_route_post = require(\'./routes/route_{}_post.js\');'.format(r,r))
            lst.append('const {}_route_get = require(\'./routes/route_{}_get.js\');'.format(r,r))
            lst.append('const {}_route_put = require(\'./routes/route_{}_put.js\');'.format(r,r))
            lst.append('const {}_route_delete = require(\'./routes/route_{}_delete.js\');'.format(r,r))

        contents = '\n'.join(lst)

        instance = super().__new__(cls, contents)
        return instance

class ApiRoutes(str):
    def __new__(cls,project_dict):
        resource_list = project_dict['project']['resources']
        # lst = ['/* generated in RouteConstantsJS from {} */'.format(str(__file__))]
        lst=[]
        for r in resource_list:
            # crud = CRUD_Collective(project_dict, r)
            # if 'C' in crud:
            lst.append('  {}_route_post'.format(r))
            lst.append('  {}_route_get'.format(r))
            lst.append('  {}_route_put'.format(r))
            lst.append('  {}_route_delete'.format(r))

        contents = ',\n'.join(lst)

        instance = super().__new__(cls, contents)
        return instance




class depResourcePatterns(str):
    def __new__(cls, field_dict):
        print('field_dict', field_dict)
        contents = 'fixme'

        instance = super().__new__(cls, contents)
        return instance

# Task
class TaskInitializeEnv(ProcessProject):
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
        self.set_env_var('WS_ORGANIZATION', 'test_org')
        ##    * __Configure__ WS_WORKSPACE
        self.set_env_var('WS_WORKSPACE', 'test_ws')
        ##    * __Configure__ WS_PROJECT
        self.set_env_var('WS_PROJECT', 'test_prj')
        ##    * __Configure__ WS_REPO
        self.set_env_var('WS_REPO', 'py_test')

        ##
        ##2. GitHub Values
        ##    * __Configure__ GH_TRUNK
        self.set_env_var('GH_TRUNK','main')
        ##    * __Configure__ GH_PROJECT
        self.set_env_var('GH_PROJECT','test_prj')
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


class TaskInitializeProjecMd(ProcessProject):
    ##
    ###### Configure MD2 Environment Values
    def __init__(self): #, env_file_content_string): # , recorder):
        ProcessProject.__init__(self)
        self.set_template_folder_key('__project__')

        # package is {nv_list, repo_folder, template_folder}
        #
    '''
    def get_template_file_list(self, nv_list):
        template_folder = self.get_template_folder()
        template_list = TemplateList_Latest(folder_path=template_folder)
        #template_list = {TemplateString(f,nv_list): template_list[f] for f in template_list}
        #template_list['']
        print('template_list', template_list)
        lst = {}
        for f in template_list:
            print('f', f, TemplateString(f, nv_list))
            lst[TemplateString(f, nv_list)] = []
            for ff in template_list[f]:
                lst[TemplateString(f, nv_list)][ff]=template_list[f][ff]
                #print('ff', ff, template_list[f][ff] )
                #template_list[ff]=TemplateString(template_list[ff], nv_list)

        #template_list = {TemplateString(tmpl, nv_list): template_list[tmpl] for tmpl in template_list}
        return lst
    '''
    def initialize_project_md(self):
        # copy template/__project__/project_<<WS_PROJECT>>.md.C---.tmpl.tmpl
        nv_list = self.get_template_key_list() # self.get_template_name_value_pairs()
        #print('initialize_project_md nv_list',nv_list)
        #nv_list = self.templatize_list(nv_list)
        #print('initialize_project_md template_folder', nv_list)
        #template_list = self.get_template_file_list(nv_list)
        pprint(nv_list)
        #print('initialize_project_md template_list',nv_list)
        # self.templatize(nv_list=nv_list)
        #for tmpl in template_list:
        #    print('tmpl', TemplateString(tmpl,nv_list))
        #tl = TemplateList_Latest(folder_path=self.get_template_folder())
        #print('template list', tl)
        project_folder = os.getcwd()
        if project_folder.endswith('/bin'):
            print('project folder', project_folder)
            self.templatize(nv_list=nv_list,output_subfolder=project_folder)
        return self

    def process(self):
        MultiLogger().set_msg('xxx. Initialize {}'.format(self.get_application().get_name())).runtime().terminal()

        self.initialize_project_md()

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
        MultiLogger().set_msg('5. ProjectSpace: {}'.format(repo_name)).runtime().terminal()

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
        MultiLogger().set_msg('6. Docker: {}'.format(repo_name)).runtime().terminal()

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
        MultiLogger().set_msg('7. Heroku: {}'.format(repo_name)).runtime().terminal()

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
        MultiLogger().set_msg('8. Node: {}'.format(repo_name)).runtime().terminal()

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
        MultiLogger().set_msg('9. JWT: {}'.format(repo_name)).runtime().terminal()

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
        MultiLogger().set_msg('10. Nodemon: {}'.format(repo_name)).runtime().terminal()

        self.nodemon_templates()

        return self

class TaskInitializeHapi(ProcessProject):
    ##
    ###### Initialize Hapi
    ##
    ## create singleton templates i.e. templates/hapi
    ## applies .env values to templates

    def __init__(self):
        ProcessProject.__init__(self)
        self.set_template_folder_key('hapi')
        nv_list = self.get_template_key_list() # self.get_template_name_value_pairs()
        print('nv_list', nv_list)
        resource_md = '{}/{}'.format('/'.join(str(__file__).split('/')[0:-1]), TemplateString('project_<<WS_PROJECT>>.md',nv_list))
        print('project_<<WS_PROJECT>>.md.C---.tmpl', resource_md)

    def hapi_templates(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        self.get_application().add('hapi')
        ##* Templatize Hapi templates
        self.templatize()
        return self

    def process(self):

        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('11. Hapi: {}'.format(repo_name)).runtime().terminal()

        self.hapi_templates()

        return self

# create server_ext
# merge server_ext with <<API_ROUTES>> TaskMergeHapiServerRouteNames
# merge server_ext with <<ROUTE_CONST>> TaskMergeHapiServerRouteNames
# intialize routes_*.js files TaskInitializeHapiRoutes

#class TaskMergeHapiRoutes(ProcessProject):
# update server_ext with <<API_ROUTES>> and <<ROUTE_CONST>> values from <project>.md
# need to generate route_post,route_get, route_put, route_delete files
class TaskInitializeHapiRoutes(ProcessProject):
    # create CRUD files from CRUD template

    # server_ext.js
    # + ------------------------ +
    # + require(route_const.js) + < -- route_const.js
    # +                          +
    # + [] + < -- route_list.js
    # + ------------------------ +

    def __init__(self):
        ProcessProject.__init__(self)
        self.set_template_folder_key('hapi_routes')

    def route_templates(self):
        # handle generated routes
        # open 'bin/<project>.md'

        # create a nv_list for <<API_ROUTES>> and <<ROUTE_CONST>>, eg [{name: '', value: ''},...]

        # make template list for each resource (route_post,route_get, route_put, route_delete)
        # remove routes not defined in the <project>.md
        # apply nv_list to each template
        # save to /<project>/lib/__routes__
        return self

    def process(self):

        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('12. Fix Me Hapi CRUD: {}'.format(repo_name)).runtime().terminal()

        self.route_templates()

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
        MultiLogger().set_msg('13. Postgres: {}'.format(repo_name)).runtime().terminal()

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
        MultiLogger().set_msg('14. Model: {}'.format(repo_name)).runtime().terminal()

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