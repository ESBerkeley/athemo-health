'''
Created on Oct 28, 2013

@author: hemantbhonsle
'''
from __future__ import print_function

import xlrd
from xlrd.timemachine import REPR
import openpyxl
from openpyxl import load_workbook
import sys
import glob

def get_zip_code_info(zip):
    book = xlrd.open_workbook("Marketplace_premium_databook_2014.xlsx")
    sheet = book.sheet_by_name("Zip Code-Rating Area Lookup")
    for row_num in xrange(sheet.nrows):
        if sheet.row(row_num)[3].value == str(zip):
            return sheet.row(row_num)
        
def get_state_name(zip):
    book = xlrd.open_workbook("Marketplace_premium_databook_2014.xlsx")
    sheet = book.sheet_by_name("Zip Code-Rating Area Lookup")
    for row_num in xrange(sheet.nrows):
        if sheet.row(row_num)[3].value == str(zip):
            return sheet.row(row_num)[0].value
        
def get_county_code(zip):
    book = xlrd.open_workbook("Marketplace_premium_databook_2014.xlsx")
    sheet = book.sheet_by_name("Zip Code-Rating Area Lookup")
    for row_num in xrange(sheet.nrows):
        if sheet.row(row_num)[3].value == str(zip):
            return sheet.row(row_num)[1].value
        
def get_county_name(zip):
    book = xlrd.open_workbook("Marketplace_premium_databook_2014.xlsx")
    sheet = book.sheet_by_name("Zip Code-Rating Area Lookup")
    for row_num in xrange(sheet.nrows):
        if sheet.row(row_num)[3].value == str(zip):
            return sheet.row(row_num)[2].value
        
def get_rating_area(zip):
    book = xlrd.open_workbook("Marketplace_premium_databook_2014.xlsx")
    sheet = book.sheet_by_name("Zip Code-Rating Area Lookup")
    for row_num in xrange(sheet.nrows):
        if sheet.row(row_num)[3].value == str(zip):
            return sheet.row(row_num)[4].value

# stateInitials must be entered in '', and rating should be entered as x.0, so 1 is 1.0
def get_state_rating_info(stateInitials, rating):
    book = xlrd.open_workbook("Marketplace_premium_databook_2014.xlsx")
    sheet = book.sheet_by_name(stateInitials)
    for row_num in xrange(sheet.nrows):
        print(sheet.row(row_num)[3].value)
        if sheet.row(row_num)[3].value == rating:
            return sheet.row(row_num)

def safs(stateInitials, age):
    if age > 0 && age < 21:
        wb=load_workbook('0to20.xlsx')
    elif age > 20 && age < 23:
        wb=load_workbook('25.xlsx')
    elif age > 22 && age < 28:
        wb=load_workbook('25.xlsx')
    elif age > 27 && age < 33:
        wb=load_workbook('30.xlsx')
    elif age > 32 && age < 38:
        wb=load_workbook('35.xlsx')
    elif age > 37 && age < 43:
        wb=load_workbook('40.xlsx')
    elif age > 42 && age < 48:
        wb=load_workbook('45.xlsx')
    elif age > 47 && age < 53:
        wb=load_workbook('50.xlsx')
    elif age > 52 && age < 58:
        wb=load_workbook('55.xlsx')
    elif age > 57:
        wb=load_workbook('60.xlsx')
    ws=wb.get_sheet_by_name(stateInitials)
#    ws.cell('F2').value= str(age)
#    wb.save('Marketplace_premium_databook_2014 (2).xlsx')
