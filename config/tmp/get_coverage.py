import subprocess
from tqdm import tqdm


pname = 'Chart'
rng = 27
exc = 27

subprocess.run("bash ./clone.sh {} {} {}".format(pname, rng, exc), shell=True)
subprocess.run("bash ./relevant.sh {} {} {}".format(pname, rng, exc), shell=True)

def reformat_testcase(tst):
    tmp = tst.split('(')
    name = tmp[0]
    tmp = tmp[1].split(')')
    path = tmp[0]
    return path+'::'+name


for i in tqdm(range(1, rng)):
    if i != exc:
        rel_file_path = "./relevant_tests/relevant_{}.txt".format(i)
        tests = []
        with open(rel_file_path, 'r') as rf:
            tests = rf.read().splitlines()
        tests = list(map(reformat_testcase, tests))
        for ti, t in tqdm(enumerate(tests), total=len(tests), leave=False):
            rc = subprocess.run("bash ./get_coverage.sh {} {} {} {}".format(i, ti, t, pname), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
