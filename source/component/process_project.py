import os
from pprint import pprint
from source.component import ProcessPackage, MultiLogger, Permissions
from source.component.markdown.tier_md import TierMD

from source.component.markdown.project_string_default import ProjectStringDefault
from source.component.status import Status

# from source.component.project_string import ProjectStringDefault
from able import TemplateString, \
                 EnvVarString, \
                 NameValuePairs, \
    StringWriter, \
                 TemplateList_Latest,\
                 StringReader, \
    Inputable, \
                 UpdaterString


class ProcessProject(ProcessPackage):
    ##
    ##### Process Project
    ##
    ## Base class for project_dict methods

    def __init__(self):

        #def __init__(self, template_folder_key, application=None):
        ProcessPackage.__init__(self)
        ##* optional recorder
        # convert recorder to application
        self.application = None # application
        ##* template_folder_key, eg 'github'
        self.template_folder_key = None # template_folder_key # eg 'github'

        self.e_var = []
        self.status = None

    def getStatus(self):
        #if not self.status:
        #    print('init status')
        #    self.status = Status()
        return self.status

    def setStatus(self, status):
        self.status = status
        return self

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

    def get_project_dictionary(self):
        # set resource_string to default
        resource_string = ProjectStringDefault()
        nv_list = self.get_template_key_list()
        # attempt to open project_dict
        filename_md = TemplateString('project_<<WS_PROJECT>>.md', nv_list)
        if '<<' not in filename_md:
            folderfilename_md = '{}/{}'.format(os.getcwd(), filename_md)
            resource_string = StringReader(folderfilename_md)
        #else:
        #    print('**** ProjectStringDefault is set to Default...use for testing ****')
        project_dict = TierMD(resource_string)

        return project_dict

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
    '''
    def templatize_a(self, body_text, crud, nv_list):
        operations = ''

        if 'd' in crud or 'D' in crud:  # delete target
            operations += 'D'
            if os.path.exists(repo_folderfile):
                # print('D ', repo_folderfile)
                os.remove(repo_folderfile)
        else:
            operations += '-'

        if 'c' in crud or 'C' in crud:  # create from template
            # print('templatize 2.3 create', repo_folderfile)

            # if not os.path.exists(repo_folderfile):
            operations += 'C'

            if not os.path.exists(TemplateString(repo_folderfile, nv_list)):
                # print('templatize 2.3.1')

                # template_content = StringReader(template_folderfile)
                template_content = TemplateString(StringReader(template_folderfile), nv_list)
                # print('write', repo_folderfile)
                # print('write', template_content)
                if active_resource:  # active: Y or N
                    # print('templatize 2.3 create', repo_folderfile)
                    # print('C ', repo_folderfile)
                    StringWriter(TemplateString(repo_folderfile, nv_list), template_content)
                # else:
                #    print(TemplateString('  Inactive Resource <<API_RESOURCE>>',nv_list))
                # StringWriter(repo_folderfile, template_content)
        else:
            operations += '-'

        if 'r' in crud or 'R' in crud:  # read from target
            # print('templatize 2.4')
            operations += 'R'
            print('repo_folderfile', repo_folderfile)
            print('repo_folderfile exits', os.path.exists(repo_folderfile))
            print('repo_folderfile', StringReader(repo_folderfile))
            print('A .env     exits', os.path.exists(
                '/Users/jameswilfong/Development/test_org/test_ws/test_prj/first/py_test/.env'))
            print('B .env          ', StringReader(
                '/Users/jameswilfong/Development/test_org/test_ws/test_prj/first/py_test/.env').replace('\n', '|'))

            print('README.md     exits',
                  os.path.exists('/Users/jameswilfong/Development/test_org/test_ws/test_prj/first/py_test/README.md'))
            print('README.md          ',
                  StringReader('/Users/jameswilfong/Development/test_org/test_ws/test_prj/first/py_test/README.md'))

            target_content = TemplateString(StringReader(repo_folderfile), nv_list)
            print('target_content', target_content, repo_folderfile)
            template_content = TemplateString(StringReader(template_folderfile), nv_list)
            print('template_content', template_content)
            if target_content:
                print('  R target_content  ', target_content.replace('\n', '|'))
            if template_content:
                print('  R template_content', template_content.replace('\n', '|'))

        else:
            operations += '-'

        if 'u' in crud or 'U' in crud:  # update
            # print('templatize 2.5')
            operations += 'U'
            print('U', StringReader(repo_folderfile))
            # read template
            # read target
            tmp = UpdaterString(target_content).updates(template_content)
            ## print('file {} nv-list {}'.format(repo_folderfile,nv_list), nv_list)
            if repo_folderfile.endswith('.env'):
                # print('  U repo_folderfile ',repo_folderfile)
                # print('  U target_content  ', target_content.replace('\n','|'))
                # print('  U template_content', template_content.replace('\n','|'))
                print('  U tmp             ', tmp.replace('\n', '|'))
            # here StringWriter(repo_folderfile, TemplateString(tmp, nv_list))
            ## print('tmp', tmp)
        else:
            operations += '-'

        return body_text
    '''
    def templatize(self, nv_list=None, output_folder=None, active_resource=True, verbose=False):
        ##* __templatize__ convert templates to code
        ##* generate templates
        # C - Create out-file when it doesn't exist
        # R - Read contents of out-file when it exists
        # U - Update contents of out-file when it exists
        # D - Delete out-file when it exits

        # print('templatize 1')
        template_folder = self.get_template_folder()
        self.getStatus().addLine('Templatize {}'.format(template_folder.split('/')[-1].upper()))

        # #* Convert Templates to Code

        # get list of templates i.e., files ending in .tmpl
        template_list = TemplateList_Latest(folder_path=template_folder)

        # make list of template-keys and values ... {key: value, key: value, ...}
        if not nv_list: nv_list = self.get_template_key_list() # self.get_template_name_value_pairs()

        # process list of specific templates
        #print('nv_list', nv_list)
        for tmplt in template_list:
            #print('templatize 2 tmplt', tmplt)
            # ??
            if self.get_application(): self.get_application().add('templatize')

            # handle multiple templates of the same name
            for template_folderfile in template_list[tmplt]['template']:
                # print('templatize 2.1')
                operations = ''
                # make input and output file names
                if not output_folder:
                    output_subfolder = template_list[tmplt]['output_subfolder']
                    repo_folderfile = '{}/{}'.format(self.get_repo_folder(), output_subfolder)
                    repo_folderfile = repo_folderfile.replace('root/', '')
                    fld = repo_folderfile.split('/')[-2]
                    fn = repo_folderfile.split('/')[-1]
                    self.getStatus().addBullet('{}/{} -> {}'.format(fld, fn, output_subfolder))
                else:
                    #repo_folderfile = output_folder
                    repo_folderfile = '{}/{}'.format(output_folder, template_list[tmplt]['output_subfolder'])
                    fld = repo_folderfile.split('/')[-2]
                    fn = repo_folderfile.split('/')[-1]
                    self.getStatus().addBullet('{}/{}'.format(fld, fn))
                # make the command string e.g., whatever.js.CRUD.tmpl -> CRUD
                cmd = str(template_folderfile).split('/')[-1].split('.')[-2]

                # make templatized-content from template
                #new_content = TemplateString(StringReader(template_folderfile), nv_list)
                target_content = ''
                template_content = ''
                # make target-file from templatized-content
                self.makedirs(repo_folderfile) # make output folder
                # make the template folder e.g., /template/__project__ -> /template
                template_name = '/'.join(self.get_template_folder().split('/')[0:-1])
                # print('template_name',template_name)
                MultiLogger().set_msg('   template({}) -> actual({})'.format(str(template_folderfile).replace(template_name,''), repo_folderfile.replace(self.get_branch_folder(),''))).runtime()
                # make the target folder in the new repo
                #print('repo_folderfile',repo_folderfile.split('\n'))
                #print('nv_list',nv_list)
                #print('-----A')
                #pprint(nv_list)
                #print('-----B')
                #for ln in str(repo_folderfile).split('\n'):
                #    for nv in nv_list:
                #        print('nv', nv)
                #        if nv['name'] in ln:
                #            ln = ln.replace(nv['name'], '{}'.format(nv['value']))
                if '<<' in repo_folderfile:
                    #print('A repo_folderfile',repo_folderfile)
                    #nv_list.extend(NVResource(project_dict,)) do this befor call to templatize
                    #pprint(nv_list)
                    #print('A repo_folderfile',repo_folderfile)

                    repo_folderfile = TemplateString(repo_folderfile, nv_list)
                    #print('B repo_folderfile',repo_folderfile)
                #print('template_folderfile     ',template_folderfile.split('/')[-1],template_folderfile)
                #print('repo_folderfile         ', repo_folderfile.split('/')[-1] ,repo_folderfile)
                #print('repo_folderfile exits   ', repo_folderfile.split('/')[-1], os.path.exists(repo_folderfile))
                #print('repo_folderfile contents', repo_folderfile.split('/')[-1], StringReader(str(repo_folderfile)).replace('\n','|'))

                #if os.path.exists(repo_folderfile):
                #    print('  exists')
                if '.env' in repo_folderfile:
                    if verbose: print('found .env')

                if 'd' in cmd or 'D' in cmd:  # delete target
                    operations += 'D'
                    if os.path.exists(repo_folderfile):
                        if verbose: print('  D ', repo_folderfile)

                        os.remove(repo_folderfile)
                else:
                    operations += '-'

                if 'c' in cmd or 'C' in cmd:  # create from template
                    # print('templatize 2.3 create', repo_folderfile)

                    #if not os.path.exists(repo_folderfile):
                    operations += 'C'

                    if not os.path.exists(TemplateString(repo_folderfile, nv_list)):
                        # print('templatize 2.3.1')

                        #template_content = StringReader(template_folderfile)
                        template_content = TemplateString(StringReader([template_folderfile]), nv_list)
                        # print('write', repo_folderfile)
                        # print('write', template_content)
                        if active_resource: # active: Y or N
                            #print('templatize 2.3 create', repo_folderfile)
                            #print('C ', repo_folderfile)
                            if verbose: print('  C ', repo_folderfile.split('/')[-1],template_content.replace('\n','|'))
                            StringWriter(TemplateString(repo_folderfile, nv_list), template_content)
                        #else:
                        #    print(TemplateString('  Inactive Resource <<API_RESOURCE>>',nv_list))
                        #StringWriter(repo_folderfile, template_content)
                else:
                    operations += '-'

                if 'r' in cmd or 'R' in cmd:  # read from target
                    # print('templatize 2.4')
                    operations += 'R'

                    #print('A .env     exits', os.path.exists(
                    #    '/Users/jameswilfong/Development/test_org/test_ws/test_prj/first/py_test/.env'))
                    #print('B .env          ', StringReader(
                    #    '/Users/jameswilfong/Development/test_org/test_ws/test_prj/first/py_test/.env').replace('\n','|'))

                    #print('README.md     exits',os.path.exists('/Users/jameswilfong/Development/test_org/test_ws/test_prj/first/py_test/README.md'))
                    #print('README.md          ',StringReader('/Users/jameswilfong/Development/test_org/test_ws/test_prj/first/py_test/README.md'))

                    target_content = TemplateString(StringReader(str(repo_folderfile)), nv_list)
                    template_content = TemplateString(StringReader([template_folderfile]), nv_list)
                    if template_content:
                        if verbose: print('  R template_content', template_content.replace('\n','|'))

                    if target_content:
                        if verbose: print('  R target_content  ', target_content.replace('\n','|'))

                else:
                    operations += '-'

                if 'u' in cmd or 'U' in cmd:  # update
                    # print('templatize 2.5')
                    operations += 'U'
                    #print('  U', StringReader(repo_folderfile))
                    # read template
                    # read target
                    tmp = UpdaterString(target_content).updates(template_content)
                    ## print('file {} nv-list {}'.format(repo_folderfile,nv_list), nv_list)
                    if repo_folderfile.endswith('.env'):
                        #print('  U repo_folderfile ',repo_folderfile)
                        #print('  U target_content  ', target_content.replace('\n','|'))
                        #print('  U template_content', template_content.replace('\n','|'))
                        if verbose: print('  U write contents  ', tmp.replace('\n','|'))

                    StringWriter(repo_folderfile, TemplateString(tmp, nv_list))

                    ## print('tmp', tmp)
                else:
                    operations += '-'

                if repo_folderfile.endswith('.sh'):
                    # make file runable
                    # Change the mode of path
                    Permissions(repo_folderfile, verbose=False)
            #print('---')
            #print('  operations', operations, repo_folderfile.split('/')[-1])

        #import subprocess

        #subprocess.run(["ls", "-l"])
        # print('templatize out')
        #if repo_folderfile.endswith('.env'):
        #    print('  operations', operations, repo_folderfile)

        #print('  operations', operations, repo_folderfile.split('/')[-1])

        return self

    def process(self):
        print('Hi process')
        return self

    def run(self):
        return self.process()
