##
### MD2 Script
##
## __Goal__: Make what is not there
##
## __Strategy__: break down process into tasks and code those tasks in classes. Run the classes in order.

import os
import re
from source.component import Tier
from source.component.markdown.tier_md import TierMD
from source.component import RouteScopes
from source.component.markdown.helper.resource_names import ResourceNames
from source.component import ProjectStringDefault
from source.component.markdown.helper.project_name_first import ProjectNameFirst

# SCRIPT_DIR = os.path.dirname(str(os.path.abspath(__file__)).replace('/bin','/source/component'))
# sys.path.append(os.path.dirname(SCRIPT_DIR))
# print('SCRIPT_DIR',SCRIPT_DIR)
from able import StringReader, \
    StringWriter, \
    UpserterString, \
    EnvVarString, \
    CloneRepo, \
    DiagramString, \
    RuntimeLogger, \
    TemplateString

from source.component.nv_list import NVList

from functions import get_env_variable_values_string
# get_env_var,\

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
    no = 0
    print('runtime', RuntimeLogger())
    ##
    #### MD2 Process
    ##
    MultiLogger('df').set_msg('start').runtime().terminal()
    app = ApplicationMD2().load_environment()
    ##### Process

    ##1. [Initialize MD2](#initialize-md2)
    Auto(Task_InitializeEnv(no=app.incNo()).set_application(app))

    ##1. [Configure MD2 Environment Values](#configure-md2-environment-values)
    Auto(Task_Configure(no=app.incNo()).set_application(app))  # (env_file_content_string, app)

    ##1. [Initialize project_<<WS_PROJECT>>.md.C---.tmpl](#configure-md2-environment-values)
    print('-----')
    Auto(Task_InitializeProjecMd(no=app.incNo()).set_application(app))  # (env_file_content_string, app)
    print('-----')
    # exit(0)
    ##1. [Clone GitHub Repository](#clone-github-repository)
    Auto(Task_Github(no=app.incNo()).set_application(app))
    #Test_TemplateOutputs().test(template_folder=app.get_template_folder(subfolder='github'))
    # assert ('' in StringReader())
    #exit(0)
    print('-----')
    ##1. [Patch Clone](#patch-clone)
    Auto(Task_GithubPatch(no=app.incNo()).set_application(app))
    #exit(0)
    print('-----')
    ##1. [Initialize ProjectSpace](#initialize-projectspace)
    Auto(Task_InitializeProjectSpace(no=app.incNo()).set_application(app))
    #exit(0)
    print('-----')
    ##1. [Initialize Docker](#initialize-docker)
    Auto(Task_InitializeDocker(no=app.incNo()).set_application(app))
    #exit(0)
    print('-----')
    ##1. [Initialize Heroku](#initialize-heroku)
    Auto(Task_InitializeHeroku(no=app.incNo()).set_application(app))
    #exit(0)
    print('-----')
    ##1. [Initialize Node](#initialize-node)
    Auto(Task_InitializeNode(no=app.incNo()).set_application(app))
    #exit(0)
    print('-----')
    ##1. [Initialize JWT](#initialize-jwt)
    Auto(Task_InitializeJWT(no=app.incNo()).set_application(app))
    print('-----')
    ##1. [Initialize Nodemon](#initialize-nodemon)
    Auto(Task_InitializeNodemon(no=app.incNo()).set_application(app))
    print('-----')
    ##1. [Initialize Hapi](#initialize-hapi)
    Auto(Task_InitializeHapi(no=app.incNo()).set_application(app))  # move /templates to project, apply .env nv_list

    '''
    resource_string = ConvertMdTableToListString(StringReader('{}/{}'.format(get_bin_folder(), 'test_prj.md')))
    # resource_string = ConvertMdTableToListString(StringReader('{}/{}'.format(get_bin_folder(), 'app_starter.md')))

    #print('app_starter', resource_string)
    #print('Tier',Tier(resource_string))
    #pprint(Tier(resource_string))
    #print('ResourceNames', ResourceNames(Tier(resource_string)))
    #print('RoleNames',RoleNames(Tier(resource_string)))
    #print('ProjectName',ProjectName(Tier(resource_string)))
    #print('permissions', ResourcePermissions(Tier(resource_string)))
    #print('--')
    #pprint(ResourcePermissions(Tier(resource_string)))
    #print('--')
    #print('model A', ResourceModel(Tier(resource_string)))
    #print('model B', ResourceModel(Tier(resource_string),'account'))
    #print('resource_string', resource_string)
    print('--fields')
    # {id:{}, owner:'' ...}
    print('fields', ResourceFields(Tier(resource_string),'account'))
    #print('create form', ResourceFields(Tier(resource_string),'account').getNewForm())
    print('route_list', RouteConstantsJS(Tier(resource_string)))
    print('api_route_list', ApiRoutes(Tier(resource_string)))
    nv_list = [
        {'<<ROUTE_CONST>>': RouteConstantsJS(Tier(resource_string))},
        {'<<API_ROUTES>>': ApiRoutes(Tier(resource_string))}
    ]
    print('nv_list', nv_list)
    #resource_fields = ResourceFields(Tier(resource_string),'account')
    # file.md --> Tier -->
    #pprint(ResourceModel(Tier(resource_string)))
    #print('--')
    #pprint(ResourceModel(Tier(resource_string), 'account2'))
    #print('get()',ResourceModel(Tier(resource_string)).get('account'))
    #pprint(ResourceModel(Tier(resource_string)).get('account'))

    #print('pattern', ResourceFields(ResourceModel(Tier(resource_string))))

    #print('xxx',JSONString((resource_string)))
    #test_resource_fields()
    #test_pattern()
    '''
    print('-----')
    ##1. [Initialize Hapi Routes](#initialize-hapi-routes)
    Auto(Task_InitializeHapiRoutes(no=app.incNo()).set_application(app))  # -->
    # exit(0)
    ##1. [Initialize Postgres](#initialize-postgres)
    print('-----')
    Auto(Task_InitializePostgres(no=app.incNo()).set_application(app))
    print('-----')
    ##1. [Initialize Model](#initialize-model)
    Auto(Task_InitializeModel(no=app.incNo()).set_application(app))
    exit(0)
    print('-----')
    ##1. [Update Environment Values](#update-md2-environment-variables)
    Auto(Task_UpdateEnvironment(no=app.incNo()).set_application(app))

    xx = 'Summary {} {}'.format(app.get_name(), DiagramString(app))
    MultiLogger().set_msg(xx).runtime().terminal()
    MultiLogger().set_msg('end').runtime().terminal()

