# Wix-Hotels-Reservation-Python
Python script to parse and extract data from Wix Hotels "New Reservation" email


This python script can extract data (such as customer name, customer email, nights booked, nightly rate, etc.) from emails
received when a new booking is made through Wix Hotels.  

In my customer's use case, we used Zapier to integrate with their G Suite account and search for new emails with the subject 
line "You just got a new reservation!"

You can use smtplib as well to check email, but Zapier was already present for some other automation.

Calculating Deposit:
In Wix Hotels, it is possible to collect a deposit up front from the customer when booking.  In my customer's case, they 
collect a 25% deposit of the total before taxes or add-ons.  The python script takes care of calculating how much was paid as a deposit (since this is not present in the Wix email).  This deposit amount is then subtracted from the total amount (present in the email), giving the remaining balance. This percentage can vary and may not be necessary for everyone.  

After parsing the data, the script will output the data in json.  We then use this to send to SignRequest (again using Zapier integration).  SignRequest will auto-populate a pdf template using the variables extracted from the original Wix email. This is used for generating rental contracts which are then signed by the renters and returned back to my customer prior to arriving.  
