import pandas as pd
from  .Questionnaire import Questionnaire


class RCADS_P(Questionnaire):
	"""
	A class used to represent the Revised Children's Anxiety and Depression Scale - parent answers

	Attributes
	----------
	df : DataFrame
		Pandas' data frame with the specific columns
		for the questionnaire 
	grades : Series
		A column represent the child's grade (2-12)
	genders : Series
		A column represent rhe child's gender (F/M)

	Methods
	-------
	grade()
		Calculates the grading of the questionnaire. 
		The scores are scaled according to norms tables. 
	getNorm(norm_tables, grade, gender, subject_row)
		Gets the t_score for each criterion

	"""
	def __init__(self, df, grades, genders):
		"""
		Init the following arguments: 
		names = the new columns' names (after grading)
		labels = labels for the columns to be written in the SPSS output file
		values = explanation for the value for SPSS columns - empty for this questionaire 
		code_dic = a dictionary from each pharse to a number
		norm_dic = a dictionary from each grade, gender and category to sheet and column in the norm excel
		new_df = new DataFrame with the graded values
		grades = a column represent the child's grade (2-12)
		genders = a column represent rhe child's gender (F/M)
		norm_tables = DataFrame with the norm tables

		Parameters
		----------
		df : DataFrame
			Pandas data frame with the specific columns
			for the questionnaire. 
			The first column MUST represent the child's grade (2-12)
			The second column MUST represent the child's gender (F/M)
		"""
		Questionnaire.__init__(self, df)
		self.names = ["RCADS_P_SP", "RCADS_P_PD", "RCADS_P_MDD", "RCADS_P_SAD", "RCADS_P_GAD", "RCADS_P_OCD"]
		self.labels = ["Social Phobia", "Panic Disorder", "Major Depression", "Separation Anxiety", "Generalized Anxiety", "Obsessive-Compulsive"]
		self.values = {'RCADS_P_SP' : {}, 'RCADS_P_PD' : {}, 'RCADS_P_MDD' : {}, 'RCADS_P_SAD' : {}, 'RCADS_P_GAD' : {}, 'RCADS_P_OCD' : {}}
		self.code_dic = rcads_dic
		self.norm_dic = norm_dic
		self.new_df = pd.DataFrame(0,index=self.df.index,columns=self.names)
		self.grades = grades
		self.genders = genders
		self.norm_tables = pd.read_excel("norm_tables\Parent RCADS-P T-Score.xlsx", sheet_name=None)
		
	def grade(self):
		"""
		grade the questionaire according to the questionaire grading rules
				
		Returns
		----------
		DataFrame
			a new DataFrame with the new columns after grading
		"""

		rcads_p_df =  pd.DataFrame(index=self.df.index,columns=self.df.columns)
		#Iterate over the cells and convert each pharse to number (without the first and second columns)
		for i in range(self.df.shape[0]):
			for j in range(self.df.shape[1]):
				rcads_p_df.iloc[i,j] = self.code_dic[self.df.iloc[i,j]]
		#create columns with summary of all the numbers
		#summary of questions 4,7,8,12,20,30,32,38,43
		self.new_df.loc[:,"RCADS_P_SP"] = rcads_p_df.iloc[:,[3,6,7,11,19,29,31,37,42]].sum(axis=1)
		#summary of questions 3,14,24,26,28,34,36,39,41
		self.new_df.loc[:,"RCADS_P_PD"] = rcads_p_df.iloc[:,[2,13,23,25,27,33,35,38,40]].sum(axis=1)
		#summary of questions 2,6,11,15,19,21,25,29,40,47
		self.new_df.loc[:,"RCADS_P_MDD"] = rcads_p_df.iloc[:,[1,5,10,14,18,20,24,28,39,46]].sum(axis=1)
		#summary of questions 5,9,17,18,33,45,46
		self.new_df.loc[:,"RCADS_P_SAD"] = rcads_p_df.iloc[:,[4,8,16,17,32,44,45]].sum(axis=1)
		#summary of questions 1,13,22,27,35,37
		self.new_df.loc[:,"RCADS_P_GAD"] = rcads_p_df.iloc[:,[0,12,21,26,34,36]].sum(axis=1)
		#summary of questions 10,16,23,31,42,44
		self.new_df.loc[:,"RCADS_P_OCD"] = rcads_p_df.iloc[:,[9,15,22,30,41,43]].sum(axis=1)
		
		#Get the score according to norm table
		for r_i in range(len(self.new_df)):
			self.new_df.iloc[r_i] = self.getNorm(self.norm_tables, self.grades[r_i], self.genders[r_i], self.new_df.iloc[r_i])
		return self.new_df
	
	def getNorm(self,norm_tables, grade, gender, subject_row):
		"""
		Gets the t_score for each criterion
			
		Parameters
		----------
		norm_tables : Dictionary
			Dictionary between sheet's name and DataFrame
		grade: Integer
			The child's grade (2-12)
		gender: String
			The child's gender (M/F)
		subject_row: Series
			All the raw scores for each criterion (SP, PD, MDD, SAD, GAD, OCD)
		
			
		Returns
		----------
		Series
			a new row with the t-scores for each criterion 
		"""
		#Input check 
		if (grade < 2 or grade > 12):
			print ("Grade is not valid! Please insert a number between 2-12")
			exit(1)
		if (gender != 'M' and gender != 'F'):
			print ("Gender is not valid! Please insert 'M' or 'F'")
			exit(1)
		subject_t_score = pd.Series(index = subject_row.index)
		for i in range(0, len(subject_row)):
			criterion = subject_row.index[i]		
			t_score_col = norm_tables[self.norm_dic[grade]].iloc[:,self.norm_dic[criterion] + self.norm_dic[gender]]
			t_score_col = t_score_col[1:] #The first value is the criterion name 
			raw_col =  norm_tables[self.norm_dic[grade]].iloc[1:,0] #Get the RAW column and remove the first value - "RAW"
			raw_index = raw_col[raw_col == subject_row[i]].index
			subject_t_score[i] = t_score_col[raw_index]
		return subject_t_score
	
rcads_dic = {
		'תמיד' : 3,
		'בדרך כלל' : 2,
		'לפעמים' : 1,
		'אף פעם' : 0
		}
		
norm_dic = { 2 : "3rd&4rd",
			 3 : "3rd&4rd",
			 4 : "3rd&4rd", 
			 5 : "5th&6th",
			 6 : "5th&6th",
			 7 : "7th&8th",
			 8 : "7th&8th",
			 9 : "9th&10th",
			 10 : "9th&10th",
			 11 : "11th&12th",
			 11 : "11th&12th",
			 'F' : 6,
			 'M' : 0,
			 'RCADS_P_MDD' : 1,
			 'RCADS_P_GAD' : 2,
			 'RCADS_P_OCD' : 3,
			 'RCADS_P_PD' : 4,
			 'RCADS_P_SAD' : 5,
			 'RCADS_P_SP' : 6}
			 