# Defaults
from source.component.env.env_string_default import EnvStringDefault

# String to String Conversions

class ConvertMdTableToListString(str):
    def __new__(cls, md_text):

        md_text = str(md_text).split('\n')
        contents = []
        tbl_cols = []

        table = False
        for ln in md_text:
            if len(ln.strip()) == 0:
                contents.append('')
            if not ln.startswith('|'):
                table = False

            if ln.startswith('|'): # start processing a table line
                if not table: # get the column headers
                    table = True
                    tbl_cols = ln.replace(' ', '').split('|')
                    tbl_cols = [c for c in tbl_cols if c != '']
                elif ln.startswith('|-'): # skip the header line
                    pass
                else: # process the row line into list of name-value pairs
                    # eg '| abc | 123 |' -> '|abc|123|'
                    tbl_row = ln.replace(' ', '').split('|')
                    # get rid of blank lines
                    tbl_row = [r for r in tbl_row if r != '']
                    # convert row values to name-value pairs
                    r = {tbl_cols[k]: tbl_row[k] for k in range(len(tbl_row))}
                    # append name-value pair to str
                    contents.append('1. {}: {}'.format(tbl_row[0], r))
                    # contents.append('1. {}: {}'.format(tbl_row[1], r))

            else:
                # append non-row lines to str
                contents.append(ln)

        contents = '\n'.join(contents)
        instance = super().__new__(cls, contents)
        return instance
# with stack pointing to last and active

# Lists and Dicts


# Assemblers

class NVListEnv(NVList):
    def __init__(self, env_string):
        pattern = re.compile(r'^\s*[A-Za-z0-9_]+=[A-Za-z0-9]+\s*$')
        for ln in env_string.split('\n'):
            if pattern.match(ln):
                pts = [l.strip() for l in ln.split('=')]
                self.append({'name': pts[0], 'value': pts[1]})
