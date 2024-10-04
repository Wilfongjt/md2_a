
class StatusReport(str):
    def __new__(cls, status):
        # status is Status()
        contents = '\n'.join(status)
        #print('contents', contents)
        instance = super().__new__(cls, contents)
        #print(instance)
        return instance

def status_report_test(status):
    status.addTitle('Status Report test')
    status.addBullet('xxx')

    actual = StatusReport(status)
    #print('A',actual)
    status.assert_test("'Status Report test' in status", 'Status Report test' in actual)
    status.assert_test("xxx in StatusReport", 'xxx' in actual)

def main(status):
    status_report_test(status)


if __name__ == "__main__":
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))