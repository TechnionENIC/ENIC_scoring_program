import pandas as pd
from  .Questionnaire import Questionnaire
import numpy as np

class Brief_by_Parent(Questionnaire):
	"""
	A class use to represent the Child Brief Questionnaire answered by the parent

	Attributes
	----------
	df : DataFrame
		A Pandas data frame with the specific columns
		for the questionnaire 
		

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
	grade_initiate ()
		Calculates the grading of the initiate scale
	grade_organization_of_materials ()
		Calculates the grading of organization of materials scale
	grade_monitor()
		Calculates the grading of monitor scale
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
		self.names = ["Brief_Inhibit_r", "Brief_Shift_r", "Brief_Emotional_control_r", "Brief_Initiate_r", "Brief_Working_memory_r", "Brief_Plan_r", "Brief_OOM_r", "Brief_Monitor_r",
						"Brief_Negativity_r", "Brief_Negativity_perc", "Brief_Negativity_class", "Brief_Consistency_r", "Brief_Consistency_perc",
						"Brief_Consistency_class", "Brief_BRI_r", "Brief_MI_r", "Brief_GEC_r"]
		self.labels = ["Brief Inhibit raw score ", "Brief Shift raw score", "Brief Emotional control raw score", "Brief Initiate raw score", "Brief Working memory raw score",
							"Brief Plan raw score", "Brief Organization of Materials raw score","Brief Monitor raw score",
							 "Brief Negativity raw score", "Brief Negativity percentage", "Brief Negativity classification", "Brief Consistency raw score",
							 "Brief Consistency percentage", "Brief Consistency classification", "Behavioral Regulation raw score", "Metacognition raw score", 
							 "Global Executive Composite raw score"]
		self.values = {'Brief_Inhibit_r' : {}, 'Brief_Shift_r' : {}, 'Brief_Emotional_control_r' : {}, 'Brief_Initiate_r' : {}, 'Brief_Working_memory_r' : {},
						'Brief_Plan_r' : {}, 'Brief_OOM_r' : {}, 'Brief_Monitor_r' : {}, 'Brief_P_Negativity_r' : {}, 'Brief_Negativity_perc' : {1: '<=90', 2: '91-98', 3: '>98'},
						'Brief_Negativity_class' : {1:'Acceptable', 2:'Elevated', 3:'Highly elevated'}, 'Brief_Consistency_r' : {}, 'Brief_Consistency_perc' : {1: '<=98', 2: '99', 3:'>99'}, 
						'Brief_Consistency_class' : {1: 'Acceptable', 2:'Questionable', 3:'Inconsistent'}, 'Brief_BRI_r' : {}, 'Brief_MI_r' : {}, 'Brief_GEC_r' : {}}
		self.new_df = pd.DataFrame(0,index=self.df.index,columns=self.names)
		self.code_dic = Brief_dic
	
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
				
		functions = [self.grade_inhibit, self.grade_shift, self.grade_emotional_control, self.grade_wm, self.grade_initiate, self.grade_plan, 
					self.grade_organization_of_materials, self.grade_monitor, self.grade_negativity, self.grade_consistency]
		for func in functions:
			func(brief_questions)
		self.new_df["Brief_BRI_r"] = self.new_df["Brief_Inhibit_r"] + self.new_df["Brief_Shift_r"] + self.new_df["Brief_Emotional_control_r"]
		self.new_df["Brief_MI_r"] =  self.new_df["Brief_Initiate_r"] + self.new_df["Brief_Working_memory_r"] + self.new_df["Brief_Plan_r"] + self.new_df["Brief_OOM_r"] + self.new_df["Brief_Monitor_r"]
		self.new_df["Brief_GEC_r"] = self.new_df["Brief_BRI_r"] + self.new_df["Brief_MI_r"]
		return self.new_df
	
	def grade_inhibit(self, all_questions):
		"""
		Grade inhibit scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief_P questions after coding
		"""
			   #38, 41, 43, 49, 54, 55, 56, 59, 65  
		cols = [37, 40, 42, 48, 53, 54, 55, 58, 64]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_Inhibit_r"] = sum
	def grade_shift(self, all_questions):
		"""
		Grade shift scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief questions after coding
		"""
			   #5, 6, 8, 12, 13, 23, 30, 39
		cols = [4, 5, 7, 11, 12, 22, 29, 38]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_Shift_r"] = sum
	def grade_emotional_control(self, all_questions):
		"""
		Grade emotional control scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief questions after coding
		"""
			   #1, 7, 20, 25, 26, 45, 50, 62, 64, 70 
		cols = [0, 6, 19, 24, 25, 44, 49, 61, 63, 69]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_Emotional_control_r"] = sum
	def grade_wm(self, all_questions):
		"""
		Grade working memory scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief questions after coding
		"""
			   #2, 9, 17, 19, 24, 27, 32, 33, 37, 57 
		cols = [1, 8, 16, 18, 23, 26, 31, 32, 36, 56 ]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_Working_memory_r"] = sum
	def grade_plan(self, all_questions):
		"""
		Grade plan scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief questions after coding
		"""
			   #11, 15, 18, 22, 28, 35, 36, 40, 46, 51, 53, 58
		cols = [10, 14, 17, 21, 27, 34, 35, 39, 45, 50, 52, 57 ]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_Plan_r"] = sum
		
	def grade_initiate(self, all_questions):
		"""
		Grade initiate scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief questions after coding
		"""
			   #3, 10, 16, 47, 48, 61, 66, 71 
		cols = [2, 9, 15, 46, 47, 60, 65, 70 ]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_Initiate_r"] = sum
		
	def grade_organization_of_materials(self, all_questions):
		"""
		Grade organization of materials - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief questions after coding
		"""
			   #4, 29, 67, 68, 69, 72  
		cols = [3, 28, 66, 67, 68, 71]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_OOM_r"] = sum
		
	def grade_monitor(self, all_questions):
		"""
		Grade monitor scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief questions after coding
		"""
			   #14, 21, 31, 34, 42, 52, 60, 63 
		cols = [13, 20, 30, 33, 41, 51, 59, 62]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_Monitor_r"] = sum
		
	def grade_negativity(self, all_questions):
		"""
		Grade negativity scale: raw score, percentage and classification
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief_P questions after coding
		"""
			   #8, 13, 23, 30, 62, 71, 80, 83, 85
		cols = [7, 12, 22, 29, 61, 70, 79, 82, 84]
		#Count all the values that are 3
		count = all_questions.iloc[:,cols][all_questions.iloc[:,cols] == 3].count(axis=1)
		self.new_df["Brief_Negativity_r"] = count
		for i in range(len(self.new_df)):
			self.new_df['Brief_Negativity_perc'][i] = self.grade_negativity_perc(count[i])
			self.new_df['Brief_Negativity_class'][i] = self.grade_negativity_class(count[i])
		
	def grade_negativity_perc(self, score):
		"""
		Grade negativity percantage
				
		Parameters
		----------
		score: int
			negativity score 
			
		Returns
		----------
		int
			percentage coding number
			
		"""
		perc = 0
		if (score <= 4):
			perc = 1 # <=90
		elif (score >= 7):
			perc = 3 #>98
		else:
			perc = 2 #91 - 98
		return perc
			
	def grade_negativity_class(self, score):
		"""
		Grade negativity classification
				
		Parameters
		----------
		score: int
			negativity score
			
		Returns
		----------
		int
			classification coding number
			
		"""
		neg_class = 0
		if (score <= 4):
			neg_class = 1 #Acceptable
		elif (score >= 7):
			neg_class = 3 #Highly elevated
		else:
			neg_class = 2 #Elevated
		return neg_class
		
	def grade_consistency(self, all_questions):
		"""
		Grade consistency scale: raw score, percentage and classification
				
		Parameters
		----------
		all_questions : DataFrame
			all Brief_P questions after coding
		"""
				#7, 11, 27, 33, 38, 41, 42, 44, 53, 55
		cols1 = [6, 10, 26, 32, 37, 40, 41, 43, 52, 54]
				#25, 22, 17, 32, 59, 65, 63, 54, 60, 44
		cols2 = [24, 21, 16, 31, 58, 64, 62, 53, 59, 43]
		diff_all = []
		for pair in list(zip(all_questions.iloc[:,cols1],all_questions.iloc[:,cols2])):
			diff = list(all_questions[pair[0]] - all_questions[pair[1]])
			diff = list(map(abs, diff))
			diff_all.append(diff)
		diff_all = pd.DataFrame(diff_all)
		sum = diff_all.sum(axis=0)
		self.new_df["Brief_Consistency_r"] = sum
		
		for i in range(len(self.new_df)):
			self.new_df['Brief_Consistency_perc'][i] = self.grade_consistency_perc(sum[i])
			self.new_df['Brief_Consistency_class'][i] = self.grade_consistency_class(sum[i])
		
	def grade_consistency_perc(self, score):
		"""
		Grade consistency percantage
				
		Parameters
		----------
		score: int
			consistency score
			
		Returns
		----------
		int
			percentage coding number
		"""
		perc = 0
		if(score <= 6):
			perc = 1 # <=98
		elif(score >=9):
			perc = 3 # >99
		else:
			perc = 2 # 99
		return perc
	
	def grade_consistency_class(self, score):
		"""
		Grade consistency classification
				
		Parameters
		----------
		score: int
			consistency score
			
		Returns
		----------
		int
			classification coding number
			
		"""
		cons_class = 0
		if(score <= 6):
			cons_class = 1 #Acceptable
		elif(score >= 9):
			cons_class = 3 #Inconsistent
		else:
			cons_class = 2 #Questionable
		return cons_class

	
Brief_dic = {
		'אף פעם לא' : 1,
		'לפעמיים' : 2,
		'לעיתים קרובות\תמיד' : 3,
		}