def test_list_env():
    nv_list = NVListEnv(EnvStringDefault())
    print('            list_env:', nv_list)
    assert ({'name': 'GH_TRUNK', 'value': 'main'} in nv_list)
    assert ({'name': 'GH_BRANCH', 'value': 'first'} in nv_list)
    assert ({'name': 'GH_USER', 'value': 'wilfongjt'} in nv_list)
    assert ({'name': 'GH_MESSAGE', 'value': 'init'} in nv_list)


# class ProjectResource()




# TASKS
'''
class depResourcePermissions(dict):
    # { account: {id: {api_admin: R, api_guest:CR, api_user:RUD},...}
    def __init__(self, project_dict):
        #print('project_dict',project_dict)
        #pprint(project_dict)
        # self {}
        for r in project_dict['project']['resource']:
            # {account: {}, ...}
            self[r]={}
            for m in project_dict['project']['resource'][r]['model']:
                for row in project_dict['project']['resource'][r]['model']['rows']:
                    for fld in row:
                        if fld=='field':
                            # {account: {id: {}, ...}, ...}
                            self[r][row[fld]]={}
                            fld_key= fld
                        if fld.startswith('api_'):
                            # {account: {id: {api_admin: R, ... }, ...}, ...}
                            self[r][row['field']][fld] = row[fld]

def test_resource_permissions():
    resource_permissions = ResourcePermissions(Tier(getProjectMDString()))
    print('resource_permissions:', resource_permissions)
    assert('account' in resource_permissions)
    assert('id' in resource_permissions['account'])
    assert('api_admin' in resource_permissions['account']['id'])
'''
'''
class depResourceFields(dict):
    def __init__(self, project_dict, resource_name):
        resource_list = project_dict['project']['resource']

        if resource_name:
            resource_list = {r: resource_list[r] for r in resource_list if r == resource_name}
        for r in project_dict['project']['resource']:
            # {account: {}, ...}
            self[r] = {}
            for m in project_dict['project']['resource'][r]['model']:
                for row in project_dict['project']['resource'][r]['model']['rows']:

                    for fld in row:
                        if fld=='field':
                            # {account: {id: {}, ...}, ...}
                            self[r][row[fld]]={}
                            #fld_key= fld
                        # {account: {id: {field: id, ... }, ...}, ...}
                        self[r][row['field']][fld] = row[fld]
                        # {account: {id: {field: id, pattern: ^.{3,330}$, ... }, ...}, ...}
                        self[r][row['field']]['pattern'] = Pattern(row)
                        self[r][row['field']]['min'] = Min(row) # min no of char
                        self[r][row['field']]['max'] = Max(row) # max no of char

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
def test_resource_fields():
    resource_fields = ResourceFields(Tier(getProjectMDString()),'account')
    print('     resource_fields:', resource_fields)
    assert('id' in resource_fields['account'])
    assert('field' in resource_fields['account']['id'])
'''


# class ResourceFieldSizes(dict):
#    def __init__(self, project_dict, resource_name):
#        #resource_list = project_dict['project']['resource']

#        #if resource_name:
#        #    resource_list = {r: resource_list[r] for r in resource_list if r == resource_name}

#        for r in project_dict['project']['resource']:
#            # {account: {}, ...}
#            self[r] = {}
#            for m in project_dict['project']['resource'][r]['model']:

#                for row in project_dict['project']['resource'][r]['model']['rows']:
#                    print('row', row)
#    for fld in row:
#        if fld=='field':
#            # {account: {id: {}, ...}, ...}
#            self[r][row[fld]]={}
#            #fld_key= fld
#        # {account: {id: {field: id, ... }, ...}, ...}
#        self[r][row['field']][fld] = row[fld]
#        # {account: {id: {field: id, pattern: ^.{3,330}$, ... }, ...}, ...}
#        self[r][row['field']]['pattern'] = Pattern(row)

# def test_resource_field_sizes():
#    actual = ResourceFieldSizes(Tier(getProjectMDString()),'account')





class ResourcePatterns(dict):
    def __init__(self, project_dict, resource_name):
        resource_list = project_dict['project']['resource']

        if resource_name:
            resource_list = {r: resource_list[r] for r in resource_list if r == resource_name}
        for r in project_dict['project']['resource']:
            # {account: {}, ...}
            self[r] = {}
            for m in project_dict['project']['resource'][r]['model']:
                for row in project_dict['project']['resource'][r]['model']['rows']:

                    for fld in row:
                        if fld == 'field':
                            # {account: {id: {}, ...}, ...}
                            self[r][row[fld]] = {}
                            # fld_key= fld

                        # {account: {id: {pattern: ^.{3,330}$, ... }, ...}, ...}
                        self[r][row['field']]['pattern'] = Pattern(row)
