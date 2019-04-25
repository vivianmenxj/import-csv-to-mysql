'''
import_csv_data.py

This script retrieves data from CSV file and 
insert the data to corresponding database.

'''
import csv
import pymysql
import traceback
import io
import time
import datetime
import configparser
import os


def main():
    '''
    main module
    '''
    try:
        # get configurations from config file
        cf = configparser.ConfigParser()
        cf.read("config.conf")
        db_host = cf.get('database','dbhost')
        db_port = int(cf.get('database','dbport'))
        db_name = cf.get('database','dbname')
        db_user = cf.get('database','dbuser')
        db_password = cf.get('database','dbpassword')
        db_charset = cf.get('database','dbcharset')
        csv_file = cf.get('csvfile','name')
        #establish sql connection
        sqlconn = get_conn(db_host,db_port,db_name,db_user,db_password,db_charset) 
        cur = sqlconn.cursor()
        record ={}
        print("Reading data from file...")
        with open(os.path.split(os.path.realpath(__file__))[0] + "/" + csv_file, newline='',encoding='utf-8') as f:
        
            reader = csv.reader(f) 
            head = next(reader)   
            for item in reader: 
                record['A'] = capitalize_acronyms(item[0])
                record['B'] = convert_title(item[1])
                record['C'] = capitalize_first_letter_of_name(item[2])
                record['D'] = capitalize_first_letter_of_name(item[3])
                record['E'] = convert_birth(item[4])
                record['F'] = item[5]
                record['G'] = item[6] 
                record['H'] = item[7]
                record['I'] = item[8] 
                record['J'] = item[9]      
                record['K'] = add_prefix_to_numbers(item[10])
                record['L'] = add_prefix_to_numbers(item[11])
                record['M'] = add_prefix_to_numbers(item[12])
                record['N'] = add_prefix_to_numbers(item[13])
                record['O'] = add_prefix_to_numbers(item[14])
                record['P'] = item[15]
    
                record['contact_id'] = -1
                # Step 1: insert into contact
                sql = build_insert_sql('contact', get_contact_data(record), sqlconn)
                if(sql):
                    result = cur.execute(sql[0])
                    if(result is not False):
                        record['contact_id'] = sqlconn.insert_id()
                        print("Data has been inserted to contact table with contact_id" + str(record['contact_id']))
       
                # step 2: insert into address  
                sql = build_insert_sql('address', get_address_data(record), sqlconn)
                if(sql):
                    for item in sql:
                        result = cur.execute(item)  
                        print("Data has been inserted to address table with contact_id" + str(record['contact_id']))
        
                # step 3: insert into phone  
                sql = build_insert_sql('phone', get_phone_data(record), sqlconn)
                if(sql):
                    for item in sql:
                        result = cur.execute(item) 
                        print("Data has been inserted to phone table with contact_id" + str(record['contact_id']))
        
        sqlconn.commit()
        sqlconn.close()
        print("All data have been inserted into DB.")

    # pylint: disable=bare-except
    except:
        print("Failed to insert to db.")
        traceback.print_exc()
        exit(1)


def get_conn(db_host,db_port,db_name,db_user,db_password,db_charset) : 
    conn = pymysql.connect(host=db_host, port=db_port, user=db_user, passwd=db_password, db=db_name, charset=db_charset) 
    return conn

def build_insert_sql(table, data, sqlconn):
    if (any(data)):
        sql_list = []
        for item in data:
            sql_key = '' 
            sql_value = '' 
            for key in item.keys():
                sql_value = (sql_value + '"' + sqlconn.escape_string(str(item[key])) + '"' + ',') 
                sql_key = sql_key + ' ' + key + ','
            sql = "INSERT INTO %s (%s) VALUES (%s)" %(table, sql_key[:-1], sql_value[:-1])
            sql_list.append(sql)
        return sql_list
    

