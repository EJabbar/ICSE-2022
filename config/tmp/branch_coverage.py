from csv import reader
from pandas.core.common import flatten
import xml.etree.ElementTree as ET
from random import choice
import pandas as pd
from tqdm import tqdm
import os

version_tests = [77, 69, 1, 85, 88, 0, 1, 21, 89, 90, 25, 36, 427, 288, 361, 451, 98, 99, 100, 101, 435, 112, 36, 38, 38, 148, 181, 237, 302, 314, 353, 47, 48, 360, 404, 294, 65, 66, 18, 35]
version_failings = [[76], [68], [0], [39, 41], [57, 81], [], [0], [15], [39, 43], [43], [22], [26, 28, 30], [45], [28], [44, 46], [42, 43, 44, 118, 161, 197, 235], [55], [56], [55], [58], [50], [2, 80], [33, 34], [34], [34], [55], [25, 75, 146], [213], [273], [50, 53, 106, 115, 178, 181, 206, 261, 269], [209], [34, 41], [20], [79, 224], [329], [276], [64], [65], [9, 14], [34]]


def get_covered_lines(file_path):
    class_cvlines = {}
    if not os.path.exists(file_path):
        return class_cvlines
    tree = ET.parse(file_path)
    root = tree.getroot()
    for pkgs in root.findall('packages'):
        for pkg in pkgs.findall('package'):
            for clz in pkg.findall('classes'):
                for cls in clz.findall('class'):
                    cl_name = cls.get('name')
                    class_cvlines[cl_name] = {}
                    for ls in cls.findall('lines'):
                        for l in ls.findall('line'):
                            l_n = int(l.get('number'))
                            l_h = int(l.get('hits'))
                            class_cvlines[cl_name][l_n]= l_h
    return class_cvlines


def exec():
    version_results = []
    for version in range (1,41):
        if version != 6:
            num_of_test = version_tests[version-1]
            failing_tests = version_failings[version-1]
            types = []
            covered_branches = []
            lines_of_branches = []
            classes = []

            def get_branches():
                with open('./branches/{}.csv'.format(version), 'r') as brchcsv:
                    csv_reader = reader(brchcsv)
                    for row in csv_reader:
                        covered_branches.append([False]*(len(row)-2))
                        types.append(row[1])
                        classes.append(row[0])
                        lines_of_branches.append([int(i) for i in row[2:]])

            get_branches()

            def get_score_of_test(tstcvrdlines):
                score = 0
                for i in range(len(lines_of_branches)):
                    clsname = classes[i]
                    lines = lines_of_branches[i]
                    tp = types[i]
                    if tp == 'jump':
                        h_cnd = tstcvrdlines[clsname][lines[0]]
                        h_nxt = tstcvrdlines[clsname][lines[1]]
                        brnch_false = (h_cnd-h_nxt) > 0
                        brnch_true = h_nxt > 0
                        if brnch_false and covered_branches[i][0] == False:
                            score = score + 1
                        if brnch_true and covered_branches[i][1] == False:
                            score = score + 1
                    elif tp == 'switch':
                        for j, lbr in enumerate(lines):
                            if tstcvrdlines[clsname][lbr] > 0 and covered_branches[i][j] == False:
                                score == score + 1
                return score

            test_covered = {}
            for i in range(num_of_test):
                file_path = './coverage_results/coverage_{}_{}.xml'.format(version, i)
                cl = get_covered_lines(file_path)
                test_covered[i] = cl

            rank = []
            remained_tests = list(range(num_of_test))

            def rank_remained_tests():
                id_score = {}
                for tst in remained_tests:
                    score = get_score_of_test(test_covered[tst])
                    id_score[tst] = score
                return id_score

            def add_test_to_covered_branches(tstcvrdlines):
                for i in range(len(lines_of_branches)):
                    clsname = classes[i]
                    lines = lines_of_branches[i]
                    tp = types[i]
                    if tp == 'jump':
                        h_cnd = tstcvrdlines[clsname][lines[0]]
                        h_nxt = tstcvrdlines[clsname][lines[1]]
                        brnch_false = (h_cnd-h_nxt) > 0
                        brnch_true = h_nxt > 0
                        if brnch_false:
                            covered_branches[i][0] = True
                        if brnch_true:
                            covered_branches[i][1] = True
                    elif tp == 'switch':
                        for j, lbr in enumerate(lines):
                            if tstcvrdlines[clsname][lbr] > 0:
                                covered_branches[i][j] = True

            while len(remained_tests) > 0:
                id_score = rank_remained_tests()
                
                vls = id_score.values()
                mx_vl = max(vls)
                mx_ks = [k for k, v in id_score.items() if v == mx_vl]
                nid = choice(mx_ks)
                add_test_to_covered_branches(test_covered[nid])
                rank.append(nid)
                remained_tests.remove(nid)

            #print('----------------version: {} ---------------------'.format(version))
            #print('num of tests: ', num_of_test)
            frl = []
            for ft in failing_tests:
                frl.append(rank.index(ft)+1)

            version_results.append(min(frl))

    return version_results

final_rslts = []
for i in tqdm(range(0, 30)):
    rslt = exec()
    final_rslts.append(rslt)

df = pd.DataFrame(final_rslts)
df.to_csv('./results_BC.csv', index=False, header=False)