def test_resource_patterns():
    actual = ResourcePatterns(Tier(ProjectStringDefault()), 'account')
    print('   resource_patterns:', actual)
    assert ('account' in actual)
    assert ('id' in actual['account'])
    assert ('pattern' in actual['account']['id'])


class RouteConstantsJS(str):
    def __new__(cls, project_dict, project_name):
        #resource_list = project_dict['project'][ProjectNameFirst(project_dict)]['resource']

        resource_list = ResourceNames(project_dict, project_name)
        lst = ['/* generated in RouteConstantsJS from {} */'.format(str(__file__))]
        for r in resource_list:
            # crud = CRUD_Collective(project_dict, r)
            # if 'C' in crud:
            lst.append('const {}_route_post = require(\'../route/__routes__/{}_route_post.js\');'.format(r, r))
            lst.append('const {}_route_get = require(\'../route/__routes__/{}_route_get.js\');'.format(r, r))
            lst.append('const {}_route_put = require(\'../route/__routes__/{}_route_put.js\');'.format(r, r))
            lst.append('const {}_route_delete = require(\'../route/__routes__/{}_route_delete.js\');'.format(r, r))

        contents = '\n'.join(lst)

        instance = super().__new__(cls, contents)
        return instance
def test_route_constants_js():
    project = TierMD(ProjectStringDefault())
    project_name =  ProjectNameFirst(project)
    route_constants = RouteConstantsJS(project, project_name)
    route_constants = ['                      {}'.format(x) for x in route_constants.split('\n')]
    print('  route_constants_js:', '\n'.join(route_constants).strip())
    assert (
                "                      const account_route_post = require('../route/__routes__/account_route_post.js');" in route_constants)
    assert (
                "                      const account_route_delete = require('../route/__routes__/account_route_delete.js');" in route_constants)


class ApiRoutes(str):
    def __new__(cls, project_dict, project_name):
        resource_list = project_dict['project'][project_name]['resources']
        # lst = ['/* generated in RouteConstantsJS from {} */'.format(str(__file__))]
        lst = []
        # lst_comments=[]
        for r in resource_list:
            # crud = CRUD_Collective(project_dict, r)
            # if 'C' in crud:
            # lst_comments.append('  // [* {} Route Configuration, Create {}]'.format(r,r))
            # lst.append('  {}_route_post'.format(r))
            # lst.append('  {}_route_get'.format(r))
            # lst.append('  {}_route_put'.format(r))
            # lst.append('  {}_route_delete'.format(r))
            lst.append('server.route({})'.format('{}_route_post'.format(r)))
            lst.append('server.route({})'.format('{}_route_get'.format(r)))
            lst.append('server.route({})'.format('{}_route_put'.format(r)))
            lst.append('server.route({})'.format('{}_route_delete'.format(r)))

        contents = ';\n'.join(lst) + ';'

        instance = super().__new__(cls, contents)
        return instance
'''
class ApiRoutes(str):
    def __new__(cls,project_dict):
        resource_list = project_dict['project']['resource']
        # lst = ['/* generated in RouteConstantsJS from {} */'.format(str(__file__))]
        lst=[]
        #lst_comments=[]
        for r in resource_list:
            # crud = CRUD_Collective(project_dict, r)
            # if 'C' in crud:
            # lst_comments.append('  // [* {} Route Configuration, Create {}]'.format(r,r))
            lst.append('  {}_route_post'.format(r))
            lst.append('  {}_route_get'.format(r))
            lst.append('  {}_route_put'.format(r))
            lst.append('  {}_route_delete'.format(r))

        contents = ',\n'.join(lst)

        instance = super().__new__(cls, contents)
        return instance
'''
def test_api_routes():
    api_routes = ApiRoutes(Tier(ProjectStringDefault()))
    api_routes = ['                    {}'.format(x) for x in api_routes.split('\n')]
    print('          api_routes:', '\n'.join(api_routes).strip())
    print()
    assert ('                    server.route(account_route_post);' in api_routes)
    assert ('                    server.route(account_route_delete);' in api_routes)


