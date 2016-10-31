#!/usr/bin/python
#-*- coding:utf-8 -*-
################################################
#File Name: FindPromoterMutationFromExome.py
#Author: C.J. Liu
#Mail: samliu@hust.edu.cn
#Created Time: Mon 31 Oct 2016 01:13:37 PM CDT
################################################



import os,sys
import argparse

sys.insert(0,'/home/cliu18/liucj/projects/1.Mutation_calling_in_non-condig_region_through_EXOME/0.scripts')
import callVariantsOfNoncodingRegion
import IntegrativeRecurrencyProcessing


def usage():
	description='''Task:
	Find Non-coding region mutation by exome sequencing, and find recurency of mutation in one tumor. Exome sequencing protocol is to captures all exon regions of human genome, besides, it can capture some other parts of genome such as 5'utr, 3'utr, non coding regions et al. I got all regulatory feature region of human from Ensembl, and use GATK -L paramter to call mutation only on these region. Annotation of mutation site is provided. The final result of scripts are the recurent mutation site.
	'''
	usage = """%(prog)s -i <bam_dir> -o <output_dir> -n <number_of_threads"""
	parser = argparse.ArgumentParser(description = description,usage = usage)
	
	parser.add_argument("-i", dest = "input", type = str, help = "Input directory, The output of calling result directory, the calling result directory", required = True)
	parser.add_argument("-o", dest = "output", type = str, help = "Output directory, final recurrency result directory", default=os.getcwd())
	parser.add_argument("-n", dest = "number", type = int, help = "The number of parallel running sample, default 30", default = 20)
	parser.add_argument('-v','--version',action='version', version='%(prog)s 1.0')
	
	args = parser.parse_args()
	return args

def run(indir, outdir, nthreads=20):
	callVariantsOfNoncodingRegion.run(dataDir = indir, outputDir = outdir, nthread = nthreads)
	IntegrativeRecurrencyProcessing.run(indir, outdir, nthreads = nthreads)
	
def main():
	args = usage()
	run(args.input, args.output, nthreads = args.number)

if __name__ == '__main__':
	main()

