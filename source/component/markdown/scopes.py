
class Scopes(list):
    def __init__(self):
        self.append('api_admin')
        self.append('api_guest')
        self.append('api_user')

def test_scopes(status):
    status.addTitle('Scopes test')
    actual = Scopes()
    expected = ['api_admin', 'api_guest', 'api_user']
    status.addBullet('Instantiated {}'.format(actual))
    status.assert_test('Expected Scopes = {}'.format(actual), actual == expected)

def main(status):
    test_scopes(status)

if __name__ == "__main__":
    # execute as docker
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))