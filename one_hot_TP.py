import numpy as np
from CV_TP import TP
from parse import get_covered_lines
from one_hot import OneHotModel, AMD

class OneHot(TP):
    
    def __init__(self, config, pname, version, one_hot_model):
        super().__init__(config, pname, version)
        self.one_hot_model = one_hot_model


    def exec(self):
        super().exec()
        return self.rank_relevant_tests()

    def rank_relevant_tests(self, save_file=True):
        rel_file_path = './relevant_tests/relevant_{}_{}.txt'.format(self.pname, self.version)
        tests = []
        with open(rel_file_path, 'r') as rf:
            tests = rf.read().split()

        def reformat_tests(tst):
            tmp = tst.split('(')
            test_name = tmp[0]
            tmp = tmp[1].split(')')
            tmp = tmp[0].split('.')
            class_name = tmp[len(tmp)-1]
            return [class_name, test_name]

        tests = list(map(reformat_tests, tests))

        tst_file_path = './traces/{}{}/data.test.txt'.format(self.pname, self.version)
        traces = []
        with open(tst_file_path, 'r') as rf:
            traces = rf.read().split('<NEXT_TEST>')

        idx = []
        idx_rel = []
        rel_traces = []
        st_tst_names = set([])
        st_cls_names = set([])
        for i, t in enumerate(traces):
            tmp = t.split(' ', 2)
            if tmp[0] != '':
                cls_name = tmp[0]
                tst_name = tmp[1]
                st_tst_names.add(tst_name)
                st_cls_names.add(cls_name)
                for ir, tst in enumerate(tests):
                    if tst_name == tst[1] and cls_name in tst[0]:
                        idx.append(i)
                        idx_rel.append(ir)
                        rel_traces.append([ir, tmp[0], tmp[1], tmp[2]])


        def get_score(lines):
            new_lines = 0
            for k in lines.keys():
                new_covered_set = set(lines[k])
                new_lines += len(new_covered_set)
            return new_lines

        rankd_rel_traces = []
        for rt in rel_traces:
            fp = './coverage_files/coverage_{}_{}_{}.xml'.format(self.pname, self.version, rt[0])
            cv_lines = get_covered_lines(fp)
            sc = get_score(cv_lines)
            tmp = rt
            tmp.append(sc)
            rankd_rel_traces.append(tmp)

        rankd_rel_traces = sorted(rankd_rel_traces, key=lambda x: x[4], reverse=True)


        embeddin_model = OneHotModel()
        model_all_traces = []
        for rt in rankd_rel_traces:
            model_all_traces.append(rt[3])

        embeddin_model.fit(model_all_traces)

        rnkd_rel_traces_embd = []
        for rt in rankd_rel_traces:
            embd = embeddin_model.generate_embedding(rt[3])
            tmp = rt
            tmp.append(embd)
            rnkd_rel_traces_embd.append(tmp)

        # if len(rnkd_rel_traces_embd) == 0:
        #         all_ranks.append(1)
        #         all_norm_ranks.append(100)
        #         return

        rank = []
        frank = rnkd_rel_traces_embd.pop(0)
        rank.append(frank[0])
        vcs = []
        vcs.append(frank[5])

        amd = AMD()
        def calculate_distance_from_NNs(e):
            new_test_case_vec = np.array(e).reshape(1, -1)
            test_suite_vecs = np.array(vcs)
            amd_score = amd.calculate_score(test_suite_vecs, new_test_case_vec)
            return amd_score

        while len(rnkd_rel_traces_embd) > 0:
            for r in rnkd_rel_traces_embd:
                s = calculate_distance_from_NNs(r[5])
                r[2] = s

            rnkd_rel_traces_embd = sorted(rnkd_rel_traces_embd, key=lambda x: x[2], reverse=True)

            frank = rnkd_rel_traces_embd.pop(0)
            rank.append(frank[0])
            vcs.append(frank[5])


        def find_rank(fti):
            if fti in rank:
                return rank.index(fti)+1
            return len(rank)

        failing_ranks = list(map(find_rank, self.failing_test_ids))

        if save_file:
            with open(self.config['DEFAULT']['OutPath']+'ONEHOT_{}_{}.txt'.format(self.pname, self.version), 'w') as f:
                f.write('ranks:\n')
                f.write(str(rank))
                f.write('\n')
                f.write('failing ranks:')
                f.write('\n')
                f.write(str(failing_ranks))
                f.close()

        return rank, failing_ranks
