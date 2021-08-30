class Questionnaire():
	"""
    A generic class used to represent an Questionnaire

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
		self.df = df
	def grade(self):
		print("Generic questionnaire class")