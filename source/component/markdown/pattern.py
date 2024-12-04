import re
class Pattern(str):
    # format a regexp pattern for a model field
    def __new__(cls, model_field):
        # model_field is {'encrypt': 'N', 'field': 'id', 'resource': 'account','size': '3-330', 'type': 'C', 'validate': 'R'}
        contents = ''
        if 'type' in model_field:
            if model_field['type'] == 'C':
                contents = '^<<TYPE>>{<<MIN>>,<<MAX>>}$'
                contents = contents.replace('<<TYPE>>', '.')
                min = model_field['size'].split('-')[0]
                max = model_field['size'].split('-')[1]
                contents = contents.replace('<<MIN>>', min).replace('<<MAX>>', max)
            elif model_field['type'] == 'L':
                contents = '(True|False|Y|N|T|F|1|0)'
                model_field['size'] = '1-5'  # eg True, False, Y, N, T, F, 1, or 0
            elif model_field['type'] == 'I':
                contents = '-?\d{<<MIN>>,<<MAX>>}'
                min = model_field['size'].split('-')[0]
                max = model_field['size'].split('-')[1]
                contents = contents.replace('<<MIN>>', min).replace('<<MAX>>', max)
            elif model_field['type'] == 'N':
                contents = '-?\d{1,<<W>>}(\.\d{1,<<D>>})?'  # .replace('<<W>',w).replace('<<D>>',d) # eg
                w = model_field['size'].split(',')[0]
                d = model_field['size'].replace('-', ',').split(',')[1]
                contents = contents.replace('<<W>>', w).replace('<<D>>', d)
            elif model_field['type'] == 'D':
                contents = '(\d{4}-\d{2}-\d{2})([T ]?)(\d{2}:\d{2}:\d{2})?(\.\d+)?(Z|([+-]\d{2}:\d{2}))?'
                model_field['size'] = '8-19'  # eg 2024-06-23 18:30:00

        instance = super().__new__(cls, contents)
        return instance

def test_pattern(status):
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD
    from source.component.markdown.model import Model
    from source.component.markdown.field import Field
    from pprint import pprint

    status.addTitle('Pattern test')
    # character
    #model_field = {'size': '3-330', 'type': 'C'}
    project_dict = TierMD(ProjectStringDefault())
    model_field = Field(project_dict, 'account', 'id')
    pprint(model_field)
    # model_field = {'size': '3-330', 'type': 'C', 'api_admin': 'R', 'api_guest': 'CR', 'api_user': 'RUD', 'encrypt': 'N', 'field': 'id', 'resource': 'account', 'validate': 'R'}
    # print('C', Pattern(model_field))
    #print('   character pattern: {} -> {}'.format(model_field, Pattern(model_field)))

    #assert (Pattern(model_field) == '^.{3,330}$')
    #status.assert_test("Pattern({}) == '^.{3,330}$'".format(model_field), Pattern(model_field) == '^.{3,330}$')
    status.assert_test("Pattern({}) == {}'".format(model_field, '^.{3,330}$'), Pattern(model_field) == '^.{3,330}$')

    #assert (re.match(Pattern(model_field), 'abc!89'))
    status.assert_test("re.match(Pattern({}), 'abc!89')".format(model_field), re.match(Pattern(model_field), 'abc!89'))
    # logical
    model_field = {'size': '14,6', 'type': 'L'}
    status.addLine('logical pattern: {} -> {}'.format(model_field, Pattern(model_field)))
    status.assert_test ("Pattern({}) == '(True|False|Y|N|T|F|1|0)'".format(model_field), Pattern(model_field) == '(True|False|Y|N|T|F|1|0)')
    status.assert_test ("re.match(Pattern({}), 'False')".format(model_field), re.match(Pattern(model_field), 'False'))
    status.assert_test ("re.match(Pattern({}), 'True')".format(model_field), re.match(Pattern(model_field), 'True'))
    status.assert_test ("re.match(Pattern({}), 'Y')".format(model_field), re.match(Pattern(model_field), 'Y'))
    status.assert_test ("re.match(Pattern({}), 'N')".format(model_field), re.match(Pattern(model_field), 'N'))
    status.assert_test ("re.match(Pattern({}), 'T')".format(model_field), re.match(Pattern(model_field), 'T'))
    status.assert_test ("re.match(Pattern({}), 'F')".format(model_field), re.match(Pattern(model_field), 'F'))
    status.assert_test ("re.match(Pattern({}), '0')".format(model_field), re.match(Pattern(model_field), '0'))
    status.assert_test ("re.match(Pattern({}), '1')".format(model_field), re.match(Pattern(model_field), '1'))
    status.assert_test ("not re.match(Pattern({}), 'z')".format(model_field), not re.match(Pattern(model_field), 'z'))
    # integer
    model_field = {'size': '1-6', 'type': 'I'}
    # print('integer',Pattern(model_field))
    status.addLine('integer pattern: {} -> {}'.format(model_field, Pattern(model_field)))
    status.assert_test ("Pattern({}) == '{}'".format(model_field,'-?\d{1,6}'), Pattern(model_field) == '-?\d{1,6}')
    status.assert_test ("Pattern(model_field) == 'a'".format(model_field), not re.match(Pattern(model_field), 'a'))
    status.assert_test ("Pattern(model_field) == '1'".format(model_field), re.match(Pattern(model_field), '1'))
    status.assert_test ("Pattern(model_field) == '-1'".format(model_field), re.match(Pattern(model_field), '-1'))

    # number
    model_field = {'size': '14,6', 'type': 'N'}
    status.addLine('number pattern: {} -> {}'.format(model_field, Pattern(model_field)))
    status.assert_test ("Pattern({}) == '{}'".format(model_field,'-?\d{1,14}(\.\d{1,6})?'), Pattern(model_field) == '-?\d{1,14}(\.\d{1,6})?')
    status.assert_test ("Pattern({}) == '{}'".format(model_field,'a'), not re.match(Pattern(model_field), 'a'))
    status.assert_test ("Pattern({}) == '{}'".format(model_field,'1'), re.match(Pattern(model_field), '1'))
    status.assert_test ("Pattern({}) == '{}'".format(model_field,'-1'), re.match(Pattern(model_field), '-1'))
    status.assert_test ("Pattern({}) == '{}'".format(model_field,'1.1'), re.match(Pattern(model_field), '1.1'))
    # datetime
    model_field = {'size': '14,6', 'type': 'D'}
    status.addLine('datetime pattern: {} -> {}'.format(model_field, Pattern(model_field)))
    status.assert_test ("Pattern({}) == '{}'".format(model_field,'(\d{4}-\d{2}-\d{2})([T ]?)(\d{2}:\d{2}:\d{2})?(\.\d+)?(Z|([+-]\d{2}:\d{2}))?'), Pattern(model_field) == '(\d{4}-\d{2}-\d{2})([T ]?)(\d{2}:\d{2}:\d{2})?(\.\d+)?(Z|([+-]\d{2}:\d{2}))?')
    status.assert_test ("Pattern({}) == '{}'".format(model_field,'a'), not re.match(Pattern(model_field), 'a'))
    status.assert_test ("Pattern({}) == '{}'".format(model_field,'2024-06-23'), re.match(Pattern(model_field), '2024-06-23'))
    status.assert_test ("Pattern({}) == '{}'".format(model_field,'2024-06-23 18:30:00'), re.match(Pattern(model_field), '2024-06-23 18:30:00'))

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