'''
class NVResourceMethodScopes(NVList):
    # NVResourceMethodScopes(project_dict, resource_name)
    def __init__(self, project_dict, resource_name):
        print('NVResourceMethodScopes type', type(project_dict))
        print('NVResourceMethodScopes dict',project_dict)

        if resource_name not in project_dict['project']['resource']:
            # print('project_dict', project_dict['project']['resource'])
            raise Exception('Resource Name Not Found: {}'.format(resource_name))
        # Route Scopes
        self.add({'name': '<<DELETE_SCOPE>>', 'value': RouteScopes(project_dict, resource_name, 'DELETE')})
        self.add({'name': '<<GET_SCOPE>>', 'value': RouteScopes(project_dict, resource_name, 'GET')})
        self.add({'name': '<<POST_SCOPE>>', 'value': RouteScopes(project_dict, resource_name, 'POST')})
        self.add({'name': '<<PUT_SCOPE>>', 'value': RouteScopes(project_dict, resource_name, 'PUT')})

def test_nv_resource_method_scopes():
    actual = NVResourceMethodScopes(Tier(ProjectStringDefault()), 'account')
    print('         resource method scope:', actual)
    for nv in actual:
        assert ('name' in nv)
        assert ('value' in nv)
        assert (nv['name'] in ['<<DELETE_SCOPE>>', '<<GET_SCOPE>>','<<POST_SCOPE>>','<<PUT_SCOPE>>'])
        assert (nv['value'][0] in ['api_admin', 'api_guest', 'api_user'])
'''


'''
class NVResourceSchemaVersion(NVList):
    def __init__(self, project_dict, resource_name):
        schema = 'api'
        print('project_dict',project_dict)
        #print('resource_name',resource_name)
        if 'schema' in project_dict['project']['resource'][resource_name]:  # schema:
            schema = project_dict['project']['resource'][resource_name]['schema']
        version = '0.0.1'
        if 'version' in project_dict['project']['resource'][resource_name]:  # schema:
            version = project_dict['project']['resource'][resource_name]['version']

        self.add({'name': '<<API_SCHEMA>>', 'value': '{}_{}'.format(schema, version.replace('.', '_'))})
def test_nv_resource_schema_version():
    actual = NVResourceSchemaVersion(Tier(ProjectStringDefault()), 'account')
    print('nv resource schema version', actual)
    assert(actual == [{'name': '<<API_SCHEMA>>', 'value': 'api_0_0_0'}])
'''
# Tasks

class Task_InitializeEnv(ProcessProject):
    ##
    ###### Initialize MD2
    ##
    ## Make the md2.env file
    def __init__(self, no=0):
        ProcessProject.__init__(self)
        self.no = no

    def initialize_md2(self):

        if not self.get_application():
            MultiLogger().set_msg('Application Not Found!').runtime().terminal()
            raise Exception('Application Not Found!')

        ##* __Create__ '\<root>/bin/md2.env' __From__ template __When__ file NF

        env_name = self.get_application().get_environment_filename().split('/')[-1]
        if not os.path.isfile(self.get_application().get_environment_filename()):
            MultiLogger().set_msg('    Create ({})'.format(env_name)).runtime().terminal()

            # init .env from template
            env_file_content_string = self.get_application().isStringNone(
                StringReader(self.get_application().get_environment_template_filename()))
            assert (env_file_content_string)
            StringWriter(self.get_application().get_environment_filename(), env_file_content_string)

        self.get_application().add('initialize ({})'.format(env_name))
        return self

    def process(self):
        # print('1. Initialize MD2')
        MultiLogger().set_msg(
            '{}. Initialize Environment {}'.format(self.no, self.get_application().get_name())).runtime().terminal()

        self.initialize_md2()

        return self


