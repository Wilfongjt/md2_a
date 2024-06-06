import os
from able import StringReader, \
                 Recorder

#class MDReader(StringReader):
#    def __new__(cls, folder_filename_list, recorder=None):
#        super.__new__(cls)

class Application(Recorder):
    ##
    ##### __Application__
    ##
    ##Application data and methods
    # def __init__(self, name='md2'):

    def __init__(self, name=None):
        Recorder.__init__(self)
        #self.name = name
        self['name']=name

    def get_name(self):
        ##* __get_name__, get repository name (aka repo-name)
        return self['name']

    #def set_name(self, name):
    #    self['name']=name
    #    ##* __set_name__
    #    return self

    def get_bin_folder(self):
        ##* __get_bin_folder__, eg "\<repo>/bin" (aka bin-folder)
        return os.getcwd()

    def get_template_folder(self):
        ##* __get_template_folder__, eg "\<repo>/source/template" (aka template-folder)
        return os.getcwd().replace('/bin', '/source/template')
    def get_environment_filename(self):
        ##* __get_environment_filename___, eg "\<repo>/bin/\<repo-name>_.env" (aka runtime-env)
        # env is stored in the bin folder bin/md2
        return '{}/{}.env'.format(self.get_bin_folder(), self.get_name())

    def get_environment_template_filename(self):
        ##* __get_environment_template_filename__, eg "\<repo>/bin/\<name>.env" (aka app-env)
        return '{}/{}.env.tmpl'.format(self.get_template_folder(), self.get_name())

    def get_environment_varable_names(self, prefix):
        ##* __get_environment_varable_names__, get env var names from memory
        rc = [item for item in os.environ
                if item.startswith(prefix)]
        return ', '.join(rc)

    def load_environment(self):
        ##* __load_environment__, put env vars into memory from file
        if not os.path.isfile(self.get_environment_filename()):
            return self

        env_string = StringReader(self.get_environment_filename())
        env_string = [ln.strip() for ln in env_string.split('\n')]
        for ln in env_string:
            if '=' in ln:
                ln = [i.strip() for i in ln.split('=')]
                #print('{} = {}'.format(ln[0],ln[1]))
                os.environ[ln[0]]=ln[1]

        return self
