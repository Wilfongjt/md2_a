import os
import datetime
import __main__

class MultiLogger():
    ##
    ##### MultiLogger
    ##
    ## Application logging system
    ##* Create runtime.log at \<root>/log/runtime.log

    def __init__(self,setting_string='f', log_folder=None):
        # d is datetime
        # f is file name
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
        dt = ''
        fn = ''
        #print('setting_string', self.setting_string)
        if 'd' in self.setting_string:
            dt += '{}'.format(datetime.datetime.now())
        if 'f' in self.setting_string :
            # print('file', __main__.__file__)
            fn += ' <- {}'.format(str(__main__.__file__).split('/')[-1])

        rc = dt + self.msg + fn

        return rc

    def runtime(self):
        log_foldefile = '{}/runtime.log'.format(self.log_folder)
        with open(log_foldefile, 'a') as f:
            f.write('{}\n'.format(self.format()))
            #if 'PY_TEST' in os.environ and eval(os.environ['PY_TEST']):
            #    print('MultiLogger', self.format())
        return self

    def terminal(self):
        print(self.format())
        return self

def main(status):
    #if 'PY_TEST' in os.environ and eval(os.environ['PY_TEST']):
    #    print('MultiLogger test')
    status.addTitle('MultiLogger test')

    status.addBullet('no tests for multilogger')


if __name__ == "__main__":
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))