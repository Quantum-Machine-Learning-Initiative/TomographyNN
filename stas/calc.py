import numpy as np 
import os
import re
from numpy import linalg as LA

proj = [
[-0.707107,0.707107,0.,0.,0.,0.],
[0.707107,0.707107,0.,0.,0.,0.],
[0.,0.,0.,0.,0.,1.],
[0.,0.,0.,0.,1.,0.],
[0.,0.,0.,1.,0.,0.],
[0.,0.,1.,0.,0.,0.],
[-0.707107,0.,0.707107,0.,0.,0.],
[0.707107,0.,0.707107,0.,0.,0.],
[0.,1.,0.,0.,0.,0.],
[0.,-0.707107,0.707107,0.,0.,0.],
[0.,0.707107,0.707107,0.,0.,0.],
[1.,0.,0.,0.,0.,0.],
[-0.707107,0.,0.,0.707107,0.,0.],
[0.707107,0.,0.,0.707107,0.,0.],
[0.,-0.707107,0.,0.707107,0.,0.],
[0.,0.707107,0.,0.707107,0.,0.],
[0.,0.,-0.707107,0.707107,0.,0.],
[0.,0.,0.707107,0.707107,0.,0.],
[-0.707107,0.,0.,0.,0.707107,0.],
[0.707107,0.,0.,0.,0.707107,0.],
[0.,-0.707107,0.,0.,0.707107,0.],
[0.,0.707107,0.,0.,0.707107,0.],
[0.,0.,-0.707107,0.,0.707107,0.],
[0.,0.,0.707107,0.,0.707107,0.],
[0.,0.,0.,-0.707107,0.707107,0.],
[0.,0.,0.,0.707107,0.707107,0.],
[-0.707107,0.,0.,0.,0.,0.707107],
[0.707107,0.,0.,0.,0.,0.707107],
[0.,-0.707107,0.,0.,0.,0.707107],
[0.,0.707107,0.,0.,0.,0.707107],
[0.,0.,-0.707107,0.,0.,0.707107],
[0.,0.,0.707107,0.,0.,0.707107],
[0.,0.,0.,-0.707107,0.,0.707107],
[0.,0.,0.,0.707107,0.,0.707107],
[0.,0.,0.,0.,-0.707107,0.707107],
[0.,0.,0.,0.,0.707107,0.707107]
]

state = np.array([0.111892 + 0.523052j,-0.108129 - 0.0432387j, 0.343178 + 0.282662j, \
	 -0.0795876 - 0.188787j, 0.17109 + 0.453712j, 0.377329 + 0.288423j])



""" DENSITY MATRIX AND OUTER PRODUCT FOR MATRICE M OF PROJECTOR """

def outer_prod_projector(proj):

	return  np.outer(np.conjugate(proj),proj)

def density_matrix(state):

	return np.outer(np.conjugate(state),state)

""" READ INPUTS """ 

def read():

	mypath = 'datas/'
	
	fullpath = os.path.join(mypath,'proj.csv')
	with open(fullpath) as proj_data:

		content = proj_data.readlines()
	content = [x.strip(',').strip('\n').strip('\,') for x in content]
	print(content)
	content = list(content)
	
	m =  re.findall('\d+\.\d*', content[1])	

	print([ float(x) for x in m])

#SEVERAL ATTEMPTS FOR CALCULATE BOHR RULE
	
def mixeddensity(state,proj):

	#HERE my supposed-mixed density matrix
	mixdens = np.eye(6,6)*(np.conjugate(state)*state)
	

	#calculate the expectations values with projectors
	return np.trace(np.matmul(proj, np.matmul(proj,mixdens)))

def expectation(projector,state):

	return np.cumsum( np.conjugate(state)*(np.matmul(projector,state)))[-1]

def expectationtrace(projector):

	return np.trace(np.matmul(np.outer(np.conjugate(state),state),projector))

def withouterprods(proj,density_m):

	return np.trace(np.matmul(proj,np.matmul(proj, density_m )))

def lastxperiment(proj,state):



	M = np.array(proj)

	L = np.matmul(np.conjugate(state),M)
	D = np.matmul(state,M)
	return np.cumsum(L*D)[-1]

def main():

	density_m = density_matrix(state)
	proje2 = outer_prod_projector(proj[1])
	print(proj)
	#newdens = mixeddensity(state,projector)
	#print(proj)
	
	print("")

	my_good = map(lambda x : lastxperiment(x,state), proj)
	my_good = np.array(list(my_good))

	tot = np.cumsum(my_good)[-1]
	
	print("")

	print('THAT S MY GOOD NORMALIZED {mygood}'.format(mygood = my_good/float(tot)))
	print(" ")
	print(tot)
	print(np.cumsum(my_good/float(tot))[-1])


if __name__=='__main__':
	main()