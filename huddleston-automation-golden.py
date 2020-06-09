###Here is example output from a real email, after converting to a list and removing excess lines.
###0
###['{\'email_message\': "Wix.com', 'You just got a new reservation!', "Can't see this email? Click here", 'Great News!', 'You Just Got A New Reservation', 'Great News!', 'You Just Got A', 'New Reservation', 'Dates', 'Check-In: 2020-05-29', '>', 'Check-Out: 2020-05-31', 'Summary', '# 141396', 'Price', 'USD 144.0 x 2 Night(s)', 'Room', '2019 VIBE 29BH DOUBLE SLIDE', 'Extras', '0.0', 'Tax(11.0%)', 'USD 31.68', 'Total Price', 'USD 319.68', 'Deposit Paid Via Stripe', 'Guest Info', 'Full Name', 'John Doe', 'Email', 'johndoe@yopmail.com', 'Phone', '5551234567', 'Location', 'U.S.A.', 'Special Requests', 'I have rented from you in the past. Might need a late return time, maybe around 6:00 pm. Having a family reunion at the lake.', 'Dates', 'Check-In: 2020-05-29', '>', 'Check-Out: 2020-05-31', '# 141396', 'Summary', 'Price', 'USD 144.0 x 2 Night(s)', 'Room', '2019 VIBE 29BH DOUBLE SLIDE', 'Extras', '0.0', 'Tax(11.0%)', 'USD 31.68', 'Total Price', 'USD 319.68', 'Deposit Paid Via Stripe', 'Guest Info', 'Full Name', 'John Doe', 'Email', 'johndoe@yopmail.com', 'Phone', '5551234567', 'Location', 'U.S.A.', 'Special Requests', 'I have rented from you in the past. Might need a late return time, maybe around 6:00 pm. Having a family reunion at the lake.', 'Rate your experience with Wix Hotels', 'Your review is super helpful for us to achieve greatness', 'Add Review', 'Rate your experience with Wix Hotels', 'Your review is super helpful for us to achieve greatness', 'Add', 'Review', 'Please do not reply to this email', '500 Terry A Francois Blvd San Francisco,', 'CA\xa094158', 'Wix.com Ltd., Wix.com Inc.', 'www.wix.com', 'View our', 'privacy', 'policy', '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"}']



import re
import json

###Zapier stores the email data as a variable labeled "input_data", this would differ if not using Zapier
###
###If customer is collecting a deposit when a user books through Wix Hotels, input the deposit percentage below (in decimal format) in the parentheses following the word float
###

deposit_pct = float(.25)
input_data = str(input_data)
input_data = input_data.encode().decode('unicode_escape')
input_data = input_data.strip()

###Convert data to a list, so we can run our loop below
input_data_list = input_data.splitlines()
input_data_list = iter(list(filter(None, input_data_list)))

###if line in list starts with x, print the next line after that and strip whitespace 
for line in input_data_list:
    if line.startswith("Room"):
        camper_final = (next(input_data_list, '').strip())
    if line.startswith("Full Name"):
        cust_name_final = (next(input_data_list, '').strip())
    if line.startswith("Email"):
        customer_email_final = (next(input_data_list, '').strip()) 
    if line.startswith("Phone"):
        customer_phone_final = (next(input_data_list, '').strip())
    if line.startswith("Price"):
        rate = (next(input_data_list, '').strip())
    if line.startswith("Extras"):
        extras_final = (next(input_data_list, '').strip())     
    if line.startswith("Tax"):
        taxes = (next(input_data_list, '').strip())
    if line.startswith("Total Price"):
        total = (next(input_data_list, '').strip())

### Some of these lines have excess data which needs to be stripped out.  Below takes care of this

rate_str = str(rate)
rate_spl_word1 = 'USD '
rate_spl_word2 = ' x'
rate_1 = rate_str.partition(rate_spl_word1)[2]
rate_final = rate_1.partition(rate_spl_word2)[0]
total_str = str(total)
total_spl_word = 'USD '
total_final = total_str.partition(total_spl_word)[2]
nights = (re.search(r"USD [\d*\].[?\d]+ x [\w\.-]+", input_data))
nights_str = str(nights.group(0))
nights_spl_word = ' x '
nights_final = nights_str.partition(nights_spl_word)[2]

### Convert to appropriate data type so we can do some simple calucations


###rate is the nightly rate.  nights is the amount of nights booked.
rate_float = float(rate_final)
nights_int = int(nights_final)

###base rate is nights x nightly rate.  Deposit is a percentage of this value (set above)
base_rate_total =  str(rate_float * nights_int)
deposit_total = str(rate_float * nights_int * deposit_pct)

###Remember, total is actually the total amount less the deposit paid.  So actually total remaining
total_final = float(total_final) - float(deposit_total)
total_final = str(round(total_final, 2))
taxes_str = str(taxes)
taxes_spl_word = 'USD '
taxes_final = taxes_str.partition(taxes_spl_word)[2]
check_in = (re.search(r"Check-In: [\w\.-]+", input_data))
check_in_str = str(check_in.group(0))
check_in_spl_word = 'Check-In: '
check_in_final = check_in_str.partition(check_in_spl_word)[2]
check_out = (re.search(r"Check-Out: [\w\.-]+", input_data))         
check_out_str = str(check_out.group(0))
check_out_spl_word = 'Check-Out: '
check_out_final = check_out_str.partition(check_out_spl_word)[2]


###This customer rents campers, so there are delivery options available.  In their case, we use the below if/else to determine what values to assign in their contracts
###for delivery/pickup options.  This would not be needed for a traditional hotel/b&b type booking.

na = "na"
if "delivery" in input_data.lower():
    delivery_by_us = str(check_in_final)
    pu_by_us = str(check_out_final)
    pu_by_you = str(na)
    return_by_you = str(na)
else:
    delivery_by_us = str(na)
    pu_by_us = str(na)
    pu_by_you = str(check_in_final)
    return_by_you = str(check_out_final) 


json_info = [
{"camper": camper_final,
"cust_name": cust_name_final,
"cust_email": customer_email_final,
"cust_phone": customer_phone_final,
"check_in": check_in_final,
"check_out": check_out_final,
"rate": rate_final,
"extras": extras_final,
"taxes": taxes_final,
"total": total_final,
"pickup_by_you": pu_by_you,
"return_by_you": return_by_you,
"delivery_by_us": delivery_by_us,
"pickup_by_us": pu_by_us,
"nights": nights_final,
"base_rate_total": base_rate_total,
"deposit_total": deposit_total}
]
json_data = json.dumps(json_info, indent=2)
output = json.loads(json_data)