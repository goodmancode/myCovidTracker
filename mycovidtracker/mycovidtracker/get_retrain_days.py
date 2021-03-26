import os

# Keeps track of how many days since the last retrain for the model
def post_new_retrain_time(new_refresh_time):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	file_name = dir_path + '/days_since_last_retrain.txt'
	f = open(file_name, 'w')
	f.write(str(new_refresh_time))
	f.close()
	return

def get_retrain_time():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	file_name = dir_path + '/days_since_last_retrain.txt'
	f = open(file_name, 'r')

	try:
		days_since_last_refresh = int(f.readline())
	except ValueError:
		days_since_last_refresh = 1

	f.close()
	return days_since_last_refresh
