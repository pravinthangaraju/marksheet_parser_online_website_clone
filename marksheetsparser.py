import os
import re
from PIL import Image
from dateutil import parser
import pytesseract
import csv
import cv2
import numpy as np
from scipy.ndimage import rotate as rotate_image
import difflib
from flask import Flask, request, render_template, flash, redirect,send_file, url_for
from itertools import islice

app = Flask(__name__)

UPLOAD_FOLDER = 'UploadedMarksheets'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
OUTPUT_FOLDER = 'C:\\Users\\pravin\\Desktop\\image_to_text'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
################################################################################################################

###############################################################################################################    

uploaded_filenames_set = set()

@app.route('/')
def homepage():
    global uploaded_filenames_set  # Declare the variable as global inside the function
    uploaded_filenames_set = set()  # Reset uploaded_filenames_set to an empty set

    if os.path.exists('StateboardTenthInputcsvfile.csv'):
        open('StateboardTenthInputcsvfile.csv', 'w').close() # If file exists, append; otherwise, write

    if os.path.exists('StateboardTwelthInputcsvfile.csv'):
        open('StateboardTwelthInputcsvfile.csv', 'w').close() # If file exists, append; otherwise, write

    if os.path.exists('CBSETenthInputcsvfile.csv'):
        open('CBSETenthInputcsvfile.csv', 'w').close() # If file exists, append; otherwise, write
   
    if os.path.exists('CBSETwelthInputcsvfile.csv'):
        open('CBSETwelthInputcsvfile.csv', 'w').close() # If file exists, append; otherwise, write

    return render_template('homepage.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#UploadMarksheetsStateboardTenthInputcsvfile--1
@app.route('/UploadMarksheetsStateboardTenthInputcsvfile', methods=['GET', 'POST'])
def upload_file1():
    global uploaded_filenames_set
    
    upload_message = None
    Marksheetstype = None
    uploaded_filenames = []  # List to store newly uploaded filenames

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        files = request.files.getlist('file')  # Get list of uploaded files

        # Iterate through each uploaded file
        for file in files:
            # If user does not select file, browser also submits an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = file.filename
                if filename not in uploaded_filenames_set:  # Check if filename is not already uploaded
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    uploaded_filenames_set.add(filename)  # Add filename to the set
                    uploaded_filenames.append(filename)  # Add filename to the list
                    upload_message = 'Files uploaded successfully'
                    Marksheetstype = 'StateboardTenth'
                else:
                    flash(f'File "{filename}" has already been uploaded')  # Flash message for duplicate filename
            else:
                flash('Invalid file type. Only images (png, jpg, jpeg, gif) are allowed.')

    # Append newly uploaded filenames to the existing CSV file
    if uploaded_filenames:
        csv_file = 'StateboardTenthInputcsvfile.csv'
        mode = 'a' if os.path.exists(csv_file) else 'w'  # If file exists, append; otherwise, write

        with open(csv_file, mode, newline='') as csvfile:
            writer = csv.writer(csvfile)
            for filename in uploaded_filenames:
                writer.writerow([filename])

    print('StateboardTenthInputcsvfile.csv is ready')
    return render_template('index.html', upload_message=upload_message, Marksheetstype=Marksheetstype)
###############################################################################################################
#UploadMarksheetsStateboardtwelthInputcsvfile--2 
@app.route('/UploadMarksheetsStateboardtwelthInputcsvfile', methods=['GET', 'POST'])
def upload_file2():
    global uploaded_filenames_set
    upload_message = None
    Marksheetstype = None
    uploaded_filenames = []  # List to store newly uploaded filenames

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        files = request.files.getlist('file')  # Get list of uploaded files

        # Iterate through each uploaded file
        for file in files:
            # If user does not select file, browser also submits an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = file.filename
                if filename not in uploaded_filenames_set:  # Check if filename is not already uploaded
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    uploaded_filenames_set.add(filename)  # Add filename to the set
                    uploaded_filenames.append(filename)  # Add filename to the list
                    upload_message = 'Files uploaded successfully'
                    Marksheetstype = 'StateboardTwelth'
                else:
                    flash(f'File "{filename}" has already been uploaded')  # Flash message for duplicate filename
            else:
                flash('Invalid file type. Only images (png, jpg, jpeg, gif) are allowed.')

    # Append newly uploaded filenames to the existing CSV file
    if uploaded_filenames:
        csv_file = 'StateboardTwelthInputcsvfile.csv'
        mode = 'a' if os.path.exists(csv_file) else 'w'  # If file exists, append; otherwise, write
        with open(csv_file, mode, newline='') as csvfile:
            writer = csv.writer(csvfile)
            #if mode == 'w':  # If writing for the first time, add header
                #writer.writerow(['Filename'])
            for filename in uploaded_filenames:
                writer.writerow([filename])

    print('StateboardTwelthInputcsvfile.csv is ready')
    return render_template('index.html', upload_message=upload_message, Marksheetstype=Marksheetstype)
###############################################################################################################
#UploadMarksheetsCBSETenthInputcsvfile--3
@app.route('/UploadMarksheetsCBSETenthInputcsvfile', methods=['GET', 'POST'])
def upload_file3():
    global uploaded_filenames_set
    upload_message = None
    Marksheetstype = None
    uploaded_filenames = []  # List to store newly uploaded filenames

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        files = request.files.getlist('file')  # Get list of uploaded files

        # Iterate through each uploaded file
        for file in files:
            # If user does not select file, browser also submits an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = file.filename
                if filename not in uploaded_filenames_set:  # Check if filename is not already uploaded
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    uploaded_filenames_set.add(filename)  # Add filename to the set
                    uploaded_filenames.append(filename)  # Add filename to the list
                    upload_message = 'Files uploaded successfully'
                    Marksheetstype = 'CBSETenth'
                else:
                    flash(f'File "{filename}" has already been uploaded')  # Flash message for duplicate filename
            else:
                flash('Invalid file type. Only images (png, jpg, jpeg, gif) are allowed.')

    # Append newly uploaded filenames to the existing CSV file
    if uploaded_filenames:
        csv_file = 'CBSETenthInputcsvfile.csv'
        mode = 'a' if os.path.exists(csv_file) else 'w'  # If file exists, append; otherwise, write
        with open(csv_file, mode, newline='') as csvfile:
            writer = csv.writer(csvfile)
            #if mode == 'w':  # If writing for the first time, add header
                #writer.writerow(['Filename'])
            for filename in uploaded_filenames:
                writer.writerow([filename])

    print('CBSETenthInputcsvfile.csv is ready')
    return render_template('index.html', upload_message=upload_message, Marksheetstype=Marksheetstype)

#########################################################################################################################
#UploadMarksheetsStateboardtwelthInputcsvfile--4 
@app.route('/UploadMarksheetsCBSEtwelthInputcsvfile', methods=['GET', 'POST'])
def upload_file4():
    global uploaded_filenames_set
    upload_message = None
    Marksheetstype = None
    uploaded_filenames = []  # List to store newly uploaded filenames

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        files = request.files.getlist('file')  # Get list of uploaded files

        # Iterate through each uploaded file
        for file in files:
            # If user does not select file, browser also submits an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = file.filename
                if filename not in uploaded_filenames_set:  # Check if filename is not already uploaded
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    uploaded_filenames_set.add(filename)  # Add filename to the set
                    uploaded_filenames.append(filename)  # Add filename to the list
                    upload_message = 'Files uploaded successfully'
                    Marksheetstype = 'CBSETwelth'
                else:
                    flash(f'File "{filename}" has already been uploaded')  # Flash message for duplicate filename
            else:
                flash('Invalid file type. Only images (png, jpg, jpeg, gif) are allowed.')

    # Append newly uploaded filenames to the existing CSV file
    if uploaded_filenames:
        csv_file = 'CBSETwelthInputcsvfile.csv'
        mode = 'a' if os.path.exists(csv_file) else 'w'  # If file exists, append; otherwise, write
        with open(csv_file, mode, newline='') as csvfile:
            writer = csv.writer(csvfile)
            #if mode == 'w':  # If writing for the first time, add header
                #writer.writerow(['Filename'])
            for filename in uploaded_filenames:
                writer.writerow([filename])

    print('CBSETwelthInputcsvfile.csv is ready')
    return render_template('index.html', upload_message=upload_message, Marksheetstype=Marksheetstype)

#######################################################################################################################
#######################################stateboard10th###########################################
def Stateboard_tenth_total_marks_extraction_Line_to_number(text):
    # Define a regular expression pattern to match numerical words
    pattern = r'\b(?:ZERO|ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE)+\b'
     # Find all numerical words in the line
    numerical_words = re.findall(pattern, text)
    # Convert numerical words to their corresponding digits
    digits_mapping = {
        "ZERO": "0",
        "ONE": "1",
        "TWO": "2",
        "THREE": "3",
        "FOUR": "4",
        "FIVE": "5",
        "SIX": "6",
        "SEVEN": "7",
        "EIGHT": "8",
        "NINE": "9"
    }
    numers = ''.join(digits_mapping[word] for word in numerical_words)
    return numers
def extract_date(line):
    # Define the regex pattern for matching dates in the format dd.mm.yyyy
    date_pattern = r'\b(\d{2}\.\d{2}\.\d{4})\b'
    
    # Search for the date pattern in the line
    match = re.search(date_pattern, line)
    
    # If a match is found, parse the date using dateutil.parser
    if match:
        '''
        date_str = match.group(1)
        date = parser.parse(date_str, dayfirst=True)
        formatted_date = date.strftime("%d.%m.%Y")'''
        matched_string = match.group(1)
        return matched_string
    else:
        return None
    


def postprocess_Stateboard_tenth(mystring):
    keywords = ['total','school','mar','english']
    lines = mystring.split('\n')

    # dictionary for relevant lines
    l={}

    # dictionary for final result
    ans = {}
    ans.setdefault('studentname',[])
    ans.setdefault('school',[])
    ans.setdefault('dateofbirth',[])
    ans.setdefault('examno',[])
    ans.setdefault('percentage',[])
    for k in keywords:
        l.setdefault(k,[])
        

    # extracting relevant lines from tesseract output
    for line in lines:
        if(len(line)>0):
            words = line.split(' ')
            for w in words:
                w = w.lower()
                result = difflib.get_close_matches(w,keywords,1,0.85)
                if(len(result)>0):
                    key = result[0]
                    l[result[0]].append(line)

    # extracting relevant information from the dictionary l
    for k in keywords:
        prev=''
        for str in l[k]:
            if(prev == ''):
                prev = l[k]
            elif(prev == str):
                continue
            else:
                prev = str

            if (k == 'mar'):
                wrds = str.split('  ')
                for wrd in wrds:
                    subwrds = wrd.lower().split(' ')
                    result = difflib.get_close_matches(k, subwrds, 1, 0.85)
                    if(len(result)>0):
                        namestudent = ' '.join(wrd.split()[:-2])
                        ans['studentname'].append(namestudent)

            if (k == 'school'):
                wrds = str.split('  ')
                for wrd in wrds:
                    subwrds = wrd.lower().split(' ')
                    result = difflib.get_close_matches(k, subwrds, 1, 0.85)
                    if(len(result) > 0):
                        # Append the entire line after the first occurrence of "school"
                        if 'name' in wrd.lower() or 'secondary' in wrd.lower() or 'leaving' in wrd.lower() or 'board' in wrd.lower() or 'examinations' in wrd.lower():
                            continue
                        schoolname = ' '.join(wrd.lower().split())
                        ans['school'].append(schoolname)


            if(k=='english'):
                wrds = str.split('  ')
                for wrd in wrds:
                    subwrds = wrd.lower().split(' ')
                    result = difflib.get_close_matches(k, subwrds, 1, 0.85)
                    if(len(result)>0):
                            if '9ydiéteutb' in wrd.lower() or 'Qyruélovwd' in wrd.lower()  or 'zero' in wrd.lower() or 'one'in wrd.lower() or 'two'in wrd.lower() or 'three'in wrd.lower() or 'four'in wrd.lower() or 'five'in wrd.lower() or 'six'in wrd.lower() or 'seven'in wrd.lower() or 'eight'in wrd.lower() or 'nine'in wrd.lower():
                                continue   
                            
                            examno = ' '.join(wrd.split())
                            sa=examno.split()
                            # Use list comprehension to extract numeric values
                            numeric_values = [word for word in sa if word.isdigit()]
                            array_as_string = ' '.join(numeric_values)
                            ans['examno'].append(array_as_string)
                            #birthday = ' '.join(wrd.split()[:1])
                            birthday = ' '.join(wrd.split())
                            date = extract_date(birthday)
                            ans['dateofbirth'].append(date)
            
            if (k == 'total'):
                wrds = str.split('  ')
                for wrd in wrds:
                    subwrds = wrd.lower().split(' ')
                    result = difflib.get_close_matches(k, subwrds, 1, 0.85)
                    if(len(result)>0):
                        #totalstateboardtenth = ' '.join(wrd.split()[-3:])
                        numericalwordsinline = ' '.join(wrd.split())
                        totalmarks=Stateboard_tenth_total_marks_extraction_Line_to_number(numericalwordsinline)
                        if totalmarks!='':
                            tot=int(totalmarks)
                            percentage = round(tot/5,2)
                            ans['percentage'].append(percentage)
                        

    return ans


###############################################################################################################################################################

#########################################################################################################################################################################

def words_to_number_conversion_stateboard_twelth(text):
    # Define a regular expression pattern to match numerical words
    pattern = r'\b(?:zero|one|two|three|four|five|six|seven|eight|nine)+\b'
    # Find all numerical words in the line
    numerical_words = re.findall(pattern, text.lower())  # Convert text to lowercase
    # Convert numerical words to their corresponding digits
    digits_mapping = {
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9"
    }
    numbers = ''.join(digits_mapping[word] for word in numerical_words)
    return numbers


##################################################################################################################

#######################################################################################################################
def extract_stateboard_twelth_percentage(mystring):
    numberwords = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    
    lines = mystring.split('\n')
    # dictionary for relevant lines
    l={}
    # dictionary for final result
    ans = {}
    #ans.setdefault('numberinwords',[])
    #ans.setdefault('total',[])
    ans.setdefault('percentage',[])
    for k in numberwords:
        l.setdefault(k,[])
        

    # extracting relevant lines from tesseract output
    for line in lines:
        if(len(line)>0):
            words = line.split(' ')
            for w in words:
                w = w.lower()
                result = difflib.get_close_matches(w,numberwords,1,0.85)
                if(len(result)>0):
                    key = result[0]
                    l[result[0]].append(line)
                    
    # extracting relevant information from the dictionary l
    total=''
    nos=0
    for k in numberwords:
        prev=''
        for str in l[k]:
            if(prev == ''):
                prev = l[k]
            elif(prev == str):
                continue
            else:
                prev = str
            
            if(k == 'zero' or k == 'one' or k == 'two' or k == 'three' or k == 'four' or k == 'five' or k == 'six' or k == 'seven' or k == 'eight' or k == 'nine'):
                wrds = str.split('  ')
                #combined_numbers = []  # List to store combined numbers
                for wrd in wrds:
                        subwrds = wrd.lower().split(' ')
                        result = difflib.get_close_matches(k, subwrds, 1, 0.85)
                        if(len(result)>0):
                            #temp = ' '.join(subwrds.split())
                            #numberformat = words_to_number(temp)
                            if 'obtained' in wrd.lower() or 'lone' in wrd.lower():
                                continue
                            words_in_number = ' '.join(k.split())
                            words_to_number = words_to_number_conversion_stateboard_twelth(words_in_number)
                            #combined_numbers.append(words_in_number)
                            total=total+words_to_number
    if total!='':
        integer_number = int(total)
        percentage = integer_number/6
        percentage = round(percentage,2)
        ans['percentage'].append(percentage)
    return ans

######################################################################################################################
def postprocess_Stateboard_twelth(mystring):
    keywords = ['total','school','mar',]
    lines = mystring.split('\n')

    # dictionary for relevant lines
    l={}

    # dictionary for final result
    ans = {}
    ans.setdefault('exno',[])
    ans.setdefault('dob',[])
    ans.setdefault('school',[])
    
    
    for k in keywords:
        l.setdefault(k,[])
        

    # extracting relevant lines from tesseract output
    for line in lines:
        if(len(line)>0):
            words = line.split(' ')
            for w in words:
                w = w.lower()
                result = difflib.get_close_matches(w,keywords,1,0.85)
                if(len(result)>0):
                    key = result[0]
                    l[result[0]].append(line)

    # extracting relevant information from the dictionary l
    for k in keywords:
        prev=''
        for str in l[k]:
            if(prev == ''):
                prev = l[k]
            elif(prev == str):
                continue
            else:
                prev = str

          
            if (k == 'mar'):
                wrds = str.split('  ')
                for wrd in wrds:
                    subwrds = wrd.lower().split(' ')
                    result = difflib.get_close_matches(k, subwrds, 1, 0.85)
                    if(len(result)>0):
                        if 'higher' in wrd.lower() or 'secondary' in wrd.lower() or 'course' in wrd.lower() or 'board' in wrd.lower() or 'examinations' in wrd.lower() or 'certificate' in wrd.lower() or 'permanent' in wrd.lower():
                            continue
                        exno = ' '.join(wrd.split()[1:-2])
                        #namestudent = ' '.join(wrd.split())
                        ans['exno'].append(exno)
                        dob =' '.join(wrd.split()[:-3])
                        ans['dob'].append(dob)
                 ##################################################       
                
                if 'exno' in ans:
                    # Check if 'exno' has any values
                     if ans['exno']:
                        break     
            ############################################################
            if (k == 'school'):
                wrds = str.split('  ')
                for wrd in wrds:
                    subwrds = wrd.lower().split(' ')
                    result = difflib.get_close_matches(k, subwrds, 1, 0.85)
                    if(len(result) > 0):
                        # Append the entire line after the first occurrence of "school"
                        if 'name' in wrd.lower() or 'secondary' in wrd.lower() or 'leaving' in wrd.lower() or 'board' in wrd.lower() or 'examinations' in wrd.lower():
                            continue
                        schoolname = ' '.join(wrd.lower().split())
                        ans['school'].append(schoolname)


            
                           
    
    return ans

#######################################################################################################################################################
#################################################################################################################################################################
############################################################################################################################################################################


#cbse 10th code starts here#######################################################
########################################################################################################
#function1
def preprocess_and_extract_text(input_image_path):
   
    image = cv2.imread(input_image_path) # Load the input image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)# Convert the image to grayscale
    binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    denoised = cv2.fastNlMeansDenoising(binary, None, h=6, searchWindowSize=21, templateWindowSize=7)# Perform denoising
    #extracted_text = pytesseract.image_to_string(denoised)# Extract text using Pytesseract
    extracted_text = pytesseract.image_to_string(denoised,config="-l eng -c preserve_interword_spaces=1 output-preserve-enabled")# Extract text using Pytesseract
    return extracted_text# Return the extracted text
#############################################################################################################
#function2
def words_to_number_conversion_cbse_marksheets(text):
    # Define a regular expression pattern to match numerical words
    pattern = r'\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred)+\b'
    # Find all numerical words in the line
    numerical_words = re.findall(pattern, text.lower())  # Convert text to lowercase
    # Convert numerical words to their corresponding digits
    digits_mapping = {
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "ten": "10",
        "eleven": "11",
        "twelve": "12",
        "thirteen": "13",
        "fourteen": "14",
        "fifteen": "15",
        "sixteen": "16",
        "seventeen": "17",
        "eighteen": "18",
        "nineteen": "19",
        "twenty": "20",
        "thirty": "30",
        "forty": "40",
        "fifty": "50",
        "sixty": "60",
        "seventy": "70",
        "eighty": "80",
        "ninety": "90",
        "hundred": "100"
    }
    numbers = ''.join(digits_mapping[word] for word in numerical_words)
    return numbers
#######################################################################################################
#function3
def extractinfo(wrds, i):
    p = []
    flag = 0
    while i < len(wrds):
        if (wrds[i] == '' or wrds[i] == ':' or wrds[i] == '-' or wrds[i] == '='):
            if flag == 1:
                break
        else:
            p.append(wrds[i])
            p.append(' ')
            flag = 1
        i += 1
    s = ''.join(p)
    return s


##########################################################################################################
#function4
def post_process_cbse_tenth(mystring):
    keywords = ['student','certify','name','roll','birth','school','result']
    lines = mystring.split('\n')

    # dictionary for relevant lines
    l={}

    # dictionary for final result
    ans = {}

    ans.setdefault('student',[])
    ans.setdefault('name',[])
    ans.setdefault('roll',[])
    ans.setdefault('birth',[])
    ans.setdefault('school',[])
    ans.setdefault('result',[])

    for k in keywords:
        l.setdefault(k,[])
        #ans.setdefault(k,[])

    # extracting relevant lines from tesseract output
    for line in lines:
        if(len(line)>0):
            words = line.split(' ')
            for w in words:
                w = w.lower()
                result = difflib.get_close_matches(w,keywords,1,0.85)
                if(len(result)>0):
                    key = result[0]
                    l[result[0]].append(line)

    # extracting relevant information from the dictionary l
    for k in keywords:
        prev=''
        for str in l[k]:
            if(prev == ''):
                prev = l[k]
            elif(prev == str):
                continue
            else:
                prev = str
           
            if (k == 'student'):
                wrds = str.split('  ')
                for wrd in wrds:
                    subwrds = wrd.lower().split(' ')
                    result = difflib.get_close_matches(k, subwrds, 1, 0.85)
                    if(len(result)>0):
                        student_name = ' '.join(wrd.split()[-2:])
                        ans['student'].append(student_name)

            if (k == 'certify'):
                wrds = str.split('  ')
                for wrd in wrds:
                    subwrds = wrd.lower().split(' ')
                    result = difflib.get_close_matches(k, subwrds, 1, 0.85)
                    if(len(result)>0):
                        student_name = ' '.join(wrd.split()[-2:])
                        ans['student'].append(student_name)


            if (k == 'roll'):
                wrds = str.split('  ')
                for wrd in wrds:
                    subwrds = wrd.lower().split(' ')
                    result = difflib.get_close_matches(k, subwrds, 1, 0.85)
                    if(len(result)>0):
                        student_name = ' '.join(wrd.split()[-1:])
                        ans[k].append(student_name)

            if(k == 'name'):
                orgwrds = str.lower().split(' ')
                wrds = str.replace('/',' ').lower().split(' ')
                result = difflib.get_close_matches("father's", wrds, 1, 0.75)
                if(len(result)<=0):
                    result = difflib.get_close_matches("mother's", wrds, 1, 0.75)
                if (len(result) <= 0):
                    result = difflib.get_close_matches("guardian's", wrds, 1, 0.75)
                if(len(result)>0):
                    pos = difflib.get_close_matches("name", orgwrds, 1, 0.75)
                    i = orgwrds.index(pos[0])+1
                    ans['name'].append(extractinfo(str.split(' '),i))

            if (k == 'birth' or k=='result'):
                
                key = k
                wrds = str.lower().split(' ')
                result = difflib.get_close_matches(key, wrds, 1, 0.75)
                if (len(result) > 0):
                    i = wrds.index(result[0])+1
                    ans[k].append(extractinfo(str.split(' '),i))
                    
            if (k == 'school'):
                wrds = str.split('  ')
                for wrd in wrds:
                    subwrds = wrd.lower().split(' ')
                    if 'examination' in subwrds or 'secondary' in subwrds:
                    # Skip appending to the dictionary
                        continue
                    result = difflib.get_close_matches('school', subwrds, 1, 0.85)
                    if(len(result)>0):
                        if re.search(r'\d{5}', wrd):
                            index = subwrds.index(next(filter(lambda x: re.search(r'\d{5}', x), subwrds)))
                            merged_subwords = ' '.join(subwrds[index:])
                            #school_name_cbse_tenth = ' '.join(wrd.split())
                            #ans[k].append(school_name_cbse_tenth)
                            ans[k].append(merged_subwords)

                 ##################################################       
                if 'school' in ans:
                    # Check if 'school' has any values
                     if ans['school']:
                        break     
            ############################################################

    return ans
#####################################################################################################
#function5
def extract_percentage_cbse(mystring):

    numberwords = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen",
        "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred"]

    lines = mystring.split('\n')
    # dictionary for relevant lines
    l={}
    # dictionary for final result
    ans = {}
    #ans.setdefault('numberinwords',[])
    #ans.setdefault('total',[])
    ans.setdefault('percentage',[])
    for k in numberwords:
        l.setdefault(k,[])
        

    # extracting relevant lines from tesseract output
    for line in lines:
        if(len(line)>0):
            words = line.split(' ')
            for w in words:
                w = w.lower()
                result = difflib.get_close_matches(w,numberwords,1,0.85)
                if(len(result)>0):
                    key = result[0]
                    l[result[0]].append(line)
                    
    # extracting relevant information from the dictionary l
    total_ones_digit=0
    total_two_digit=0
    nos=0
    for k in numberwords:
        prev=''
        for str in l[k]:
            if(prev == ''):
                prev = l[k]
            elif(prev == str):
                continue
            else:
                prev = str
            
            if(k == 'zero' or k == 'one' or k == 'two' or k == 'three' or k == 'four' or k == 'five' or k == 'six' or k == 'seven' or k == 'eight' or k == 'nine' ):
                wrds = str.split('  ')
                for wrd in wrds:
                        subwrds = wrd.lower().split(' ')
                        result = difflib.get_close_matches(k, subwrds, 1, 0.85)
                        if(len(result)>0):
                            if 'date' in wrd.lower() or 'birth' in wrd.lower() :
                                continue
                            words_in_number = ' '.join(k.split())
                            words_to_number = words_to_number_conversion_cbse_marksheets(words_in_number)
                            words_to_number = int(words_to_number)
                            total_ones_digit=total_ones_digit+words_to_number


            if(k == 'ten' or k == 'eleven' or k == 'twelve' or k == 'thirteen' or k == 'fourteen' or k == 'fifteen' or k == 'sixteen' or k == 'seventeen' or k == 'eighteen' or k == 'nineteen' or k == 'twenty' or k == 'thirty' or k == 'forty' or k == 'fifty' or k == 'sixty' or k == 'seventy' or k == 'eighty' or k == 'ninety' or k == 'hundred'):
                wrds = str.split('  ')
                for wrd in wrds:
                        subwrds = wrd.lower().split(' ')
                        result = difflib.get_close_matches(k, subwrds, 1, 0.85)
                        if(len(result)>0):
                            if 'date' in wrd.lower() or 'birth' in wrd.lower() :
                                continue
                            words_in_number = ' '.join(k.split())
                            #ans['percentage'].append(words_in_number)
                            nos+=1
                            words_to_number = words_to_number_conversion_cbse_marksheets(words_in_number)
                            words_to_number = int(words_to_number)
                            total_two_digit=total_two_digit+words_to_number 
                
    
    if(nos>0):
        total = total_ones_digit+total_two_digit
        total = round(total/nos,2)
        ans['percentage'].append(total)
    return ans
