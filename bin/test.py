import os

import source.component

def main(status=None):

    # print('os.env', os.environ)
    os.environ['PY_TEST']='True'

    source.component.application.main(status)

    source.component.multilogger.main(status)

    source.component.nv_field.main(status)

    source.component.nv_list.main(status)

    source.component.nv_resource.main(status)

    source.component.nv_resource_fields.main(status)

    source.component.permissions.main(status)

    source.component.process_package.main(status)

    source.component.process_project.main(status)

    source.component.status.main(status)
    source.component.status_report.main(status)

    source.component.task_initialize_hapi_routes.main(status)

    source.component.tier.main(status)
    source.component.find.main(status)

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