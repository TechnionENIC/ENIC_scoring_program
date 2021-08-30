import pandas as pd
from  .Questionnaire import Questionnaire
import numpy as np


class CBCL(Questionnaire):
	"""
	A class use to represent the CBCL 6-18 Questionnaire

	Attributes
	----------
	df : DataFrame
		A Pandas data frame with the specific columns
		for the questionnaire 

	Methods
	-------
	grade()
		Calculates the grading of the questionnaire
	grade_p_relate()
		Convert from text to score the relatedness of the person filling out the questionnaire
	grade_g_gender()
		Convert from text to score the gender of the person filling out the questionnaire
	grade_anxdep()
		Calculates the scoring of the anxiety/depression scale
	grade_withdep()
		Calculates the scoring of the withdrawal/depression scale
	grade_somatic()
		Calculates the scoring of the somatic complaints scale
	grade_social()
		Calculates the scoring of the social problems scale
	grade_thought()
		Calculates the scoring of the thought problems scale
	grade_attention()
		Calculates the scoring of the attention problems scale
	grade_rulebreak()
		Calculates the scoring of the rule-breaking scale
	grade_aggressive()
		Calculates the scoring of the aggressive behaviour scale
	grade_other()
		Calculates the scoring of the other problems scale
		***Please note: Question 113 was not included in the calculation because it was written as an open question 
		and could not be calculated automatically 
		
	"""
	
	def __init__(self, df):
		"""
		Init the following arguments: 
		names = the new columns' names (after grading)
		labels = labels for each column to be written in the SPSS output file
		values = explanation for the values in each SPSS column
		new_df = new DataFrame with the graded values

		Parameters
		----------
		df : DataFrame
			a Pandas data frame with the specific columns
			for the questionnaire

		"""
	
		Questionnaire.__init__(self, df)
		self.names = ["cbcl_father_Prof", "cbcl_mother_Prof", "cbcl_child_relate", "cbcl_g_gender","cbcl_anxdep_r", "cbcl_withdep_r",
						"cbcl_somatic_r", "cbcl_social_r", "cbcl_thought_r", "cbcl_attention_r", "cbcl_rulebreak_r", "cbcl_aggressive_r", "cbcl_other_r", 
						"cbcl_internalizing_r", "cbcl_externalizing_r", "cbcl_other_sum_r", "cbcl_all_r"]
		self.labels = ["father's profession","cbcl mother's profession", "relatedness to the child", "guardian's gender", "cbcl anxiety/depression raw score", 
						"cbcl withdrawal/depression raw score", "cbcl somatic complaints raw score", "cbcl social problems raw score", 
						"cbcl thought problems raw score", "cbcl attention problems raw score", "cbcl rule-breaking raw score", "cbcl aggressive behaviour raw score", 
						"cbcl other problems raw score", "cbcl internalizing scale raw score", "cbcl externalizing scale raw score", "cbcl other remaining scale raw score", 
						"cbcl summary of all scales raw score"]
		self.values = {'cbcl_father_Prof' : {}, 'cbcl_mother_Prof' : {}, 'cbcl_child_relate' : {1: 'biological parent', 2: 'step parent', 3: 'grandfather/grandmother',
						4: 'adoptive parent', 5: 'parent in a foster family', 6: 'other'}, 'cbcl_g_gender' : {1: 'Male', 2: 'Female'}, 'cbcl_anxdep_r' : {}, 
							'cbcl_withdep_r' : {}, 'cbcl_somatic_r' : {}, 'cbcl_social_r' : {}, 'cbcl_thought_r' : {}, 'cbcl_attention_r' : {}, 'cbcl_rulebreak_r' : {},
							'cbcl_aggressive_r' : {}, 'cbcl_other_r' : {}, 'cbcl_internalizing_r' : {}, 'cbcl_externalizing_r' : {}, 'cbcl_other_sum_r' : {}, 'cbcl_all_r' : {}}
		self.new_df = pd.DataFrame(0,index=self.df.index,columns=self.names)
		self.code_dic = cbcl_dic
		
	def grade(self):
		"""
		Grades the questionaire according to the questionaire grading rules
		*** Plaese note: Question 113 was not included in the calculation because it was written as an open question 
		and could not be calculated automatically. It affects the following scales: cbcl_other_r, cbcl_other_sum_r, cbcl_all_r
		
		
		Returns
		----------
		DataFrame
			a new DataFrame with the new columns after grading
		"""
		
		self.new_df["cbcl_father_Prof"] = self.df.iloc[:,0]
		self.new_df["cbcl_mother_Prof"] = self.df.iloc[:,1]
		self.new_df["cbcl_child_relate"] = self.grade_p_relate(self.df.iloc[:,2])
		self.new_df["cbcl_g_gender"] = self.grade_g_gender(self.df.iloc[:,3])
		
		#Discard questions 5-35 and the last (113) 
		cbcl_questions =  self.df.iloc[:,36:self.df.shape[1]-1]
		cbcl_questions_coded = pd.DataFrame(index=cbcl_questions.index,columns=cbcl_questions.columns)
		#Iterate over the cells and convert each pharse to number
		for i in range(cbcl_questions.shape[0]):
			for j in range(cbcl_questions.shape[1]):
				cbcl_questions_coded.iloc[i,j] = self.code_dic[cbcl_questions.iloc[i,j]]

		functions = [self.grade_anxdep, self.grade_withdep, self.grade_somatic, self.grade_social, self.grade_thought, self.grade_attention, 
					self.grade_rulebreak, self.grade_aggressive, self.grade_other]
		for func in functions:
			func(cbcl_questions_coded)
		
		self.new_df["cbcl_internalizing_r"] = self.new_df["cbcl_anxdep_r"] + self.new_df["cbcl_withdep_r"] + self.new_df["cbcl_somatic_r"]
		self.new_df["cbcl_externalizing_r"] = self.new_df["cbcl_rulebreak_r"] + self.new_df["cbcl_aggressive_r"]
		self.new_df["cbcl_other_sum_r"] = self.new_df["cbcl_thought_r"] + self.new_df["cbcl_attention_r"]  + self.new_df["cbcl_social_r"]   + self.new_df["cbcl_other_r"]  
		self.new_df["cbcl_all_r"] = self.new_df["cbcl_other_sum_r"] + self.new_df["cbcl_externalizing_r"] + self.new_df["cbcl_internalizing_r"]
		return self.new_df
		
	def grade_p_relate(self, p_relate_col):
		"""
		Convert from text to score the relatedness of the person filling out the questionnaire
				
		Parameters
		----------
		p_relate_col: Series
			column with the relatedness data
		"""
		p_relate_dic = {'הורה ביולוגי' : 1, 
						'הורה חורג' : 2,
						'סבא\ סבתא' : 3,
						'הורה מאמץ' : 4, 
						'הורה במשפחת אומנה' : 5,
						'אחר (פרט)' : 6
						}
		return p_relate_col.map(p_relate_dic)
		
	def grade_g_gender(self, g_gender_col):
		"""
		Convert from text to score the gender of the person filling out the questionnaire
				
		Parameters
		----------
		p_relate_col: Series
			column with the gender data
		"""
		g_gender_dic = { 'זכר' : 1,
						 'נקבה' : 2,
						}
		return g_gender_col.map(g_gender_dic)
		
	def grade_anxdep(self, all_questions):
		"""
		Grade anxiety/depression scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all cbcl questions after coding
		"""
		#Till question 55 the order is the same,question 56 is divided to 8 sub questions
		#so after question 56 need to add 7 to the question number
			   #14, 29, 30, 31, 32, 33, 35, 45, 50, 52, 71, 	91, 	112
		cols = [13, 28, 29, 30, 31, 32, 34, 44, 49, 51, 70 + 7, 90 + 7, 111 + 7]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["cbcl_anxdep_r"] = sum
		
	def grade_withdep(self, all_questions):
		"""
		Grade withdrawal/depression scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all cbcl questions after coding
		"""
		#Till question 55 the order is the same,question 56 is divided to 8 sub questions
	    #so after question 56 need to add 7 to the question number
			   #5, 42, 65, 	   69,     75,     102,     103,     111,
		cols = [4, 41, 64 + 7, 68 + 7, 74 + 7, 101 + 7, 102 + 7, 110 + 7]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["cbcl_withdep_r"] = sum
		
	def grade_somatic(self, all_questions):
		"""
		Grade somatic complaints scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all cbcl questions after coding
		"""
			   #47, 49, 51, 54, 56a,56b,    56c,    56d,    56e,    56f,    56g
		cols = [46, 48, 50, 53, 55, 55 + 1, 55 + 2, 55 + 3, 55 + 4, 55 + 5, 55 + 6]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["cbcl_somatic_r"] = sum
		
	def grade_social(self, all_questions):
		"""
		Grade social problems scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all cbcl questions after coding
		"""
		#Till question 55 the order is the same,question 56 is divided to 8 sub questions
	    #so after question 56 need to add 7 to the question number	
			   #11, 12, 25, 27, 34, 36, 38, 48, 62, 	64,		79
		cols = [10, 11, 24, 26, 33, 35, 37, 47, 61 + 7, 63 + 7, 78 + 7] 
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["cbcl_social_r"] = sum
		
	def grade_thought(self, all_questions):
		"""
		Grade thought problems scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all cbcl questions after coding
		"""
		#Till question 55 the order is the same,question 56 is divided to 8 sub questions
	    #so after question 56 need to add 7 to the question number	
			   #9, 18, 40, 46, 58,	   59,	   60,	   66,	   70,	   76,	   83,	   84,	   85,	   92,	   100
		cols = [8, 17, 39, 45, 57 + 7, 58 + 7, 59 + 7, 65 + 7, 69 + 7, 75 + 7, 82 + 7, 83 + 7, 84 + 7, 91 + 7, 99 + 7] 
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["cbcl_thought_r"] = sum
		
	def grade_attention(self, all_questions):
		"""
		Grade attention problems scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all cbcl questions after coding
		"""
		#Till question 55 the order is the same,question 56 is divided to 8 sub questions
	    #so after question 56 need to add 7 to the question number	
			   #1, 4, 8, 10, 13, 17, 41,61,     78,     80 
		cols = [0, 3, 7, 9, 12, 16, 40, 60 + 7, 77 + 7, 79 + 7] 
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["cbcl_attention_r"] = sum
		
	def grade_rulebreak(self, all_questions):
		"""
		Grade rule-breaking scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all cbcl questions after coding
		"""
		#Till question 55 the order is the same,question 56 is divided to 8 sub questions
	    #so after question 56 need to add 7 to the question number	
			   #2, 26, 28, 39, 43, 63, 	   67,     72, 	   73, 	   81, 	   82,     90,     96,     99,     101,     105,     106 
		cols = [1, 25, 27, 38, 42, 62 + 7, 66 + 7, 71 + 7, 72 + 7, 80 + 7, 81 + 7, 89 + 7, 95 + 7, 98 + 7, 100 + 7, 104 + 7, 105 + 7] 
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["cbcl_rulebreak_r"] = sum
		
	def grade_aggressive(self, all_questions):
		"""
		Grade aggressive behaviour scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all cbcl questions after coding
		"""
		#Till question 55 the order is the same,question 56 is divided to 8 sub questions
	    #so after question 56 need to add 7 to the question number	
			   #3, 16, 19, 20, 21, 22, 23, 37, 57,	   68,     86,     87,     88,     89,     94,     95,     97,     104 
		cols = [2, 15, 18, 19, 20, 21, 22, 36, 56 + 7, 67 + 7, 85 + 7, 86 + 7, 87 + 7, 88 + 7, 93 + 7, 94 + 7, 96 + 7, 103 + 7] 
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["cbcl_aggressive_r"] = sum
		
	def grade_other(self, all_questions):
		"""
		Grade other problems scale: raw score
		***
		Please note: Question 113 was not included in the calculation because it was written as an open question 
		and could not be calculated automatically
		***
				
		Parameters
		----------
		all_questions: DataFrame
			all cbcl questions after coding
		"""
		#Till question 55 the order is the same,question 56 is divided to 8 sub questions
	    #so after question 56 need to add 7 to the question number	
			   #6, 7, 15, 24, 44, 53, 55, 56h, 	  74,     77,     93,     98,     107,     108,     109,     110 
		cols = [5, 6, 14, 23, 43, 52, 54, 55 + 7, 73 + 7, 76 + 7, 92 + 7, 97 + 7, 106 + 7, 107 + 7, 108 + 7, 109 + 7] 
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["cbcl_other_r"] = sum


cbcl_dic = { 'לא נכון (עד כמה שידוע לך)' : 0,
			'נכון לפעמים או במידת מה' : 1, 
			'נכון מאוד או לעיתים קרובות' : 2
			}
			
