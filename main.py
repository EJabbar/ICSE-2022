import argparse
import configparser

from numpy import mod
from CV_TP import LC, BC
from one_hot_TP import OneHot
from one_hot import OneHotModel, AMD

parser = argparse.ArgumentParser(description='Testcase prioritization.')

parser.add_argument('-t', '--technique', help='TP technique to be used')
parser.add_argument('-c', '--config', help='config file for selected technique')
parser.add_argument('-p', '--pname', help='project name')
parser.add_argument('-v', '--version', help='version of project')

args = vars(parser.parse_args())

config_path = args['config']
tech = args['technique']
pname = args['pname']
version = int(args['version'])

config = configparser.ConfigParser()
config.read(config_path)

if tech == 'LC':
    print('start LC-based TP for (p:{} v:{}) ...'.format(pname, version))
    lc = LC(config, pname, version)
    lc.exec()

elif tech == 'BC':
    print('start BC-based TP for (p:{} v:{}) ...'.format(pname, version))
    bc = BC(config, pname, version)
    bc.exec()

elif tech == 'ONE-HOT':
    print('start ONE-HOT-based TP for (p:{} v:{}) ...'.format(pname, version))
    model = OneHotModel()
    num_neigbours = int(config['DEFAULT']['NumNeighbours'])
    score_calculator = AMD(num_neigbours)
    ohm = OneHot(config, pname, version, model, score_calculator)

else:
    raise ValueError('invalid technique selected')