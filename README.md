# clipw
Python3 Powered Command Line Password Manager

## Installation:

- Run pip3 install -r requirements.txt to install dependencies (only need pyaes)
- Clone this repository to your computer. Place `clipw.py` somewhere in your system path (like /usr/local/bin). 
- Add executable permission to `clipw.py` (chmod +x)


## Usage:
<pre>
usage: clipw.py [-h] [-i,--init_database] [-s] [-r GEN_RANDOM] [-o]

Python Cli Password Manager

optional arguments:
  -h, --help            show this help message and exit
  -i,--init_database    Re|Init Database
  -s, --store           Enter and store a new password in the database
  -r GEN_RANDOM, --random GEN_RANDOM
                        Generate and store a random password of n length
  -o, --open            Open the password database

</pre>

First, run with -i or --init_database. You will be prompted to enter a master passphrase which will be used to encrypt all of the passwords which you store in the database. Key must be at least 8 and up to 32 characters long. 

## Flowchart / Psuedocode

init database:
 - input master key
   - Check keysize - add padding for AES compliance if necessary
 - hash master key
 - store hash in file
 - create empty database

 generate_password:
 - store from getpass || generate random password
 - encrypt password
 - get description data
 - store encrypted password in database with description data

 open_database:
 - prompt use for master key
 - check master key against stored hash
  - if correct:
    - open database
     - iterate through database
     - display description with numeric id
     - prompt for id of password to retrieve
     - show password
     -exit
  - if incorrect:
    - prompt to try again
    
  TODO: Add a function to edit current entries
