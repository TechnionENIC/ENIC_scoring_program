import pandas as pd
from  .Questionnaire import Questionnaire

class AIMSCon(Questionnaire):
	"""
	A class used to represent an the Affect Intensity Measure Questionnaire - Continue

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
		names = the new columns' names (after grading)
		labels = labels for column to be written in the SPSS output file
		values = explanation for the value for SPSS column - empty for this questionaire 
		code_dic = a dictionary from each pharse to a number
		new_df = new DataFrame with the graded values

		Parameters
		----------
		df : DataFrame
			a Pandas data frame with the specific columns
			for the questionnaire
		"""
		Questionnaire.__init__(self, df)
		self.names = ["AIMS_Positive", "AIMS_Negative", "AIMS_Positive_Reversed"]
		self.labels = ["Positive emotions", "Negative emotions", "Positive emotions reversed"]
		self.values = {'AIMS_Positive' : {}, 'AIMS_Negative' : {}, 'AIMS_Positive_Reversed' : {}}
		self.code_dic = aims_dic
		self.new_df = pd.DataFrame(0,index=self.df.index,columns=self.names)
	def grade(self):
		"""
		grade the questionaire according to the questionaire grading rules
				
		Returns
		----------
		DataFrame
			a new DataFrame with the new columns after grading
		"""
		aims_df =  pd.DataFrame(index=self.df.index,columns=self.df.columns)
		#Iterate over the cells and convert each pharse to number
		for i in range(self.df.shape[0]):
			for j in range(self.df.shape[1]):
				aims_df.iloc[i,j] = self.code_dic[self.df.iloc[i,j]]
		#recode the 5,10,13,15,18,20 questions
		aims_df.iloc[:,4] = self.recode(aims_df.iloc[:,4])
		aims_df.iloc[:,9] = self.recode(aims_df.iloc[:,9])
		aims_df.iloc[:,12] = self.recode(aims_df.iloc[:,12])
		aims_df.iloc[:,14] = self.recode(aims_df.iloc[:,14])
		aims_df.iloc[:,17] = self.recode(aims_df.iloc[:,17])
		aims_df.iloc[:,19] = self.recode(aims_df.iloc[:,19])
		
		#create columns with summary of all the numbers
		#summary of questions 1,2,3,7,8,9,12,16
		self.new_df.loc[:,"AIMS_Positive"] = aims_df.iloc[:,[0,1,2,6,7,8,11,15]].sum(axis=1)
		#summary of questions 4,6,11,14,17,19
		self.new_df.loc[:,"AIMS_Negative"] = aims_df.iloc[:,[3,5,10,13,16,18]].sum(axis=1)
		#summary of questions 5,10,13,15,18,20
		self.new_df.loc[:,"AIMS_Positive_Reversed"] = aims_df.iloc[:,[4,9,12,14,17,19]].sum(axis=1)

		return self.new_df
	
	def recode(self,col):
		"""
		Recode the values in a column as following:
		1=6, 2=5, 3=4, 4=3, 5=2, 6=1
		
		Parameters
        ----------
        col : Pandas Series 
            One column from DataFrame		
		Returns
		----------
		Pandas Series
			a new column after the recode
		"""
		func = lambda x : 7-x
		col = col.apply(func)
		return col

aims_dic = {
			'לעולם לא' : 1,
			'כמעט אף פעם' : 2,
			'מדי פעם' : 3,
			'בדרך כלל' : 4,
			'כמעט תמיד' : 5,
			'תמיד' : 6
			}
					  
	