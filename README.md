# clipw
Python3 Powered Command Line Password Manager


### Description:


<p>Clipw is a very simply, secure (audits welcome) command line interface, python3 powered 
password manager! Store a password, and a description; with the option to create secure random 
passwords. Notice: This is work in progress. New features will be added as I get to them. 
If you want to fork and help out, pull requests are welcome.
</p>

### Features:

- Fast sqlite powered database
- Passwords encrypted in AES-CRT using pure python package `pyaes`
- Libs organized into neat packages for easy reuse or expansion
- Functional setup.py script includes
- Option to store or generate a random password
- Simple cli friendly interface
- Pure python3




### Installation:

- Clone this repository to your computer. 
- Run pip3 install -r requirements.txt to install dependencies )
- Now includes setup.py:

<pre>
$ python3 setup.py build
$ python3 setup.py install --user
</pre>


### Usage:
<pre>
usage: clipw [-h] [--init,] [-i] [-o] [-s] [-e] [-d]
             [-r [GEN_RANDOM [GEN_RANDOM ...]]]

Python Cli Password Manager

optional arguments:
  -h, --help            show this help message and exit
  --init, --init_database
                        Re|Init Database
  -i, --interactive     Interactive mode
  -o, --open            Open the password database
  -s, --store           Enter and store a new password in the database
  -e, --edit            Edit an entry.
  -d, --delete          Delete an entry
  -r [GEN_RANDOM [GEN_RANDOM ...]], --random [GEN_RANDOM [GEN_RANDOM ...]]
                        Generate and store a random password of n length


</pre>

First, run with --init_database. You will be prompted to enter a master passphrase which will be used to encrypt 
all of the passwords which you store in the database. Key must be at least 8 and up to 
32 characters long. Pick a `strong` master passphrase. 


##### <b>New</b>: Interactive mode (`clipw -i`)

Interactive mode keeps the program open without having to re-enter the key over and 
over over every time you need to retrieve a password.
TODO: add a timeout feature


<pre>
$ clipw -i
Master Password: 
Success!
Running in interactive mode.
Enter action: store (s), generate: (g), open and select entry: (o), edit entry: (e), delete entry: (d), quit program (q)
</pre>

Generate a random password 8 characters long:

<pre>
$ clipw.py -r 8 
Master Password: 
Success!
Description: test4
Password: cnY{2k"6|@Ho
</pre>

Store a password into the database:
<pre>
$ clipw.py -s
Master Password: 
Success!
Description: test 
Password: 
Confirm: 
Stored password ok.
</pre>

Open the database and retrieve a password:
<pre>
Master Password: 
Success!
ID:  0 Description test 1
ID:  1 Description gmail
ID:  2 Description github
ID:  3 Description test 2
Enter ID of password to decrypt: 3
Retrieving ID  3
Id:  3
Description: test test 
Password: lol
</pre>


### Flowchart / Psuedocode

- init database:
 - input master key
   - Check keysize - add padding for AES compliance if necessary
 - hash master key
 - store hash in file
 - create empty database

- generate_password:
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
    
