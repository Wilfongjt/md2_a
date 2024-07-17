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
    JSONString, NormalString, Stack, Level, \
    TemplateString, \
    TemplateList_Latest

from source.component.nv_list import NVList

from functions import get_bin_folder, \
    get_template_folder, \
    get_env_variable_values_string
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
    Auto(TaskInitializeEnv(no=app.incNo()).set_application(app))

    ##1. [Configure MD2 Environment Values](#configure-md2-environment-values)
    Auto(TaskConfigure(no=app.incNo()).set_application(app))  # (env_file_content_string, app)

    ##1. [Initialize project_<<WS_PROJECT>>.md.C---.tmpl](#configure-md2-environment-values)
    print('-----')
    Auto(TaskInitializeProjecMd(no=app.incNo()).set_application(app))  # (env_file_content_string, app)
    print('-----')
    # exit(0)
    ##1. [Clone GitHub Repository](#clone-github-repository)
    Auto(TaskGithub(no=app.incNo()).set_application(app))

    ##1. [Patch Clone](#patch-clone)
    Auto(TaskGithubPatch(no=app.incNo()).set_application(app))

    ##1. [Initialize ProjectSpace](#initialize-projectspace)
    Auto(TaskInitializeProjectSpace(no=app.incNo()).set_application(app))

    ##1. [Initialize Docker](#initialize-docker)
    Auto(TaskInitializeDocker(no=app.incNo()).set_application(app))

    ##1. [Initialize Heroku](#initialize-heroku)
    Auto(TaskInitializeHeroku(no=app.incNo()).set_application(app))

    ##1. [Initialize Node](#initialize-node)
    Auto(TaskInitializeNode(no=app.incNo()).set_application(app))

    ##1. [Initialize JWT](#initialize-jwt)
    Auto(TaskInitializeJWT(no=app.incNo()).set_application(app))

    ##1. [Initialize Nodemon](#initialize-nodemon)
    Auto(TaskInitializeNodemon(no=app.incNo()).set_application(app))

    ##1. [Initialize Hapi](#initialize-hapi)
    Auto(TaskInitializeHapi(no=app.incNo()).set_application(app))  # move /templates to project, apply .env nv_list
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
    ##1. [Initialize Hapi Routes](#initialize-hapi-routes)
    Auto(TaskInitializeHapiRoutes(no=app.incNo()).set_application(app))  # -->
    # exit(0)
    ##1. [Initialize Postgres](#initialize-postgres)
    Auto(TaskInitializePostgres(no=app.incNo()).set_application(app))

    ##1. [Initialize Model](#initialize-model)
    Auto(TaskInitializeModel(no=app.incNo()).set_application(app))

    ##1. [Update Environment Values](#update-md2-environment-variables)
    Auto(TaskUpdateEnvironment(no=app.incNo()).set_application(app))

    xx = 'Summary {} {}'.format(app.get_name(), DiagramString(app))
    MultiLogger().set_msg(xx).runtime().terminal()
    MultiLogger().set_msg('end').runtime().terminal()


def getEnvString():
    return '''# #
# ### Environment
# #* last github organization
WS_ORGANIZATION=test_org

# #* last workspace
WS_WORKSPACE=test_ws

# #* last project
WS_PROJECT=test_prj

WS_REPO=py_test

# #* last trunk
GH_TRUNK=main

# #* last branch
GH_BRANCH=first

# #* last repo
GH_REPO=py_test

GH_PROJECT=test_prj

# #* last user
GH_USER=wilfongjt

# #* last message
GH_MESSAGE=init

# #* last token
GH_TOKEN=<<GH_TOKEN>>

# #* MD2DM_INPUT_FOLDER defines where to get input
MD2DM_INPUT_FOLDER=<<MD2DM_INPUT_FOLDER>>

# #* MD2DM_OUTPUT_FOLDER defines where to send output
MD2DM_OUTPUT_FOLDER=<<MD2DM_OUTPUT_FOLDER>>

# #* MD2DM_OUTPUT_FILENAME defines the name of the output file
MD2DM_OUTPUT_FILENAME=<<MD2DM_OUTPUT_FILENAME>>


'''


