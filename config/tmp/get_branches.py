import xml.etree.ElementTree as ET
import pandas as pd
from tqdm import tqdm
import os

rng = 41
expt = 6
lst_swtch = []

def get_covered_lines(file_path, version):
    class_cvlines = []
    if not os.path.exists(file_path):
        return class_cvlines
    tree = ET.parse(file_path)
    root = tree.getroot()
    for pkgs in root.findall('packages'):
        for pkg in pkgs.findall('package'):
            for clz in pkg.findall('classes'):
                for cls in clz.findall('class'):
                    is_branch = False
                    cl_name = cls.get('name')
                    for ls in cls.findall('lines'):
                        for l in ls.findall('line'):
                            l_n = int(l.get('number'))
                            l_h = int(l.get('hits'))
                            if is_branch:
                                is_branch = False
                                class_cvlines[len(class_cvlines)-1].append(l_n)
                            if l.get('branch') == 'true':
                                is_branch = True
                                nrow = []
                                nrow.append(cl_name)
                                cnds = l.find('conditions')
                                cnd = cnds.find('condition')
                                tp = cnd.get('type')
                                if tp == 'switch':
                                    lst_swtch.append('there is a switch in: {}'.format(version))
                                nrow.append(tp)
                                nrow.append(l_n)
                                class_cvlines.append(nrow)

    return class_cvlines

for version in tqdm(range(1, rng)):
    if version != expt:
        rslt = get_covered_lines('./coverage_results/coverage_{}_0.xml'.format(version), version)
        df = pd.DataFrame(rslt)
        df.to_csv('./branches/{}.csv'.format(version), index=False, header=False)


for item in lst_swtch:
    print(item)

