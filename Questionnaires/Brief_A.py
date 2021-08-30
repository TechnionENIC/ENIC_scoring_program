import pandas as pd
from  .Questionnaire import Questionnaire
import numpy as np

class Brief_A(Questionnaire):
	"""
	A class use to represent the Parent Brief Questionnaire

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
	grade_self_monitor()
		Calculates the grading of the self-monitor scale
	grade_initiate()
		Calculates the grading of the initiate scale
	grade_wm()
		Calculates the grading of the working memory scale
	grade_plan()
		Calculates the grading of the plan scale
	grade_task_monitor()
		Calculates the grading of task monitor scale
	grade_organization_of_materials()
		Calculates the grading of organization of materials scale
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
	grade_infrequency()
		Calculates the grading of the infrequency scale: raw score, percentage and classification
	grade_infrequency_perc()
		Calculates the grading of the infrequency percentage, used by grade_infrequency() function
	grade_infrequency_class()
		Calculates the grading of the infrequency classification, used by grade_infrequency() function
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
		self.names = ["Brief_A_Inhibit_r", "Brief_A_Shift_r", "Brief_A_Emotional_control_r", "Brief_A_Self_monitor_r","Brief_A_Initiate_r", "Brief_A_WM_r",
						"Brief_A_Plan_r", "Brief_A_Task_monitor_r", "Brief_A_OOM", "Brief_A_Negativity_r", "Brief_A_Negativity_perc", "Brief_A_Negativity_class",
						"Brief_A_Consistency_r", "Brief_A_Consistency_perc", "Brief_A_Consistency_class", "Brief_A_Infrequency_r", "Brief_A_Infrequency_perc", "Brief_A_Infrequency_class",
						"Brief_A_BRI_r", "Brief_A_MI_r", "Brief_A_GER_r"]
		self.labels = ["Brief_A Inhibit raw score ", "Brief_A Shift raw score", "Brief_A Emotional control raw score", "Brief_A self-monitor raw score","Brief_A Initiate raw score",
							"Brief_A Working memory raw score", "Brief_A Plan raw score", "Brief_A Task-monitor raw score", "Brief_A Organization of Materials raw score",
							"Brief_A Negativity raw score", "Brief_A Negativity percentage", "Brief_A Negativity classification", "Brief_A Consistency raw score",
							"Brief_A Consistency percentage", "Brief_A Consistency classification", "Brief_A Infrequency raw score", "Brief_A Infrequency percentage", 
							"Brief_A Infrequency classification", "BRI raw score", "MI raw score", "GER raw score"]
		self.values = {'Brief_A_Inhibit_r' : {}, 'Brief_A_Shift_r' : {}, 'Brief_A_Emotional_control_r' : {}, "Brief_A_Self_monitor_r" : {}, "Brief_A_Initiate_r" : {}, 
						'Brief_A_WM_r' : {}, 'Brief_A_Plan_r' : {}, 'Brief_A_Task_monitor_r' : {}, 'Brief_A_OOM' : {},
						'Brief_A_Negativity_r' : {}, 'Brief_A_Negativity_perc' : {1: '0-98.3', 2: '99.4-100'},'Brief_A_Negativity_class' : {1: 'normal', 2:'high'},
						'Brief_A_Consistency_r' : {}, 'Brief_A_Consistency_perc' : {1: '0-99.2', 2: '99.8-100'}, 'Brief_A_Consistency_class' : {1: 'normal', 2:'not consistent'},
						'Brief_A_Infrequency_r' : {}, 'Brief_A_Infrequency_perc' : {1: '0-97.3', 2: '100'}, 'Brief_A_Infrequency_class' : {1: 'normal', 2: 'infrequent'},
						'Brief_A_BRI_r' : {}, 'Brief_A_MI_r' : {}, 'Brief_A_GER_r' : {}}
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
				
		functions = [self.grade_inhibit, self.grade_shift, self.grade_emotional_control, self.grade_self_monitor, self.grade_initiate, self.grade_wm, self.grade_plan,
					self.grade_task_monitor, self.grade_organization_of_materials ,self.grade_negativity, self.grade_consistency, self.grade_infrequency]
		for func in functions:
			func(brief_questions)
		self.new_df["Brief_A_BRI_r"] = self.new_df["Brief_A_Inhibit_r"] + self.new_df["Brief_A_Emotional_control_r"] + self.new_df["Brief_A_Shift_r"] + self.new_df["Brief_A_Self_monitor_r"]
		self.new_df["Brief_A_MI_r"] =  self.new_df["Brief_A_Initiate_r"] + self.new_df["Brief_A_WM_r"] + self.new_df["Brief_A_Plan_r"] + self.new_df["Brief_A_Task_monitor_r"] + self.new_df["Brief_A_OOM"]
		self.new_df["Brief_A_GER_r"] = self.new_df["Brief_A_BRI_r"] + self.new_df["Brief_A_MI_r"] 
		return self.new_df
	
	def grade_inhibit(self, all_questions):
		"""
		Grade inhibit scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief_A questions after coding
		"""
			   #5, 16, 29, 36, 43, 55, 58, 73
		cols = [4, 15, 28, 35, 42, 54, 57, 72]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_A_Inhibit_r"] = sum
	def grade_shift(self, all_questions):
		"""
		Grade shift scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief_A questions after coding
		"""
			   #8, 22, 32, 44, 61, 67
		cols = [7, 21, 31, 43, 60, 66]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_A_Shift_r"] = sum
		
	def grade_emotional_control(self, all_questions):
		"""
		Grade emotional control scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief_A questions after coding
		"""
			   #1, 12, 19, 28, 33, 42, 51, 57, 69, 72 
		cols = [0, 11, 18, 27, 32, 41, 50, 56, 68, 71]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_A_Emotional_control_r"] = sum
	
	def grade_self_monitor(self, all_questions):
		"""
		Grade self monitor scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief_A questions after coding
		"""
			   #13, 23, 37, 50, 64, 70 
		cols = [12, 22, 36, 49, 63, 69]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_A_Self_monitor_r"] = sum

	def grade_initiate(self, all_questions):
		"""
		Grade initiate scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief_A questions after coding
		"""
			   #6, 14, 20, 25, 45, 49, 53, 62 
		cols = [5, 13, 19, 24, 44, 48, 52, 61]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_A_Initiate_r"] = sum
		
		
	def grade_wm(self, all_questions):
		"""
		Grade working memory scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief_A questions after coding
		"""
			   #4, 11, 17, 26, 35, 46, 56, 68  
		cols = [3, 10, 16, 25, 34, 45, 55, 67]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_A_WM_r"] = sum
		
	def grade_plan(self, all_questions):
		"""
		Grade plan scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief_A questions after coding
		"""
			   #9, 15, 21, 34, 39, 47, 54, 63, 66, 71 
		cols = [8, 14, 20, 33, 38, 46, 53, 62, 65, 70]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_A_Plan_r"] = sum
	
	def grade_task_monitor(self, all_questions):
		"""
		Grade task-monitor scale - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief_A questions after coding
		"""
			   #2, 18, 24, 41, 52, 75 
		cols = [1, 17, 23, 40, 51, 74]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_A_Task_monitor_r"] = sum
		
	def grade_organization_of_materials(self, all_questions):
		"""
		Grade organization of materials - raw score
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief_A questions after coding
		"""
			   #3, 7, 30, 31, 40, 60, 65, 74 
		cols = [2, 6, 29, 30, 39, 59, 64, 73]
		sum = np.array(all_questions.iloc[:,cols].sum(axis=1))
		self.new_df["Brief_A_OOM"] = sum
		
	def grade_negativity(self, all_questions):
		"""
		Grade negativity scale: raw score, percentage and classification
				
		Parameters
		----------
		all_questions: DataFrame
			all Brief_A questions after coding
		"""
			   #1, 8, 19, 21, 22, 23, 29, 36, 39, 40
		cols = [0, 7, 18, 20, 21, 22, 28, 35, 38, 39]
		#Count all the values that are 3
		count = all_questions.iloc[:,cols][all_questions.iloc[:,cols] == 3].count(axis=1)
		self.new_df["Brief_A_Negativity_r"] = count
		self.new_df["Brief_A_Negativity_perc"] = self.new_df["Brief_A_Negativity_r"].apply(self.grade_negativity_perc)
		self.new_df["Brief_A_Negativity_class"] = self.new_df["Brief_A_Negativity_r"].apply(self.grade_negativity_class)
		
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
		if (score <= 5):
			perc = 1 # 0-98.3
		else:
			perc = 2 #99.4-100

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
		if (score <= 5):
			neg_class = 1 #normal
		else:
			neg_class = 2 #high

		return neg_class
		
	def grade_consistency(self, all_questions):
		"""
		Grade consistency scale: raw score, percentage and classification
				
		Parameters
		----------
		all_questions : DataFrame
			all Brief_A questions after coding
		"""
				#2, 25, 28, 33, 34, 44, 46, 52, 60, 64
		cols1 = [1, 24, 27, 32, 33, 43, 45, 51, 59, 63]
				#41, 49, 42, 72, 63, 61, 56, 75, 74, 70
		cols2 = [40, 48, 41, 71, 62, 60, 55, 74, 73, 69]
		diff_all = []
		for pair in list(zip(all_questions.iloc[:,cols1],all_questions.iloc[:,cols2])):
			diff = list(all_questions[pair[0]] - all_questions[pair[1]])
			diff = list(map(abs, diff))
			diff_all.append(diff)
		diff_all = pd.DataFrame(diff_all)
		sum = diff_all.sum(axis=0)
		self.new_df["Brief_A_Consistency_r"] = sum
		self.new_df["Brief_A_Consistency_perc"] = self.new_df["Brief_A_Consistency_r"].apply(self.grade_consistency_perc)
		self.new_df["Brief_A_Consistency_class"] = self.new_df["Brief_A_Consistency_r"].apply(self.grade_consistency_class)
		
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
		if(score <= 7):
			perc = 1 # 0-99.2
		else:
			perc = 2 # 99.8-100
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
		if(score <= 7):
			cons_class = 1 #normal
		else:
			cons_class = 2 #not consistent
		return cons_class
		
	def grade_infrequency(self, all_questions):
		"""
		Grade infrequency scale: raw score, percentage and classification
				
		Parameters
		----------
		all_questions : DataFrame
			all Brief_A questions after coding
		"""
		score = 0
		col_grade_dic = { 3 : [9] #10
						 ,1 : [26, 37, 47, 58] # 27, 38, 48, 59
						 }
		for key, value in col_grade_dic.items():
			#Count all the values that are as key 
			count = all_questions.iloc[:,value][all_questions.iloc[:,value] == key].count(axis=1)
			score += count
		
		self.new_df["Brief_A_Infrequency_r"] = score
		self.new_df["Brief_A_Infrequency_perc"] = self.new_df["Brief_A_Infrequency_r"].apply(self.grade_infrequency_perc)
		self.new_df["Brief_A_Infrequency_class"] = self.new_df["Brief_A_Infrequency_r"].apply(self.grade_infrequency_class)
		
	def grade_infrequency_perc(self, score):
		"""
		Grade infrequency percantage
				
		Parameters
		----------
		score: int
			infrequency score
			
		Returns
		----------
		int
			percentage coding number
		"""
		perc = 0
		if(score <= 2):
			perc = 1 # 0-97.3
		else:
			perc = 2 # 100
		return perc
		
	def grade_infrequency_class(self, score):
		"""
		Grade infrequency classification
				
		Parameters
		----------
		score: int
			infrequency score
			
		Returns
		----------
		int
			classification coding number
			
		"""
		infrequent_class = 0
		if(score <= 2):
			infrenquent_class = 1 #normal
		else:
			infrenquent_class = 2 #infrequent
		return infrenquent_class
		
Brief_dic = {
		'אף פעם' : 1,
		'מדי פעם' : 2,
		'לעיתים קרובות' : 3,
		}