def getProjectString():
    # used for testing
    return '''
    # Project: sample

    ## Claims:

    | name      | aud       | iss                | sub        | user       | scope     | key |
    |-----------|-----------|--------------------|------------|------------|-----------|-----|
    | api_admin | lyttlebit | sample_api_client  | client_api | client_api | api_admin | ?   |
    | api_guest | lyttlebit | sample_api_client  | client_api | client_api | api_guest | 0   |
    | api_user  | lyttlebit | sample_api_client  | client_api | client_api | api_user  | ?   |

    ## Resources
    ### Resource: Account
    1. version: 1.0.0

    #### Model:

    | field       | type | size   | validate | encrypt | api_admin | api_guest | api_user |
    |-------------|------|--------|----------|---------|-----------|-----------|----------|
    | id          | C    | 3-330  | R        | N       | R         | CR        | RUD      |
    | type        | C    | 3-330  | R        | N       | R         | CR        | RUD      |
    | owner       | C    | 3-330  | R        | N       | R         | CR        | RUD      |
    | username    | C    | 3-330  | R        | N       | R         | CR        | RUD      |
    | displayname | C    | 3-330  | R        | N       | R         | CR        | RUD      |
    | password    | C    | 10-330 | R        | Y       | -         | CR        | UD       |
    | scope       | C    | 3-330  | R        | N       | R         | CR        | RUD      |

    Types
    * C is character, any keyboard character
    * L is logical aka boolean, eg ‘True', ‘False', ’T', ‘F', ‘Y', ’N', ‘1', ‘0' 
    * N is numeric, eg ‘1' or ‘1.1' or ‘-1.1' 
    * D is datetime, eg '2024-06-23' or '2024-06-23 18:30:00'

    Roles
    * C is Create
    * R is Read
    * U is Update
    * D is Delete
    * - is None

    #### Data:

    | id        | type    | owner                    | username                | displayname | password | scope     |
    |-----------|---------|--------------------------|-------------------------|-------------|----------|-----------|
    | api_admin | ACCOUNT | api_admin@lyttlebit.com  | api_admin@lyttlebit.com | Admin       | a1A!aaa  | api_admin |
    | api_guest | ACCOUNT | api_guest@lyttlebit.com  | api_guest@lyttlebit.com | Guest       | a1A!aaa  | api_guest |
    | api_user  | ACCOUNT | api_user@lyttlebit.com   | api_user@lyttlebit.com  | User        | a1A!aaa  | api_user  |

    * Do not use same passwords in production
    * Set type to capitalized(resource)
    * ? means value is unknown until runtime
    * - means not applicable


    ### Resource: Sample_resource
    1. version: 1.0.0

    #### Model:

    | field       | type | size   | validate | encrypt | api_admin | api_guest | api_user |
    |-------------|------|--------|----------|---------|-----------|-----------|----------|
    | id          | C    | 3-330  | R        | N       | R         | CR        | RUD      |
    | type        | C    | 3-330  | R        | N       | R         | CR        | RUD      |
    | owner       | C    | 3-330  | R        | N       | R         | CR        | RUD      |
    | s_integer   | C    | 3-330  | R        | N       | R         | CR        | RUD      |
    | s_character | C    | 3-330  | R        | N       | R         | CR        | RUD      |
    | s_number    | C    | 10-330 | R        | Y       | -         | CR        | UD       |
    | s_datetime  | C    | 3-330  | R        | N       | R         | CR        | RUD      |

    server_ext.js
    + ------------------------ +
    + require(route_const.js)  + <-- route_const.js
    +                          +
    + require(route_list.js)   + <-- route_list.js
    + ------------------------ +
    '''.replace('    ', '')


##### Coversion

#####
class StringExpandMdTable(str):
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
def getProjectMDString():
    return '''
    # Project: sample

    ## Claims:

    | name      | aud       | iss                | sub        | user       | scope     | key |
    |-----------|-----------|--------------------|------------|------------|-----------|-----|
    | api_admin | lyttlebit | sample_api_client  | client_api | client_api | api_admin | ?   |
    | api_guest | lyttlebit | sample_api_client  | client_api | client_api | api_guest | 0   |
    | api_user  | lyttlebit | sample_api_client  | client_api | client_api | api_user  | ?   |

    ## Resources
    ### Resource: Account
    1. version: 1.0.0

    #### Model:

    | field       | type | size   | validate | encrypt | api_admin | api_guest | api_user |
    |-------------|------|--------|----------|---------|-----------|-----------|----------|
    | id          | C    | 3-330  | R        | N       | R         | CR        | RUD      |
    | type        | C    | 3-330  | R        | N       | R         | CR        | RUD      |
    | owner       | C    | 3-330  | R        | N       | R         | CR        | RUD      |
    | username    | C    | 3-330  | R        | N       | R         | CR        | RUD      |
    | displayname | C    | 3-330  | R        | N       | R         | CR        | RUD      |
    | password    | C    | 10-330 | R        | Y       | -         | CR        | UD       |
    | scope       | C    | 3-330  | R        | N       | R         | CR        | RUD      |

    Types
    * C is character, any keyboard character
    * L is logical aka boolean, eg ‘True', ‘False', ’T', ‘F', ‘Y', ’N', ‘1', ‘0' 
    * N is numeric, eg ‘1' or ‘1.1' or ‘-1.1' 
    * D is datetime, eg '2024-06-23' or '2024-06-23 18:30:00'

    Roles
    * C is Create
    * R is Read
    * U is Update
    * D is Delete
    * - is None

    #### Data:

    | id        | type    | owner                    | username                | displayname | password | scope     |
    |-----------|---------|--------------------------|-------------------------|-------------|----------|-----------|
    | api_admin | ACCOUNT | api_admin@lyttlebit.com  | api_admin@lyttlebit.com | Admin       | a1A!aaa  | api_admin |
    | api_guest | ACCOUNT | api_guest@lyttlebit.com  | api_guest@lyttlebit.com | Guest       | a1A!aaa  | api_guest |
    | api_user  | ACCOUNT | api_user@lyttlebit.com   | api_user@lyttlebit.com  | User        | a1A!aaa  | api_user  |

    * Do not use same passwords in production
    * Set type to capitalized(resource)
    * ? means value is unknown until runtime
    * - means not applicable


    ### Resource: Sample_resource
    1. version: 1.0.0

    #### Model:

    | field       | type | size   | validate | encrypt | api_admin | api_guest | api_user |
    |-------------|------|--------|----------|---------|-----------|-----------|----------|
    | id          | C    | 3-330  | R        | N       | R         | CR        | RUD      |
    | type        | C    | 3-330  | R        | N       | R         | CR        | RUD      |
    | owner       | C    | 3-330  | R        | N       | R         | CR        | RUD      |
    | s_integer   | C    | 3-330  | R        | N       | R         | CR        | RUD      |
    | s_character | C    | 3-330  | R        | N       | R         | CR        | RUD      |
    | s_number    | C    | 10-330 | R        | Y       | -         | CR        | UD       |
    | s_datetime  | C    | 3-330  | R        | N       | R         | CR        | RUD      |

    server_ext.js
    + ------------------------ +
    + require(route_const.js)  + <-- route_const.js
    +                          +
    + require(route_list.js)   + <-- route_list.js
    + ------------------------ +
    '''.replace('    ', '')


