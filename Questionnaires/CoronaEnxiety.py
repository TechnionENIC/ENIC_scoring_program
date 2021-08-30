import pandas as pd
from  .Questionnaire import Questionnaire
import re

class CoronaEnxiety(Questionnaire):
	"""
	A class used to represent the Corona Enxiety Questionnaire

	Attributes
	----------
	df : DataFrame
		A Pandas data frame with the specific columns
		for the questionnaire 

	Methods
	-------
	grade()
		Calculates the grading of the questionnaire
	
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
		self.names = ["CAS", "OCS"]
		self.labels = ["The coronavirus anxiety scale", "Obsession with COVID scale"]
		self.values = {'CAS' : {}, 'OCS' : {}}
		self.new_df = pd.DataFrame(0,index=self.df.index,columns=self.names)
	def grade(self):
		"""
		Grades the questionaire according to the questionaire grading rules
				
		Returns
		----------
		DataFrame
			a new DataFrame with the new columns after grading
		"""
		corona_df =  pd.DataFrame(index=self.df.index,columns=self.df.columns)
		#Iterate over the cells and convert to number if needed
		for i in range(self.df.shape[0]):
			for j in range(self.df.shape[1]):
				if (type(self.df.iloc[i,j]) == str):
					corona_df.iloc[i,j] = int(re.findall("\d",self.df.iloc[i,j])[0])
				else:
					corona_df.iloc[i,j] = self.df.iloc[i,j]
		
		#summary
		self.new_df.loc[:,"CAS"] = corona_df.iloc[:,[0,1,2,3,4]].sum(axis=1)
		self.new_df.loc[:,"OCS"] = corona_df.iloc[:,[5,6,7,8]].sum(axis=1)
		return self.new_df

	