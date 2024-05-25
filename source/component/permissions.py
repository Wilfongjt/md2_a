import os
import subprocess

class Permissions():
    def __init__(self, folderfilename, verbose=False):
        if folderfilename.endswith('.sh'):
            command = 'chmod +x {}'.format(folderfilename)
            #rc = False
            ret = subprocess.run(command, capture_output=True, shell=True)
            if verbose:
                print('subprocess'.format(command))
            if ret.returncode != 0:
                self.set_fail(True, ret.stderr.decode('ascii'))
                if verbose:
                    self.print('    - ret {}'.format(ret))
                #rc= ret.stderr.decoce('ascii')
            else:
                if verbose:
                    print('    - ret {}'.format(ret))
                rc = ret.stdout.decode('ascii').strip()

def main():
    folder = '{}/Development/Temp/permissions'.format(os.environ['HOME'])
    folder_filename = '{}/permissions.sh'.format(folder)

    # setup
    contents = "echo 'permissions 1'"

    os.makedirs(folder, exist_ok=True)

    # create a file to read
    with open(folder_filename, 'w') as f:
        f.write(contents)

    assert(Permissions(folder_filename, verbose=True))

    if os.path.isfile(folder_filename):
        os.remove(folder_filename)

if __name__ == "__main__":
    # execute as docker-dep
    main()