###############################################################################################################
##########################cbsetwelth extract 'certify','name','roll','school'##############################
def post_process_cbse_twelth(mystring):
    keywords = ['certify','name','roll','school']
    lines = mystring.split('\n')

    # dictionary for relevant lines
    l={}

    # dictionary for final result
    ans = {}

    for k in keywords:
        l.setdefault(k,[])
        ans.setdefault(k,[])

    # extracting relevant lines from tesseract output
    for line in lines:
        if(len(line)>0):
            words = line.split(' ')
            for w in words:
                w = w.lower()
                result = difflib.get_close_matches(w,keywords,1,0.85)
                if(len(result)>0):
                    key = result[0]
                    l[result[0]].append(line)

    # extracting relevant information from the dictionary l
    for k in keywords:
        prev=''
        for str in l[k]:
            if(prev == ''):
                prev = l[k]
            elif(prev == str):
                continue
            else:
                prev = str
           

            if (k == 'certify'):
                wrds = str.split('  ')
                for wrd in wrds:
                    subwrds = wrd.lower().split(' ')
                    result = difflib.get_close_matches(k, subwrds, 1, 0.85)
                    if(len(result)>0):
                        student_name = ' '.join(wrd.split()[-2:])
                        ans['certify'].append(student_name)


            if (k == 'roll'):
                wrds = str.split('  ')
                for wrd in wrds:
                    subwrds = wrd.lower().split(' ')
                    result = difflib.get_close_matches(k, subwrds, 1, 0.85)
                    if(len(result)>0):
                        #student_name = ' '.join(wrd)
                        student_name = ' '.join(wrd.split()[-1:])
                        ans[k].append(student_name)

            if(k == 'name'):
                orgwrds = str.lower().split(' ')
                wrds = str.replace('/',' ').lower().split(' ')
                result = difflib.get_close_matches("father's", wrds, 1, 0.75)
                if(len(result)<=0):
                    result = difflib.get_close_matches("mother's", wrds, 1, 0.75)
                if (len(result) <= 0):
                    result = difflib.get_close_matches("guardian's", wrds, 1, 0.75)
                if(len(result)>0):
                    pos = difflib.get_close_matches("name", orgwrds, 1, 0.75)
                    i = orgwrds.index(pos[0])+1
                    ans['name'].append(extractinfo(str.split(' '),i))

            
            if (k == 'school'):
                wrds = str.split('  ')
                for wrd in wrds:
                    subwrds = wrd.lower().split(' ')
                    if 'examination' in subwrds or 'secondary' in subwrds:
                    # Skip appending to the dictionary
                        continue
                    result = difflib.get_close_matches('school', subwrds, 1, 0.85)
                    if(len(result)>0):
                        '''
                        if re.search(r'\d{5}', wrd):
                            index = subwrds.index(next(filter(lambda x: re.search(r'\d{5}', x), subwrds)))
                            merged_subwords = ' '.join(subwrds[index:])
                            ans[k].append(merged_subwords) 
                            #ans[k].append(wrd)
                        '''
                        if 'name' in wrd.lower() or 'secondary' in wrd.lower() or 'senior' in wrd.lower() or 'certificate' in wrd.lower() or 'examination' in wrd.lower():
                            continue
                        school_name_cbse_twelth = ' '.join(wrd.split())
                        ans[k].append(school_name_cbse_twelth)
          
                 ##################################################       
                if 'school' in ans:
                    # Check if 'school' has any values
                     if ans['school']:
                        break     
            ############################################################
           

    return ans
