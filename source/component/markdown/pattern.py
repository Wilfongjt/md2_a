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

def test_pattern():
    # character
    resource_field = {'size': '3-330', 'type': 'C'}
    # resource_field = {'size': '3-330', 'type': 'C', 'api_admin': 'R', 'api_guest': 'CR', 'api_user': 'RUD', 'encrypt': 'N', 'field': 'id', 'resource': 'account', 'validate': 'R'}
    # print('C', Pattern(resource_field))
    print('   character pattern: {} -> {}'.format(resource_field, Pattern(resource_field)))
    assert (Pattern(resource_field) == '^.{3,330}$')
    assert (re.match(Pattern(resource_field), 'abc!89'))
    # logical
    resource_field = {'size': '14,6', 'type': 'L'}
    print('     logical pattern: {} -> {}'.format(resource_field, Pattern(resource_field)))
    assert (Pattern(resource_field) == '(True|False|Y|N|T|F|1|0)')
    assert (re.match(Pattern(resource_field), 'False'))
    assert (re.match(Pattern(resource_field), 'True'))
    assert (re.match(Pattern(resource_field), 'Y'))
    assert (re.match(Pattern(resource_field), 'N'))
    assert (re.match(Pattern(resource_field), 'T'))
    assert (re.match(Pattern(resource_field), 'F'))
    assert (re.match(Pattern(resource_field), '0'))
    assert (re.match(Pattern(resource_field), '1'))
    assert (not re.match(Pattern(resource_field), 'z'))
    # integer
    resource_field = {'size': '1-6', 'type': 'I'}
    # print('integer',Pattern(resource_field))
    print('     integer pattern: {} -> {}'.format(resource_field, Pattern(resource_field)))
    assert (Pattern(resource_field) == '-?\d{1,6}')
    assert (not re.match(Pattern(resource_field), 'a'))
    assert (re.match(Pattern(resource_field), '1'))
    assert (re.match(Pattern(resource_field), '-1'))

    # number
    resource_field = {'size': '14,6', 'type': 'N'}
    print('      number pattern: {} -> {}'.format(resource_field, Pattern(resource_field)))
    assert (Pattern(resource_field) == '-?\d{1,14}(\.\d{1,6})?')
    assert (not re.match(Pattern(resource_field), 'a'))
    assert (re.match(Pattern(resource_field), '1'))
    assert (re.match(Pattern(resource_field), '-1'))
    assert (re.match(Pattern(resource_field), '1.1'))
    # datetime
    resource_field = {'size': '14,6', 'type': 'D'}
    print('    datetime pattern: {} -> {}'.format(resource_field, Pattern(resource_field)))
    assert (Pattern(resource_field) == '(\d{4}-\d{2}-\d{2})([T ]?)(\d{2}:\d{2}:\d{2})?(\.\d+)?(Z|([+-]\d{2}:\d{2}))?')
    assert (not re.match(Pattern(resource_field), 'a'))
    assert (re.match(Pattern(resource_field), '2024-06-23'))
    assert (re.match(Pattern(resource_field), '2024-06-23 18:30:00'))

def main():
    test_pattern()

if __name__ == "__main__":
    # execute as docker
    main()
