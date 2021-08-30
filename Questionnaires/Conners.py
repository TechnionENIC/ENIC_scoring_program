from  .Questionnaire import Questionnaire
import pandas as pd

class Conners(Questionnaire): 
	"""
	A class used to represent an the CONNERS Questionnaire

	Attributes
	----------
	df : DataFrame
		A Pandas data frame with the specific columns
		for the questionnaire 
	ages: Series
		A column represents the child's age (6-18)
	genders: Series
		A column represent rhe child's gender (F/M)

	Methods
	-------
	grade()
		Calculates the grading of the questionnaire.
	get_probability()
		Extract the probability according to raw score
	get_t_score()
		Extract the T score according to raw score and child's age and gender

	"""
	def __init__(self, df, ages, genders):
		"""
		Init the following arguments: 
		names = the new columns' names
		labels = labels for the columns to be written in the SPSS output file
		values = explanation for the value for SPSS columns - empty for this questionaire
		code_dic = a dictionary from each pharse to a number		
		new_df = new DataFrame with the graded values
		ages = a column represents the child's age (6-18)
		genders = a column represents the child's gender (F/M)
		norm_tables = DataFrame with the norm tables
		
		Parameters
		----------
		df : DataFrame
			A Pandas data frame with the specific columns
			for the questionnaire
		ages: Series
			A column with the children's age
		genders: Series
			A column with the children's gender
		"""
		Questionnaire.__init__(self, df)
		self.names = ["Conners_Raw", "Conners_Prob","Conners_T"]
		self.labels = ["Conners raw score","Conners probability","Conners T score"]
		self.values = {'Conners_T' : {}, 'Conners_Raw' : {}, 'Conners_Prob' : {}}	   
		self.code_dic = conners_dic			   
		self.new_df = pd.DataFrame(0,index=self.df.index,columns=self.names)
		self.ages = ages
		self.genders = genders
		#Open the norm tables
		self.norm_tables = pd.read_excel("norm_tables\Conners.xlsx", sheet_name=None)
		
	def grade(self):
		"""
		Grades the questionaire according to the questionaire grading rules. 
				
		Returns
		----------
		DataFrame
			A new DataFrame with the new columns 
		"""
		
		
		#Step1 - Get the score for each question according to norm table
		step1_table = self.norm_tables["Step1"]
		
		conners_df =  pd.DataFrame(index=self.df.index,columns=self.df.columns)
		#Iterate over the cells and convert each pharse to number
		#Use the Step1 table

		for i in range(self.df.shape[0]):
			for j in range(self.df.shape[1]):				
				score = self.code_dic[self.df.iloc[i,j]]
				conners_df.iloc[i,j] = step1_table.iloc[j,score]
				
		#Get the raw score by summing all the scores 
		self.new_df['Conners_Raw'] = conners_df.sum(axis=1)

		#Get the probability from step2
		self.new_df['Conners_Prob'] = self.new_df['Conners_Raw'].apply(self.get_probability)

		#Get the T score - Step3
		for p_i in range(len(self.new_df['Conners_Raw'])):
			self.new_df['Conners_T'][p_i] = self.get_t_score(self.new_df['Conners_Raw'][p_i], self.ages[p_i], self.genders[p_i])
			
		return self.new_df
			
	def get_probability(self,score):
		"""
		Get the probability according to the raw score and probability table 
		
		Parameters
		----------
		score : int
			The raw score
			
		Returns
		----------
		int
			The probability 
		"""
		step2_table = self.norm_tables["Step2"]
		return int(step2_table[step2_table['Raw Score'] == score]['Probability'])
	
	def get_t_score(self,raw_score,age, gender):
		"""
		Get the T score according to the raw score, age, gender and T scores table
		
		Parameters
		----------
		raw_score : int
			The raw score
		age: int
			child's age (6-18)
		gender : str
			child's gender ('M'/'F')
			
		Returns
		----------
		int
			The T score 
		"""
		#Input check 
		if (age < 6 or age > 18):
			print ("Age is not valid! Please insert a number between 6-18")
			exit(1)
		if (gender != 'M' and gender != 'F'):
			print ("Gender is not valid! Please insert 'M' or 'F'")
			exit(1)
	
		#Get the right norm table
		if (gender == 'M'):
			step3_table = self.norm_tables["Step3-Male"]
		else :
			step3_table = self.norm_tables["Step3-Female"]
		#Get the age column
		age_col = step3_table[age]
		#Find the raw score in the age column
		raw_score_index = age_col[age_col == raw_score].index.values
		#Get the T score
		t_score = step3_table['T'].iloc[raw_score_index]
		return t_score

		
		
		
conners_dic = {
			'אף פעם או לעתים רחוקות' : 0,
			'לפעמים' : 1,
			'לעיתים תכופות' : 2,
			'בדרך כלל' : 3,
			}
				
		