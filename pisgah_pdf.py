#!/usr/bin/env python3
#
# 2021 11 08 jcm added code to search more carefully for the case number, since different
#       systems produce slightly different formats for PDF files
# 2021 11 08 jcm added code to give a warning if keywords were not found in the input files:
#       CIPRS will have: "Court Case:"
#       Lexis will have: "Case Number:"
#
#
# Inputs (provided by legal department)
# Two PDF files as input
# - one Lexis report PDF file and
# - one CIPRS report PDF file
# 
# Outputs
# One text file as output, which has a list of all case numbers in the Lexis PDF report that are 
# NOT in the CIPRS PDF report, with the name:
# - one text output file (also shown on the screen) called "comparison.txt"
#   (default location is same directory as exe file)
#
# Note: As per client, we are using the last 6 characters of the case number identifies the case
# number, even though the other characters might be coded differently.

# external libraries
import fitz
from datetime import datetime
import sys

def find_case_number(str):
    # 2021 11 08 jcm added code to search more carefully for the case number
    # parses a string to look for first alpha-numeric (which is the start of the case number),
    # and collecting all alpha-numerics until the next newline ('\n')
    # Note: skips over any newlines ('\n') if before the first alpha-numeric
    # Note: drops all non-alpha-numerics within the case number, including spaces
    start = False
    case_number = ""
    for i in range(len(str)):
        char = str[i]
        if (char.isdigit()):
            case_number += char
            start = True
        elif((char >= 'A' and char <= 'Z') or
            # could add space character if we don't want to drop spaces inside case number
            # (char = ' ' and start == True) or
            (char >= 'a' and char <= 'z')):
            case_number += char
            start = True
        elif char == '\n' and start == True:
            # stop if we hit a newline after already getting a case number
            break
    return case_number

def get_lexis_case_numbers(doc):
    # Lexis PDF parsing based on exact keyword "Case Number:"
    lexis_case_number_list = []
    for page_number in range(0,doc.pageCount):
        page = doc.loadPage(page_number)
        page_text = page.getText("text")
        keyword = "Case Number:"
        case_number_split = page_text.split(keyword)
        for case_number_plus in case_number_split[1:]:
            # 2021 11 08 jcm The challenge is to pull the case number out of the text that
            # follows the keyword. Sometimes, that text has special characters before the case
            # number (like '\n') and sometimes it just has a space. So the start of the case
            # number will be the first alpha-numeric character in the string. The case number
            # will be all the alpha-numeric characters from that first one to the newline ('\n').
            # Note: This excludes all non-alpha-numeric characters, like spaces.
            case_number = find_case_number(case_number_plus)
            lexis_case_number_list.append(case_number)
    return lexis_case_number_list

def get_ciprs_case_numbers(doc):
    # CIPRS PDF parsing based on exact keyword "Court Case:"
    ciprs_case_number_list = []
    for page_number in range(0,doc.pageCount):
        page = doc.loadPage(page_number)
        page_text = page.getText("text")
        keyword = "Court Case:"
        case_number_split = page_text.split(keyword)
        for case_number_plus in case_number_split[1:]:
            case_number = find_case_number(case_number_plus)
            ciprs_case_number_list.append(case_number)
    return ciprs_case_number_list

def get_lexis_cases_not_in_ciprs(lexis_case_number_list, ciprs_case_number_list):
    # compare the case numbers based on last 6 digits
    lexis_cases_not_found = []
    lexis_cases_six_digits_not_found = []
    for lexis_case_number in lexis_case_number_list:
        lexis_case_six_digit = lexis_case_number[-6:]
        found_match = False
        for ciprs_case_number in ciprs_case_number_list:
            if lexis_case_six_digit == ciprs_case_number[-6:]:
                found_match = True
        if found_match == False:
            # only report if new case number (based on last-6-digits)
            if lexis_case_six_digit not in lexis_cases_six_digits_not_found:
                lexis_cases_six_digits_not_found.append(lexis_case_six_digit)
                # only report if full case number not already in the list
                if lexis_case_number not in lexis_cases_not_found:
                    lexis_cases_not_found.append(lexis_case_number)
    return lexis_cases_not_found

def file_comparison(lexis_file_path, ciprs_file_path, out_file_path):
    # write the case numbers found in Lexis but not in CIPRS
    lexis_doc = fitz.open(lexis_file_path)
    ciprs_doc = fitz.open(ciprs_file_path)
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")

    lexis_case_numbers = get_lexis_case_numbers(lexis_doc)
    ciprs_case_numbers = get_ciprs_case_numbers(ciprs_doc)
    lexis_not_in_ciprs = get_lexis_cases_not_in_ciprs(lexis_case_numbers, ciprs_case_numbers)
    with open(out_file_path,"w") as f:
        f.write(
            "Lexis versus CIPRS v3 (" + dt_string + ")" + "\n" + 
            "--------------------------------------------"+ "\n" + 
            "Lexis PDF: " + lexis_file_path + "\n" + 
            "CIPRS PDF: " + ciprs_file_path + "\n" +
            "--------------------------------------------"+ "\n" +
        # 2021 11 11 jcm added lexis and ciprs counts to report
            str(len(lexis_case_numbers)) + " Lexis cases found" + '\n' + 
            str(len(ciprs_case_numbers)) + " CIPRS cases found" + '\n' +
            '\n'
        )
        for lexis_case_number in lexis_not_in_ciprs:
                f.write("Lexis case " + lexis_case_number + " not in CIPRS" + "\n")
        # 2021 11 08 jcm added code to give a warning if keywords were not found
        if lexis_case_numbers == []:
            f.write("WARNING! Wrong file? Lexis PDF file does not contain any cases (keyword='Case Number:')" + "\n")
        if ciprs_case_numbers == []:
            f.write("WARNING! Wrong file? CIPRS PDF file does not contain any cases (keyword='Court Case:')" + "\n")
        # 2021 11 11 jcm added code to report if no missing cases found
        if lexis_not_in_ciprs == []:
            f.write("All Lexis PDF case numbers were found in the CIPRS PDF" + "\n")

def main():

    # Inputs (default)
    lexis_file_path = "Lexis.pdf"
    ciprs_file_path = "CIPRS.pdf"

    # override defaults if filenames passed through arguments (via drag/drop)
    file_paths = sys.argv[1:]  # skip first argument, which is the script name
    if len(file_paths) == 2:
        lexis_file_path = file_paths[0]
        ciprs_file_path = file_paths[1]

    # Outputs
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d-%H-%M-%S.%f")[:-4]
    out_file_path = "In-Lexis-Not-In-CIPRS-" + dt_string + ".txt"

    # test to make sure input file paths exist
    lexis_file_found = True
    try:
        doc = fitz.open(lexis_file_path)
    except:
        lexis_file_found = False
        pass

    ciprs_file_found = True
    try:
        doc = fitz.open(ciprs_file_path)
    except:
        ciprs_file_found = False
        pass

    if lexis_file_found == False or ciprs_file_found == False:
        with open(out_file_path,"w") as f:
            f.write("Lexis versus CIPRS (" + dt_string + ")" + "\n" + 
                    "--------------------------------------------"+ "\n")
            if lexis_file_found == False:
                f.write("Lexis PDF: ERROR: FILE NOT FOUND: " + lexis_file_path + "\n")
            if ciprs_file_found == False:
                f.write("CIPRS PDF: ERROR: FILE NOT FOUND: " + ciprs_file_path + "\n")
            f.write("--------------------------------------------"+ "\n")
        return

    file_comparison(lexis_file_path, ciprs_file_path, out_file_path)

if __name__ == "__main__":
    main()
