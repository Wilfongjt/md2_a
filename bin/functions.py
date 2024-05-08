import os
def get_root_folder():
    return os.getcwd().replace('/bin','')

def get_bin_folder():
    return os.getcwd()


def get_data_folder():
    return os.getcwd().replace('/bin', '/source/data')

def get_template_folder():
    return os.getcwd().replace('/bin', '/source/template')

def get_default_input_folder():
    return os.getcwd().replace('/bin', '')

def get_default_output_folder():
    return os.getcwd()


def get_env_var(env_name, default_value=None):
    rc = None
    if env_name in os.environ:
        rc = os.environ[env_name]
    elif default_value:
        rc = default_value
    return rc

def get_env_variable_values_string(prefix=['WS_', 'GH_']):
    rc = []
    for e in os.environ:
        for p in prefix:
            if e.startswith(p):
                rc.append('{}={}'.format(e, os.environ[e]))

    return '\n'.join(rc)


def test_bin():
    assert (get_bin_folder()==os.getcwd())
def test_get_data_folder():
    assert ('source/data' in get_data_folder())
def test_template_folder():
    assert ('source/template' in get_template_folder())
def test_get_default_input_folder():
    assert ('/bin' not in get_default_input_folder())
def test_get_default_output_folder():
    assert ('source/template' in get_template_folder())
def test_get_env_var():
    assert (get_env_var('TEST_VAR', default_value=None)==None)
    assert (get_env_var('TEST_VAR', default_value='main') == 'main')
def isStringNone(str_object):
    #
    #__isStringNone__
    #
    # Determine if str_object is None

    rc = str_object

    if str_object == None:
        rc = None
    elif str_object == 'None':
        rc = None

    return rc

def main():
    print('bin:       ', get_bin_folder())
    print('data:      ', get_data_folder())
    print('template:  ', get_template_folder())
    print('default_input_folder:  ', get_default_input_folder())
    print('default_output_folder: ', get_default_output_folder())

    test_bin()
    test_get_data_folder()
    test_template_folder()
    test_get_default_input_folder()
    test_get_default_output_folder()
    test_get_env_var()

if __name__ == "__main__":
    # execute as docker
    main()