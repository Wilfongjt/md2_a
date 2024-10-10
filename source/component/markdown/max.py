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

def test_max(status):
    status.addTitle('Max test')
    resource_field = {'size': '3-330', 'type': 'C'}
    #print('        characer min:', Max(resource_field))
    status.assert_test ("Max({}) == 330".format(resource_field), Max(resource_field) == 330)

    resource_field = {'size': '1-14', 'type': 'I'}
    #print('         integer max:', Max(resource_field))
    status.assert_test ("Max({}) == 14".format(resource_field), Max(resource_field) == 14)

    resource_field = {'size': '14,6', 'type': 'N'}
    #print('          number min:', Max(resource_field))
    status.assert_test ("Max({}) == 6".format(resource_field), Max(resource_field) == 14)

    resource_field = {'size': '8-19', 'type': 'D'}
    #print('            date min:', Max(resource_field))
    status.assert_test ("Max({}) == 19".format(resource_field), Max(resource_field) == 19)

def main(status):
    test_max(status)

if __name__ == "__main__":
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))

