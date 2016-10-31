#!/usr/bin/python
#-*- coding:utf-8 -*-
################################################
#File Name: findRecurrency.py
#Author: C.J. Liu
#Mail: samliu@hust.edu.cn
#Created Time: Thu 27 Oct 2016 05:36:09 PM CDT
################################################



import os,sys
from glob import glob
from collections import Counter

def usage():
	description = 	'''
	DESCRITPION:
		Find the mutation recurrency in the One tumor of all samples.
		Result like "#CHROM,POS,REF,ALT,ENSID,DESC,FEATURE,NO. RECURRENCY"
	ERROR:
		Input directory contains all added featured vcf fiels.
		Directory should be absolute directory
	'''
	if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]) or not os.path.isdir(sys.argv[1]):
		print(description)
		sys.exit(1)
	
def dataPath(path):
	path = os.path.abspath(path)
	vcfFilePath = glob(path + "/*.feature.vcf")
	return vcfFilePath
	
def getVCFInfo(f):
	'''
	Get info from vcf
	'''
	with open(f, 'r') as foo:
		keyList = list()
		for line in foo:
			if line.startswith("#"): continue
			arr = line.rstrip().split("\t")
			key = "#".join([arr[0],arr[1],arr[3],arr[4],arr[10],arr[11], arr[12]])
			keyList.append(key)
		return keyList
		
	
def run(path):
	vcfList = list()
	vcfFiles = dataPath(path)
	for vcf in vcfFiles:
		vcfList.extend(getVCFInfo(vcf))
	#print(vcfList)
	# Total variations
	# totalVariations = set.union(*map(set, vcfList))
	# print(totalVariations)
	# for v in totalVariations:
	vcfDict = dict(Counter(vcfList))
	# print(vcfDict)
	# print(len(vcfDict))
	print("#CHROM,POS,REF,ALT,ENSID,DESC,FEATURE,NO. RECURRENCY".replace(",","\t"))
	for k,v in vcfDict.items():
		k = k.split("#")
		print(*k,v,sep="\t")
	
	
def main():
	usage()
	run(sys.argv[1])

if __name__ == '__main__':
	main()

