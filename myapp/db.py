import cx_Oracle
from datetime import datetime

local_host = 'localhost'
port_no = '1521'
service_name='XE'
user_name = 'awad'
pwd = 'root'

dsn_tns = cx_Oracle.makedsn(local_host, port_no, service_name=service_name) 


"""sQuery = "commit"
c.execute(sQuery)
c.execute("select * from EMPL3")
for row in c:
    for l in range(len(row)):
        print(f"{row[l]} -", end =" ")
    print("")    
    print("--"*100)"""

def convert_date_format(input_date):
    # Convert input date string to a datetime object
    input_date_object = datetime.strptime(input_date, "%Y-%m-%d")

    # Format the datetime object to the desired output format
    output_date = input_date_object.strftime("%d-%b-%y").upper()

    return output_date

def get_user_logins():
    conn = cx_Oracle.connect(user=user_name, password=pwd, dsn=dsn_tns)
    creds = {'usernames':[], 'passwords':[], 'id':[], 'role':[]}
    query = ('select * from credentials')
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row)
        creds['id'].append(row[0])
        creds['usernames'].append(row[1])
        creds['passwords'].append(row[2])
        creds['role'].append(row[3])
    conn.close()
    return(creds)

def check_user_name_exists(user_name):
    creds = get_user_logins()
    print(creds)
    if user_name in creds['usernames']:
        # If the username exists, find its index
        index = creds['usernames'].index(user_name)
        return index
    else:
        return -1
    
def check_user_name_pwd(user_name, pwd):
    index = check_user_name_exists(user_name)
    print(index)
    if index == -1:
        return False
    creds = get_user_logins()
    if creds['passwords'][index] == pwd:
        return True
    else:
        False

def isadmin(username):
    index = check_user_name_exists(username)
    if index == -1:
        return False
    creds = get_user_logins()
    print(creds['role'][index])
    if creds['role'][index] == 'admin':
        return True
    else:
        False

def ishr(username):
    index = check_user_name_exists(username)
    if index == -1:
        return False
    creds = get_user_logins()
    print(creds['role'][index])
    if creds['role'][index] == 'hr':
        return True
    else:
        False

def return_next_id():
    conn = cx_Oracle.connect(user=user_name, password=pwd, dsn=dsn_tns)
    ids = []
    query = ('select * from credentials')
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        ids.append(row[0])
    conn.close()
    return(max(ids)+1)

def add_user(input_user_name, input_pwd):
    conn = cx_Oracle.connect(user=user_name, password=pwd, dsn=dsn_tns)
    query_check = ('SELECT COUNT(*) FROM credentials WHERE USER_NAME = :input_user_name')
    
    cur_check = conn.cursor()
    cur_check.execute(query_check, input_user_name=input_user_name)
    count = cur_check.fetchone()[0]
    curr_user_id = return_next_id()
    query_insert = ('INSERT INTO credentials(USER_ID, USER_NAME, pass_word, ROLE)'
                    'VALUES(:USER_ID, :USER_NAME, :pass_word, :ROLE)')

    cur_insert = conn.cursor()
    try:
        cur_insert.execute(query_insert, [curr_user_id, input_user_name, input_pwd, 'subscriber'])
        conn.commit()
        conn.close()
        return True 
    except:
        conn.commit()
        conn.close()
        return True 
    
def add_user_admin_db(input_user_name, input_pwd, role):
    conn = cx_Oracle.connect(user=user_name, password=pwd, dsn=dsn_tns)
    query_check = ('SELECT COUNT(*) FROM credentials WHERE USER_NAME = :input_user_name')
    
    cur_check = conn.cursor()
    cur_check.execute(query_check, input_user_name=input_user_name)
    count = cur_check.fetchone()[0]
    curr_user_id = return_next_id()
    query_insert = ('INSERT INTO credentials(USER_ID, USER_NAME, pass_word, ROLE)'
                    'VALUES(:USER_ID, :USER_NAME, :pass_word, :ROLE)')

    cur_insert = conn.cursor()
    try:
        cur_insert.execute(query_insert, [curr_user_id, input_user_name, input_pwd, role])
        conn.commit()
        conn.close()
        return True 
    except:
        conn.commit()
        conn.close()
        return True 
    
