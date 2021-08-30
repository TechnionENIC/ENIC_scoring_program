from  .Questionnaire import Questionnaire
import pandas as pd

class STIMQ(Questionnaire): 
	"""
	A class used to represent an the STIMQ Questionnaire

	Attributes
	----------
	df : DataFrame
		A Pandas data frame with the specific columns
		for the questionnaire 

	Methods
	-------
	grade()
		Calculates the grading of the questionnaire.
		In this case the same values as the input (hours)

	"""
	def __init__(self, df):
		"""
		Init the following arguments: 
		names = the new columns' names
		labels = labels for the columns to be written in the SPSS output file
		values = explanation for the value for SPSS columns - empty for this questionaire 
		new_df = new DataFrame with the graded values
		
		Parameters
		----------
		df : DataFrame
			A Pandas data frame with the specific columns
			for the questionnaire
		"""
		Questionnaire.__init__(self, df)
		self.names = ["STIMQ_child_q1","STIMQ_child_q2","STIMQ_child_q3","STIMQ_child_q4","STIMQ_parent_q5","STIMQ_parent_q6","STIMQ_parent_q7",
						"STIMQ_parent_q8","STIMQ_parent_q9"]
		self.labels = ["How many hours a day does your child spend in front of the screen (TV, computer, tablet, cell phone)?", 
						"How many hours a day does your child spend playing in front of a screen?",
						"How many hours a day does your child spend passively watching the screen?",
						"How many hours a day does your child use the screen to read a book or for educational purposes?",
						"How many hours a day do you spend in front of the screen (TV, computer, tablet, cell phone)?",
						"How many hours a day do you spend playing in front of a screen?", 
						"How many hours a day do you spend passively watching the screen?",
						"How many hours a day do you use the screen to read a book or for educational purposes?",
						"How many hours a day do you spend in front of a book / newspaper?"]
		self.values = {'STIMQ_child_q1' : {}, 'STIMQ_child_q2' : {}, 'STIMQ_child_q3' : {}, 'STIMQ_child_q4' : {}, 'STIMQ_parent_q5' : {},
						'STIMQ_parent_q6' : {}, 'STIMQ_parent_q7' : {}, 'STIMQ_parent_q8' : {}, 'STIMQ_parent_q9' : {}}
					   
					   
		self.new_df = pd.DataFrame(0,index=self.df.index,columns=self.names)
		
	def grade(self):
		"""
		Grades the questionaire according to the questionaire grading rules. 
		In this case the values in the new DataFrame are the same as in the input DataFrame. 
		The only change is the columns names
				
		Returns
		----------
		DataFrame
			A new DataFrame with the new columns 
		"""
		self.df.columns = self.names 
		return self.df
		