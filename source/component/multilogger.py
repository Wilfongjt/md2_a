import os
import datetime

class MultiLogger():
    ##
    ##### MultiLogger
    ##
    ## Application logging system
    ##* Create runtime.log at \<root>/log/runtime.log

    def __init__(self,setting_string='df', log_folder=None):
        self.msg = '{}'.format(datetime.datetime.now())
        self.log_folder=log_folder
        if not self.log_folder:
            # default log folder is the current working dir
            self.log_folder = str(os.getcwd()).replace('/bin','/log')
        os.makedirs(self.log_folder, exist_ok=True)
        self.setting_string=setting_string

    def set_msg(self, msg):
        self.msg = msg
        return self

    def format(self):
        rc = ''
        if 'd' in self.setting_string:
            rc += '{}'.format(datetime.datetime.now())
        if 'f' in self.setting_string :
            rc += ' {}'.format(str(__file__).split('/')[-1])

        rc += ' ' + self.msg

        return rc

    def runtime(self):
        log_foldefile = '{}/runtime.log'.format(self.log_folder)
        with open(log_foldefile, 'a') as f:
            f.write('{}\n'.format(self.format()))
        return self

    def terminal(self):
        print(self.format())
        return self
