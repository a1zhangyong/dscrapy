# coding=utf-8
'''
Created on 2012-7-13

@author: Administrator
'''

import xlrd
import xlwt
from xlutils.copy import copy

class ExcelUtil:
    workbook = None
    filename = None
    sheets = None
    newFile = None
    new_sheet_count = 0
    workbookCopy = None #append时使用
    def __init__(self,filename=None):
        self.filename = filename
    
    def open_file(self):
        if(self.filename is None):
            return None
        self.workbook = xlrd.open_workbook(self.filename)
        return self.workbook
    
    def get_all_sheets(self):
        if(self.workbook is None):
            if(self.filename is not None):
                self.open_file()
        self.sheets = self.workbook.sheets()
        return self.sheets
    def get_sheet(self,idx):
        return self.get_all_sheets()[idx]
    def get_row_of_sheet(self,sheet):
        if(sheet is None):
            return 0
        return sheet.nrows
    def get_col_of_sheet(self,sheet):
        if(sheet is None):
            return 0
        return sheet.ncols
    def get_data_of_sheet(self,index,startRow):
        idx = int(index)
        if(idx < 0):
            return None
        sheet = self.get_all_sheets()[idx]
        rows = self.get_row_of_sheet(sheet)
        #cols = self.get_col_of_sheet(sheet)
        self.datas = []
        for i in range (startRow,rows):
            self.datas.append(sheet.row_values(i))
        return self.datas
    
    def write_data(self,dataList):
        if(self.newFile is None):
            self.newFile = xlwt.Workbook()
        #if(self.new_sheet_count is None or self.new_sheet_count == 0):
        self.new_sheet_count = self.new_sheet_count + 1;
        sheetName = "sheet" + str(self.new_sheet_count)
        workBook = self.newFile.add_sheet(sheetName, cell_overwrite_ok=True)
        if dataList and len(dataList)>0:
            data_num = len(dataList)
            for i in range(data_num): 
                col_num = len(dataList[i])
                for j in range(col_num): 
                    row = dataList[i]
                    vStr = str(row[j])
                    vStr = unicode(vStr,"utf-8")
                    workBook.write(i, j, row[j])
    def append_data(self,dataList):
        if(self.workbook is None):
            self.open_file()
        self.workbookCopy = copy(self.workbook)
        sheet = self.workbookCopy.get_sheet(0)
        #Workbook Worksheet
        rows = sheet.get_rows()
        rowNum = len(rows)
        if dataList and len(dataList)>0:
            data_num = len(dataList)
            for i in range(data_num): 
                col_num = len(dataList[i])
                for j in range(col_num): 
                    row = dataList[i]
                    vStr = str(row[j])
                    vStr = unicode(vStr,"utf8")
                    type(vStr)
                    sheet.write(i+rowNum, j, row[j])
    def save_new_file(self,fName=None):
        if(fName is not None):
            if(self.newFile is not None):
                self.newFile.save(fName)
        else:
            if(self.newFile is not None):
                self.newFile.save("./result/result.xls")
    def save_open_file(self):
        if(self.workbookCopy is not None):
            self.workbookCopy.save(self.filename)
    
    def write_and_save(self,dataList,fName=None):
        self.write_data(dataList)
        self.save_new_file(fName)
    
    def append_and_save(self,dataList):
        self.append_data(dataList)
        self.save_open_file()
        