def get_user_id(input_user_name):
    conn = cx_Oracle.connect(user=user_name, password=pwd, dsn=dsn_tns)
    ids = []
    query = f"select user_id from credentials where user_name = '{input_user_name}'"
    
    cur = conn.cursor()
    cur.execute(query)
    
    rows = cur.fetchall()
    for row in rows:
        ids.append(row[0])
    
    conn.close()
    
    if len(ids) > 0:
        return ids[-1]
    else:
        return -1
    
def get_nationality_id(nationality_name):
    conn = cx_Oracle.connect(user=user_name, password=pwd, dsn=dsn_tns)
    query = f"select country_id from countries where country_name = '{nationality_name}'"
    cur = conn.cursor()
    cur.execute(query)
    nationality_id = None
    rows = cur.fetchall()
    for row in rows:
        nationality_id = row[0]
    return nationality_id


def get_residence_id(residence_name):
    conn = cx_Oracle.connect(user=user_name, password=pwd, dsn=dsn_tns)
    query = f"select country_id from countries where country_name = '{residence_name}'"
    cur = conn.cursor()
    cur.execute(query)
    residence_id = None
    rows = cur.fetchall()
    for row in rows:
        residence_id = row[0]
    return residence_id

def get_religion_id(religion_name):
    conn = cx_Oracle.connect(user=user_name, password=pwd, dsn=dsn_tns)
    query = f"select religion_id from religions where religion_name = '{religion_name}'"
    cur = conn.cursor()
    cur.execute(query)
    religion_id = None
    rows = cur.fetchall()
    for row in rows:
        religion_id = row[0]
    return religion_id


    
def add_user_profile(input_user_name, user_values):
    user_id = get_user_id(input_user_name)
    if user_id == -1:
        return -1
    else:
        conn = cx_Oracle.connect(user=user_name, password=pwd, dsn=dsn_tns)

        first_name = user_values['first_name']
        last_name = user_values['last_name']
        birth_date = convert_date_format(user_values['birth_date'])
        gender = user_values['gender']
        education = user_values['education']
        job = user_values['job']
        income = user_values['income']
        nationality = user_values['nationality']
        residence = user_values['residence']
        religion_id = user_values['religion']
        fashion_style = user_values['fashion_style']
        hijab_type = user_values['hijab_type']
        marriages_count = user_values['marriages_count']
        divorces_count = user_values['divorces_count']

        nationality_id = get_nationality_id(nationality)
        residence_id = get_residence_id(residence)
        #2023-12-21 ---> 21-DEC-23
        print(user_id)
        query_insert = ('INSERT INTO profile(USER_ID, FIRST_NAME, LAST_NAME, BIRTHDATE, GENDER, EDUCATION, JOB, INCOME, NATIONALITY, RESIDENCE, RELIGION_ID, MARRIAGES_COUNT, DIVORCES_COUNT)'
                        "VALUES(:USER_ID, :FIRST_NAME, :LAST_NAME, :BIRTHDATE, :GENDER, :EDUCATION, :JOB, :INCOME, :NATIONALITY, :RESIDENCE, :RELIGION_ID, :MARRIAGES_COUNT, :DIVORCES_COUNT)")
        

        cur_insert = conn.cursor()
        # cur_insert.execute(query_insert, [user_id, first_name, last_name, birth_date, gender, education, job, income, nationality_id, residence_id, religion_id, marriages_count, divorces_count])
        # conn.commit()
        # conn.close()
        # return True 
        try:
            cur_insert.execute(query_insert, [user_id, first_name, last_name, birth_date, gender, education, job, income, nationality_id, residence_id, religion_id, marriages_count, divorces_count])
            conn.commit()
            conn.close()
            return True 
        except:
            conn.commit()
            conn.close()
            return True 
        
