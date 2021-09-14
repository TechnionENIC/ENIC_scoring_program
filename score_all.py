#!/usr/bin/python3

import os, sys, argparse
from bs4 import BeautifulSoup
import pandas as pd
import pyreadstat
from Questionnaires.Stai import Stai
from Questionnaires.BeckDepression import BeckDepression
from Questionnaires.ScreenQ import ScreenQ
from Questionnaires.PRFC import PRFC
from Questionnaires.AIMS import AIMS
from Questionnaires.AIMSCon import AIMSCon
from Questionnaires.STIMQ import STIMQ
from Questionnaires.RCADS_P import RCADS_P
from Questionnaires.CoronaEnxiety import CoronaEnxiety
from Questionnaires.Conners import Conners
from Questionnaires.Brief_by_Parent import Brief_by_Parent
from Questionnaires.Brief_A import Brief_A
from Questionnaires.CBCL import CBCL

import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")


	
def excel_column_number(name):
	"""
	Convert Excel-style column name to number, e.g., A = 1, Z = 26, AA = 27, AAA = 703.
		
	Parameters
	----------
	name : string
		Excel-style column name
			
	Returns
	----------
	Integer
		The column number
	"""

	n = 0
	for c in name:
		n = n * 26 + 1 + ord(c) - ord('A')
	return n
	
def excel_column_name(n):
	"""
	Convert number to excel-style column name to number, e.g., 1 = A, 26 = Z, 27 = AA, 703 = AAA.
		
	Parameters
	----------
	name : integer
		The column number
			
	Returns
	----------
	string
		The column excel-style name
	"""
	name = ''
	while n > 0:
		n, r = divmod (n - 1, 26)
		name = chr(r + ord('A')) + name
	return name
	
	
def list_of_letters(begin, end):
	"""
	Receive two excel-style column names, begin and end, and returns list of the the columns names
	between begin and end

	e.g. for list_of_letters('A', 'D'), the function will return ['A', 'B', 'C', 'D']
		
	Parameters
	----------
	begin : string
		The beginning column name
		
	end : string
		The ending column name
			
	Returns
	----------
	list of strings
		List of the the columns names between begin and end 
	"""
	num_begin = excel_column_number(begin)
	num_end = excel_column_number(end)
	numbers = list(range(num_begin, num_end+1))
	letters = list(map(excel_column_name,numbers))
	return letters

def age_months_to_year(age_months):
	"""
	Convert age in months to age in years
		
	Parameters
	----------
	name : integer
		Age in months
			
	Returns
	----------
	integer
		The column excel-style name
	"""
	return int(age_months / 12)
	
	
if __name__ == "__main__":
	# Reading the data inside the xml
	with open('param.xml', 'r') as f:
		data = f.read()
	 
	# Parse all data from xml file
	q_data = BeautifulSoup(data, "xml")
	 
	input_file = q_data.find('input_file').string
	out_folder = q_data.find('output_folder').string
	if out_folder == None:
		out_folder = '.'
	age_col = q_data.find('age_col').string
	gender_col = q_data.find('gender_col').string
	grade_col = q_data.find('grade_col').string
	questionnaire_params = q_data.find('questionnaire_params')
	
 
	df_data = pd.read_excel(input_file)
	#Convert the columns names to the excel-style names
	col_list = [ excel_column_name(i) for i in range(1,len(df_data.columns)+1) ]
	df_data.columns = col_list
	
	
	#For SPSS output
	column_labels = []
	variable_value_labels = {}
	new_df = pd.DataFrame()
	
	#Iterate over the questionaires
	children = questionnaire_params.findChildren(recursive=False)
	for q in children:
		print(q.name)
		begin_col = q.find("begin_col").string
		end_col = q.find("end_col").string
		q_class = None
		if (q.name == "RCADS_P"):
			if (grade_col == None):
				print("!!!Insert grade column!!!\n")
				continue
			if (gender_col == None):
				print("!!!Insert gender column!!!\n")
				continue
			#Convert string to class
			q_class = getattr(sys.modules[__name__], q.name)(df_data[list_of_letters(begin_col, end_col)], df_data[grade_col], df_data[gender_col])
		elif (q.name == "Conners"):
			if (age_col == None):
				print("!!!Insert age column!!!\n")
				continue
			if (gender_col == None):
				print("!!!Insert gender column!!!\n")
				continue
			#Convert age column to years
			age_col_years = df_data[age_col].apply(age_months_to_year)
			#Convert string to class
			q_class = getattr(sys.modules[__name__], q.name)(df_data[list_of_letters(begin_col, end_col)], age_col_years, df_data[gender_col])
		else:
			q_class = getattr(sys.modules[__name__], q.name)(df_data[list_of_letters(begin_col, end_col)])
		if(q_class is not None):
			new_df = pd.concat([new_df, q_class.grade()], axis=1)
			variable_value_labels.update(q_class.values)
			for label in q_class.labels:
				column_labels.append(label)
		

	pyreadstat.pyreadstat.write_sav(new_df,os.path.join(out_folder,"output.sav"),column_labels = column_labels, 
			variable_value_labels = variable_value_labels)

		