class ListEnv(NVList):
    def __init__(self, env_string):
        pattern = re.compile(r'^\s*[A-Za-z0-9_]+=[A-Za-z0-9]+\s*$')
        for ln in env_string.split('\n'):
            if pattern.match(ln):
                pts = [l.strip() for l in ln.split('=')]
                self.append({'name': pts[0], 'value': pts[1]})


def test_list_env():
    nv_list = ListEnv(getEnvString())
    print('            list_env:', nv_list)
    assert ({'name': 'GH_TRUNK', 'value': 'main'} in nv_list)
    assert ({'name': 'GH_BRANCH', 'value': 'first'} in nv_list)
    assert ({'name': 'GH_USER', 'value': 'wilfongjt'} in nv_list)
    assert ({'name': 'GH_MESSAGE', 'value': 'init'} in nv_list)


class DictMd(dict):

    def __init__(self, md_text):
        # skip spaces
        # skip *
        # stack = Stack()
        ostack = Stack()
        table = False
        tbl_cols = []
        last_key = ''
        last_obj = {}
        i = 0
        a = 0
        resource_name = ''
        for ln in str(md_text).split('\n'):
            # print('lineno',i)
            # print('DictMd ln', ln)
            if not ln.startswith('|'):
                table = False
            if ln.startswith('#'):
                # print('DictMd level', Level(ln))
                level = Level(ln)
                ln = ln.replace(':', '')
                ln = ln.split(' ')
                if len(ln) < 2:
                    raise Exception('Bad Line')
                # while stack.size() >= level: stack.pop()
                while ostack.size() >= level: ostack.pop()

                if ostack.size() == 0:  # 1:  # projecrt
                    self[ln[1].lower()] = {'name': ln[2].lower()}
                    # self[ln[1].lower()] = {'name': ln[2].lower()}
                    ostack.push(self[ln[1].lower()])

                elif ostack.size() >= 1:  # project claims

                    if len(ln) == 2:
                        # print('2 split ', ln)
                        if 'resource' == ln[0].lower(): resource_name = ln[1].lower()
                        last_key = ln[1].lower()
                        ostack.peek()[ln[1].lower()] = {}  # table rows
                        # ostack.peek()[ln[1].lower()] = {}
                        ostack.push(ostack.peek()[ln[1].lower()])
                        last_obj = ostack.peek()
                        # print('  ostack', ostack)
                        # print('  self', self)
                    elif len(ln) == 3:
                        # print('3 split ', ln)
                        if 'resource' == ln[1].lower():
                            # print('resource found')
                            resource_name = ln[2].lower()

                        last_key = ln[2].lower()
                        ostack.peek()[ln[2].lower()] = {'name': ln[2].lower()}
                        # last_key = ln[1].lower()
                        # ostack.peek()[ln[1].lower()] = {'name': ln[2].lower()}
                        # ostack.peek()[ln[1].lower()] = {'name': ln[2].lower()}
                        ostack.push(ostack.peek()[ln[2].lower()])
                        # ostack.push(ostack.peek()[ln[1].lower()])

                        last_obj = ostack.peek()

                # print('1 peek', ostack.peek())
                # print('last_obj', last_obj)
            elif ln.startswith('1.'):
                # print('ln',ln)
                ln = ln.replace('1. ', '')
                ln = ln.split(':', maxsplit=1)

                line = ln[1].strip()

                if line.startswith('{'):
                    line = ast.literal_eval(line)
                # print('xxx peek', ostack.peek())
                # print('xxx ln[0]', ln[0])
                # print('xxx line', line)

                ostack.peek()[ln[0]] = line
            elif ln.startswith('|'):  # handle table
                if not table:
                    table = True
                    tbl_cols = ln.split('|')
                    tbl_cols = [c.strip() for c in tbl_cols if c != '']

                    last_obj['rows'] = []
                elif ln.startswith('|-'):  # table line break
                    pass
                else:  # row
                    # print('table self       ', self)
                    tbl_row = ln.split('|')
                    tbl_row = [c.strip() for c in tbl_row if c != '']
                    #
                    tbl_row = {tbl_cols[i]: tbl_row[i] for i in range(len(tbl_row))}
                    if 'field' in tbl_row:
                        tbl_row['resource'] = resource_name
                        tbl_row['pattern'] = Pattern(tbl_row)
                        tbl_row['min'] = Min(tbl_row)
                        tbl_row['max'] = Max(tbl_row)

                    ostack.peek()['rows'].append(tbl_row)

                    # last_obj['rows'].append(tbl_row)

            i += 1
        # print('DictMd')
        # pprint(self)
        # print('DictMd', self)
        # pprint(self)


def test_dict_md():
    # filename_md = 'project_test_prj.md'
    # folderfilename_md = '{}/{}'.format(os.getcwd(), filename_md)
    # print('folderfilename_md', folderfilename_md)
    # resource_string = getProjectMDString(DictMd(getProjectString())) # StringReader(folderfilename_md)
    # print('resource_string',resource_string)
    project_dict = DictMd(getProjectString())
    assert ('project' in project_dict)
    assert ('resources' in project_dict['project'])
    assert ('account' in project_dict['project']['resources'])
    assert ('model' in project_dict['project']['resources']['account'])
    assert ('rows' in project_dict['project']['resources']['account']['model'])
    assert ('sample_resource' in project_dict['project']['resources'])
    assert ('model' in project_dict['project']['resources']['sample_resource'])
    assert ('rows' in project_dict['project']['resources']['sample_resource']['model'])

    # print('route_templates project_dict', project_dict)
    # pprint(project_dict)
    # ResourceNames(project_dict)