def add_fashion_hijab(input_user_name, fashion_style, hijab_type):
    user_id = get_user_id(input_user_name)
    if user_id == -1:
        return -1
    else:
        conn = cx_Oracle.connect(user=user_name, password=pwd, dsn=dsn_tns)
        cur_insert = conn.cursor()
        query_insert = ('INSERT INTO fashion(USER_ID, STYLE, HIJAB)'
                        "VALUES(:USER_ID, :STYLE, :HIJAB)")
        
        try:
            cur_insert.execute(query_insert, [user_id, fashion_style, hijab_type])
            conn.commit()
            conn.close()
            return True 
        except:
            conn.commit()
            conn.close()
            return True
        

        

def add_hobby(input_user_name, user_hobbies_list):
    user_id = get_user_id(input_user_name)
    if user_id == -1:
        return -1
    else:
        conn = cx_Oracle.connect(user=user_name, password=pwd, dsn=dsn_tns)
        cur_insert = conn.cursor()
        query_insert = ('INSERT INTO user_hobbies(USER_ID, HOBBY_ID)'
                        "VALUES(:USER_ID, :HOBBY_ID)")
        
        for hobby in user_hobbies_list:
            user_hobby = int(hobby)  
            try:
                cur_insert.execute(query_insert, [user_id, user_hobby])
                conn.commit()
            except:
                conn.commit()
    conn.close()
    return True
    
def add_home_skills(input_user_name, user_home_skills_list):
    user_id = get_user_id(input_user_name)
    if user_id == -1:
        return -1
    else:
        conn = cx_Oracle.connect(user=user_name, password=pwd, dsn=dsn_tns)
        cur_insert = conn.cursor()
        query_insert = ('INSERT INTO user_home_skills(USER_ID, SKILL_ID)'
                        "VALUES(:USER_ID, :SKILL_ID)")
        
        for home_skill in user_home_skills_list:
            user_home_skill = int(home_skill)  
            try:
                cur_insert.execute(query_insert, [user_id, home_skill])
                conn.commit()
            except:
                conn.commit()
    conn.close()
    return True

def add_character(input_user_name, user_character_list):
    user_id = get_user_id(input_user_name)
    if user_id == -1:
        return -1
    else:
        conn = cx_Oracle.connect(user=user_name, password=pwd, dsn=dsn_tns)
        cur_insert = conn.cursor()
        query_insert = ('INSERT INTO CHARACTER(USER_ID, SKIN_COLOR, HEIGHT, WEIGHT, EYE_COLOR, HAIR_COLOR, HAIR_LENGTH, HAIR_TYPE, MUSTACHE, BEARD, EYE_GLASSES)'
                        "VALUES(:USER_ID, :SKIN_COLOR, :HEIGHT, :WEIGHT, :EYE_COLOR, :HAIR_COLOR, :HAIR_LENGTH, :HAIR_TYPE, :MUSTACHE, :BEARD, :EYE_GLASSES)")
        try:
            cur_insert.execute(query_insert, [user_id, user_character_list['skin_color'], user_character_list['height'], user_character_list['weight'], user_character_list['eye_color'], user_character_list['hair_color'], user_character_list['hair_length'], user_character_list['hair_type'], user_character_list['mustache'], user_character_list['beard'], user_character_list['eye_glasses']])
            conn.commit()
            conn.close()
            return True 
        except:
            conn.commit()
            conn.close()
            return True
        
