import argparse
import configparser
from CV_TP import LC, BC

parser = argparse.ArgumentParser(description='Testcase prioritization.')

parser.add_argument('--technique', help='TP technique to be used')
parser.add_argument('--config', help='config file for selected technique')
parser.add_argument('--pname', help='project name')
parser.add_argument('--version', help='version of project')

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

else:
    raise ValueError('invalid technique selected')