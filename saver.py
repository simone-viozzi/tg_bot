import pickle

class saver:
	file_name = ""

	def __init__(self, file_name):
		self.file_name = file_name

	def save(self, str_to_save):
		pickle.dump( str_to_save, open( self.file_name + '.p', 'wb' ) )  
			

	def load(self):
		try:
			str_loaded = pickle.load( open( self.file_name + '.p', 'rb'))
			return [0, str_loaded]
		except IOError: 
			return [-1, ""]
			print("file non esistente")
