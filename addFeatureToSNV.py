#!/usr/bin/python
#-*- coding:utf-8 -*-
################################################
#File Name: addFeatureToSNV.py
#Author: C.J. Liu
#Mail: samliu@hust.edu.cn
#Created Time: Thu 27 Oct 2016 03:40:54 PM CDT
################################################



import os,sys
import re

RegulatoryFeaturesBed = "/home/cliu18/liucj/reference/ENSEMBL/release-86/regulations/RegulatoryFeatures.gff.sortByChrom.bed"
RegulatoryFeaturesBedIndex = "/home/cliu18/liucj/reference/ENSEMBL/release-86/regulations/RegulatoryFeatures.gff.sortByChrom.bed.idx"

def usage():
	description = '''ERROR: 
	Only one input, the input must be filter.pass.vcf file
Usage:
	python addFeatureToSNV.py snp.vcf > result.vcf
	'''
	if len(sys.argv) < 2:
		print(description)
		sys.exit(1)
	
	if not sys.argv[1].endswith("vcf"):
		print(description)
		sys.exit(1)

def getInfoFromVCFandRegulatoryBed(s):
	arr = s.rstrip().split("\t")
	info = arr[0:5]
	depthInfo = arr[9].split(":")
	info.extend(depthInfo)
	# print(*info, sep="\t")
	
	# Read bed index and read file
	index = open(RegulatoryFeaturesBedIndex, 'r')
	bed = open(RegulatoryFeaturesBed, 'r')
	
	indexArr = index.readline().rstrip().split("\t")
	
	feature = [".",".","."]
	
	while indexArr[0] != arr[0] or (int(arr[1]) - int(indexArr[1])) > 1000:
		indexArr = index.readline().rstrip().split("\t")
	
	seek1 = int(indexArr[2])
	seek2 = int(indexArr[3])
	
	bed.seek(seek1)
	
	while True:
		if bed.tell() > seek2: break
		
		flag = 0
		
		bedArr = bed.readline().rstrip().split("\t")
		
		if int(bedArr[1]) <= int(arr[1]) <= int(bedArr[2]):
			feature = [bedArr[3], bedArr[6], bedArr[7]]
			flag = 1
		
		if flag == 1: break
	
	info.extend(feature)
	print(*info, sep="\t")


def run(vcf):
	title = "#" + "\t".join("CHROM,POS,ID,REF,ALT,GT,AD,DP,GQ,PL,ENSID,DESC,FEATURE".split(","))
	# print(title)
	with open(vcf ,'r') as foo:
		for line in foo:
			line = line.rstrip()
			if line.startswith("##"):
				print(line)
				continue
			elif line.startswith("#CHROM"):
				print(title)
				continue
			else:
				getInfoFromVCFandRegulatoryBed(line)
	
	
def main():
	'''
	The RegulatoryFeatures.gff was converted to sorted bed file 
	'/home/cliu18/liucj/reference/ENSEMBL/release-86/regulations/RegulatoryFeatures.gff.sortByChrom.bed'
	and I build idx to the gff 
	'/home/cliu18/liucj/reference/ENSEMBL/release-86/regulations/RegulatoryFeatures.gff.sortByChrom.bed.idx'.
	Then rearrange the format of vcf to we need. The information we need are
	CHROM,POS,ID,REF,ALT,GT,AD,DP,GQ,PL,ENSID,DESC,FEATURE
	'''
	usage()
	run(sys.argv[1])

if __name__ == '__main__':
	main()

