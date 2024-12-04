
from pprint import pprint

class RouteScopes(list):
    # list of scope(s) for a given method
    # -> ['api_xxx', ...]
    # POST is C`
    # GET is R
    # PUT is U
    # DELETE is D
    # fix missing project_dict name
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
        #print(project_dict['project'])
        #project_dict = project_dict['project']
        #resources = project_dict['project']['resources']
        #pprint(resources)

        for p in project_dict['project']['privileges']:
            #print('p', method, p, project_dict['project']['privileges'][p])
            for s in project_dict['project']['privileges'][p]:
                #print('s',s, method, project_dict['project']['privileges'][p][s])
                for fld in project_dict['project']['privileges'][p][s]:
                    if method in project_dict['project']['privileges'][p][s][fld]:
                        if s not in self:
                            #print('fld', method, fld, project_dict['project']['privileges'][p][s][fld])
                            self.append(s)
        '''
        for r in project_dict['project']['resources']: # all resource
            print('r',r)
            for m in project_dict['project']['models'][r]: # all models 
                print('m',m)
                for s in resources[r]['model'][m]: # all resource model 
                    #print('s is ', s)
                    if s.startswith('api_'): #
                        for y in resources[r]['model'][m]:
                            #print('model', resources[r]['model'])
                            for fld in resources[r]['model']:
                                #print('fld', resources[r]['model'][fld])
                                for att in resources[r]['model'][fld]:
                                    #print('att',att,resources[r]['model'][fld][att])
                                    if att.startswith('api_'):
                                        #print('scope', att, resources[r]['model'][fld][att])
                                        if method in resources[r]['model'][fld][att]:
                                            lst.append(att)
                '''
        #lst = set(lst)  # get rid of duplicates
        #print('lst', lst)
        #for r in lst:
        #    print('r', r, self)
        #    if r not in self:
        #        self.append(r)
        print('RouteScopes', method, self)

def test_route_scope(status):
    from source.component.markdown.tier_md import TierMD
    from source.component.markdown.project_string_default import ProjectStringDefault

    status.addTitle('route scope test')

    project_dict = TierMD(ProjectStringDefault())
    project = 'sample'
    status.addBullet('account POST scopes: {}'.format(RouteScopes(project_dict, 'account','POST')))

    status.addBullet('account GET scopes: {}'.format(RouteScopes(project_dict, 'account','GET')))
    status.addBullet('account PUT scopes: {}'.format(RouteScopes(project_dict, 'account','PUT')))
    status.addBullet('account DELETE scopes: {}'.format(RouteScopes(project_dict, 'account','DELETE')))
    
    assert( 'api_guest' not in RouteScopes(project_dict, 'account','DELETE'))
    status.addBullet("'api_guest' not in {}".format(RouteScopes(project_dict, 'account','DELETE')))

    assert( 'api_user' in RouteScopes(project_dict, 'account','DELETE'))
    status.addBullet("'api_user' in {}".format(RouteScopes(project_dict, 'account','DELETE')))

    assert( 'api_admin' not in RouteScopes(project_dict, 'account','DELETE'))
    status.addBullet("'api_admin' not in {}".format(RouteScopes(project_dict, 'account','DELETE')))

    assert( 'api_guest' in RouteScopes(project_dict, 'account','POST'))
    status.addBullet("'api_guest' in {}".format(RouteScopes(project_dict, 'account','POST')))

    assert( 'api_user' not in RouteScopes(project_dict, 'account','POST'))
    status.addBullet("'api_user' not in {}".format(RouteScopes(project_dict, 'account','POST')))

    assert( 'api_admin' not in RouteScopes(project_dict, 'account','POST'))
    status.addBullet("'api_admin' not in {}".format(RouteScopes(project_dict, 'account','POST')))

    assert( 'api_guest' not in RouteScopes(project_dict, 'account','PUT'))
    status.addBullet("'api_guest' not in {}".format(RouteScopes(project_dict, 'account','PUT')))

    assert( 'api_user' in RouteScopes(project_dict, 'account','PUT'))
    status.addBullet("'api_user' in {}".format(RouteScopes(project_dict, 'account','PUT')))

    assert( 'api_admin' not in RouteScopes(project_dict, 'account','PUT'))
    status.addBullet("'api_admin' not in {}".format(RouteScopes(project_dict, 'account','PUT')))

    assert( 'api_guest' in RouteScopes(project_dict, 'account','GET'))
    status.addBullet("'api_guest' in {}".format(RouteScopes(project_dict, 'account','GET')))

    assert( 'api_user' in RouteScopes(project_dict, 'account','GET'))
    status.addBullet("'api_guest' in {}".format(RouteScopes(project_dict, 'account','GET')))

    assert( 'api_admin' in RouteScopes(project_dict, 'account','GET'))
    status.addBullet("'api_admin' in {}".format(RouteScopes(project_dict, 'account','GET')))


def main(status):
    test_route_scope(status)


if __name__ == "__main__":
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))