# Keeps track of how many days since the last retrain for the model
def post_new_retrain_time(new_refresh_time):
    f = open('days_since_last_retrain.txt', 'w')
    f.write(str(new_refresh_time))
    f.close()
    return

def get_retrain_time():
    f = open('days_since_last_retrain.txt', 'r')

    try:
        days_since_last_refresh = int(f.readline())
    except ValueError:
        days_since_last_refresh = 1

    f.close()
    return days_since_last_refresh
