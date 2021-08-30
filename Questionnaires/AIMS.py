import pandas as pd
from  .Questionnaire import Questionnaire

class AIMS(Questionnaire):
	"""
	A class used to represent an the Affect Intensity Measure Questionnaire

	Attributes
	----------
	df : DataFrame
		a Pandas data frame with the specific columns
		for the questionnaire 

	Methods
	-------
	grade()
		calculate the grading of the questionnaire

	"""
	def __init__(self, df):
		"""
		Init the following arguments: 
		name = the new column name (after grading)
		labels = labels for column to be written in the SPSS output file
		values = explanation for the value for SPSS column - empty for this questionaire 
		self.code_dic = a dictionary from each pharse to a number

		Parameters
		----------
		df : DataFrame
			a Pandas data frame with the specific columns
			for the questionnaire
		"""
		Questionnaire.__init__(self, df)
		self.name = "AIMS_General"
		self.labels = ["Affect Intensity Measure - General"]
		self.values = {'AIMS_General' : {}}
		self.code_dic = aims_dic
	def grade(self):
		"""
		grade the questionaire according to the questionaire grading rules
				
		Returns
		----------
		Pandas Series
			a new column with the new values after grading
		"""
		aims_df =  pd.DataFrame(index=self.df.index,columns=self.df.columns)
		#Iterate over the cells and convert each pharse to number
		for i in range(self.df.shape[0]):
			for j in range(self.df.shape[1]):
				aims_df.iloc[i,j] = self.code_dic[self.df.iloc[i,j]]
		
		#create a column with summary of all the numbers
		new_series = aims_df.sum(axis=1)
		new_series.name = self.name
		return new_series
		

aims_dic = {
			'לעולם לא' : 1,
			'כמעט אף פעם' : 2,
			'מדי פעם' : 3,
			'בדרך כלל' : 4,
			'כמעט תמיד' : 5,
			'תמיד' : 6
			}
					  
	