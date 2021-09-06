# this is a simple terminal app to add data to our database for the user hashes
from hashlib import sha256
import random
# import mysql.connector


try:

    dbx = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root"
    )
    
    cursor = dbx.cursor()

except:

    print("MYSQL DB Connection Error")



"""
CREATION FUNCTIONS
"""

def make_voter_table():
    global dbx
    global cursor
    """
    Makes the voters / users table
    """
    make_voter_table = '''
    CREATE TABLE voters (
        voterhash VARCHAR(255) PRIMARY KEY
    )
    '''
    try:
        cursor.execute(make_voter_table)
        dbx.commit()
    except:
        return False
    return



def make_candidates_table():
    """
    Creates a Candidate Table. Which stores the name of the candidate and a short description of the candidate
    """
    make_candidates_table = '''
    CREATE TABLE candidates (
        candidate_name VARCHAR(255) PRIMARY KEY,
        description VARCHAR(255)
    )
    '''
    try:
        cursor.execute(make_candidates_table)
        dbx.commit()
    except:
        return False
    return




"""
ADDITION FUNCTIONS
"""



def add_candidate(name, description):
    """
    Adds a candidate to the candidate table
    """
    insert_candidate = '''
    INSERT INTO candidates VALUES (
        %s,
        %s
    )
    '''
    vals = (name, description)
    try:
        cursor.execute(insert_candidate, vals)
        dbx.commit()
    except:
        return False
    return



def add_voter(fname, lname, password):
    """
    Function adds a user to our database.

    To protect user anonyminity and prevent vote suppression, we will not be storing the actual identity
    of these voters, rather we will be storing a hash based on details, that we can verify later on.

    This returns the voterid for the person. We will be generating a voterid here, only ONCE.
    """
    insert_voter = '''
    INSERT INTO voter VALUES (
        %s
    )
    '''
    voter_id = random.randint(10000000, 999999999)
    details_string = fname + lname + password + voter_id
    hashed = sha256(details_string.encode()).hexdigest()
    vals = (hashed)
    try:
        cursor.execute(insert_voter, vals)
        dbx.commit()
    except:
        return voter_id

    ## now add this to the mysql database. Just make one column called voters, and store this hash.

    return voter_id


"""
READ FUNCTIONS
"""

def verify_exists(fname, lname, password, voter_id):
    """
    This function is to ensure that a certain voter exists.

    It takes in some data, and computes the hash. If the hash exists, it returns True, else false.
    """
    details_string = fname + lname + password + voter_id
    hashed = sha256(details_string.encode()).hexdigest()

    verify_voter = '''
    SELECT * FROM voters
    WHERE voterhash='%s'
    '''
    vals = (hashed)
    try:
        cursor.execute(verify_voter, vals)
        result = cursor.fetchone()
        if len(result) != 0:
            return True
    except:
        #TODO: Must change later
        return True


def get_candidates():
    """
    Returns the entire table and the descriptions
    """
    get_candidate_statement = '''
    SELECT * FROM candidates
    '''
    try:
        cursor.execute(get_candidate_statement)
        result = cursor.fetchall()
        return result
    except:
        # to stop failures at this point
        return [
            ('Candidate1', 'Description'),
            ('Candidate2', 'Description2'),
            ('Candidate3', 'Description3'),
            
        ]
    return


def remove_candidate():
    """
    Removes a candidate from the candidate table
    """
    return