def add_family_status(input_user_name, no_sibilings, order_siblings):
    user_id = get_user_id(input_user_name)
    if user_id == -1:
        return -1
    else:
        conn = cx_Oracle.connect(user=user_name, password=pwd, dsn=dsn_tns)
        cur_insert = conn.cursor()
        query_insert = ('INSERT INTO FAMILY_STATUS(USER_ID, NUM_SIBLINGS, ORDER_BETWN_SIBLINGS)'
                        "VALUES(:USER_ID, :NUM_SIBLINGS, :ORDER_BETWN_SIBLINGS)")
        try:
            cur_insert.execute(query_insert, [user_id, no_sibilings, order_siblings])
            conn.commit()
            conn.close()
            return True 
        except:
            conn.commit()
            conn.close()
            return True
        
def add_social_class(input_user_name, user_class, bank_balance, car_type):
    user_id = get_user_id(input_user_name)
    if user_id == -1:
        return -1
    else:
        conn = cx_Oracle.connect(user=user_name, password=pwd, dsn=dsn_tns)
        cur_insert = conn.cursor()
        query_insert = ('INSERT INTO SOCIAL_CLASS(USER_ID, USER_CLASS, BANK_BALANCE, CAR_TYPE)'
                        "VALUES(:USER_ID, :USER_CLASS, :BANK_BALANCE, :CAR_TYPE)")
        try:
            cur_insert.execute(query_insert, [user_id, user_class, bank_balance, car_type])
            conn.commit()
            conn.close()
            return True 
        except:
            conn.commit()
            conn.close()
            return True
        
def get_partner(input_user_name, partner_character_list):
    user_id = get_user_id(input_user_name)
    if user_id == -1:
        return -1
    else:
        conn = cx_Oracle.connect(user=user_name, password=pwd, dsn=dsn_tns)
        cur_insert = conn.cursor()
        skin_color = partner_character_list['skin_color']
        height = partner_character_list['height']
        weight = partner_character_list['weight']
        eye_color = partner_character_list['eye_color']
        hair_color = partner_character_list['hair_color']
        hair_length = partner_character_list['hair_length']
        hair_type = partner_character_list['hair_type']
        mustache = partner_character_list['mustache']
        beard = partner_character_list['beard']
        eye_glasses = partner_character_list['eye_glasses']
        hijab_type  = partner_character_list['hijab_type']
        fashion_style  = partner_character_list['fashion_style']
        min_income  = partner_character_list['min_income']
        gender  = partner_character_list['gender']
        religion  = int(partner_character_list['religion'])

        query_find = f"""
                SELECT P.FIRST_NAME, P.LAST_NAME, P.INCOME, P.MARRIAGES_COUNT
                FROM PROFILE P
                JOIN CHARACTER R ON P.USER_ID = R.USER_ID
                JOIN FASHION F ON P.USER_ID = F.USER_ID
                WHERE R.SKIN_COLOR = '{skin_color}'
                    AND R.HEIGHT >= {height}
                    AND R.WEIGHT <= {weight}
                    AND R.EYE_COLOR = '{eye_color}'
                    AND R.HAIR_COLOR = '{hair_color}'
                    AND R.HAIR_LENGTH = '{hair_length}'
                    AND R.HAIR_TYPE = '{hair_type}'
                    AND R.MUSTACHE = '{mustache}'
                    AND R.BEARD = '{beard}'
                    AND F.HIJAB = '{hijab_type}'
                    AND F.STYLE = '{fashion_style}'
                    AND P.INCOME > {min_income}
                    AND P.GENDER = '{gender}'
                    AND P.RELIGION_ID = {religion}
            """
        print(query_find)
        
        cur_insert.execute(query_find)
        rows = cur_insert.fetchall()
        result_list = []
        for row in rows:
            result_dict = {
                'first_name': row[0],
                'last_name': row[1],
                'income': row[2],
                'marriages_count': row[3]
            }
            result_list.append(result_dict)
    return result_list
        
def delete_user_db(input_user_name):
    user_id = get_user_id(input_user_name)
    if user_id == -1:
        return -1
    else:
        conn = cx_Oracle.connect(user=user_name, password=pwd, dsn=dsn_tns)
        cur_delete = conn.cursor()
        query_delete = 'DELETE FROM credentials WHERE user_id = :user_id'
        try:
            cur_delete.execute(query_delete, {'user_id': user_id})
            conn.commit()
            conn.close()
            return True 
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print("Error code:", error.code)
            print("Error message:", error.message)
            conn.rollback()
            conn.close()
            return False
        