class ProjectName(str):
    def __new__(cls, project_dict):
        contents = project_dict['project']['name']

        instance = super().__new__(cls, contents)
        return instance


def test_project_name():
    actual = ProjectName(DictMd(getProjectMDString()))
    print('        project_name:', actual)
    assert (actual == 'sample')


class ResourceNames(list):
    def __init__(self, project_dict):
        for r in project_dict['project']['resources']:
            print('Resource Names', r)
            self.append(r)


def test_resource_names():
    actual = ResourceNames(DictMd(getProjectMDString()))
    print('      resource_names:', actual)
    assert (actual == ['account', 'sample_resource'])


class RoleNames(list):
    def __init__(self, project_dict):
        lst = []
        for r in project_dict['project']['resources']:
            for f in project_dict['project']['resources'][r]['model']:
                for s in project_dict['project']['resources'][r]['model'][f]:
                    for x in s:
                        if x.startswith('api_'):
                            lst.append(x)
        # print('lst', lst)
        lst = set(lst)  # get rid of duplicates
        for r in lst:
            self.append(r)

    # TASKS


def test_role_names():
    actual = RoleNames(DictMd(getProjectMDString()))
    print('          role_names:', actual)
    assert ('api_admin' in actual)
    assert ('api_guest' in actual)
    assert ('api_user' in actual)


'''
class depResourcePermissions(dict):
    # { account: {id: {api_admin: R, api_guest:CR, api_user:RUD},...}
    def __init__(self, project_dict):
        #print('project_dict',project_dict)
        #pprint(project_dict)
        # self {}
        for r in project_dict['project']['resources']:
            # {account: {}, ...}
            self[r]={}
            for m in project_dict['project']['resources'][r]['model']:
                for row in project_dict['project']['resources'][r]['model']['rows']:
                    for fld in row:
                        if fld=='field':
                            # {account: {id: {}, ...}, ...}
                            self[r][row[fld]]={}
                            fld_key= fld
                        if fld.startswith('api_'):
                            # {account: {id: {api_admin: R, ... }, ...}, ...}
                            self[r][row['field']][fld] = row[fld]

def test_resource_permissions():
    resource_permissions = ResourcePermissions(DictMd(getProjectMDString()))
    print('resource_permissions:', resource_permissions)
    assert('account' in resource_permissions)
    assert('id' in resource_permissions['account'])
    assert('api_admin' in resource_permissions['account']['id'])
'''
'''
class depResourceFields(dict):
    def __init__(self, project_dict, resource_name):
        resource_list = project_dict['project']['resources']

        if resource_name:
            resource_list = {r: resource_list[r] for r in resource_list if r == resource_name}
        for r in project_dict['project']['resources']:
            # {account: {}, ...}
            self[r] = {}
            for m in project_dict['project']['resources'][r]['model']:
                for row in project_dict['project']['resources'][r]['model']['rows']:

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
    resource_fields = ResourceFields(DictMd(getProjectMDString()),'account')
    print('     resource_fields:', resource_fields)
    assert('id' in resource_fields['account'])
    assert('field' in resource_fields['account']['id'])
'''


# class ResourceFieldSizes(dict):
#    def __init__(self, project_dict, resource_name):
#        #resource_list = project_dict['project']['resources']

#        #if resource_name:
#        #    resource_list = {r: resource_list[r] for r in resource_list if r == resource_name}

#        for r in project_dict['project']['resources']:
#            # {account: {}, ...}
#            self[r] = {}
#            for m in project_dict['project']['resources'][r]['model']:

#                for row in project_dict['project']['resources'][r]['model']['rows']:
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
#    actual = ResourceFieldSizes(DictMd(getProjectMDString()),'account')

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
                contents = contents.replace('<<MIN>>', min).replace('<<MAX>>', max)
            elif resource_field['type'] == 'L':
                contents = '(True|False|Y|N|T|F|1|0)'
                resource_field['size'] = '1-5'  # eg True, False, Y, N, T, F, 1, or 0
            elif resource_field['type'] == 'I':
                contents = '-?\d{<<MIN>>,<<MAX>>}'
                min = resource_field['size'].split('-')[0]
                max = resource_field['size'].split('-')[1]
                contents = contents.replace('<<MIN>>', min).replace('<<MAX>>', max)
            elif resource_field['type'] == 'N':
                contents = '-?\d{1,<<W>>}(\.\d{1,<<D>>})?'  # .replace('<<W>',w).replace('<<D>>',d) # eg
                w = resource_field['size'].split(',')[0]
                d = resource_field['size'].replace('-', ',').split(',')[1]
                contents = contents.replace('<<W>>', w).replace('<<D>>', d)
            elif resource_field['type'] == 'D':
                contents = '(\d{4}-\d{2}-\d{2})([T ]?)(\d{2}:\d{2}:\d{2})?(\.\d+)?(Z|([+-]\d{2}:\d{2}))?'
                resource_field['size'] = '8-19'  # eg 2024-06-23 18:30:00

        instance = super().__new__(cls, contents)
        return instance