def get_contact_data(record):
    '''
    get the data for table: contact
    '''
    print("Executing get_contact_data  ")
    data_list = []
    data = {
        'first_name': record['C'],
        'last_name': record['D'],
        'company_name': record['A'],
        'notes': record['P']
        }
    if (any(record['B'])):
        data['title'] = record['B']
    if (record['E']):
        data['date_of_birth'] = record['E']
    data_list.append(data)
    print("Successfully executed get_contact_data ")
    return data_list

def get_address_data(record):
    '''
    get the data for table: address
    '''
    if (record['contact_id'] < 0):
        print("contact_id does not exist, exiting")
        exit(1)
    else:
        data_list = []
        data = {
            'contact_id':record['contact_id'],
            'street1':record['F'],
            'street2':record['G'],
            'suburb':record['H'],
            'city':record['I'],
            'post_code':record['J']
            }
        data_list.append(data)
        return data_list

def get_phone_data(record):
    '''
    get the data for table: phone
    '''
    if (record['contact_id'] < 0):
        print("contact_id does not exist, exiting")
        exit(1)
    else:
        data_list = []
        name = record['C'] + " " + record['D']
        if (any(record['K'])):
            data = {
                'contact_id':record['contact_id'],
                'name':name,
                'content':record['K'],
                'type':'Home'
            }
            data_list.append(data)
        if (any(record['L'])):
            data = {
                'contact_id':record['contact_id'],
                'name':name,
                'content':record['L'],
                'type':'Other'
            }
            data_list.append(data)           
        if (any(record['M'])):
            data = {
                'contact_id':record['contact_id'],
                'name':name,
                'content':record['M'],
                'type':'Work'
            }
            data_list.append(data)
        if (any(record['N'])):
            data = {
                'contact_id':record['contact_id'],
                'name':name,
                'content':record['N'],
                'type':'Mobile'
            }
            data_list.append(data)
        if (any(record['O'])):
            data = {
                'contact_id':record['contact_id'],
                'name':name,
                'content':record['O'],
                'type':'Other'
            }
            data_list.append(data)
        return data_list

def capitalize_acronyms(business):
    '''
    business: value of business column in the csv
    return capitalized acronyms
    '''
    input = business.strip()
    if (any(input) == False):
        return business
    items = input.split(' ')
    if (items[0].find('.') != -1):
        items[0] = items[0].upper()
    return  ' '.join(items)   

def capitalize_first_letter_of_name(name):   
    '''
    name: First and Last names.
    '''
    name = name.strip()
    if (any(name) == False):
        return ''
    return name.capitalize()
    
def add_prefix_to_numbers(number): 
    '''
    number: Mobile and Landline numbers.
    add prefix 64 to Mobile numbers and 09 to Landline numbers
    '''   
    number = number.strip()
    if (any(number) == False):
        return ''
    number = number.replace('(','').replace(')','').replace('-','').replace(' ','')
    if (any(number) == False):
        return ''
    if(len(number) <= 7):
        return "09{$number}" 
    if(number.find('09') == 0) or (number.find('64') == 0):
        return number
    return "64{$number}"

def convert_birth(birth):
    '''
    birth: Date Of Birth column .
    make the birth data using same format
    '''
    birth = birth.strip()
    if (any(birth) == False):
        return ''
    birth = birth.replace('-','/')
    items = birth.split('/')
    if(len(items[2]) == 2):
        items[2] = "19" + items[2]
    birth = '-'.join(items)
    birth_time = datetime.datetime(int(items[2]),int(items[0]),int(items[1]),0,0)
    return birth_time

def convert_title(title):
    '''
    title: data from column title.
    make sure the data in ('Mr', 'Mrs', 'Miss', 'Ms', 'Dr')
    '''
    title = title.strip().strip('.').title()
    titles = {'Mr', 'Mrs', 'Miss', 'Ms', 'Dr'}
    if title in titles:
        return title
    else:
        return ''

        
        
if __name__ == '__main__':
    main()
