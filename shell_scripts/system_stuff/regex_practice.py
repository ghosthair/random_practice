import re

test_strings = ["Denver, CO 80208", "George C. Wallace", "800-555-2424", "999-4653"]

#Match a city, state ZIP
city_regex = re.compile('\w+, [A-Z]{2} \d{5}')
#Match a word
word_regex = re.compile('\w+')
#Match a name
name_regex = re.compile('^[A-Z][\w]+ [\w\. ]*[A-Z][\w]+$')
#Match a phone number
phone_regex = re.compile('[0-9]{3}-[0-9]{3}-[0-9]{4}')

def main():
	for line in test_strings:
		if city_regex.match(line):
			print(f"Matched city regex on {line}")
		if name_regex.match(line):
			print(f"Matched name regex on {line}")
		if phone_regex.match(line):
			print(f"Matched phone regex on {line}")



if __name__=="__main__":
	main()
