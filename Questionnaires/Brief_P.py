import pandas as pd
from  .Questionnaire import Questionnaire
import numpy as np

class Brief_P(Questionnaire):
	"""
	A class use to represent the Child Brief Questionnaire

	Attributes
	----------
	df : DataFrame
		A Pandas data frame with the specific columns
		for the questionnaire 
		
	guardian_col : series
		column of 'parent' or 'teacher' - the person how filled the questionaire

	Methods
	-------
	grade()
		Calculates the grading of the questionnaire
	grade_inhibit()
		Calculates the grading of the inhibit scale
	grade_shift()
		Calculates the grading of the shift scale
	grade_emotional_control()
		Calculates the grading of the emotional control scale
	grade_wm()
		Calculates the grading of the working memory scale
	grade_plan()
		Calculates the grading of the plan scale
	grade_negativity()
		Calculates the grading of the negativity scale: raw score, percentage and classification
	grade_negativity_perc()
		Calculates the grading of the negativity percentage, used by grade_negativity() function
	grade_negativity_class()
		Calculates the grading of the negativity classification, used by grade_negativity() function
	grade_consistency()
		Calculates the grading of the consistency scale: raw score, percentage and classification
	grade_consistency_perc()
		Calculates the grading of the consistency percentage, used by grade_consistency() function
	grade_consistency_class()
		Calculates the grading of the consistency classification, used by grade_consistency() function
	"""
	
	def __init__(self, df, guardian_col):
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
		guardian: Series
			column of 'parent' or 'teacher' - the person how filled the questionaire
		"""
	
		Questionnaire.__init__(self, df)
		self.names = ["Brief_P_Inhibit_r", "Brief_P_Shift_r", "Brief_P_Emotional_control_r", "Brief_P_Working_memory_r", "Brief_P_Plan_r", "Brief_P_Negativity_r", 
						"Brief_P_Negativity_perc", "Brief_P_Negativity_class", "Brief_P_Consistency_r", "Brief_P_Consistency_perc", "Brief_P_Consistency_class", "Brief_P_ISCI_r", "Brief_P_FI_r", "Brief_P_EMI_r", "Brief_P_GER_r"]
		self.labels = ["Brief_P Inhibit raw score ", "Brief_P Shift raw score", "Brief_P Emotional control raw score", "Brief_P Working memory raw score", "Brief_P Plan raw score",
							 "Brief_P Negativity raw score", "Brief_P Negativity percentage", "Brief_P Negativity classification", "Brief_P Consistency raw score",
							 "Brief_P Consistency percentage", "Brief_P Consistency classification", "ISCI raw score", "FI raw score", "EMI  raw score", "GER raw score"]
		self.values = {'Brief_P_Inhibit_r' : {}, 'Brief_P_Shift_r' : {}, 'Brief_P_Emotional_control_r' : {}, 'Brief_P_Working_memory_r' : {},
						'Brief_P_Plan_r' : {}, 'Brief_P_Negativity_r' : {}, 'Brief_P_Negativity_perc' : {1: '0-97', 2: '0-98', 3: '98-99', 4: '99', 5: '100'},
						'Brief_P_Negativity_class' : {1: 'normal', 2:'high'}, 'Brief_P_Consistency_r' : {}, 'Brief_P_Consistency_perc' : {1: '0-94', 2: '0-98', 3:'97-98', 4: '99', 5: '99-100', 6: '100'}, 
						'Brief_P_Consistency_class' : {1: 'normal', 2:'not consistent'}, 'Brief_P_ISCI_r' : {}, 'Brief_P_FI_r' : {}, 'Brief_P_EMI_r' : {}, 'Brief_P_GER_r' : {}}
		self.new_df = pd.DataFrame(0,index=self.df.index,columns=self.names)
		self.code_dic = Brief_dic
		self.guardian_col = guardian_col
	
	def grade(self):
		"""
		Grades the questionaire according to the questionaire grading rules
				
		Returns
		----------
		DataFrame
			a new DataFrame with the new columns after grading
		"""
		brief_questions =  pd.DataFrame(index=self.df.index,columns=self.df.columns)
		#Iterate over the cells and convert each pharse to number
		for i in range(self.df.shape[0]):
			for j in range(self.df.shape[1]):
				brief_questions.iloc[i,j] = self.code_dic[self.df.iloc[i,j]]
				
		functions = [self.grade_inhibit, self.grade_shift, self.grade_emotional_control, self.grade_wm, self.grade_plan, self.grade_negativity, 
					self.grade_consistency]
		for func in functions:
			func(brief_questions)
		self.new_df["Brief_P_ISCI_r"] = self.new_df["Brief_P_Inhibit_r"] + self.new_df["Brief_P_Emotional_control_r"]
		self.new_df["Brief_P_FI_r"] =  self.new_df["Brief_P_Shift_r"] + self.new_df["Brief_P_Emotional_control_r"]
		self.new_df["Brief_P_EMI_r"] = self.new_df["Brief_P_Working_memory_r"] + self.new_df["Brief_P_Plan_r"]
		self.new_df["Brief_P_GER_r"] = self.new_df["Brief_P_Inhibit_r"] + self.new_df["Brief_P_Shift_r"] + self.new_df["Brief_P_Emotional_control_r"] + self.new_df["Brief_P_Working_memory_r"] + self.new_df["Brief_P_Plan_r"]
		return self.new_df
	
	def grade_inhibit(self, all_questions):
		"""
		Grade inhibit scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief_P questions after coding
		"""
				#3, 8, 13, 18, 23, 28, 33, 38, 43, 48, 52, 54, 56, 58, 60, 62 
		cols = [2, 7, 12, 17, 22, 27, 32, 37, 42, 47, 51, 53, 55, 57, 59, 61]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_P_Inhibit_r"] = sum
	def grade_shift(self, all_questions):
		"""
		Grade shift scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief_P questions after coding
		"""
			#5, 10, 15, 20, 25, 30, 35, 40, 45, 50
		cols = [4, 9, 14, 19, 24, 29, 34, 39, 44, 49]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_P_Shift_r"] = sum
	def grade_emotional_control(self, all_questions):
		"""
		Grade emotional control scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief_P questions after coding
		"""
				#1, 6, 11, 16, 21, 26, 31, 36, 41, 46 
		cols = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_P_Emotional_control_r"] = sum
	def grade_wm(self, all_questions):
		"""
		Grade working memory scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief_P questions after coding
		"""
				#2, 7, 12, 17, 22, 27, 32, 37, 42, 47, 51, 53, 55, 57, 59, 61, 63 
		cols = [1, 6, 11, 16, 21, 26, 31, 36, 41, 46, 50, 52, 54, 56, 58, 60, 62]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_P_Working_memory_r"] = sum
	def grade_plan(self, all_questions):
		"""
		Grade plan scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief_P questions after coding
		"""
				#4, 9, 14, 19, 24, 29, 34, 39, 44, 49 
		cols = [3, 8, 13, 18, 23, 28, 33, 38, 43, 48]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_P_Plan_r"] = sum
	def grade_negativity(self, all_questions):
		"""
		Grade negativity scale: raw score, percentage and classification
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief_P questions after coding
		"""
				#30, 44, 46, 47, 53, 55, 56, 57, 59, 63
		cols = [29, 43, 45, 46, 52, 54, 55, 56, 58, 62]
		#Count all the values that are 3
		count = all_questions.iloc[:,cols][all_questions.iloc[:,cols] == 3].count(axis=1)
		self.new_df["Brief_P_Negativity_r"] = count
		for i in range(len(self.new_df)):
			self.new_df['Brief_P_Negativity_perc'][i] = self.grade_negativity_perc(count[i], self.guardian_col[i])
			self.new_df['Brief_P_Negativity_class'][i] = self.grade_negativity_class(count[i], self.guardian_col[i])
		
	def grade_negativity_perc(self, score, guardian):
		"""
		Grade negativity percantage
				
		Parameters
		----------
		score: int
			negativity score
		
		guardian : string
			'parent' or 'teacher' 
			
		Returns
		----------
		int
			percentage coding number
			
		"""
		perc = 0
		neg_class = 0
		if(guardian == 'parent'):
			if (score <= 2):
				perc = 1 # 0-97
			elif (score == 3):
				perc = 3 #98-99
			else:
				perc = 5 #100
		elif(guardian == 'teacher'):
			if (score <= 2):
				perc = 2 #0-98
			elif (score == 3):
				perc = 4 #99
			else:
				perc = 5 #100
		else:
			print("Brief_P Negativity : guardian invalid!")
		return perc
			
	def grade_negativity_class(self, score, guardian):
		"""
		Grade negativity classification
				
		Parameters
		----------
		score: int
			negativity score
		
		guardian : string
			'parent' or 'teacher'
			
		Returns
		----------
		int
			classification coding number
			
		"""
		neg_class = 0
		if(guardian == 'parent'):
			if (score <= 2):
				neg_class = 1 #normal
			elif (score == 3):
				neg_class = 1 #normal
			else:
				neg_class = 2 #high
		elif(guardian == 'teacher'):
			if (score <= 2):
				neg_class = 1 #normal
			elif (score == 3):
				neg_class = 2 #high
			else:
				neg_class = 2 #high
		else:
			print("Brief_P Negativity : guardian invalid!")
		return neg_class
		
	def grade_consistency(self, all_questions):
		"""
		Grade consistency scale: raw score, percentage and classification
				
		Parameters
		----------
		all_questions : DataFrame
			all Brief_P questions after coding
		"""
				#1, 3, 5, 10, 11, 16, 18, 33, 43, 48
		cols1 = [0, 2, 4, 9, 10, 15, 17, 32, 42, 47]
				#11, 33, 45, 20, 26, 21, 52, 38, 52, 54
		cols2 = [10, 32, 44, 19, 25, 20, 51, 37, 51, 53]
		diff_all = []
		for pair in list(zip(all_questions.iloc[:,cols1],all_questions.iloc[:,cols2])):
			diff = list(all_questions[pair[0]] - all_questions[pair[1]])
			diff = list(map(abs, diff))
			diff_all.append(diff)
		diff_all = pd.DataFrame(diff_all)
		sum = diff_all.sum(axis=0)
		self.new_df["Brief_P_Consistency_r"] = sum
		
		for i in range(len(self.new_df)):
			self.new_df['Brief_P_Consistency_perc'][i] = self.grade_consistency_perc(sum[i], self.guardian_col[i])
			self.new_df['Brief_P_Consistency_class'][i] = self.grade_consistency_class(sum[i], self.guardian_col[i])
		
	def grade_consistency_perc(self, score, guardian):
		"""
		Grade consistency percantage
				
		Parameters
		----------
		score: int
			consistency score
		
		guardian : string
			'parent' or 'teacher'
			
		Returns
		----------
		int
			percentage coding number
		"""
		perc = 0
		if(guardian == 'parent'):
			if(score <= 6):
				perc = 1 # 0-94
			elif(score == 7):
				perc = 3 # 97-98
			else:
				perc = 5 # 99-100
		elif(guardian == 'teacher'):
			if(score <= 6):
				perc = 2 # 0-98
			elif(score == 7):
				perc = 4 # 99
			else:
				perc = 6 # 100
		else:
			print("Brief_P Consistency : guardian invalid!")
		return perc
	
	def grade_consistency_class(self, score, guardian):
		"""
		Grade consistency classification
				
		Parameters
		----------
		score: int
			consistency score
			
		guardian : string
			'parent' or 'teacher'
			
		Returns
		----------
		int
			classification coding number
			
		"""
		cons_class = 0
		if(guardian == 'parent'):
			if(score <= 6):
				cons_class = 1 #normal
			elif(score == 7):
				cons_class = 1 #normal
			else:
				cons_class = 2 #not consistent
		elif(guardian == 'teacher'):
			if(score <= 6):
				cons_class = 1 #normal
			elif(score == 7):
				cons_class = 2 #not consistent
			else:
				cons_class = 2 #not consistent
		else:
			print("Brief_P Consistency : guardian invalid!")
		return cons_class

	
Brief_dic = {
		'אף פעם לא' : 1,
		'לפעמיים' : 2,
		'לעיתים קרובות\תמיד' : 3,
		}