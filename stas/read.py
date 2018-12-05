import numpy as np 
import re
import os
import glob
from os import walk
import json
import argparse
import sys

"""
I create a preprocessed_data folder wehere inside stuff the new files of data; ready-to-use for calculations
"""

def from_txt_to_csv(path):
	mypath=path

	l = glob.glob(mypath+'/*.dat')
	
	for el in l :
		names = os.path.splitext(el)[0]
		os.system('cp'+' '+el+' '+names+'.csv')
	

def projectors_regex(content):

	return 	re.findall('\d+\.\d*', content)	

def states_regex(content2):

	newcontent = content2.replace('{','').replace('}','').replace(' I','j').split(',')
	new = []
	newtest = []
	for el in newcontent:
		new.append(complex(''.join(el.split())))

	return new 

"""
HERE the new regex that returns string values, but properly formatted, for saving the C numbers as text files, gieven that
it's impossible to save them in others way than this

"""

def states_regex_string(content2):

	newcontent = content2.replace('{','').replace('}','').replace(' I','j').split(',')
	
	newtest = []
	for el in newcontent:
		newtest.append(''.join(el.split()))

	return newtest

def read(path):

	mypath=path
	
	fullpath1 = os.path.join(mypath,'proj.csv')
	fullpath2 = os.path.join(mypath,'states.csv')

	with open(fullpath1) as proj_data, open (fullpath2) as states_data : 

		proj_content = proj_data.readlines()
		states_content = states_data.readlines()

	""" STATES LOADING FORM FILE"""
	
	states_content = [x.strip(',').strip('\n').strip(',') for x in states_content]
	states_content = list(states_content)

	"""  STATES_CONTENT DATA RESHAPING INTO NUMPYU COMPLEX ARRAY
	arg : some  .dat file containg list of complex numbers
	return : 2 dimensional list. Each single list it's a state. Numbers inside are numpy.complex

	states_values = map(lambda x : states_regex(x), states_content[1:-1])
	states_values = list(states_values)

	"""

	"""
	STATES CONTENT data reshaped and prepared as a list of list, row a state
	arg : a .dat file containing a list of ocmplex numbers
	return: 2 dimensional list. Each list it's a state. Numbers inside in string format.
	HAving numbers in string format will allow me to save them into a new file ready for use in the calculation part

	"""

	states_values_string = map(lambda x : states_regex_string(x), states_content[1:-1])
	states_values_string = list(states_values_string)

	"""
	PROJ_CONTENT DATA RESHAPING
	"""

	proj_content = [x.strip(',').strip('\n').strip('\,') for x in proj_content]
	proj_content = list(proj_content)
	
	proj_values  = map(lambda x: projectors_regex(x), proj_content[1:-1] )
	proj_values = list(proj_values)

	proj_values = [ [float(x) for x in line] for line in proj_values]

	return proj_values, states_values_string

def dumper(project,states):

	"""
	take two list and dump them inside json files.
	Arg: 2 dimensional list of float for project, 2 dimensiona list of string for states
	return: two json files 
	"""

	with open (preprocessed_path+"/projectors_new.json ","w") as proj_, open (preprocessed_path+'/states_new.json','w') as st_:
		json.dump(project,proj_)
		json.dump(states,st_)
	
def main(argv=None):

	
	preprocessed_path = 'preprocessed_data'

	argv = sys.argv if argv is None else argv
	args = parser().parse_args(args=argv[1:])

	if not os.path.exists(preprocessed_path):
		os.makedirs(preprocessed_path)


	proj, states,  = read(argv[2])	
	dumper(proj,states)

def parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('--original_data', help = 'folders with original data')
	return parser


if __name__ == '__main__':
	main()