def test_pattern():
    # character
    resource_field = {'size': '3-330', 'type': 'C'}
    # resource_field = {'size': '3-330', 'type': 'C', 'api_admin': 'R', 'api_guest': 'CR', 'api_user': 'RUD', 'encrypt': 'N', 'field': 'id', 'resource': 'account', 'validate': 'R'}
    # print('C', Pattern(resource_field))
    print('   character pattern: {} -> {}'.format(resource_field, Pattern(resource_field)))
    assert (Pattern(resource_field) == '^.{3,330}$')
    assert (re.match(Pattern(resource_field), 'abc!89'))
    # logical
    resource_field = {'size': '14,6', 'type': 'L'}
    print('     logical pattern: {} -> {}'.format(resource_field, Pattern(resource_field)))
    assert (Pattern(resource_field) == '(True|False|Y|N|T|F|1|0)')
    assert (re.match(Pattern(resource_field), 'False'))
    assert (re.match(Pattern(resource_field), 'True'))
    assert (re.match(Pattern(resource_field), 'Y'))
    assert (re.match(Pattern(resource_field), 'N'))
    assert (re.match(Pattern(resource_field), 'T'))
    assert (re.match(Pattern(resource_field), 'F'))
    assert (re.match(Pattern(resource_field), '0'))
    assert (re.match(Pattern(resource_field), '1'))
    assert (not re.match(Pattern(resource_field), 'z'))
    # integer
    resource_field = {'size': '1-6', 'type': 'I'}
    # print('integer',Pattern(resource_field))
    print('     integer pattern: {} -> {}'.format(resource_field, Pattern(resource_field)))
    assert (Pattern(resource_field) == '-?\d{1,6}')
    assert (not re.match(Pattern(resource_field), 'a'))
    assert (re.match(Pattern(resource_field), '1'))
    assert (re.match(Pattern(resource_field), '-1'))

    # number
    resource_field = {'size': '14,6', 'type': 'N'}
    print('      number pattern: {} -> {}'.format(resource_field, Pattern(resource_field)))
    assert (Pattern(resource_field) == '-?\d{1,14}(\.\d{1,6})?')
    assert (not re.match(Pattern(resource_field), 'a'))
    assert (re.match(Pattern(resource_field), '1'))
    assert (re.match(Pattern(resource_field), '-1'))
    assert (re.match(Pattern(resource_field), '1.1'))
    # datetime
    resource_field = {'size': '14,6', 'type': 'D'}
    print('    datetime pattern: {} -> {}'.format(resource_field, Pattern(resource_field)))
    assert (Pattern(resource_field) == '(\d{4}-\d{2}-\d{2})([T ]?)(\d{2}:\d{2}:\d{2})?(\.\d+)?(Z|([+-]\d{2}:\d{2}))?')
    assert (not re.match(Pattern(resource_field), 'a'))
    assert (re.match(Pattern(resource_field), '2024-06-23'))
    assert (re.match(Pattern(resource_field), '2024-06-23 18:30:00'))


class Min(int):
    def __new__(cls, resource_field):
        # resource_field is {'api_admin': 'R', 'api_guest': 'CR', 'api_user': 'RUD', 'encrypt': 'N', 'field': 'id', 'pattern': '^.{3,330}$', 'resource': 'account','size': '3-330', 'type': 'C', 'validate': 'R'}
        contents = ''
        if 'type' in resource_field:
            if resource_field['type'] == 'C':
                # contents = '^<<TYPE>>{<<MIN>>,<<MAX>>}$'
                min = resource_field['size'].split('-')[0]
                contents = int(min)
            elif resource_field['type'] == 'L':
                # contents = '(True|False|Y|N|T|F|1|0)'
                contents = 1
            elif resource_field['type'] == 'I':
                # contents = '-?\d{<<MIN>>,<<MAX>>}'
                contents = 1
            elif resource_field['type'] == 'N':
                # contents = '-?\d{1,<<W>>}(\.\d{1,<<D>>})?'  # .replace('<<W>',w).replace('<<D>>',d) # eg
                contents = 1
            elif resource_field['type'] == 'D':
                # contents = '(\d{4}-\d{2}-\d{2})([T ]?)(\d{2}:\d{2}:\d{2})?(\.\d+)?(Z|([+-]\d{2}:\d{2}))?'
                contents = 8
        instance = super().__new__(cls, contents)
        return instance


def test_min():
    resource_field = {'size': '3-330', 'type': 'C'}
    print('        characer min:', Min(resource_field))
    assert (Min(resource_field) == 3)

    resource_field = {'size': '1-14', 'type': 'I'}
    print('         integer min:', Min(resource_field))
    assert (Min(resource_field) == 1)

    resource_field = {'size': '14,6', 'type': 'N'}
    print('          number min:', Min(resource_field))
    assert (Min(resource_field) == 1)

    resource_field = {'size': '8-19', 'type': 'D'}
    print('            date min:', Min(resource_field))
    assert (Min(resource_field) == 8)


class Max(int):
    def __new__(cls, resource_field):
        # resource_field is {'api_admin': 'R', 'api_guest': 'CR', 'api_user': 'RUD', 'encrypt': 'N', 'field': 'id', 'pattern': '^.{3,330}$', 'resource': 'account','size': '3-330', 'type': 'C', 'validate': 'R'}
        contents = ''
        if 'type' in resource_field:
            if resource_field['type'] == 'C':
                # contents = '^<<TYPE>>{<<MIN>>,<<MAX>>}$'
                max = resource_field['size'].split('-')[1]
                contents = int(max)
            elif resource_field['type'] == 'L':
                # contents = '(True|False|Y|N|T|F|1|0)'
                contents = 5
            elif resource_field['type'] == 'I':
                # contents = '-?\d{<<MIN>>,<<MAX>>}'
                max = int(resource_field['size'].split('-')[1])
                contents = max
            elif resource_field['type'] == 'N':
                # contents = '-?\d{1,<<W>>}(\.\d{1,<<D>>})?'  # .replace('<<W>',w).replace('<<D>>',d) # eg
                max = int(resource_field['size'].split(',')[0])
                contents = int(max)
            elif resource_field['type'] == 'D':
                # contents = '(\d{4}-\d{2}-\d{2})([T ]?)(\d{2}:\d{2}:\d{2})?(\.\d+)?(Z|([+-]\d{2}:\d{2}))?'
                contents = 19
        instance = super().__new__(cls, contents)
        return instance


