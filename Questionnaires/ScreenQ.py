from  .Questionnaire import Questionnaire
import pandas as pd

class ScreenQ(Questionnaire): 
	"""
	A class used to represent the ScreenQ questionaire 

	Attributes
	----------
	df : DataFrame
		Pandas' data frame with the specific columns
		for the questionnaire 

	Methods
	-------
	grade()
		Calculates the grading of the questionnaire. 
			
	q1-q20:
		Claculates the score for each question

	"""
	def __init__(self, df):
		"""
		Init the following arguments: 
		names = the new columns' names (after grading)
		labels = labels for the columns to be written in the SPSS output file
		values = explanation for the value for SPSS columns
		new_df = new DataFrame with the graded values

		Parameters
		----------
		df : DataFrame
			Pandas data frame with the specific columns
			for the questionnaire. 
		"""
		Questionnaire.__init__(self, df)
		self.names = ["ScreenQ_q1","ScreenQ_q1_type","ScreenQ_q2","ScreenQ_q3","ScreenQ_q4","ScreenQ_q5","ScreenQ_q6",
						"ScreenQ_q7","ScreenQ_q8_raw","ScreenQ_q8","ScreenQ_q9","ScreenQ_q10","ScreenQ_q11","ScreenQ_q12","ScreenQ_q13",
						"ScreenQ_q14","ScreenQ_q15","ScreenQ_q16","ScreenQ_q17","ScreenQ_q18","ScreenQ_q19","ScreenQ_q20",
						"ScreenQ_total_raw","ScreenQ_access_raw","ScreenQ_frequency_raw","ScreenQ_content_raw","ScreenQ_dialogic_raw"]
		self.labels = ["Does the child have any of these in his bedroom? TV, video game system, Handheld device, Computer with Internet access, None", 
						"Does the child have any of these in his bedroom?", 
						"Does the child have his own portable device he can carry with him and watch or play on, such as a Leapster, iPad, or smartphone?",
						"Number of child's favorite shows, movies or apps", "Does the child watch or play during meals?", "Does the child watch or play on school nights?",
						"Does the child watch or play while waiting for something, such as in the doctor’s office or in line at the store?", 
						"At what age did the child start watching TV/videos or using apps or the computer?", 
						"How many hours in a typical day does the child watch TV/videos, play video or computer games, or use apps? raw data",
						"How many hours in a typical day does the child watch TV/videos, play video or computer games, or use apps?",
						"Does the child watch TV/videos at bedtime to help him fall asleep?”", "Does the child watch TV/videos or play apps to help him calm down?", 
						"Does the child watch shows or play video games or apps that teach skills for school, like ABCs?",
						"Does the child watch shows or play video games or apps that involve shooting, battles or fighting?",
						"Does the child choose TV shows/videos or download apps by HIMSELF?", "How would you describe most of the shows, video games or apps that the child watches or plays?",
						"How would you describe how the child usually watches TV/videos?", "How would you describe how the child usually plays video games/apps?",
						"While the child is watching TV shows or movies, how often do you talk to him about what’s happening, or ask questions?",
						"When the child is finished watching a TV show/movie, or playing an app or video game, how often do you talk about what it was about or why he liked it?",
						"In general, how do you feel about the screen use of your child?", 
						"In general, do you think the screen use of your child couse him to spend more, less or equal time with you?",
						"Summary of questions 1-18", "Summary of question 1-6", "Summary of questions 7-10", "Summary of questions 11-14", "Summary of questions 15-18"]
		self.values = {'ScreenQ_q1' : {0 : 'None', 2 : 'Other'}, 
					   'ScreenQ_q1_type' : {},
					   'ScreenQ_q2' : {0 : 'No', 2 : 'Yes'},
					   'ScreenQ_q3' : {},
					   'ScreenQ_q4' : {0 : 'No', 1 : 'Yes'},
					   'ScreenQ_q5' : {0 : 'No', 1 : 'Yes'},
					   'ScreenQ_q6' : {0 : 'No', 1 : 'Yes'},
					   'ScreenQ_q7' : {0 : '18+ months', 1 : '13-18 months', 2 : '0-12 months'},
					   'ScreenQ_q8_raw' : {},
					   'ScreenQ_q8' : {0 : '< 1', 1 : '1 <= x <= 2.9', 2 : 'x > 3'},
					   'ScreenQ_q9' : {0 : 'Never', 1 : 'Sometimes', 2 : 'Often'},
					   'ScreenQ_q10' : {0 : 'Never', 1 : 'Sometimes', 2 : 'Often'},
					   'ScreenQ_q11' : {2 : 'Rarely/never', 1 : 'Sometimes', 0 : 'Often'},
					   'ScreenQ_q12' : {0 : 'Rarely/never', 1 : 'Sometimes', 2 : 'Often'},
					   'ScreenQ_q13' : {0 : 'Rarely/never', 1 : 'Sometimes', 2 : 'Often'},
					   'ScreenQ_q14' : {1 : 'Fast-paced, more action', 0 : 'Slower-paced, more talking or singing'},
					   'ScreenQ_q15' : {0 : 'Together with a grownup', 1 : 'By himself'},
					   'ScreenQ_q16' : {0 : 'Together with a grownup', 1 : 'By himself'},
					   'ScreenQ_q17' : {0 : 'Often, consistently throughout', 1 : 'Sometimes, during exciting parts', 2 : 'Rarely/never, don’t want to bother her/him'},
					   'ScreenQ_q18' : {0 : 'Often', 1 : 'Sometimes', 2 : 'Rarely/never'},
					   'ScreenQ_q19' : {},
					   'ScreenQ_q20' : {},
					   'ScreenQ_total_raw' : {},
					   'ScreenQ_access_raw' : {},
					   'ScreenQ_frequency_raw' : {},
					   'ScreenQ_content_raw' : {},
					   'ScreenQ_dialogic_raw' : {}
					   }
					   
					   
		self.new_df = pd.DataFrame(0,index=self.df.index,columns=self.names)
	def grade(self):
		"""
		Grades the questionaire according to the questionaire grading rules.
		Each question has it's own function with the grading logic
				
		Returns
		----------
		DataFrame
			a new DataFrame with the new columns after grading
		"""
		functions = [self.q1,self.q2,self.q3,self.q4,self.q5,self.q6,self.q7, self.q8, self.q9, self.q10, self.q11, self.q12, self.q13, self.q14, self.q15, 
					self.q16, self.q17, self.q18, self.q19, self.q20]
		for func in functions:
			func()
		return self.new_df
		
		
	def q1(self):
		"""
		q1 grading. 
		Get the same column, after converting to code number
		Get the screen type
		Sum to "ACCESS" criterion
		Sum to "TOTAL" criterion
				
		"""
		func = lambda x : 0 if x == 'אף אחד מאלו' else 2
		new_series = self.df.iloc[:,0].apply(func) 
		self.new_df["ScreenQ_q1"] = new_series
		self.new_df["ScreenQ_q1_type"] = self.df.iloc[:,0]
		self.new_df["ScreenQ_access_raw"] = self.new_df["ScreenQ_access_raw"] + new_series
		self.new_df["ScreenQ_total_raw"] = self.new_df["ScreenQ_total_raw"] + new_series

	def q2(self):
		"""
		q2 grading. 
		Get the same column, after converting to code number
		Sum to "ACCESS" criterion
		Sum to "TOTAL" criterion
				
		"""
		func = lambda x : 0 if x == 'לא' else 2
		new_series = self.df.iloc[:,1].apply(func) 
		self.new_df["ScreenQ_q2"] = new_series
		self.new_df["ScreenQ_access_raw"] = self.new_df["ScreenQ_access_raw"] + new_series
		self.new_df["ScreenQ_total_raw"] = self.new_df["ScreenQ_total_raw"] + new_series
		
	def q3(self):
		"""
		q3 grading. 
		Get the same column
				
		"""
		self.new_df["ScreenQ_q3"] = self.df.iloc[:,2]

	def q4(self):
		"""
		q4 grading. 
		Get the same column, after converting to code number
		Sum to "ACCESS" criterion
		Sum to "TOTAL" criterion
				
		"""
		func = lambda x : 0 if x == 'לא' else 1
		new_series = self.df.iloc[:,3].apply(func) 
		self.new_df["ScreenQ_q4"] = new_series
		self.new_df["ScreenQ_access_raw"] = self.new_df["ScreenQ_access_raw"] + new_series
		self.new_df["ScreenQ_total_raw"] = self.new_df["ScreenQ_total_raw"] + new_series
	
	def q5(self):
		"""
		q5 grading. 
		Get the same column, after converting to code number
		Sum to "ACCESS" criterion
		Sum to "TOTAL" criterion
				
		"""
		func = lambda x : 0 if x == 'לא' else 1
		new_series = self.df.iloc[:,4].apply(func) 
		self.new_df["ScreenQ_q5"] = new_series
		self.new_df["ScreenQ_access_raw"] = self.new_df["ScreenQ_access_raw"] + new_series
		self.new_df["ScreenQ_total_raw"] = self.new_df["ScreenQ_total_raw"] + new_series

	def q6(self):
		"""
		q6 grading. 
		Get the same column, after converting to code number
		Sum to "ACCESS" criterion
		Sum to "TOTAL" criterion
				
		"""
		func = lambda x : 0 if x == 'לא' else 1
		new_series = self.df.iloc[:,5].apply(func) 
		self.new_df["ScreenQ_q6"] = new_series
		self.new_df["ScreenQ_access_raw"] = self.new_df["ScreenQ_access_raw"] + new_series
		self.new_df["ScreenQ_total_raw"] = self.new_df["ScreenQ_total_raw"] + new_series

	def q7(self):
		"""
		q7 grading. 
		Get the same column, after converting to code number
		Sum to "FREQUENCY" criterion
		Sum to "TOTAL" criterion
				
		"""
		q7_dic = { "18 חודשים ומעלה" : 0,
				   "13-18 חודשים" : 1,
				   "0-12 חודשים" : 2
				 }
		new_series = self.df.iloc[:,6].apply(lambda x: q7_dic[x])
		self.new_df["ScreenQ_q7"] = new_series
		self.new_df["ScreenQ_frequency_raw"] = self.new_df["ScreenQ_frequency_raw"] + new_series
		self.new_df["ScreenQ_total_raw"] = self.new_df["ScreenQ_total_raw"] + new_series
		
	def q8_grade_hours(self,x):
		"""
		Helper function for q8 grading. 
				
		"""
		if x < 1:
			return 0
		elif x >= 1 and x <= 2.9:
			return 1
		else:
			return 2
			
	def q8(self):
		"""
		q8 grading. 
		Get the same column, after converting to code number
		Get the same column, as is
		Sum to "FREQUENCY" criterion
		Sum to "TOTAL" criterion
				
		"""
		new_series = self.df.iloc[:,7].apply(self.q8_grade_hours) 
		self.new_df["ScreenQ_q8"] = new_series
		self.new_df["ScreenQ_q8_raw"] = self.df.iloc[:,7]
		self.new_df["ScreenQ_frequency_raw"] = self.new_df["ScreenQ_frequency_raw"] + new_series
		self.new_df["ScreenQ_total_raw"] = self.new_df["ScreenQ_total_raw"] + new_series
	
	def q9(self):
		"""
		q9 grading. 
		Get the same column, after converting to code number
		Sum to "FREQUENCY" criterion
		Sum to "TOTAL" criterion
				
		"""
		q9_dic = { "אף פעם" : 0,
		   "לפעמיים" : 1,
		   "לעיתים קרובות" : 2
		 }
		new_series = self.df.iloc[:,8].apply(lambda x: q9_dic[x])
		self.new_df["ScreenQ_q9"] = new_series
		self.new_df["ScreenQ_frequency_raw"] = self.new_df["ScreenQ_frequency_raw"] + new_series
		self.new_df["ScreenQ_total_raw"] = self.new_df["ScreenQ_total_raw"] + new_series

	def q10(self):
		"""
		q10 grading. 
		Get the same column, after converting to code number
		Sum to "FREQUENCY" criterion
		Sum to "TOTAL" criterion
				
		"""
		q10_dic = { "אף פעם" : 0,
		   "לפעמיים" : 1,
		   "לעיתים קרובות" : 2
		 }
		new_series = self.df.iloc[:,9].apply(lambda x: q10_dic[x])
		self.new_df["ScreenQ_q10"] = new_series
		self.new_df["ScreenQ_frequency_raw"] = self.new_df["ScreenQ_frequency_raw"] + new_series
		self.new_df["ScreenQ_total_raw"] = self.new_df["ScreenQ_total_raw"] + new_series
		
	def q11(self):
		"""
		q11 grading. 
		Get the same column, after converting to code number
		Sum to "CONTENT" criterion
		Sum to "TOTAL" criterion
				
		"""
		q11_dic = { "לעיתים רחוקות\ אף פעם" : 2,
		   "לפעמיים" : 1,
		   "לעיתים קרובות" : 0
		 }
		new_series = self.df.iloc[:,10].apply(lambda x: q11_dic[x])
		self.new_df["ScreenQ_q11"] = new_series
		self.new_df["ScreenQ_content_raw"] = self.new_df["ScreenQ_content_raw"] + new_series
		self.new_df["ScreenQ_total_raw"] = self.new_df["ScreenQ_total_raw"] + new_series
		
	def q12(self):
		"""
		q12 grading. 
		Get the same column, after converting to code number
		Sum to "CONTENT" criterion
		Sum to "TOTAL" criterion
				
		"""
		q12_dic = { "לעיתים רחוקות\ אף פעם" : 0,
		   "לפעמיים" : 1,
		   "לעיתים קרובות" : 2
		 }
		new_series = self.df.iloc[:,11].apply(lambda x: q12_dic[x])
		self.new_df["ScreenQ_q12"] = new_series
		self.new_df["ScreenQ_content_raw"] = self.new_df["ScreenQ_content_raw"] + new_series
		self.new_df["ScreenQ_total_raw"] = self.new_df["ScreenQ_total_raw"] + new_series
		
	def q13(self):
		"""
		q13 grading. 
		Get the same column, after converting to code number
		Sum to "CONTENT" criterion
		Sum to "TOTAL" criterion
				
		"""
		q13_dic = { "לעיתים רחוקות\ אף פעם" : 0,
		   "לפעמיים" : 1,
		   "לעיתים קרובות" : 2
		 }
		new_series = self.df.iloc[:,12].apply(lambda x: q13_dic[x])
		self.new_df["ScreenQ_q13"] = new_series
		self.new_df["ScreenQ_content_raw"] = self.new_df["ScreenQ_content_raw"] + new_series
		self.new_df["ScreenQ_total_raw"] = self.new_df["ScreenQ_total_raw"] + new_series
		
	def q14(self):
		"""
		q14 grading. 
		Get the same column, after converting to code number
		Sum to "CONTENT" criterion
		Sum to "TOTAL" criterion
				
		"""
		q14_dic = { "קצב איטי, יותר דיבורים ושירים" : 0,
		   "קצב מהיר, יותר אקשן" : 1,
		 }
		new_series = self.df.iloc[:,13].apply(lambda x: q14_dic[x])
		self.new_df["ScreenQ_q14"] = new_series
		self.new_df["ScreenQ_content_raw"] = self.new_df["ScreenQ_content_raw"] + new_series
		self.new_df["ScreenQ_total_raw"] = self.new_df["ScreenQ_total_raw"] + new_series
		
	def q15(self):
		"""
		q15 grading. 
		Get the same column, after converting to code number
		Sum to "DIALOGIC" criterion
		Sum to "TOTAL" criterion
				
		"""
		q15_dic = { "יחד עם מבוגר" : 0,
		   "בעצמו" : 1,
		 }
		new_series = self.df.iloc[:,14].apply(lambda x: q15_dic[x])
		self.new_df["ScreenQ_q15"] = new_series
		self.new_df["ScreenQ_dialogic_raw"] = self.new_df["ScreenQ_dialogic_raw"] + new_series
		self.new_df["ScreenQ_total_raw"] = self.new_df["ScreenQ_total_raw"] + new_series
		
	def q16(self):
		"""
		q16 grading. 
		Get the same column, after converting to code number
		Sum to "DIALOGIC" criterion
		Sum to "TOTAL" criterion
				
		"""
		q16_dic = { "יחד עם מבוגר" : 0,
		   "בעצמו" : 1,
		 }
		new_series = self.df.iloc[:,15].apply(lambda x: q16_dic[x])
		self.new_df["ScreenQ_q16"] = new_series
		self.new_df["ScreenQ_dialogic_raw"] = self.new_df["ScreenQ_dialogic_raw"] + new_series
		self.new_df["ScreenQ_total_raw"] = self.new_df["ScreenQ_total_raw"] + new_series
		
	def q17(self):
		"""
		q17 grading. 
		Get the same column, after converting to code number
		Sum to "DIALOGIC" criterion
		Sum to "TOTAL" criterion
				
		"""
		q17_dic = { "לעיתים קרובות, כמעט לאורך כל הדרך" : 0,
		   "לפעמים, בזמן חלקים מרגשים" : 1,
		   "לעיתים רחוקות\ אף פעם, אינני רוצה להטריד אותו" : 2
		 }
		new_series = self.df.iloc[:,16].apply(lambda x: q17_dic[x])
		self.new_df["ScreenQ_q17"] = new_series
		self.new_df["ScreenQ_dialogic_raw"] = self.new_df["ScreenQ_dialogic_raw"] + new_series
		self.new_df["ScreenQ_total_raw"] = self.new_df["ScreenQ_total_raw"] + new_series
		
	def q18(self):
		"""
		q18 grading. 
		Get the same column, after converting to code number
		Sum to "DIALOGIC" criterion
		Sum to "TOTAL" criterion
				
		"""
		q18_dic = { "לעיתים קרובות" : 0,
		   "לפעמים" : 1,
		   "לעיתים רחוקות\ אף פעם" : 2
		 }
		new_series = self.df.iloc[:,17].apply(lambda x: q18_dic[x])
		self.new_df["ScreenQ_q18"] = new_series
		self.new_df["ScreenQ_dialogic_raw"] = self.new_df["ScreenQ_dialogic_raw"] + new_series
		self.new_df["ScreenQ_total_raw"] = self.new_df["ScreenQ_total_raw"] + new_series
		
	def q19(self):
		"""
		q19 grading. 
		Get the same column, after converting to code number
				
		"""
		q19_dic = { "הרבה יותר מידי" : 4,
			"קצת יותר מידי" : 3,
			"בסדר גמור" : 2,
			"לא מספיק" : 1
			}
		new_series = self.df.iloc[:,18].apply(lambda x: q19_dic[x])
		self.new_df["ScreenQ_q19"] = new_series
	def q20(self):
		"""
		q20 grading. 
		Get the same column, after converting to code number
				
		"""
		q20_dic = { "יותר זמן ביחד" : 1,
			"בערך אותו משך זמן ביחד" : 2,
			"פחות זמן ביחד" : 3	
		}
		new_series = self.df.iloc[:,19].apply(lambda x: q20_dic[x])
		self.new_df["ScreenQ_q20"] = new_series