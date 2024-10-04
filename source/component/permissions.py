import os
import subprocess

class Permissions():
    def __init__(self, folderfilename, verbose=False):
        if folderfilename.endswith('.sh'):
            command = 'chmod +x {}'.format(folderfilename)
            #rc = False
            ret = subprocess.run(command, capture_output=True, shell=True)
            #if verbose:
            #    print('subprocess'.format(command))
            if ret.returncode != 0:
                self.set_fail(True, ret.stderr.decode('ascii'))
            #    if verbose:
            #        self.print('    - ret {}'.format(ret))
                #rc= ret.stderr.decoce('ascii')
            else:
            #    if verbose:
            #        print('    - ret {}'.format(ret))
                rc = ret.stdout.decode('ascii').strip()

def permission_test(status):
    #if 'PY_TEST' in os.environ and eval(os.environ['PY_TEST']):
    #    print('Permissions test')
    status.addTitle('Permissions test')
    folder = '{}/Development/Temp/permissions'.format(os.environ['HOME'])
    folder_filename = '{}/permissions.sh'.format(folder)

    # setup
    contents = "echo 'permissions 1'"

    os.makedirs(folder, exist_ok=True)

    # create a file to read
    with open(folder_filename, 'w') as f:
        f.write(contents)

    assert(Permissions(folder_filename, verbose=True))
    status.addBullet('permissions -x set {} ok'.format(folder_filename))

    if os.path.isfile(folder_filename):
        os.remove(folder_filename)

def main(status):
    permission_test(status)


if __name__ == "__main__":
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))