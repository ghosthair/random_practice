import re
import sys
from collections import Counter

# These are the regex options that need to be added.
#Question 1 - Done
match_bad_users = re.compile(r'[Ii]nvalid user (?P<invalid>[A-Za-z0-9_]+).*(?P<ip>\d+\.\d+\.\d+\.\d+)')

#Question 2 - Done
key_error = re.compile(r'(?P<key_exchange>[Kk]ex_exchange_identification: .+)')
key_error_specific = re.compile(r'(?P<key>[Kk]ex_exchange_identification: Connection closed by remote host)')

#Question 3 - Done
pre_auth_error = re.compile (r'.*(\[preauth\])$')
pre_auth_error_user = re.compile(r'.*[Ii]nvalid user (?P<user_names>[A-Za-z0-9_]+).*\[preauth\]$')
pre_auth_error_ips = re.compile(r'(?P<ip_list>\d+\.\d+\.\d+\.\d+).*[Aa]uth fail \[preauth\]$')

#Question 4 - Not completed
non_pre_auth_error_user = re.compile(r'.*Invalid user (?P<user_names>[A-Za-z0-9_]+) from (?P<ip_list>\d+\.\d+\.\d+\.\d+).*(?!\[preauth\])')
# non_pre_auth_error_ip = re.compile()

#Question 5 - Done
invalid_protocol = re.compile(r'sent (?P<bad_protocol>invalid protocol) identifier (?P<identifier>.+)')

#Question 6 - Not completed
auth_users = re.compile(r'.*(authenticating user) (?P<users>\w+\s+\w+).*(?P<ips>\d+\.\d+\.\d+\.\d+).*')

def main(file):
    #list and variables needed.
#---------------------------------------------------------------------------------------------------------------------------
    invalid_ips = []
    invalid_users = []
    key_exhchange_total = 0
    #This will not stay an python list, it will be changed to a tuple then count the number of different instances
    key_exchange_list = []
    key_error_specific_number = 0
    pre_auth = 0
    bad_protocol = 0
    identifier_list = []
    pre_auth_user_list = []
    pre_auth_user_number = 0
    pre_auth_ip_list = []
    pre_auth_ip_numner = 0
    non_pre_auth_error_user_list = []
    non_pre_auth_error_ip_list = []
    non_pre_auth_number = 0
    successful_users = []
    successful_ips = []
    auth_user_count = 0
#--------------------------------------------------------------------------------------------------------------------------
    with open(file, 'r') as logfile:
        for line in logfile:
            bad_ip = match_bad_users.search(line) #Question 1
            key_exchange = key_error.search(line) # Question 2
            key_exchange_specific_regex = key_error_specific.search(line)
            pre_auth_regex = pre_auth_error.search(line) #Question 3
            pre_auth_user_regex = pre_auth_error_user.search(line) #Question 3
            pre_auth_ip_regex = pre_auth_error_ips.search(line) #Question 3
            non_pre_auth_error_user_regex = non_pre_auth_error_user.search(line) #Question 4
            protocol = invalid_protocol.search(line) # Question 5
            auth_users_regex = auth_users.search(line)
            if bad_ip:
                #Print statements added to make sure the code was working correctly.
                # print(f"Bad Users: {bad_ip.groupdict()['invalid']}")
                # print(f"Bad IPs: {bad_ip.groupdict()['ip']}")
                invalid_users.append(bad_ip.groupdict()['invalid'])
                invalid_ips.append(bad_ip.groupdict()['ip'])

            if key_exchange:
                #   print(f"Key errors: {key_exchange.groupdict()['key_exchange']}\n")
                  key_exchange_list.append(key_exchange.groupdict()['key_exchange'])
                  key_exhchange_total += 1
                  
            if key_exchange_specific_regex:
                  key_error_specific_number += 1
            if pre_auth_regex:
                #   print(f"Found all of the preauth errors.")
                  pre_auth += 1
            if pre_auth_user_regex:
                  pre_auth_user_list.append(pre_auth_user_regex.groupdict()['user_names'])
                  pre_auth_user_number += 1
                #   print(f"List of Pre_auth user errors: {pre_auth_user_list}")

            if pre_auth_ip_regex:
                #   print("Found some Auth Fail ones")
                #   print(f"IPs: {pre_auth_ip_regex.groupdict()['ip_list']}")
                  pre_auth_ip_list.append(pre_auth_ip_regex.groupdict()['ip_list'])
                  pre_auth_ip_numner += 1

            if protocol:
                #   print(f"Invalid protocol stuff: {protocol.groupdict()['bad_protocol']}\n")
                #   print(f"Identifiers: {protocol.groupdict()['identifier']}")
                  identifier_list.append(protocol.groupdict()['identifier'])
                  bad_protocol += 1

            if non_pre_auth_error_user_regex:
                #   print("Found invalid user, but not preauth error.")
                non_pre_auth_error_user_list.append(non_pre_auth_error_user_regex.groupdict()['user_names'])
                non_pre_auth_error_ip_list.append(non_pre_auth_error_user_regex.groupdict()['ip_list'])
                non_pre_auth_number += 1
            if auth_users_regex:
                #   print("Found successful login.")
                successful_users.append(auth_users_regex.groupdict()['users'])
                successful_ips.append(auth_users_regex.groupdict()['ips'])
                auth_user_count += 1

            # else:
            #       print("No luck try working on the regex.")

