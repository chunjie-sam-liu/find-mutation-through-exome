#!/usr/bin/python
#-*- coding:utf-8 -*-
################################################
#File Name: IntegrativeRecurrencyProcessing.py
#Author: C.J. Liu
#Mail: samliu@hust.edu.cn
#Created Time: Fri 28 Oct 2016 05:14:09 PM CDT
################################################



import os,sys
import argparse
from glob import glob
import multiprocessing
import time

sys.path.insert(0,'/home/cliu18/liucj/projects/1.Mutation_calling_in_non-condig_region_through_EXOME/0.scripts')

def usage():
	description = '''
	Task:
		The script is aimed at adding features and all data recurrency calculation.
	'''
	usage = """%(prog)s -i <bam_dir> -o <output_dir>"""
	parser = argparse.ArgumentParser(description = description,usage = usage)
	
	parser.add_argument("-i", dest = "input", type = str, help = "Input directory, The output of calling result directory, the calling result directory", required = True)
	parser.add_argument("-o", dest = "output", type = str, help = "Output directory, final recurrency result directory", default=os.getcwd())
	parser.add_argument("-n", dest = "number", type = int, help = "The number of parallel running sample, default 30", default = 20)
	parser.add_argument('-v','--version',action='version', version='%(prog)s 1.0')
	
	args = parser.parse_args()
	return args

def dataPath(path):
	'''
	The output vcf files.
	'''
	SNPPath = glob(path + "/*/*/*.SNP.filter.vcf")
	INDELPath = glob(path + "/*/*/*.INDEL.filter.vcf")
	# print(SNPPath)
	return SNPPath, INDELPath
	
def passfeature(i,snpvcf,indelvcf,recSNPDir,recINDELDir):
	'''multiprocessing part'''
	
	# SNP PART
	# pass filter 
	snp = snpvcf[i]
	snpout = recSNPDir + '/' + os.path.basename(snp).rstrip('vcf') + 'pass.vcf'
	cmd = "bash GATK.PickUpPassRecords.sh %s > %s" %(snp, snpout)
	os.system(cmd)
	# print(cmd)
	
	# Add features
	snpfea = snpout.rstrip('vcf') + 'feature.vcf'
	cmd = "python /home/cliu18/liucj/projects/1.Mutation_calling_in_non-condig_region_through_EXOME/0.scripts/addFeatureToSNV.py %s > %s" %(snpout, snpfea)
	os.system(cmd)
	# print(cmd)
	
	
	# INDEL PART
	# pass filter
	indel = indelvcf[i]
	indelout = recINDELDir + '/' + os.path.basename(indel).rstrip('vcf') + 'pass.vcf'
	cmd = "bash GATK.PickUpPassRecords.sh %s > %s" %(indel, indelout)
	os.system(cmd)
	# print(cmd)
	
	# Add feature
	indelfea = indelout.rstrip('vcf') + 'feature.vcf'
	cmd = "python /home/cliu18/liucj/projects/1.Mutation_calling_in_non-condig_region_through_EXOME/0.scripts/addFeatureToSNV.py %s > %s" %(indelout, indelfea)
	os.system(cmd)
	# print(cmd)

def filterPassandFeature(snpvcf,indelvcf,recSNPDir,recINDELDir,nthreads):
	pool = multiprocessing.Pool(processes = nthreads)
	
	for i in range(len(snpvcf)):
		pool.apply_async(passfeature, (i,snpvcf,indelvcf,recSNPDir,recINDELDir))
	pool.close()
	pool.join()
	

def run(indir, outdir, nthreads = 20):
	SNPvcf, INDELvcf = dataPath(indir)
	#print(INDELvcf)
	# output directory
	outdir = indir
	recurrency = outdir + '/recurrency'
	#Create directory
	recSNPDir =recurrency + '/SNP'
	if os.path.exists(recSNPDir):
		print(recSNPDir,"already exists")
	else:
		os.makedirs(recSNPDir)
	recINDELDir = recurrency + '/INDEL'
	if os.path.exists(recINDELDir):
		print(recINDELDir, 'already exists')
	else:
		os.makedirs(recINDELDir)
	
	#filterPass records
	filterPassandFeature(SNPvcf,INDELvcf,recSNPDir,recINDELDir,nthreads)
	
	# Find recurrency
	#SNP
	recSNPDirRecurrency = recSNPDir + '/recurrency'
	cmd = "python /home/cliu18/liucj/projects/1.Mutation_calling_in_non-condig_region_through_EXOME/0.scripts/findRecurrency.py %s %s" %(recSNPDir, recSNPDirRecurrency)
	os.system(cmd)
	
	#INDEL
	recINDELDirRecurrency = recINDELDir + '/recurrency'
	cmd = "python /home/cliu18/liucj/projects/1.Mutation_calling_in_non-condig_region_through_EXOME/0.scripts/findRecurrency.py %s %s" %(recINDELDir, recINDELDirRecurrency)
	os.system(cmd)
	
def main():
	args = usage()
	run(args.input, args.output, nthreads = args.number)

if __name__ == '__main__':
	main()

