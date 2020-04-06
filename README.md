# ebay-item-finder
I made this script because it can be repetitive browsing eBay for newly listed items for sale. This script can be run in the background (or on a Raspberry Pi) and will notify you by email when it finds a new product. To use, follow these steps:
- Specify the items you are looking for in keywords.txt
- Specify information in config/settings.py
- Run the script

## Prerequisites
- Python 3.6 or newer
- requests 2.23.0

## Specifying items in keywords.txt
Input must adhere to this format:  
Format:
```
keywords, max_price
```
Example: 
```
Jordan 1 Chicago 8.5, 400
```
You can also specify many items:  
Example: 
```
Nike React Sertu, 100
Yeezy Wave Runner, 300
```
## Specifying information in config/settings.py
Use this file to input your API Key, Emails and Postcode:

- API Key - Get one by registering here -> https://developer.ebay.com/
- Emails - Enter the email address and password of the email you will be sending emails from. Enter the email address you will be directing your emails to. (Important Notice: The current SMTP settings in the script are set for Gmail! Please change if you are using another service!)
- Postcode - Enter the buyer postal code.

## Running the script
Execute:
```
python3 autoebay.py
```