'''
class Templatize(TemplateString):

    def __init__(self, template_folder_file, nv_list):
        TemplateString.__init__(StringReader(template_folder_file), nv_list=nv_list)

        #self.template_folder_file=template_folder_file
        self.nv_list=nv_list
        # make the command string e.g., /whatever.js.CRUD.tmpl -> CRUD
        self.crud = str(template_folder_file).split('/')[-1].split('.')[-2]
        # make the repo file namne e.g., /whatever.js.CRUD.tmpl -> whatever.js
        self.repo_folder_file = str(template_folder_file).split('.')[0:-2]
        print('repo_folder_file', self.repo_folder_file)

        #self.repo_folder_file = ''
    def get_template_key_list(self):
        return self.nv_list

    def get_repo_folder(self):
        ##* __get_repo_folder__, location of github repo
        #nv_list = self.get_template_name_value_pairs()
        return TemplateString(
            '{}/Development/<<WS_ORGANIZATION>>/<<WS_WORKSPACE>>/<<WS_PROJECT>>/<<GH_BRANCH>>/<<GH_REPO>>'.format(
                os.environ['HOME']), nv_list=self.get_template_key_list())
    def exists(self):
        return os.path.exists(self.repo_folder_file)

def test_templatize():
    tmpl_folder_file = '{}/temp/tmplfile.env.cru-.tmpl'.format(os.getcwd())
    nv_list = {}
    print('cwd', tmpl_folder_file)

    actual = Templatize(tmpl_folder_file, nv_list)

    if os.path.exists(tmpl_folder_file):
        os.remove(tmpl_folder_file)
'''
def process_project_test(status):
    status.addTitle('Process Project test')
    os.environ['GH_TEST'] = 'TEST'
    #print ('ProcessProject',ProcessProject('github', recorder=Recorder()))
    #print('ProcessProject', ProcessProject().set_application('github').get_application() )
    #assert (ProcessProject().set_application('github').get_application() == 'github')
    #assert (ProcessProject('github', application=None) == {})

    status.assert_test ("ProcessPackage().set('A', 'a')).get('A') == 'a'",ProcessProject().assign(ProcessPackage().set('A', 'a')).get('A') == 'a')

    status.assert_test ("ProcessProject().set_template_folder_key('github').get_template_folder_key() ",ProcessProject().set_template_folder_key('github').get_template_folder_key() == 'github')

    status.assert_test  ("ProcessProject().get_template_key_list()",ProcessProject().get_template_key_list() == [{'name': '<<GH_TEST>>', 'value': 'TEST'}])
    status.assert_test  ("ProcessProject().get_branch_folder()",ProcessProject().get_branch_folder() == '/Users/jameswilfong/Development/<<WS_ORGANIZATION>>/<<WS_WORKSPACE>>/<<WS_PROJECT>>/<<GH_BRANCH>>')
    status.assert_test  ("ProcessProject().get_repo_folder()",ProcessProject().get_repo_folder() == '/Users/jameswilfong/Development/<<WS_ORGANIZATION>>/<<WS_WORKSPACE>>/<<WS_PROJECT>>/<<GH_BRANCH>>/<<GH_REPO>>')

    # ProcessProject().set_env_var('GH_TEST', 'TEST').configure_environment()

    ProcessProject().setStatus(status).set_template_folder_key('__project__').templatize()

    #assert(ProcessProject().templatize_a('',{'<<A>>':'a'}) == 'A=a')

    #test_templatize()
    #print('project_dictionary')
    #pprint(ProcessProject().get_project_dictionary())
    status.assert_test  ("'project_dict' in ProcessProject().get_project_dictionary()", 'project' in ProcessProject().get_project_dictionary())
    #print('StringReader', StringReader('/Users/jameswilfong/Development/test_org/test_ws/test_prj/first/py_test/.env'))

def main(status):
    process_project_test(status)

if __name__ == "__main__":
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))