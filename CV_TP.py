import subprocess
from sys import version
from tqdm import tqdm
from random import choice
from parse import get_covered_lines

class LC:
    def __init__(self, config, pname, version):
        self.config = config
        self.pname = pname
        self.version = version

    def get_version_info(self):
        size = 0
        failing_ids = []
        pth = './relevant_tests/relevant_{}_{}.txt'.format(self.pname, self.version)
        tests = []
        with open(pth, 'r') as f:
            tests = f.read().splitlines()
            size = len(tests)
            tests = list(map(LC.reformat_testcase, tests))
        
        pth = './failing_tests/failing_{}_{}.txt'.format(self.pname, self.version)
        with open(pth, 'r') as f:
            ftests = f.read().splitlines()

        for ft in ftests:
            fid = tests.index(ft)
            failing_ids.append(fid)
        
        return size, failing_ids

    def exec(self):
        self.clone()
        self.load_relevant_tests()
        self.load_failing_tests() 
        self.num_of_test, self.failing_test_ids = self.get_version_info()
        self.generate_coverage_files() 
        self.rank_relevant_tests()
        ...

    def clone(self):
        print('cloning the project... ', end = '')
        subprocess.run("bash ./clone_project.sh {} {}".format(self.pname, self.version), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print('done.')

    def load_relevant_tests(self):
        print('loading relevant tests... ', end = '')
        subprocess.run("bash ./relevant_tests.sh {} {}".format(self.pname, self.version), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print('done.')

    def load_failing_tests(self):
        print('loading failing tests... ', end = '')
        subprocess.run("bash ./failing_tests.sh {} {}".format(self.pname, self.version), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print('done.')

    def generate_coverage_files(self):
        print('generating coverage files...')
        rel_file_path = "./relevant_tests/relevant_{}_{}.txt".format(self.pname, self.version)
        tests = []
        with open(rel_file_path, 'r') as rf:
            tests = rf.read().splitlines()
        tests = list(map(LC.reformat_testcase, tests))
        for ti, t in tqdm(enumerate(tests), total=len(tests)):
            rc = subprocess.run("bash ./get_coverage.sh {} {} {} {}".format(self.version, ti, t, self.pname), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


    def rank_relevant_tests(self, save_file=True):
        test_covered = {}
        for i in range(self.num_of_test):
            file_path = './coverage_files/coverage_{}_{}_{}.xml'.format(self.pname, self.version, i)
            cl = get_covered_lines(file_path)
            test_covered[i] = cl

        rank = []

        covered_lines = {}
        remained_tests = list(range(self.num_of_test))

        def get_score(lines):
            new_lines = 0
            for k in lines.keys():
                covered_set = set([])
                if k in covered_lines.keys():
                    covered_set = set(covered_lines[k])
                new_covered_set = set(lines[k])
                size_new_covered = len(new_covered_set.difference(covered_set))
                new_lines += size_new_covered

            return new_lines

        def rank_remained_tests():
            id_score = {}
            for tst in remained_tests:
                score = get_score(test_covered[tst])
                id_score[tst] = score
            
            return id_score


        while remained_tests:
            id_score = rank_remained_tests()
            
            vls = id_score.values()
            mx_vl = max(vls)
            mx_ks = [k for k, v in id_score.items() if v == mx_vl]
            nid = choice(mx_ks)
            
            for k in test_covered[nid].keys():
                if k not in covered_lines.keys():
                    covered_lines[k] = set([])
                covered_lines[k].update(set(test_covered[nid][k]))
            rank.append(nid)
            remained_tests.remove(nid)


        frl = []
        for ft in self.failing_test_ids:
            frl.append(rank.index(ft)+1)

        if save_file:
            with open(self.config['DEFAULT']['OutPath']+'{}_{}.txt'.format(self.pname, self.version), 'w') as f:
                f.write('ranks:\n')
                f.write(str(rank))
                f.write('\n')
                f.write('failing ranks:')
                f.write('\n')
                f.write(str(frl))
                f.close()

        return rank, frl
        

    @staticmethod
    def reformat_testcase(tst):
        tmp = tst.split('(')
        name = tmp[0]
        tmp = tmp[1].split(')')
        path = tmp[0]
        return path+'::'+name


class BC:
    def __init__(self) -> None:
        pass