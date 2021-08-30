import pandas as pd
from  .Questionnaire import Questionnaire
import re

class PRFC(Questionnaire):
	"""
	A class used to represent an the The Parental Reflective Functioning Questionnaire

	Attributes
	----------
	df : DataFrame
		a Pandas data frame with the specific columns
		for the questionnaire 

	Methods
	-------
	grade()
		calculate the grading of the questionnaire
	
	recode(col)
		recode each number in a column to the opposite number
	"""
	def __init__(self, df):
		"""
		Init the following arguments: 
		names = the new columns' names (after grading)
		labels = labels for each column to be written in the SPSS output file
		values = explanation for the values in each SPSS column - empty for this questionaire 
		new_df = new DataFrame with the graded values

		Parameters
		----------
		df : DataFrame
			a Pandas data frame with the specific columns
			for the questionnaire
		"""
		Questionnaire.__init__(self, df)
		self.names = ["PRFQ_PM", "PRFQ_CM", "PRFQ_IC"]
		self.labels = ["PRFQ Pre-Mentalizing Modes", "PRFQ Certainty about Mental States", "PRFQ Interest and Curiosity in Mental States"]
		self.values = {'PRFQ_PM' : {}, 'PRFQ_CM' : {}, 'PRFQ_IC' : {}}
		self.new_df = pd.DataFrame(0,index=self.df.index,columns=self.names)
	def grade(self):
		"""
		grade the questionaire according to the questionaire grading rules
				
		Returns
		----------
		DataFrame
			a new DataFrame with the new columns after grading
		"""
		prfc_df =  pd.DataFrame(index=self.df.index,columns=self.df.columns)
		#Iterate over the cells and convert to number if needed
		for i in range(self.df.shape[0]):
			for j in range(self.df.shape[1]):
				if (type(self.df.iloc[i,j]) == str):
					prfc_df.iloc[i,j] = int(re.findall("\d",self.df.iloc[i,j])[0])
				else:
					prfc_df.iloc[i,j] = self.df.iloc[i,j]
		
		#recode questions 11 and 18
		prfc_df.iloc[:,10] = self.recode(prfc_df.iloc[:,10])
		prfc_df.iloc[:,17] = self.recode(prfc_df.iloc[:,17])
		#calculate mean
		self.new_df.loc[:,"PRFQ_PM"] = prfc_df.iloc[:,[0,3,6,9,12,15]].mean(axis=1)
		self.new_df.loc[:,"PRFQ_CM"] = prfc_df.iloc[:,[1,4,7,10,13,16]].mean(axis=1)
		self.new_df.loc[:,"PRFQ_IC"] = prfc_df.iloc[:,[2,5,8,11,14,17]].mean(axis=1)
		return self.new_df
		
	def recode(self, col):
		"""
		Recode the values in a column as following:
		1=7, 2=6, 3=5, 4=4, 5=3, 6=2, 7=1
		
		Parameters
        ----------
        col : Pandas Series 
            One column from DataFrame		
		Returns
		----------
		Pandas Series
			a new column after the recode
		"""
		func = lambda x : 8-x
		col = col.apply(func)
		return col
					  
	