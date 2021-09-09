from xml.etree.ElementTree import VERSION
from parse import get_covered_lines
from random import choice
import pandas as pd
from tqdm import tqdm

version_tests = [77, 69, 1, 85, 88, 0, 1, 21, 89, 90, 25, 36, 427, 288, 361, 451, 98, 99, 100, 101, 435, 112, 36, 38, 38, 148, 181, 237, 302, 314, 353, 47, 48, 360, 404, 294, 65, 66, 18, 35]
version_failings = [[76], [68], [0], [39, 41], [57, 81], [], [0], [15], [39, 43], [43], [22], [26, 28, 30], [45], [28], [44, 46], [42, 43, 44, 118, 161, 197, 235], [55], [56], [55], [58], [50], [2, 80], [33, 34], [34], [34], [55], [25, 75, 146], [213], [273], [50, 53, 106, 115, 178, 181, 206, 261, 269], [209], [34, 41], [20], [79, 224], [329], [276], [64], [65], [9, 14], [34]]

def exec():
    version_results = []
    for version in range (1,41):
        if version != 6:
            num_of_test = version_tests[version-1]
            failing_tests = version_failings[version-1]
            test_covered = {}
            for i in range(num_of_test):
                file_path = './coverage_results/coverage_{}_{}.xml'.format(version, i)
                cl = get_covered_lines(file_path)
                test_covered[i] = cl

            rank = []

            # a = covered_lines['ar']
            covered_lines = {}
            remained_tests = list(range(num_of_test))

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


            while len(remained_tests) > 0:
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

            #print('----------------version: {} ---------------------'.format(version))
            #print('num of tests: ', num_of_test)
            frl = []
            for ft in failing_tests:
                frl.append(rank.index(ft)+1)

            #print('FFT: ', min(frl))

            version_results.append(min(frl))

    return version_results

final_rslts = []
for i in tqdm(range(0, 30)):
    rslt = exec()
    final_rslts.append(rslt)

df = pd.DataFrame(final_rslts)
df.to_csv('./results.csv', index=False, header=False)
