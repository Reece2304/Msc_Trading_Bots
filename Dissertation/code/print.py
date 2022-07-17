from datetime import datetime, timedelta

def main():
	d = datetime.today() - timedelta(days=1)
	current = str(d)
	current = current.split(" ")
	append=""
	hour_int = current[1][0] + current[1][1]
	hour = 4 * round(int(hour_int)/4)
	if(hour < 10):
		hour = '0' + str(hour) 
	apiDateTime = current[0] + 'T' + str(hour) + ":00:00"
	print(apiDateTime)

main()