def test_max():
    resource_field = {'size': '3-330', 'type': 'C'}
    print('        characer min:', Max(resource_field))
    assert (Max(resource_field) == 330)

    resource_field = {'size': '1-14', 'type': 'I'}
    print('         integer min:', Max(resource_field))
    assert (Max(resource_field) == 14)

    resource_field = {'size': '14,6', 'type': 'N'}
    print('          number min:', Max(resource_field))
    assert (Max(resource_field) == 14)

    resource_field = {'size': '8-19', 'type': 'D'}
    print('            date min:', Max(resource_field))
    assert (Max(resource_field) == 19)


class ResourcePatterns(dict):
    def __init__(self, project_dict, resource_name):
        resource_list = project_dict['project']['resources']

        if resource_name:
            resource_list = {r: resource_list[r] for r in resource_list if r == resource_name}
        for r in project_dict['project']['resources']:
            # {account: {}, ...}
            self[r] = {}
            for m in project_dict['project']['resources'][r]['model']:
                for row in project_dict['project']['resources'][r]['model']['rows']:

                    for fld in row:
                        if fld == 'field':
                            # {account: {id: {}, ...}, ...}
                            self[r][row[fld]] = {}
                            # fld_key= fld

                        # {account: {id: {pattern: ^.{3,330}$, ... }, ...}, ...}
                        self[r][row['field']]['pattern'] = Pattern(row)


def test_resource_patterns():
    actual = ResourcePatterns(DictMd(getProjectMDString()), 'account')
    print('   resource_patterns:', actual)
    assert ('account' in actual)
    assert ('id' in actual['account'])
    assert ('pattern' in actual['account']['id'])


class RouteConstantsJS(str):
    def __new__(cls, project_dict):
        resource_list = project_dict['project']['resources']
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
    route_constants = RouteConstantsJS(DictMd(getProjectMDString()))
    route_constants = ['                      {}'.format(x) for x in route_constants.split('\n')]
    print('  route_constants_js:', '\n'.join(route_constants).strip())
    assert (
                "                      const account_route_post = require('../route/__routes__/account_route_post.js');" in route_constants)
    assert (
                "                      const account_route_delete = require('../route/__routes__/account_route_delete.js');" in route_constants)


class ApiRoutes(str):
    def __new__(cls, project_dict):
        resource_list = project_dict['project']['resources']
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
        resource_list = project_dict['project']['resources']
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
    api_routes = ApiRoutes(DictMd(getProjectMDString()))
    api_routes = ['                    {}'.format(x) for x in api_routes.split('\n')]
    print('          api_routes:', '\n'.join(api_routes).strip())
    print()
    assert ('                    server.route(account_route_post);' in api_routes)
    assert ('                    server.route(account_route_delete);' in api_routes)


'''
class NVEnv(NVList):
    def __init__(self, env_list):

        for nv in [{'name': '<<{}>>'.format(nv['name']), 'value': nv['value']} for nv in env_list]:
            self.append(nv)

def test_nv_env():
    actual = NVEnv(ListEnv(getEnvString()))
    print('              nv_env:', actual)
    assert ({'name': '<<GH_TRUNK>>', 'value': 'main'} in actual)
    assert ({'name': '<<GH_BRANCH>>', 'value': 'first'} in actual)
    assert ({'name': '<<GH_USER>>', 'value': 'wilfongjt'} in actual)
    assert ({'name': '<<GH_MESSAGE>>', 'value': 'init'} in actual)
'''


class NVField(NVList):  # name value field
    # NV an individual resource field
    # apply to a template
    def __init__(self, project_dict, resource_name, field_name):
        if resource_name not in project_dict['project']['resources']:
            raise Exception('Resource Name Not Found: {}'.format(resource_name))
        row_dict = {row['field']: row for row in project_dict['project']['resources'][resource_name]['model']['rows']}
        if field_name not in row_dict:
            raise Exception('Resource Field Name Not Found: {}'.format(field_name))

        # rc = [{'name': '<<{}_{}>>'.format(field_name.upper(), fld.upper()), 'value': row_dict[field_name][fld] } for fld in row_dict[field_name]]
        # for x in rc: self.add(x)
        # print('NVField resource', resource_name)
        # pprint([{'name': '<<{}_{}>>'.format(field_name.upper(), fld.upper()), 'value': row_dict[field_name][fld], 'resource': resource_name } for fld in row_dict[field_name]])

        self.extend([{'name': '<<{}_{}>>'.format(field_name.upper(), fld.upper()), 'value': row_dict[field_name][fld],
                      'resource': resource_name} for fld in row_dict[field_name]]
                    )


