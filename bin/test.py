import os

import source.component

def main(status=None):

    # print('os.env', os.environ)
    os.environ['PY_TEST']='True'

    source.component.application.main(status)
    source.component.find.main(status)
    source.component.multilogger.main(status)
    source.component.nv_field.main(status)
    source.component.nv_list.main(status)
    source.component.nv_resource.main(status)
    source.component.nv_resource_fields.main(status)
    source.component.nv_resource_method_scopes.main(status)
    source.component.nv_resource_schema_version.main(status)
    source.component.permissions.main(status)
    source.component.process_package.main(status)
    source.component.process_project.main(status)
    source.component.status.main(status)
    source.component.status_report.main(status)
    source.component.task_initialize_hapi_routes.main(status)
    source.component.test_token.main(status)
    source.component.tier.main(status)

    source.component.env.env_string_default.main(status)

    source.component.markdown.claim.main(status)
    source.component.markdown.data.main(status)
    source.component.markdown.max.main(status)
    source.component.markdown.min.main(status)
    source.component.markdown.model.main(status)
    source.component.markdown.pattern.main(status)
    source.component.markdown.project_string_default.main(status)
    source.component.markdown.scopes.main(status)
    source.component.markdown.tier_md.main(status)

    source.component.markdown.helper.project_claim_type.main(status)
    source.component.markdown.helper.project_name.main(status)
    source.component.markdown.helper.project_name_first.main(status)
    source.component.markdown.helper.project_name_last.main(status)
    source.component.markdown.helper.resource_names.main(status)
    source.component.markdown.helper.resource_patterns.main(status)
    source.component.markdown.helper.role_names.main(status)
    source.component.markdown.helper.route_scopes.main(status)


    os.environ['PY_TEST']='False'

    #print('env', eval(os.environ['PY_TEST']))
    #print('PY_TEST', os.environ['PY_TEST'])
    #print('PY_TEST', bool(str(os.environ['PY_TEST'])))

if __name__ == "__main__":
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport
    status = Status()
    status.addTitle('Tests')
    # status= list()
    main(status=status)
    #print('status', status)
    print(StatusReport(status))