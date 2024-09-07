import re
import sys
from collections import Counter

invalid_ips = []
invalid_users = []
auth_users = []

match_basic_syslog = re.compile("Invalid user (?P<invalid>\w+)\s+from (?P<ip>\d+\.\d+\.\d+\.\d+)\s+port (?P<port>\d+)")
match_good_users = re.compile("Valid user (?P<valid>\w+)\s+from (?P<ip>\d+\.\d+\.\d+\.\d+)\s+port (?P<port>\d+)")

def main():
  with open(sys.argv[1], 'r') as logfile:
    for line in logfile:
      curr_match = match_basic_syslog.search(line)
      user_match = match_good_users.search(line)

      # Test whether line matches a regex, parse out the details
      if curr_match:
        invalid_ips.append(curr_match.groupdict()['ip'])
        invalid_users.append(curr_match.groupdict()['invalid'])

      if user_match:
        auth_users.append(user_match.groupdict()['valid'])
        #Testing that the good user list works
        # print(auth_users)
      
  #This has the information on the most connected IPs, Bad Users and Valid Users
  # print(invalid_users)
  invalid_users_count = Counter(invalid_users)
  invalid_users_count_sorted = invalid_users_count.most_common()
  for name, count in invalid_users_count_sorted:
      print(f"User name: {name} Number of connection attempts: {count}")
  
  invalid_ips_count = Counter(invalid_ips)
  invalid_ips_count_sorted = invalid_ips_count.most_common()
  
  auth_users_count = Counter(auth_users)
  auth_users_count_sorted = auth_users_count.most_common()
  print(f"The list of usernames (most to least common):\n{auth_users_count_sorted}")
  print(f"The list of IPs (most common to least):\n{invalid_ips_count_sorted}")

if __name__ == "__main__":
	if len(sys.argv) > 1:
		main()
	else:
		sys.stderr.write("Must provide a file path as argument 1.")
