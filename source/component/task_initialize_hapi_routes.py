import os
from source.component.process_project import ProcessProject
from able import TemplateString, StringReader
from source.component.tier import Tier
from source.component.multilogger import MultiLogger
from source.component.markdown.helper.resource_names import ResourceNames


class Task_InitializeHapiRoutes(ProcessProject):
    ##
    #### Task_InitializeHapiRoutes
    ##
    ##* generate hapi route defintions into 'lib/route/__routes__'
    ##* direct dependent on /bin/project_??.md
    ##* indirect dependency on /bin/md2.env

    def __init__(self, no=0):
        ProcessProject.__init__(self)
        self.set_template_folder_key('hapi_routes')
        self.no = no
    #def get_template_key_list(self):
    #    ##* __get_template_key_list__, list of template formated env vars, eg. [{\<\<GH_A>>:'abc'}, ...]
    #    nv_list = super.get_template_key_list()
    #    nv_list = self.get_template_key_list()
    #    project_dict
    #    return nv_list.extend(NVResourceSchemaVersion(project_dict, resource_name))
        #return [{'name': '<<{}>>'.format(itm['name']),
        #                    'value': itm['value']}
        #                    for itm in NameValuePairs(multi_line_string=EnvVarString())]
    def get_project_dictionary(self, nv_list):
        filename_md = TemplateString('project_<<WS_PROJECT>>.md', nv_list)
        folderfilename_md = '{}/{}'.format(os.getcwd(), filename_md)
        resource_string = StringReader(folderfilename_md)
        project_dict = Tier(resource_string)
        return project_dict

    def route_templates(self):
        # handle generated routes for each resource
        # open 'bin/<project>.md' (by default, <project>.md enables the ACCOUNT resource)

        # create a nv_list for <<API_ROUTES>> and <<ROUTE_CONST>>, eg [{name: '', value: ''},...]

        # make template list for each resource (route_post,route_get, route_put, route_delete)
        # remove routes not defined in the <project>.md
        # apply nv_list to each template
        # save to /<project>/lib/__routes__

        nv_list = self.get_template_key_list() # replacement keys and values
        print('nv_list',nv_list)
        #filename_md = TemplateString('project_<<WS_PROJECT>>.md', nv_list)
        #folderfilename_md = '{}/{}'.format(os.getcwd(), filename_md)
        #resource_string = StringReader(folderfilename_md)
        #project_dict = Tier(resource_string)
        project_dict = self.get_project_dictionary(nv_list)
        print('project_dict', project_dict)
        #pprint(project_dict)
        for resource_name in ResourceNames(project_dict):
            nv_list = self.get_template_key_list()  # reset nv_list
            nv_list.extend(NVResource(project_dict, resource_name))  # add field attributes
            print('route nv_list', nv_list)
            #print('resource name', resource_name)
            #print('resource', project_dict['project']['resource'][resource_name])
            active = True
            if 'active' in project_dict['project']['resource'][resource_name]: # active:
                if project_dict['project']['resource'][resource_name]['active'].lower() not in ['y', 'yes', 't', 'true']:
                    active = False

            schema = 'api'
            if 'schema' in project_dict['project']['resource'][resource_name]: # schema:
                schema = project_dict['project']['resource'][resource_name]['schema']
            version = '0.0.1'
            if 'version' in project_dict['project']['resource'][resource_name]:  # schema:
                version = project_dict['project']['resource'][resource_name]['version']

            #nv_list.append({'name': '<<API_SCHEMA>>', 'value':'{}_{}'.format(schema, version.replace('.','_')) })

            nv_list.extend(NVResourceSchemaVersion(project_dict, resource_name))
            # print('nv_list', nv_list)
            # Route Scopes
            nv_list.extend(NVResourceMethodScopes(project_dict, resource_name))
            #nv_list.append({'name': '<<DELETE_SCOPE>>', 'value': RouteScopes(project_dict, resource_name, 'DELETE')})
            #nv_list.append({'name': '<<GET_SCOPE>>', 'value': RouteScopes(project_dict, resource_name, 'GET')})
            #nv_list.append({'name': '<<POST_SCOPE>>', 'value': RouteScopes(project_dict, resource_name, 'POST')})
            #nv_list.append({'name': '<<PUT_SCOPE>>', 'value': RouteScopes(project_dict, resource_name, 'PUT')})
            print('pre tmpl nv_list', nv_list)
            self.templatize(nv_list=nv_list, active_resource=active) # templateize will remove resource when active is set to true

            #if 'active' not in project_dict['project']['resource'][resource_name]:
            #    # default to active = yes
            #    self.templatize(nv_list=nv_list)
            #else:
            #    if project_dict['project']['resource'][resource_name]['active'].lower() in ['y', 'yes','t', 'true']:
            #        self.templatize(nv_list=nv_list)
            #    else:
            #        print('figure out delete resource')

        return self

    def process(self):
        print('Task_InitializeHapiRoutes process')
        repo_name = os.environ['GH_REPO']
        MultiLogger().set_msg('{}. Task_InitializeHapiRoutes: {}'.format(self.no, repo_name)).runtime().terminal()

        self.route_templates()

        return self

def task_initialize_hapi_routes(status):
    status.addTitle('Task_InitializeHapiRoutes test')
    actual = Task_InitializeHapiRoutes()

    status.assert_test("Task_InitializeHapiRoutes()=={}", actual == {})


def main(status):
    task_initialize_hapi_routes(status)

if __name__ == "__main__":
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))
