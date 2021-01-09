"""Running vina docking on a group of ligands"""

# Script using the AutoDock Vina more information below
# O. Trott, A. J. Olson,                                        
# AutoDock Vina: improving the speed and accuracy of docking    
# with a new scoring function, efficient optimization and       
# multithreading, Journal of Computational Chemistry 31 (2010)  
# 455-461                                                                                                                      
# DOI 10.1002/jcc.21334                                                                                                      
# Please see http://vina.scripps.edu for more information.  

import argparse
import numpy as np
import matplotlib.pyplot as plt
import os
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from scipy.stats import pearsonr
from time import time

parser=argparse.ArgumentParser(description='Specify the parameters to run multiple docking.')
parser.add_argument('-dir','--dir', type=str, required=True, help="directory with ligands(PDBQT)")
parser.add_argument('-r','--r', type=str, required=True, help="receptor(PDBQT)")
parser.add_argument('-cx','--center_x', type=float, required=True, help="X coordinate of the center")
parser.add_argument('-cy','--center_y', type=float, required=True, help="Y coordinate of the center")
parser.add_argument('-cz','--center_z', type=float, required=True, help="Z coordinate of the center")
parser.add_argument('-sx','--size_x', type=float, required=True, help="size in the X dimension (Angstroms)")
parser.add_argument('-sy','--size_y', type=float, required=True, help="size in the Y dimension (Angstroms)")
parser.add_argument('-sz','--size_z', type=float, required=True, help="size in the Z dimension (Angstroms)")
parser.add_argument('-e','--exhaustiveness', type=int, required=False, help="exhaustiveness of the global search", default=8)
parser.add_argument('-n','--num_modes', type=int, required=False, help="maximum number of binding modes to generate", default=9)
parser.add_argument('-seed','--seed', type=int, required=False, help="random seed", default=123)
parser.add_argument('-a','--a', type=int, required=False, help="short analysis on the docking results")
args = parser.parse_args()


if __name__ == '__main__':
	#check if vina is installed and it's location
	try:
		cmd = 'type vina'
		out = subprocess.check_output(cmd, shell=True)
		out = out.decode('utf-8')
		out = out.split()[2]
	except subprocess.CalledProcessError:
		print("Couldn't find vina :(")

	# run docking in given directory
	if os.path.isdir(args.dir):
		files = [file for file in os.listdir(args.dir) if file.endswith('.pdbqt')]
		# Run docking for each pdbqt file in given directory
		start = time()
		end = 0
		for num, file in enumerate(files):
			file = args.dir + "/"+ file
			cmd = f'vina --receptor {args.r} --ligand {file} --center_x {args.center_x} --center_y {args.center_y} \
			--center_z {args.center_z} --size_x {args.size_x} --size_y {args.size_y} --size_z {args.size_z} \
			--exhaustiveness {args.exhaustiveness} --num_modes {args.num_modes} --seed {args.seed}'
			os.system(cmd)
			s_delta = time() - end
			end += s_delta
			print(f'Docking number : {num} finished with time : {s_delta}')
		delta = end - start
		print(f'Docking finished. Docking time: {delta}')

	if args.a:
		# run short analyses / Required: file names should follow a pattern name-<IC>.pdbqt
		names = []
		ic = []
		scores = []
		if os.path.isdir(args.dir):
			files = [file for file in os.listdir(args.dir) if file.endswith('out.pdbqt')]
			for file in files:
				file = args.dir + "/" + file
				print(file)
				with open(file,'r') as f :
				    lines = f.readlines()
				    for l in lines:
				    	if l.startswith('REMARK VINA RESULT'):
				    		max_val = l.split()[3]
				    		max_val = float(max_val)
				    		scores.append(max_val)
				    	if l.startswith('REMARK  Name = '):
				    		IC_val = l.split()[3]
				    		IC_val = IC_val.split('-')[1]
				    		IC_val = float(IC_val)
				    		ic.append(IC_val)
				    		break
			dict = {'Experimental': ic, 'Theoretical':scores}
			df = pd.DataFrame(dict)
			print(df)
			# calculate correlations
			corr_p, pval_p = pearsonr(df['Experimental'],df['Theoretical'])
			corr_s, pval_s = spearmanr(df['Experimental'],df['Theoretical'])
			print(f'Spearman correlation {corr_s} with p-value {pval_s}')
			print(f'Pearson correlation {corr_p} with p-value {pval_p}')
			out = args.dir + "/" + 'scores'
			df.to_csv(out)
			# plot the results
			plt.scatter(df['Experimental'],df['Theoretical'])
			plt.xlabel("Experimental")
			plt.ylabel("Theoretical")
			plt.show()
