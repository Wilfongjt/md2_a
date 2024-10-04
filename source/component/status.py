
class Status(list):
    #def __init__(self):

    def addTitle(self, title):
        self.append('# {}'.format(title))
        return self
    def addBullet(self, msg):
        self.append('  * {}'.format(msg))
        return self
    def addLine(self, msg):
        self.append('  {}'.format(msg))
        return self
    def assert_test(self, msg, test):
        assert(test)
        self.addBullet('{} {} ok'.format(msg, test))
        return self


def status_test(status):
    status.addTitle('Status test')
    actual = Status()
    actual.addTitle('Test Token test')
    actual.addBullet('a bullet')
    actual.addLine('a line')
    #print(actual)
    status.assert_test ("'# Test Token test' in actual", '# Test Token test' in actual)
    status.assert_test ("'  * a bullet' in actual", '  * a bullet' in actual)
    status.assert_test ("'  a line' in actual", '  a line' in actual)

def main(status):
    status_test(status)

if __name__ == "__main__":
    # execute as docker
    from source.component.status_report import StatusReport
    status=Status()
    main(status)
    print(StatusReport(status))