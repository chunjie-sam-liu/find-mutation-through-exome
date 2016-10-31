#!/usr/bin/python
#-*- coding:utf-8 -*-
################################################
#File Name: callTotalVariantsOf.BRCA.KIRC.py
#Author: C.J. Liu
#Mail: samliu@hust.edu.cn
#Created Time: Tue 25 Oct 2016 11:04:40 AM CDT
################################################



import os,sys
import __future__
import argparse
import json
import os.path
import multiprocessing
from glob import glob

root = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, '/home/cliu18/liucj/pipelines/exome_pipeline/bin/')

# Use previous exome pipeline scripts.
import callVariants3

# Data on server Leng-1 
#BRCA_WXS_20
# data = '/home/cliu18/liucj/projects/1.Mutation_calling_in_non-condig_region_through_EXOME/1.data/WXS/BRCA_WXS_20'

# KIRC_WXS_20
data='/home/cliu18/liucj/projects/1.Mutation_calling_in_non-condig_region_through_EXOME/1.data/WXS/KIRC_WXS_20'

# GRCh38 reference data 
index = '/home/cliu18/liucj/pipelines/exome_pipeline/data/hg38/genomeBuild/hg38.fasta'

def usage():
	description = '''
		Task: Call variants from TCGA bam files.
		Server caculation available: 48 threads, 512 memory, 23T available in /extraspace. We are not allowed to excess the caculation limit.
		Specification: 
			1. Now we have 20 BRCA and 20 KIRC samples. Later on, we will use about 1000 BRCA samples. The script needs to use multihtreads and multipross to run on the server. Maybe, the server Leng-2 can be used. 
			2. Considering the recurrency (intersections) of samples, in need to traves the total samples. It's a big problem. The recurrency(intersections, travesing) is the other script.
			3. The storage is not enough for storing all data, the bam file maybe deleted after calling.
			4. The bam mapping reference is hg38, the optional hg19 is not provided.
	Output: The results are filtered calling vcf files.
	'''
	
	usage = """%(prog)s -i <bam_dir> -o <output_dir>"""
	
	parser = argparse.ArgumentParser(description = description,usage = usage)
	
	parser.add_argument("-i", dest = "input", type = str, help = "Input directory, default is current directory", default=os.getcwd())
	parser.add_argument("-o", dest = "output", type = str, help = "Output directory, default is current directory", default=os.getcwd())
	parser.add_argument("-n", dest = "number", type = int, help = "The number of parallel running sample, default 10", default = 15)
	parser.add_argument('-v','--version',action='version', version='%(prog)s 1.0')
	
	args = parser.parse_args()
	return args
	
def dataPath(path):
	"""
	The datapath is the root path of total data of all cancer type, the current data is in /home/cliu18/liucj/data/WXS. Now, I use BRCA data set for test.
	"""
	bamFilePath = glob(path + "/*/*.bam")
	return bamFilePath

def callVariants(bam, indir, output):
	'''
	Use previous exome pipeline scripts.
	'''
	rawvcf, out = callVariants3.gatkCall(bam,indir,output, index,t=10)
	
def batchRun(bamFilePath, outputDir, nthread=15):
	'''
	run ten samples at one time,# Use multiprocessing.pool to creat 10 pool processing
	'''
	
	# Multiprocessing 
	jobs = []
	pool = multiprocessing.Pool(processes = nthread)
	
	for bamPath in bamFilePath:
		# bamPath = bamFilePath[1]
		bamInput = os.path.dirname(bamPath)
		bamName = os.path.basename(bamPath)
		bamOutDir = outputDir + "/" + os.path.basename(bamInput)
		
		# callVariants(bamName, bamInput, bamOutDir)
		pool.apply_async(callVariants, (bamName, bamInput, bamOutDir))
	pool.close()
	pool.join()
	
def run(dataDir, outputDir, nthread):
	# Specify BRCA path
	# dataDir = data
	
	#The absolute bam files locations
	bamFilePath = dataPath(dataDir)
	
	batchRun(bamFilePath, outputDir, nthread)
	
def main():
	args = usage()
	run(dataDir = args.input, outputDir = args.output, nthread = args.number)

if __name__ == '__main__':
	main()