class Task_Configure(ProcessProject):
    ##
    ###### Configure MD2 Environment Values
    def __init__(self, no=0):  # , env_file_content_string): # , recorder):
        ProcessProject.__init__(self)
        # package is {nv_list, repo_folder, template_folder}
        #
        self.env_file_content_string = None  # env_file_content_string
        self.no = no

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
        self.set_env_var('GH_TRUNK', 'main')
        ##    * __Configure__ GH_PROJECT
        self.set_env_var('GH_PROJECT', 'test_prj')
        ##    * __Configure__ GH_BRANCH
        self.set_env_var('GH_BRANCH', 'first')
        ##    * __Configure__ GH_REPO
        self.set_env_var('GH_REPO', 'py_test')
        ##    * __Configure__ GH_USER
        self.set_env_var('GH_USER', 'x')
        ##    * __Configure__ GH_MESSAGE
        self.set_env_var('GH_MESSAGE', 'init')
        ##    * __Configure__ GH_TOKEN
        self.set_env_var('GH_TOKEN', 'x')

        super().configure_environment()
        env_file_content_string = StringReader(self.get_application().get_environment_filename())

        self.env_file_content_string = UpserterString(env_file_content_string,
                                                      settings={'dup': True, 'hard_fail': True}) \
            .upsert(EnvVarString())
        return self

    def process(self):
        MultiLogger().set_msg(
            '{}. Configure {}'.format(self.no, self.get_application().get_name())).runtime().terminal()

        self.configure_environment()

        return self


class Task_InitializeProjecMd(ProcessProject):
    ##
    ###### Configure MD2 Environment Values
    def __init__(self, no=0):  # , env_file_content_string): # , recorder):
        ProcessProject.__init__(self)
        self.set_template_folder_key('__project__')
        self.no = no

        # package is {nv_list, repo_folder, template_folder}

    def initialize_project_md(self):
        # copy template/__project__/project_<<WS_PROJECT>>.md.C---.tmpl.tmpl
        nv_list = self.get_template_key_list()  # self.get_template_name_value_pairs()

        project_folder = os.getcwd()
        if project_folder.endswith('/bin'):
            # print('project folder', project_folder)
            self.templatize(nv_list=nv_list, output_folder=project_folder)
        return self

    def process(self):
        MultiLogger().set_msg(
            '{}. Task_InitializeProjecMd {}'.format(self.no, self.get_application().get_name())).runtime().terminal()

        self.initialize_project_md()

        return self


class Task_Github(ProcessProject):
    ##
    ###### Clone GitHub Repository
    ## Create and Configure a Project Repository.
    def __init__(self, no=0):  # , recorder=None ):
        ProcessProject.__init__(self)
        # super().__init__(template_folder_key='github', recorder=recorder)

        # package is {nv_list, repo_folder, template_folder}
        #
        # self.recorder=recorder
        self.set_template_folder_key('github')
        self.no = no

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
        # print('3. GitHub:')
        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('{}. GitHub: {}'.format(self.no, repo_name)).runtime().terminal()

        self.clone()
        self.templatize()

        return self