############################################################################################################

def main(Marksheetstype):
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    #1
    if Marksheetstype == 'StateboardTenth':
        f = open("StateboardTenthInputcsvfile.csv", "r")
        reader = csv.reader(f)
        reader = islice(reader, 0, None, 1)
        #next(reader)
        o = open("outputs.csv", "w",newline='')
        writer = csv.writer(o)
        header = ['StudentImageName','StudentName','school name','dateofbirth','examno','percentage']
        writer.writerow(header)
        count = 1
        for rw in reader:
                img_name = rw[0]  
                path = 'UploadedMarksheets\\' + img_name
                img = Image.open(path)
                text_data_stateboard_tenth = pytesseract.image_to_string(img)
                #mystringtenth = preprocess_and_extract_text(path)     
                
                #print(text_data_stateboard_tenth)                                        
                print('stateboard tenth preprocess_and_extract_text sucessfully completed')
                stu_data_stateboard_tenth = postprocess_Stateboard_tenth(text_data_stateboard_tenth)
                
                print('Dictionary updated sucessfully')
                writer.writerow([img_name] + list(stu_data_stateboard_tenth.values()))
                print('stateboard csv completed sucessfully for marksheet'+ str(count))
                count+=1

 #############################################################################################################               
    #2
    if Marksheetstype == 'StateboardTwelth':
        f = open("StateboardTwelthInputcsvfile.csv", "r")
        reader = csv.reader(f)
        reader = islice(reader, 0, None, 1)
        #next(reader)
        o = open("outputs.csv", "w",newline='')
        writer = csv.writer(o)
        header = ['StudentImageName','examno','DOB','school','Percentage']
        writer.writerow(header)
        count = 1
        for rw in reader:
                img_name = rw[0] 
                img = Image.open('UploadedMarksheets\\' + img_name)
                text_data_stateboard_twelth = pytesseract.image_to_string(img)
                print('StateboardTwelth Converted image to text successfully')

                stu_data_stateboard_twelth = postprocess_Stateboard_twelth(text_data_stateboard_twelth)
                print('StateboardTwelth stu_data extracted successfully')
                stu_percentage_stateboard_twelth = extract_stateboard_twelth_percentage(text_data_stateboard_twelth)
                stu_data_stateboard_twelth.update(stu_percentage_stateboard_twelth)
                writer.writerow([img_name] + list(stu_data_stateboard_twelth.values()))
                print('csv completed sucessfully for marksheet'+ str(count))
                count+=1
    #3
    if Marksheetstype == 'CBSETenth':
        f = open("CBSETenthInputcsvfile.csv", "r")
        reader = csv.reader(f)
        reader = islice(reader, 0, None, 1)
        #next(reader)
        o = open("outputs.csv", "w",newline='')
        writer = csv.writer(o)
        header = ['Student file name','Student name','Mother Name or Father Name or Guardian Name','Roll Number','Date of Birth','school Name','Result','Percentage']
        writer.writerow(header)
        count = 1
        for rw in reader:
                img_name = rw[0]  
                #img = Image.open('UploadedMarksheets\\' + img_name)
                #text = pytesseract.image_to_string(img)
                path= 'UploadedMarksheets\\' + img_name
                text_data_cbse_tenth = preprocess_and_extract_text(path)                                        
                print('preprocess_and_extract_text sucessfully completed')
                stu_data_cbse_tenth = post_process_cbse_tenth(text_data_cbse_tenth)
                stu_percentage_cbse_tenth = extract_percentage_cbse(text_data_cbse_tenth)
                stu_data_cbse_tenth.update(stu_percentage_cbse_tenth)
                print('Dictionary updated sucessfully')
                writer.writerow([img_name] + list(stu_data_cbse_tenth.values()))
                print('csv completed sucessfully for marksheet'+ str(count))
                count+=1
    #4
    if Marksheetstype == 'CBSETwelth':
        f = open("CBSETwelthInputcsvfile.csv", "r")
        reader = csv.reader(f)
        reader = islice(reader, 0, None, 1)
        #next(reader)
        o = open("outputs.csv", "w",newline='')
        writer = csv.writer(o)
        header = ['Student file name','Certify Name','Mother Name or Father Name or Guardian Name','Roll Number','school Name','Percentage']
        writer.writerow(header)
        count = 1
        for rw in reader:
                img_name = rw[0]  
                #img = Image.open('UploadedMarksheets\\' + img_name)
                #text = pytesseract.image_to_string(img)
                path= 'UploadedMarksheets\\' + img_name
                text_data_cbse_twelth = preprocess_and_extract_text(path)                                        
                print('12th marksheets preprocess_and_extract_text sucessfully completed')
                stu_data_cbse_twelth = post_process_cbse_twelth(text_data_cbse_twelth)
                stu_percentage_cbse_twelth = extract_percentage_cbse(text_data_cbse_twelth)
                stu_data_cbse_twelth.update(stu_percentage_cbse_twelth)
                print('12th marksheets Dictionary updated sucessfully')
                writer.writerow([img_name] + list(stu_data_cbse_twelth.values()))
                print('12th marksheets csv completed sucessfully for marksheet'+ str(count))
                count+=1

@app.route('/download_output')
def download_output():
    output_csv_path = os.path.join(app.config['OUTPUT_FOLDER'], 'outputs.csv')
    return send_file(output_csv_path, as_attachment=True)

@app.route('/run_main')
def run_main():
    Marksheetstype = request.args.get('Marksheetstype', None)
    print("Request args:", request.args) 
    print("Marksheetstype:", Marksheetstype)
    main(Marksheetstype)
    output_csv_url = '/download_output'
    return redirect(output_csv_url)

if __name__ == '__main__':
    app.run(debug=True)