import re
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

def test_pattern(status):
    status.addTitle('Pattern test')
    # character
    resource_field = {'size': '3-330', 'type': 'C'}
    # resource_field = {'size': '3-330', 'type': 'C', 'api_admin': 'R', 'api_guest': 'CR', 'api_user': 'RUD', 'encrypt': 'N', 'field': 'id', 'resource': 'account', 'validate': 'R'}
    # print('C', Pattern(resource_field))
    #print('   character pattern: {} -> {}'.format(resource_field, Pattern(resource_field)))

    #assert (Pattern(resource_field) == '^.{3,330}$')
    #status.assert_test("Pattern({}) == '^.{3,330}$'".format(resource_field), Pattern(resource_field) == '^.{3,330}$')
    status.assert_test("Pattern({}) == {}'".format(resource_field, '^.{3,330}$'), Pattern(resource_field) == '^.{3,330}$')

    #assert (re.match(Pattern(resource_field), 'abc!89'))
    status.assert_test("re.match(Pattern({}), 'abc!89')".format(resource_field), re.match(Pattern(resource_field), 'abc!89'))
    # logical
    resource_field = {'size': '14,6', 'type': 'L'}
    status.addLine('logical pattern: {} -> {}'.format(resource_field, Pattern(resource_field)))
    status.assert_test ("Pattern({}) == '(True|False|Y|N|T|F|1|0)'".format(resource_field), Pattern(resource_field) == '(True|False|Y|N|T|F|1|0)')
    status.assert_test ("re.match(Pattern({}), 'False')".format(resource_field), re.match(Pattern(resource_field), 'False'))
    status.assert_test ("re.match(Pattern({}), 'True')".format(resource_field), re.match(Pattern(resource_field), 'True'))
    status.assert_test ("re.match(Pattern({}), 'Y')".format(resource_field), re.match(Pattern(resource_field), 'Y'))
    status.assert_test ("re.match(Pattern({}), 'N')".format(resource_field), re.match(Pattern(resource_field), 'N'))
    status.assert_test ("re.match(Pattern({}), 'T')".format(resource_field), re.match(Pattern(resource_field), 'T'))
    status.assert_test ("re.match(Pattern({}), 'F')".format(resource_field), re.match(Pattern(resource_field), 'F'))
    status.assert_test ("re.match(Pattern({}), '0')".format(resource_field), re.match(Pattern(resource_field), '0'))
    status.assert_test ("re.match(Pattern({}), '1')".format(resource_field), re.match(Pattern(resource_field), '1'))
    status.assert_test ("not re.match(Pattern({}), 'z')".format(resource_field), not re.match(Pattern(resource_field), 'z'))
    # integer
    resource_field = {'size': '1-6', 'type': 'I'}
    # print('integer',Pattern(resource_field))
    status.addLine('integer pattern: {} -> {}'.format(resource_field, Pattern(resource_field)))
    status.assert_test ("Pattern({}) == '{}'".format(resource_field,'-?\d{1,6}'), Pattern(resource_field) == '-?\d{1,6}')
    status.assert_test ("Pattern(resource_field) == 'a'".format(resource_field), not re.match(Pattern(resource_field), 'a'))
    status.assert_test ("Pattern(resource_field) == '1'".format(resource_field), re.match(Pattern(resource_field), '1'))
    status.assert_test ("Pattern(resource_field) == '-1'".format(resource_field), re.match(Pattern(resource_field), '-1'))

    # number
    resource_field = {'size': '14,6', 'type': 'N'}
    status.addLine('number pattern: {} -> {}'.format(resource_field, Pattern(resource_field)))
    status.assert_test ("Pattern({}) == '{}'".format(resource_field,'-?\d{1,14}(\.\d{1,6})?'), Pattern(resource_field) == '-?\d{1,14}(\.\d{1,6})?')
    status.assert_test ("Pattern({}) == '{}'".format(resource_field,'a'), not re.match(Pattern(resource_field), 'a'))
    status.assert_test ("Pattern({}) == '{}'".format(resource_field,'1'), re.match(Pattern(resource_field), '1'))
    status.assert_test ("Pattern({}) == '{}'".format(resource_field,'-1'), re.match(Pattern(resource_field), '-1'))
    status.assert_test ("Pattern({}) == '{}'".format(resource_field,'1.1'), re.match(Pattern(resource_field), '1.1'))
    # datetime
    resource_field = {'size': '14,6', 'type': 'D'}
    status.addLine('datetime pattern: {} -> {}'.format(resource_field, Pattern(resource_field)))
    status.assert_test ("Pattern({}) == '{}'".format(resource_field,'(\d{4}-\d{2}-\d{2})([T ]?)(\d{2}:\d{2}:\d{2})?(\.\d+)?(Z|([+-]\d{2}:\d{2}))?'), Pattern(resource_field) == '(\d{4}-\d{2}-\d{2})([T ]?)(\d{2}:\d{2}:\d{2})?(\.\d+)?(Z|([+-]\d{2}:\d{2}))?')
    status.assert_test ("Pattern({}) == '{}'".format(resource_field,'a'), not re.match(Pattern(resource_field), 'a'))
    status.assert_test ("Pattern({}) == '{}'".format(resource_field,'2024-06-23'), re.match(Pattern(resource_field), '2024-06-23'))
    status.assert_test ("Pattern({}) == '{}'".format(resource_field,'2024-06-23 18:30:00'), re.match(Pattern(resource_field), '2024-06-23 18:30:00'))

def main(status):
    test_pattern(status)

if __name__ == "__main__":
    # execute as docker
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))

