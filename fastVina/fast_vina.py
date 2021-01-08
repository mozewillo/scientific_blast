"""Running vina docking on a group of ligands """

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