class Task_GithubPatch(ProcessProject):
    ##
    ###### Patch Clone
    ##
    ## Make sure that runtime files don't get included in the repo
    def __init__(self, no=0):  # , recorder=None ):
        ProcessProject.__init__(self)
        # package is {nv_list, repo_folder, template_folder}
        self.no = no

    def patch(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        ##* __Patch__ .gitignore

        self.get_application().add('patch(.gitignore)')

        repo_folder = self.get_repo_folder()
        # repo_name = repo_folder.split('/')[-1]

        temp_file = '{}/.gitignore'.format(repo_folder)

        if not os.path.isfile(temp_file):
            if 'GH_TEST' not in os.environ:
                raise Exception('Uninitialized file ({})'.format(temp_file.split('/')[-1]))

        temp_contents = ''
        if os.path.isfile(temp_file):
            temp_contents = StringReader(temp_file)
        temp_contents = UpserterString(temp_contents, settings={'dup': True, 'hard_fail': True},
                                       recorder=self.get_application()) \
            .upsert('*.env') \
            .upsert('.idea/')
        ##  * add "*.env" line when NF
        ##  * add "*.idea" line when NF
        ##
        # self.makedirs(temp_file)
        StringWriter(temp_file, temp_contents)
        return self

    def process(self):

        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('{}. GitHub Patch: {}'.format(self.no, repo_name)).runtime().terminal()

        self.patch()

        return self


class Task_InitializeProjectSpace(ProcessProject):
    ##
    ###### Initialize ProjectSpace
    ##
    def __init__(self, no=0):
        ProcessProject.__init__(self)

        self.set_template_folder_key('projectspace')
        self.no = no

    def projectspace_templates(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        self.get_application().add(self.get_template_folder_key())
        ##* Templatize Projectspace templates
        self.templatize()
        return self

    def process(self):
        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('{}. ProjectSpace: {}'.format(self.no, repo_name)).runtime().terminal()

        self.projectspace_templates()

        return self


class Task_InitializeDocker(ProcessProject):
    ##
    ###### Initialize Docker
    ##

    def __init__(self, no=0):  # , recorder=None ):
        ProcessProject.__init__(self)
        self.set_template_folder_key('docker')
        self.no = no

    def docker_templates(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        self.get_application().add('docker')
        ##* Templatize Docker templates
        self.templatize()
        return self

    def process(self):
        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('{}. Docker: {}'.format(self.no, repo_name)).runtime().terminal()

        self.docker_templates()

        return self


class Task_InitializeHeroku(ProcessProject):
    ##
    ###### Initialize Heroku
    ##

    def __init__(self, no=0):  # , recorder=None ):
        ProcessProject.__init__(self)
        self.set_template_folder_key('heroku')
        self.no = no

    def heroku_templates(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        self.get_application().add('heroku')
        ##* Templatize Heroku templates
        self.templatize()
        return self

    def process(self):
        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('{}. Heroku: {}'.format(self.no, repo_name)).runtime().terminal()

        self.heroku_templates()

        return self


class Task_InitializeNode(ProcessProject):
    ##
    ###### Initialize Node
    ##

    def __init__(self, no=0):
        ProcessProject.__init__(self)
        self.set_template_folder_key('node')
        self.no = no

    def node_templates(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        self.get_application().add('node')
        ##* Templatize Node templates
        self.templatize()
        return self

    def process(self):
        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('{}. Node: {}'.format(self.no, repo_name)).runtime().terminal()

        self.node_templates()

        return self


class Task_InitializeJWT(ProcessProject):
    ##
    ###### Initialize Node
    ##

    def __init__(self, no=0):
        ProcessProject.__init__(self)
        self.set_template_folder_key('jwt')
        self.no = no

    def jwt_templates(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        self.get_application().add('jwt')
        ##* Templatize JWT templates
        self.templatize()
        return self

    def process(self):
        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('{}. JWT: {}'.format(self.no, repo_name)).runtime().terminal()

        self.jwt_templates()

        return self


class Task_InitializeNodemon(ProcessProject):
    ##
    ###### Initialize Nodemon
    ##

    def __init__(self, no=0):
        ProcessProject.__init__(self)
        self.set_template_folder_key('nodemon')
        self.no = no

    def nodemon_templates(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        self.get_application().add('nodemon')
        ##* Templatize Nodemon templates
        self.templatize()
        return self

    def process(self):
        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('{}. Nodemon: {}'.format(self.no, repo_name)).runtime().terminal()

        self.nodemon_templates()

        return self

# /lib/route/__routes__
class Task_InitializeHapi(ProcessProject):
    ##
    ###### Initialize Hapi
    ##
    ## create singleton templates i.e. templates/hapi
    ## applies .env values to templates

    def __init__(self, no=0):
        ProcessProject.__init__(self)
        self.set_template_folder_key('hapi')
        self.no = no

        # nv_list = self.get_template_key_list() # self.get_template_name_value_pairs()
        # print('nv_list', nv_list)
        # resource_md = '{}/{}'.format('/'.join(str(__file__).split('/')[0:-1]), TemplateString('project_<<WS_PROJECT>>.md',nv_list))
        # print('project_<<WS_PROJECT>>.md.C---.tmpl', resource_md)

    def hapi_templates(self):
        if not self.get_application():
            raise Exception('Application Not Found!')

        print('ProcessProject', ProcessProject())

        #self.get_application().add('hapi')
        self.get_application().add(self.get_template_folder_key())
        ##* Templatize Hapi templates in '/template/hapi'
        ##* Extract ENVironment name-value pairs from memory
        nv_list = self.get_template_key_list()
        ##* Read project file from user provided bin/project_??.md file
        filename_md = TemplateString('project_<<WS_PROJECT>>.md', nv_list)
        folderfilename_md = '{}/{}'.format(os.getcwd(), filename_md)
        print('folderfilename_md', folderfilename_md)
        resource_string = StringReader(folderfilename_md)
        ##* Convert project file contents to Dictionary
        project_dict = TierMD(resource_string)
        project_name = ProjectNameFirst(project_dict)
        ##* Extract ROUTE_CONST name-value pairs from project dictionary
        nv_list.append({'name': '<<ROUTE_CONST>>', 'value': RouteConstantsJS(project_dict, project_name)})
        ##* Extract API_ROUTES name-value pairs from project dictionary
        nv_list.append({'name': '<<API_ROUTES>>', 'value': ApiRoutes(project_dict, project_name)})

        print('nv_list', nv_list)
        # pprint(nv_list)
        #
        #
        self.templatize(nv_list=nv_list)
        return self

    def process(self):
        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('{}. Hapi: {}'.format(self.no, repo_name)).runtime().terminal()

        self.hapi_templates()

        return self


# create server_ext
# merge server_ext with <<API_ROUTES>> Task_MergeHapiServerRouteNames
# merge server_ext with <<ROUTE_CONST>> Task_MergeHapiServerRouteNames
# intialize routes_*.js files Task_InitializeHapiRoutes
from source.component.task_initialize_hapi_routes import Task_InitializeHapiRoutes

class Task_InitializePostgres(ProcessProject):
    ##
    ###### Initialize Postgres
    ##

    ## Templates source/template/postgress

    def __init__(self, no=0):
        ProcessProject.__init__(self)
        self.set_template_folder_key('postgres')
        self.no = no

    def postgres_templates(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        self.get_application().add(self.get_template_folder_key())
        ##* Templatize Postgres templates
        self.templatize()
        return self

    def process(self):
        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('{}. Postgres: {}'.format(self.no, repo_name)).runtime().terminal()

        self.postgres_templates()

        return self


class Task_InitializeModel(ProcessProject):
    ##
    ###### Initialize Model
    ##
    ## Generate javascript
    ##
    ## Templates in source/template/model
    def __init__(self, no=0):
        ProcessProject.__init__(self)
        self.set_template_folder_key('model')
        self.no = no

    def db_deploy_templates(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        # self.get_application().add(self.get_template_folder_key())
        # customize nv_list
        ##* Templatize DB Deploy templates
        nv_list = self.get_template_key_list()
        project_dict = self.get_project_dictionary()
        project_name = ProjectNameFirst(project_dict)
        # get resource
        #for xxx in project_dict['project']:
        #    print('xxx',xxx)
        #print('xxx done')
        #nv_list = nv_list.extend(NVResource(project_dict=project_dict))
        for resource in project_dict['project'][project_name]['resources']:
            print('xresource', resource)

        self.templatize(nv_list=nv_list)
        return self

    def process(self):
        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('{}. Model: {}'.format(self.no, repo_name)).runtime().terminal()

        self.db_deploy_templates()

        return self


class Task_UpdateEnvironment(ProcessProject):
    ##
    ###### Update MD2 Environment Variables
    ##
    def __init__(self, no=0):  # , env_file_content_string, recorder=None):
        ProcessProject.__init__(self)  # (template_folder_key='github', recorder=recorder)
        self.no = no

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
                                                 recorder=self.get_application()).upsert(
            get_env_variable_values_string())
        ##* __Commit__ Environment Values __To__ '\<root>/bin/md2.env'

        StringWriter(self.get_application().get_environment_filename(),
                     env_file_content_string,
                     self.get_application())

        # print('   * step {} {}'.format(self.get_application().get_name(),DiagramString(self.get_application())))

        assert (self.get_application().get_environment_filename())
        return self

    def process(self):
        MultiLogger().set_msg(
            '{}. Update Environment: {}'.format(self.no, self.get_application().get_name())).runtime().terminal()

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
        self.no = 0

    def incNo(self):
        self.no += 1
        return self.no


class Auto():
    ##
    ###### Auto
    ##
    ## Launch/run Task_
    def __init__(self, process):
        process.run()


##<hr/>
##
#### Parent Classes


if __name__ == "__main__":
    # execute as docker
    test = True
    test = False
    if test:
        print('Testing...')
        # test_dict_md()

        test_project_name()
        test_resource_names()
        test_role_names()
        # test_resource_permissions()
        # test_resource_fields()
        # dep test_resource_field_sizes()
        #test_pattern()
        test_resource_patterns()
        test_route_constants_js()
        test_api_routes()
        #test_min()
        #test_max()
        test_list_env()
        # test_nv_env()
        # test_nv_field()
        # test_nv_resource_fields()
        test_nv_resource()

        test_route_scope()

        test_nv_resource_method_scopes()
        test_nv_resource_schema_version()

        print('Testing Complete')
    if not test:
        main()