def edit_user_profile_db(input_user_name, user_values):
    user_id = get_user_id(input_user_name)
    if user_id == -1:
        return -1
    else:
        conn = cx_Oracle.connect(user=user_name, password=pwd, dsn=dsn_tns)

        first_name = user_values['first_name']
        last_name = user_values['last_name']
        birth_date = convert_date_format(user_values['birth_date'])
        education = user_values['education']
        job = user_values['job']
        income = user_values['income']
        nationality = user_values['nationality']
        residence = user_values['residence']
        nationality_id = get_nationality_id(nationality)
        residence_id = get_residence_id(residence)
        role = user_values['role']
        
        query_update = ('UPDATE profile SET FIRST_NAME = :FIRST_NAME, LAST_NAME = :LAST_NAME, BIRTHDATE = :BIRTHDATE, EDUCATION = :EDUCATION, JOB = :JOB, INCOME = :INCOME, NATIONALITY = :NATIONALITY, RESIDENCE = :RESIDENCE WHERE USER_ID = :USER_ID')
        query_update_role = ('UPDATE credentials SET ROLE = :ROLE WHERE USER_ID = :USER_ID')

        cur_update = conn.cursor()
        cur_update_role = conn.cursor()
        try:
            cur_update.execute(query_update, {'USER_ID': user_id, 'FIRST_NAME': first_name, 'LAST_NAME': last_name, 'BIRTHDATE': birth_date, 'EDUCATION': education, 'JOB': job, 'INCOME': income, 'NATIONALITY': nationality_id, 'RESIDENCE': residence_id})
            cur_update_role.execute(query_update_role, {'USER_ID': user_id, 'ROLE': role})
            conn.commit()
            conn.close()
            return True 
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print("Error code:", error.code)
            print("Error message:", error.message)
            conn.rollback()
            conn.close()
            return False
        
def query_profiles_from_hr_db():
    try:
        # Establish a connection to the Oracle database
        conn = cx_Oracle.connect(user=user_name, password=pwd, dsn=dsn_tns)
        cur = conn.cursor()

        # Query the view
        query = "SELECT * FROM profile_view"
        cur.execute(query)

        # Fetch all rows from the result set
        rows = cur.fetchall()

        # Define a list to store the result
        profiles = []

        # Iterate through the rows and create a dictionary for each row
        for row in rows:
            profile = {
                'first_name': row[0],
                'last_name': row[1],
                'birthdate': row[2],
                'gender': row[3],
                'residence': row[4],
                'income': row[5]
            }
            profiles.append(profile)

        # Close the cursor and connection
        cur.close()
        conn.close()

        return profiles

    except cx_Oracle.DatabaseError as e:
        print("Error:", e)
        return None
    

def query_profiles_from_admin_db():
    try:
        # Establish a connection to the Oracle database
        conn = cx_Oracle.connect(user=user_name, password=pwd, dsn=dsn_tns)
        cur = conn.cursor()

        # Query the view
        query = "SELECT * FROM admin_users_view"
        cur.execute(query)

        # Fetch all rows from the result set
        rows = cur.fetchall()

        # Define a list to store the result
        profiles = []

        # Iterate through the rows and create a dictionary for each row
        for row in rows:
            profile = {
                'first_name': row[0],
                'last_name': row[1],
                'birthdate': row[2],
                'gender': row[3],
                'residence': row[4],
                'income': row[5],
                'username': row[6],
                'pwd':row[7]
            }
            profiles.append(profile)

        # Close the cursor and connection
        cur.close()
        conn.close()

        return profiles

    except cx_Oracle.DatabaseError as e:
        print("Error:", e)
        return None


    