def test_nv_field():
    actual = NVField(DictMd(getProjectMDString()), 'account', 'id')
    print('            nv_field:', actual)
    assert ({'name': '<<ID_FIELD>>', 'value': 'id', 'resource': 'account'} in actual)
    assert ({'name': '<<ID_MIN>>', 'value': 3, 'resource': 'account'} in actual)
    assert ({'name': '<<ID_MAX>>', 'value': 330, 'resource': 'account'} in actual)
    assert ({'name': '<<ID_RESOURCE>>', 'value': 'account', 'resource': 'account'} in actual)
    assert ({'name': '<<ID_PATTERN>>', 'value': '^.{3,330}$', 'resource': 'account'} in actual)

    actual = NVField(DictMd(getProjectMDString()), 'account', 'owner')
    print('            nv_field:', actual)
    assert ({'name': '<<OWNER_FIELD>>', 'value': 'owner', 'resource': 'account'} in actual)
    assert ({'name': '<<OWNER_MIN>>', 'value': 3, 'resource': 'account'} in actual)
    assert ({'name': '<<OWNER_MAX>>', 'value': 330, 'resource': 'account'} in actual)
    assert ({'name': '<<OWNER_RESOURCE>>', 'value': 'account', 'resource': 'account'} in actual)
    assert ({'name': '<<OWNER_PATTERN>>', 'value': '^.{3,330}$', 'resource': 'account'} in actual)


class NVResourceFields(NVList):
    # NV all resource fields
    # apply to a template
    def __init__(self, project_dict, resource_name):
        # upsert = True
        # print('B resource_name', resource_name)
        if resource_name not in project_dict['project']['resources']:
            raise Exception('Resource Name Not Found: {}'.format(resource_name))
        for row in project_dict['project']['resources'][resource_name]['model']['rows']:
            # print('NVResourceFields', resource_name)
            self.extend(NVField(project_dict, resource_name, row['field']))


def test_nv_resource_fields():
    actual = NVResourceFields(DictMd(getProjectMDString()), 'account')
    print('  nv_resource_fields:', actual)
    # pprint(actual)
    assert ({'name': '<<ID_FIELD>>', 'value': 'id', 'resource': 'account'} in actual)
    assert ({'name': '<<ID_MIN>>', 'value': 3, 'resource': 'account'} in actual)
    assert ({'name': '<<ID_MAX>>', 'value': 330, 'resource': 'account'} in actual)
    assert ({'name': '<<ID_RESOURCE>>', 'value': 'account', 'resource': 'account'} in actual)
    assert ({'name': '<<ID_PATTERN>>', 'value': '^.{3,330}$', 'resource': 'account'} in actual)
    assert ({'name': '<<OWNER_FIELD>>', 'value': 'owner', 'resource': 'account'} in actual)
    assert ({'name': '<<OWNER_MIN>>', 'value': 3, 'resource': 'account'} in actual)
    assert ({'name': '<<OWNER_MAX>>', 'value': 330, 'resource': 'account'} in actual)
    assert ({'name': '<<OWNER_RESOURCE>>', 'value': 'account', 'resource': 'account'} in actual)
    assert ({'name': '<<OWNER_PATTERN>>', 'value': '^.{3,330}$', 'resource': 'account'} in actual)


class NVResource(NVList):  # name value resource
    # NV a resource_name
    # apply to a template
    def __init__(self, project_dict, resource_name):
        if resource_name not in project_dict['project']['resources']:
            # print('project_dict', project_dict['project']['resources'])
            raise Exception('Resource Name Not Found: {}'.format(resource_name))
        self.add({'name': '<<API_RESOURCE>>', 'value': resource_name})
        # print('NVResource', resource_name)
        self.extend(NVResourceFields(project_dict, resource_name))


def test_nv_resource():
    actual = NVResource(DictMd(getProjectMDString()), 'account')
    print('         nv_resource:', actual)
    assert ({'name': '<<API_RESOURCE>>', 'value': 'account'} in actual)
    assert ({'name': '<<ID_FIELD>>', 'value': 'id', 'resource': 'account'} in actual)
    assert ({'name': '<<ID_MIN>>', 'value': 3, 'resource': 'account'} in actual)
    assert ({'name': '<<ID_MAX>>', 'value': 330, 'resource': 'account'} in actual)
    assert ({'name': '<<ID_RESOURCE>>', 'value': 'account', 'resource': 'account'} in actual)
    assert ({'name': '<<ID_PATTERN>>', 'value': '^.{3,330}$', 'resource': 'account'} in actual)
    assert ({'name': '<<OWNER_FIELD>>', 'value': 'owner', 'resource': 'account'} in actual)
    assert ({'name': '<<OWNER_MIN>>', 'value': 3, 'resource': 'account'} in actual)
    assert ({'name': '<<OWNER_MAX>>', 'value': 330, 'resource': 'account'} in actual)
    assert ({'name': '<<OWNER_RESOURCE>>', 'value': 'account', 'resource': 'account'} in actual)
    assert ({'name': '<<OWNER_PATTERN>>', 'value': '^.{3,330}$', 'resource': 'account'} in actual)

    actual = NVResource(DictMd(getProjectMDString()), 'sample_resource')
    print('         nv_resource:', actual)
    assert ({'name': '<<API_RESOURCE>>', 'value': 'sample_resource'} in actual)
    assert ({'name': '<<ID_FIELD>>', 'value': 'id', 'resource': 'sample_resource'} in actual)
    assert ({'name': '<<ID_MIN>>', 'value': 3, 'resource': 'sample_resource'} in actual)
    assert ({'name': '<<ID_MAX>>', 'value': 330, 'resource': 'sample_resource'} in actual)
    assert ({'name': '<<ID_RESOURCE>>', 'value': 'sample_resource', 'resource': 'sample_resource'} in actual)
    assert ({'name': '<<ID_PATTERN>>', 'value': '^.{3,330}$', 'resource': 'sample_resource'} in actual)
    assert ({'name': '<<OWNER_FIELD>>', 'value': 'owner', 'resource': 'sample_resource'} in actual)
    assert ({'name': '<<OWNER_MIN>>', 'value': 3, 'resource': 'sample_resource'} in actual)
    assert ({'name': '<<OWNER_MAX>>', 'value': 330, 'resource': 'sample_resource'} in actual)
    assert ({'name': '<<OWNER_RESOURCE>>', 'value': 'sample_resource', 'resource': 'sample_resource'} in actual)
    assert ({'name': '<<OWNER_PATTERN>>', 'value': '^.{3,330}$', 'resource': 'sample_resource'} in actual)


