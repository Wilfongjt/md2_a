

class RouteScopes(list):
    # POST is C`
    # GET is R
    # PUT is U
    # DELETE is D

    def __init__(self, project_dict, resource_name, method ):
        # method is POST, GET, PUT, or DELETE
        if method == 'DELETE':
            method = 'D'
        elif method == 'POST':
            method = 'C'
        elif method == 'PUT':
            method = 'U'
        else:
            method = 'R'
        lst = []
        for r in project_dict['project']['resources']:
            #print('r',r)
            for m in project_dict['project']['resources'][r]['model']:
                #print('m',project_dict['project']['resources'][r]['model'][m])
                for s in project_dict['project']['resources'][r]['model'][m]:
                    #print('s is ', s)
                    if s.startswith('api_'):
                        for y in project_dict['project']['resources'][r]['model'][m]:
                            #print('model', project_dict['project']['resources'][r]['model'])
                            for fld in project_dict['project']['resources'][r]['model']:
                                #print('fld', project_dict['project']['resources'][r]['model'][fld])
                                for att in project_dict['project']['resources'][r]['model'][fld]:
                                    #print('att',att,project_dict['project']['resources'][r]['model'][fld][att])
                                    if att.startswith('api_'):
                                        #print('scope', att, project_dict['project']['resources'][r]['model'][fld][att])
                                        if method in project_dict['project']['resources'][r]['model'][fld][att]:
                                            lst.append(att)

        lst = set(lst)  # get rid of duplicates
        for r in lst:
            self.append(r)
        #print('RouteScopes', method, self)

def test_route_scope():
    from source.component.markdown.tier_md import TierMD
    from source.component.markdown.project_string_default import ProjectStringDefault

    project_dict = TierMD(ProjectStringDefault())

    print('         account POST scopes:', RouteScopes(project_dict,'account','POST'))
    print('         account GET scopes:', RouteScopes(project_dict,'account','GET'))
    print('         account PUT scopes:', RouteScopes(project_dict,'account','PUT'))
    print('         account DELETE scopes:', RouteScopes(project_dict,'account','DELETE'))

    assert( 'api_guest' not in RouteScopes(project_dict,'account','DELETE'))
    assert( 'api_user' in RouteScopes(project_dict,'account','DELETE'))
    assert( 'api_admin' not in RouteScopes(project_dict,'account','DELETE'))

    assert( 'api_guest' in RouteScopes(project_dict,'account','POST'))
    assert( 'api_user' not in RouteScopes(project_dict,'account','POST'))
    assert( 'api_admin' not in RouteScopes(project_dict,'account','POST'))

    assert( 'api_guest' not in RouteScopes(project_dict,'account','PUT'))
    assert( 'api_user' in RouteScopes(project_dict,'account','PUT'))
    assert( 'api_admin' not in RouteScopes(project_dict,'account','PUT'))

    assert( 'api_guest' in RouteScopes(project_dict,'account','GET'))
    assert( 'api_user' in RouteScopes(project_dict,'account','GET'))
    assert( 'api_admin' in RouteScopes(project_dict,'account','GET'))


def main():
    test_route_scope()


if __name__ == "__main__":
    # execute as docker
    main()
