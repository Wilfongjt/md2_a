from source.component.nv_list import NVList
from source.component.markdown.helper.route_scopes import RouteScopes

class NVResourceMethodScopes(NVList):
    # NVResourceMethodScopes(project_dict, resource_name)
    def __init__(self, project_dict, project_name, resource_name):
        #print('NVResourceMethodScopes type', type(project_dict))
        #print('NVResourceMethodScopes dict',project_dict)

        if resource_name not in project_dict['project'][project_name]['resources']:
            # print('project_dict', project_dict['project']['resource'])
            raise Exception('Resource Name Not Found: {}'.format(resource_name))
        # Route Scopes
        self.add({'name': '<<DELETE_SCOPE>>', 'value': RouteScopes(project_dict, project_name, resource_name, 'DELETE')})
        self.add({'name': '<<GET_SCOPE>>', 'value': RouteScopes(project_dict, project_name, resource_name, 'GET')})
        self.add({'name': '<<POST_SCOPE>>', 'value': RouteScopes(project_dict, project_name, resource_name, 'POST')})
        self.add({'name': '<<PUT_SCOPE>>', 'value': RouteScopes(project_dict, project_name, resource_name, 'PUT')})

def test_nv_resource_method_scopes(status):
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD
    from source.component.markdown.helper.project_name_first import ProjectNameFirst

    status.addTitle('Nv Resource Method Scopes test')
    project_dict = TierMD(ProjectStringDefault())
    project_name = ProjectNameFirst(project_dict)
    actual = NVResourceMethodScopes(project_dict, project_name, 'account')
    #print('         resource method scope:', actual)
    for nv in actual:
        assert ('name' in nv)
        status.assert_test("'name' in {}".format(nv),'name' in nv)

    for nv in actual:
        assert ('value' in nv)
        status.assert_test("'value' in {}".format(nv),'value' in nv)

    for nv in actual:
        assert (nv['name'] in ['<<DELETE_SCOPE>>', '<<GET_SCOPE>>','<<POST_SCOPE>>','<<PUT_SCOPE>>'])
        status.assert_test("{} in ['<<DELETE_SCOPE>>', '<<GET_SCOPE>>','<<POST_SCOPE>>','<<PUT_SCOPE>>']".format(nv['name']), nv['name'] in ['<<DELETE_SCOPE>>', '<<GET_SCOPE>>','<<POST_SCOPE>>','<<PUT_SCOPE>>'])

    for nv in actual:
        assert (nv['value'][0] in ['api_admin', 'api_guest', 'api_user'])
        status.assert_test("{} in ['api_admin', 'api_guest', 'api_user']".format(nv['value'][0]),nv['value'][0] in ['api_admin', 'api_guest', 'api_user'])

def main(status):
    test_nv_resource_method_scopes(status)


if __name__ == "__main__":
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))