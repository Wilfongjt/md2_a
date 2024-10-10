class Min(int):
    def __new__(cls, resource_field):
        # resource_field is {'api_admin': 'R', 'api_guest': 'CR', 'api_user': 'RUD', 'encrypt': 'N', 'field': 'id', 'pattern': '^.{3,330}$', 'resource': 'account','size': '3-330', 'type': 'C', 'validate': 'R'}
        contents = ''
        if 'type' in resource_field:
            if resource_field['type'] == 'C':  # Character
                # contents = '^<<TYPE>>{<<MIN>>,<<MAX>>}$'
                min = resource_field['size'].split('-')[0]
                contents = int(min)
            elif resource_field['type'] == 'L':  # Boolean Logical
                # contents = '(True|False|Y|N|T|F|1|0)'
                contents = 1
            elif resource_field['type'] == 'I':  # Integer
                # contents = '-?\d{<<MIN>>,<<MAX>>}'
                contents = 1
            elif resource_field['type'] == 'N':  # Number
                # contents = '-?\d{1,<<W>>}(\.\d{1,<<D>>})?'  # .replace('<<W>',w).replace('<<D>>',d) # eg
                contents = 1
            elif resource_field['type'] == 'D':  # Datetime
                # contents = '(\d{4}-\d{2}-\d{2})([T ]?)(\d{2}:\d{2}:\d{2})?(\.\d+)?(Z|([+-]\d{2}:\d{2}))?'
                contents = 8
            else:
                print('setting default type for resource_field', resource_field)

        instance = super().__new__(cls, contents)
        return instance

def test_min(status):
    status.addTitle('Min test')
    resource_field = {'size': '3-330', 'type': 'C'}
    #print('        characer min:', Min(resource_field))
    status.assert_test ("Min({}) == 3".format(resource_field), Min(resource_field) == 3)

    resource_field = {'size': '1-14', 'type': 'I'}
    #print('         integer min:', Min(resource_field))
    status.assert_test ("Min({}) == 1".format(resource_field), Min(resource_field) == 1)

    resource_field = {'size': '14,6', 'type': 'N'}
    #print('          number min:', Min(resource_field))
    status.assert_test ("Min({}) == 14".format(resource_field), Min(resource_field) == 1)

    resource_field = {'size': '8-19', 'type': 'D'}
    #print('            date min:', Min(resource_field))
    status.assert_test ("Min({}) == 8".format(resource_field), Min(resource_field) == 8)

def main(status):
    test_min(status)

if __name__ == "__main__":
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))