# Task

class TaskInitializeEnv(ProcessProject):
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


class TaskConfigure(ProcessProject):
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


class TaskInitializeProjecMd(ProcessProject):
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
            '{}. TaskInitializeProjecMd {}'.format(self.no, self.get_application().get_name())).runtime().terminal()

        self.initialize_project_md()

        return self


class TaskGithub(ProcessProject):
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


class TaskGithubPatch(ProcessProject):
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


class TaskInitializeProjectSpace(ProcessProject):
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


class TaskInitializeDocker(ProcessProject):
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


class TaskInitializeHeroku(ProcessProject):
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


class TaskInitializeNode(ProcessProject):
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


class TaskInitializeJWT(ProcessProject):
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


class TaskInitializeNodemon(ProcessProject):
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


class TaskInitializeHapi(ProcessProject):
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
        self.get_application().add('hapi')
        ##* Templatize Hapi templates in '/template/hapi'
        nv_list = self.get_template_key_list()
        filename_md = TemplateString('project_<<WS_PROJECT>>.md', nv_list)
        folderfilename_md = '{}/{}'.format(os.getcwd(), filename_md)
        print('folderfilename_md', folderfilename_md)
        resource_string = StringReader(folderfilename_md)
        project_dict = DictMd(resource_string)
        nv_list.append({'name': '<<ROUTE_CONST>>', 'value': RouteConstantsJS(project_dict)})
        nv_list.append({'name': '<<API_ROUTES>>', 'value': ApiRoutes(project_dict)})

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
# merge server_ext with <<API_ROUTES>> TaskMergeHapiServerRouteNames
# merge server_ext with <<ROUTE_CONST>> TaskMergeHapiServerRouteNames
# intialize routes_*.js files TaskInitializeHapiRoutes

class TaskInitializeHapiRoutes(ProcessProject):
    ##
    #### TaskInitializeHapiRoutes
    ##
    ##* generate hapi route defintions into 'lib/route/__routes__'
    ##* direct dependent on /bin/project_??.md
    ##* indirect dependency on /bin/md2.env

    def __init__(self, no=0):
        ProcessProject.__init__(self)
        self.set_template_folder_key('hapi_routes')
        self.no = no

    def route_templates(self):
        # handle generated routes for each resource
        # open 'bin/<project>.md' (by default, <project>.md enables the ACCOUNT resource)

        # create a nv_list for <<API_ROUTES>> and <<ROUTE_CONST>>, eg [{name: '', value: ''},...]

        # make template list for each resource (route_post,route_get, route_put, route_delete)
        # remove routes not defined in the <project>.md
        # apply nv_list to each template
        # save to /<project>/lib/__routes__

        nv_list = self.get_template_key_list()
        filename_md = TemplateString('project_<<WS_PROJECT>>.md', nv_list)
        folderfilename_md = '{}/{}'.format(os.getcwd(), filename_md)
        resource_string = StringReader(folderfilename_md)
        project_dict = DictMd(resource_string)

        for resource_name in ResourceNames(project_dict):
            nv_list = self.get_template_key_list()  # reset nv_list
            nv_list.extend(NVResource(project_dict, resource_name))  # add field attributes

            self.templatize(nv_list=nv_list)

        return self

    def process(self):
        print('TaskInitializeHapiRoutes process')
        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('{}. TaskInitializeHapiRoutes: {}'.format(self.no, repo_name)).runtime().terminal()

        self.route_templates()

        return self


class TaskInitializePostgres(ProcessProject):
    ##
    ###### Initialize Postgres
    ##

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


class TaskInitializeModel(ProcessProject):
    ##
    ###### Initialize Model
    ##

    def __init__(self, no=0):
        ProcessProject.__init__(self)
        self.set_template_folder_key('model')
        self.no = no

    def db_deploy_templates(self):
        if not self.get_application():
            raise Exception('Application Not Found!')
        self.get_application().add(self.get_template_folder_key())
        ##* Templatize DB Deploy templates
        self.templatize()
        return self

    def process(self):
        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('{}. Model: {}'.format(self.no, repo_name)).runtime().terminal()

        self.db_deploy_templates()

        return self


class TaskUpdateEnvironment(ProcessProject):
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
    ## Launch/run task
    def __init__(self, process):
        process.run()


##<hr/>
##
#### Parent Classes


if __name__ == "__main__":
    # execute as docker
    test = False
    if test:
        print('Testing...')
        test_dict_md()

        test_project_name()
        test_resource_names()
        test_role_names()
        # test_resource_permissions()
        # test_resource_fields()
        # dep test_resource_field_sizes()
        test_pattern()
        test_resource_patterns()
        test_route_constants_js()
        test_api_routes()
        test_min()
        test_max()
        test_list_env()
        # test_nv_env()
        # test_nv_field()
        # test_nv_resource_fields()
        test_nv_resource()

        print('Testing Complete')
    if not test:
        main()
