class OneHot:
    def __init__(self, config, pname, version):
        self.config = config
        self.pname = pname
        self.version = version
        ...

    def get_version_info(self):
        size = 0
        failing_ids = []
        pth = './relevant_tests/relevant_{}_{}.txt'.format(self.pname, self.version)
        tests = []
        with open(pth, 'r') as f:
            tests = f.read().splitlines()
            size = len(tests)
            tests = list(map(CV.reformat_testcase, tests))
        
        pth = './failing_tests/failing_{}_{}.txt'.format(self.pname, self.version)
        with open(pth, 'r') as f:
            ftests = f.read().splitlines()

        for ft in ftests:
            fid = tests.index(ft)
            failing_ids.append(fid)
        
        return size, failing_ids