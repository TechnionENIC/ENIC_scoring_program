import pandas as pd
import numpy as np
from  .Questionnaire import Questionnaire


class Stai(Questionnaire):
	"""
	A class used to represent an the Spielberg‏ Anxiety Questionnaire

	Attributes
	----------
	df : DataFrame
		a Pandas data frame with the specific columns
		for the questionnaire 

	Methods
	-------
	grade()
		calculates the grading of the questionnaire
	state_trait_calc()
		helper funtion for calculating the STATE/TRAIT score

	"""
	def __init__(self, df):
		"""
		Init the following arguments: 
		names = the new columns' names (after grading)
		labels = labels for the columns to be written in the SPSS output file
		values = explanation for the value for SPSS columns - empty for this questionaire 
		code_dic = a dictionary from each pharse to a number

		Parameters
		----------
		df : DataFrame
			a Pandas data frame with the specific columns
			for the questionnaire
		"""
		Questionnaire.__init__(self, df)
		self.names = ["stai_state","stai_trait"]
		self.labels = ["STAI anxiety questionnaire - state", "STAI anxiety questionnaire - trait"]
		self.values = {'stai_state' : {}, 'stai_trait' : {}}
		self.code_dic = stai
		self.new_df = pd.DataFrame(0,index=self.df.index,columns=self.names)
		
	def grade(self):
		"""
		grade the questionaire according to the questionaire grading rules
				
		Returns
		----------
		DataFrame
			a new DataFrame with the new columns after grading
		"""
		stai_questions =  pd.DataFrame(index=self.df.index,columns=self.df.columns)
		#Iterate over the cells and convert each pharse to number
		for i in range(self.df.shape[0]):
			for j in range(self.df.shape[1]):
				stai_questions.iloc[i,j] = self.code_dic[self.df.iloc[i,j]]
				
		#Calculate STATE
		E1_state = [2, 3, 5, 6, 8, 11, 12, 13, 16, 17]
		E2_state = [0, 1, 4, 7, 9, 10, 14, 15, 18, 19]
		self.new_df["stai_state"] = self.state_trait_calc(stai_questions, E1_state,E2_state)
		
		#Calculate TRAIT
		E1_trait = [21, 22, 23, 24, 27, 28, 30, 31, 33, 34, 36, 37, 39]
		E2_trait = [20, 25, 26, 29, 32, 35, 38]
		self.new_df["stai_trait"] = self.state_trait_calc(stai_questions,E1_trait,E2_trait)

		return self.new_df
		
	def state_trait_calc(self,all_questions,E1,E2):
		"""
		calculate the STATE or TRAIT score
				
		Returns
		----------
		int
			score of STATE/TRAIT
		"""
		E1_sum = np.array(all_questions.iloc[:,E1].sum(axis=1))
		E2_sum = np.array(all_questions.iloc[:,E2].sum(axis=1))
		score = E1_sum - E2_sum + 35
		return score
			
			
	
	
stai = {
		'מאוד' : 4,
		'במידה בינונית' : 3,
		'במקצת' : 2,
		'כלל לא' : 1,
		'כמעט תמיד' : 4,
		'לעיתים קרובות' : 3,
		'לפעמים' : 2,
		'כמעט אף פעם' : 1,
		
		}

	
	