# This block is organizing the list of the regex searches into tuples and adding the count of appearence.
#----------------------------------------------------------------------------------------------------------
    invalid_ips_count = Counter(invalid_ips)
    invalid_users_count = Counter(invalid_users)
    invalid_ips_count_sort = invalid_ips_count.most_common()
    invalid_users_count_sort = invalid_users_count.most_common()
    key_exchange_list_count = Counter(key_exchange_list)
    key_exchange_list_count_sort = key_exchange_list_count.most_common()
    identifier_list_count = Counter(identifier_list)
    identifier_list_count_sort = identifier_list_count.most_common()
    pre_auth_ip_list_count = Counter(pre_auth_ip_list)
    pre_auth_ip_list_count_sort = pre_auth_ip_list_count.most_common()
    non_pre_auth_error_user_list_count = Counter(non_pre_auth_error_user_list)
    non_pre_auth_error_user_list_count_sort = non_pre_auth_error_user_list_count.most_common()
    non_pre_auth_error_ip_list_count = Counter(non_pre_auth_error_ip_list)
    non_pre_auth_error_ip_list_count_sort =non_pre_auth_error_ip_list_count.most_common()
    successful_users_count = Counter(successful_users)
    successful_users_count_sort = successful_users_count.most_common()
    successful_ips_count = Counter(successful_ips)
    successful_ips_count_sort = successful_ips_count.most_common()

    set_successful_ips = set(successful_ips)
    set_invalid_ips = set(invalid_ips)
    result = set_successful_ips & set_invalid_ips
    result_count = Counter(result)
    result_count_sort = result_count.most_common()


# ----------------------------------------------------------------------------------------------------------

#This Block will print the answers to the homework, don't forget to uncomment them out, also make it look pretty
# Qustion 1:
    print("Question 1:\n")
    print(f"Distinct User Names (from most to least seen): {invalid_users_count_sort}\n")
    print(f"Distinct IP addresses: {invalid_ips_count_sort}\n")
    
#Question 2:
    print("Question 2:\n")
    print(f"{key_exhchange_total} total connection attemps failed during the 'kex_exchange_indentification phase'\n")
    print(f"{key_error_specific_number} total errors were the 'Connection closed by remote host\n")
    print(f"List of key exchange error with count: {key_exchange_list_count_sort}\n")
    
#Question 3:
    print("Question 3:\n")
    print(f"Number of preauth errors {pre_auth}\n")
    print(f"Total of preauth invalid users: {pre_auth_user_number}")
    print(f"List of preauth error users: {pre_auth_user_list}\n")
    print(f"Total of users that contained an auth fail error: {pre_auth_ip_numner}\n")
    print(f"List of users with Auth Fail in the preauth error: {pre_auth_ip_list_count_sort}\n")

#Question 4:
    print("Question 4:\n")
    print(f"Total of failures of username but not due to preauth phase: {pre_auth_ip_numner}")
    print(f"List of invalid users without preauth error: {non_pre_auth_error_user_list_count_sort}\n")
    print(f"List of invalid ips without preauth error: {non_pre_auth_error_ip_list_count_sort}\n")

#Question 5:
    print("Question 5:\n")
    print(f"Invalid Protocol Count: {bad_protocol}\n")
    print(f"Invalid Protocol List: {identifier_list_count_sort}\n")

#Question 6:
    print("Question 6:\n")
    print(f"Total successful logins: {auth_user_count}\n")
    print(f"Successful users: {successful_users_count_sort}\n")
    print(f"Successful IPs: {successful_ips_count_sort}\n")
    print("From the information gathered, it does appear that several attackers were able to loging.\nThe list below will show ip addresses that were unsuccessful but were later found to have logged in.\n")
    print(f"IPs that were invalid at one point and logged in:\n{result_count_sort}\n")
#------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
	if len(sys.argv) > 1:
		main(sys.argv[1])
	else:
		sys.stderr.write("Must provide a file path as argument 1.")