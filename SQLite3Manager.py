#SQLite3 Manager
#SMW
#v0.02A

#TODO
#Add Duplicate Table Entry Error Handling

import tkinter, sqlite3, gridIt
from tkinter import ttk
from tkinter import filedialog, messagebox

class dbBrowser(tkinter.Frame):

    def __init__(self, parent):

        

        tkinter.Frame.__init__(self, parent)
        self.masterTableList = []
        self.a = 'sdgsd'
        self.parent = parent
        self.menuBar = tkinter.Menu(self.parent)
        self.parent.config(menu = self.menuBar)
        self.fileMenu = tkinter.Menu(self.menuBar, tearoff = 0)
        self.menuBar.add_cascade(label = 'File', menu = self.fileMenu)
        self.fileMenu.add_command(label = 'New Datatbase', command = self.new)
        self.fileMenu.add_command(label = 'Load Database', command = self.load)
        
        self.fileMenu.add_command(label = 'Exit', command = self.parent.destroy)
        self.FileName = None
        self.generateWidgets()

    def generateWidgets(self):

        

        self.statusFrame = tkinter.Frame(self, bd = 2, relief = 'ridge')
        self.statusFrameLabel = tkinter.Label(self.statusFrame, text = 'Status:')
        self.statusText = tkinter.Text(self.statusFrame, height = 3)
        self.statusText.grid(row = 0, column =1)
        self.statusFrameLabel.grid(row=0, column = 0)

        self.listFrame = tkinter.Frame(self, bd = 2, relief= 'ridge')
        self.listFrame.rowconfigure(0 , weight = 1)
        self.listFrame.rowconfigure(1 , weight = 1)
        self.listFrame.columnconfigure(0 , weight = 1)
        self.listFrame.columnconfigure(1 , weight = 1)
        self.tableList = tkinter.Listbox(self.listFrame)
        self.recordList = tkinter.Listbox(self.listFrame, width = 40)

        self.tableListHeader = tkinter.Label(self.listFrame, text = 'Tables:')
        self.recordListHeader = tkinter.Label(self.listFrame, text = 'Records:')

        self.tableListHeader.grid(row = 0, column = 0)
        self.tableList.grid(row = 1, column = 0)
        self.recordListHeader.grid(row = 0, column = 1)
        self.recordList.grid(row = 1, column = 1)

        self.recordList.bind('<<ListboxSelect>>', self.updateRecordListSelection)
        self.recordList.bind('<Double-1>', self.updateRecordListSelection)
        self.tableList.bind('<<ListboxSelect>>', self.updateTableSchemaFrame)
              

        self.tableOptionFrame = tkinter.Frame(self, bd = 2, relief = 'ridge')
        self.tableOptionFrame.rowconfigure(0, weight = 1)
        self.tableOptionFrame.rowconfigure(1, weight = 1)
        self.tableOptionFrame.rowconfigure(2, weight = 1)
        self.tableOptionFrame.rowconfigure(3, weight = 1)
        self.tableOptionFrame.columnconfigure(0, weight = 1)
        self.tableOptionFrame.columnconfigure(1, weight = 1)
        
        
        
        
        self.tableOptionFrameHeader = tkinter.Label(self.tableOptionFrame, text = 'Table Options:')
        self.newTableButton = tkinter.Button(self.tableOptionFrame, text = 'New Table', command = self.addTable)
        self.newTableEntryVariable = tkinter.StringVar()
        self.newTableEntry = tkinter.Entry(self.tableOptionFrame, textvariable = self.newTableEntryVariable)

        self.newFieldButton = tkinter.Button(self.tableOptionFrame, text = 'New Column', command = self.addRecordFrame)
        self.newFieldEntryVariable = tkinter.StringVar()
        self.newFieldEntry = tkinter.Entry(self.tableOptionFrame, textvariable = self.newFieldEntryVariable)

        self.removeFieldButton = tkinter.Button(self.tableOptionFrame, text = 'Remove Field', command = self.removeField)
        self.removeFieldEntryVariable = tkinter.StringVar()
        self.removeFieldEntryVariable.set('')
        self.removeFieldEntry = tkinter.Entry(self.tableOptionFrame, textvariable = self.removeFieldEntryVariable)

        self.deleteTableButton = tkinter.Button(self.tableOptionFrame, text = 'Delete Table', command = self.deleteTable)
        self.deleteTableEntryVariable = tkinter.StringVar()
        self.deleteTableEntryVariable.set('')
        self.deleteTableEntry = tkinter.Entry(self.tableOptionFrame, textvariable = self.deleteTableEntryVariable)

        
        



        self.tableOptionFrameHeader.grid(row = 0, column = 0, columnspan = 2)
        self.newTableButton.grid(row = 1, column = 0, sticky = 'we')
        self.newTableEntry.grid(row = 1, column = 1, sticky = 'we')
        self.deleteTableButton.grid(row = 2, column = 0, sticky = 'we')
        self.deleteTableEntry.grid(row = 2, column = 1, sticky = 'we')
        self.newFieldButton.grid(row = 3, column = 0, sticky = 'we', columnspan = 2)

        self.recordOptionFrame = tkinter.Frame(self, bd = 2, relief = 'ridge')

        self.recordOptionFrame.rowconfigure(0, weight = 1)
        self.recordOptionFrame.rowconfigure(1, weight = 1)
        self.recordOptionFrame.rowconfigure(2, weight = 1)
        self.recordOptionFrame.columnconfigure(0, weight = 1)
        self.recordOptionFrame.columnconfigure(1, weight = 1)
        
        self.recordOptionFrameHeader = tkinter.Label(self.recordOptionFrame, text = 'Record Options:')
        self.newRecordButton = tkinter.Button(self.recordOptionFrame, text = 'New Record', command = self.addRecord)
        self.modifyRecordButton = tkinter.Button(self.recordOptionFrame, text = 'Modify Record', command = self.updateDBRecord)
        self.deleteRecordButton = tkinter.Button(self.recordOptionFrame, text = 'Delete Record', command = self.deleteRecord)
  
        
        self.recordOptionFrameHeader.grid(row = 0, column = 0, columnspan = 2)
        self.newRecordButton.grid(row = 1, column = 0, columnspan = 2)
        self.modifyRecordButton.grid(row = 2, column = 0)
        self.deleteRecordButton.grid(row = 2, column = 1)


        self.tableSchemaFrame = tkinter.Frame(self, bd = 2, relief = 'ridge')
        self.tableSchemaHeaderLabel = tkinter.Label(self.tableSchemaFrame, text = 'Table Schema:')
        self.tableSchemaString = tkinter.StringVar()
        self.tableSchemaString.set('No Table Selected')
        self.tableSchemaDisplay = tkinter.Label(self.tableSchemaFrame, textvariable = self.tableSchemaString)
        self.tableSchemaHeaderLabel.grid(row = 0, column = 0)
        
       
        
        self.recordOptionFrame.grid(row = 16, column = 5, columnspan = 4,sticky ='nesw')
        self.listFrame.grid(row = 5, column = 1, columnspan = 8, rowspan = 10, sticky = 'nesw')
        self.statusFrame.grid(row = 4, column = 1, columnspan = 8, sticky = 'we')
        
        self.tableOptionFrame.grid(row = 16, column = 1, columnspan = 4, sticky ='nesw')
        self.tableSchemaFrame.grid(row = 17, column = 1, columnspan = 8, sticky ='nesw')
        self.pack()

    def gridIt(self):

        for y in range(0,20): self.rowconfigure(y, weight =1)
            
        for x in range(0,10): self.columnconfigure(x, weight =1)

        for col in range(0, 10):

            for row in range(0, 20):
                randomFrame = tkinter.LabelFrame(self, bd = 1, relief = 'sunken', bg = 'red')
                labelText = str(row)
                labelTextb = str(col)
                labelTextf = 'row:'+labelText+' col:'+labelTextb
                posLabel = tkinter.Label(randomFrame, text = labelTextf)
                posLabel.pack()
                randomFrame.grid(row = row, column = col, sticky = 'nesw')
                



        pass

    def new(self):

        self.fileName = filedialog.asksaveasfile(mode = 'w', defaultextension = '.sq3')

        
        try:
            self.fileNameString = self.fileName.name
            print(self.fileNameString)
        
            if self.fileName is None:
                return
        
            self.conn = sqlite3.connect(self.fileName.name)
            connectMessage = 'Connected to database '+self.fileName.name + '\n'
            self.statusText.insert(tkinter.INSERT, connectMessage)
            self.cursor = self.conn.cursor()
            self.updateTableList()
        except:
            pass

        

    def load(self):

        #Load Database From File and Open Connection
        self.fileName = filedialog.askopenfilename(filetypes = (('SQL3LITE Database files', '*.sq3'),
                                                                        ('All Files', '*.*') ) )
        try:
            self.fileNameString = self.fileName
            print(self.fileNameString)
            if self.fileName:

                if self.fileName:
                    self.conn = sqlite3.connect(self.fileName)
                    connectMessage = 'Connected to database '+self.fileName + '\n'
                    self.statusText.insert(tkinter.INSERT, connectMessage)
                    self.cursor = self.conn.cursor()
                    self.updateTableList()
                else:
                    connectMessage = 'Failed to connect to database '+self.fileName +'\n'
                    self.statusText.insert(tkinter.INSERT, connectMessage)
        except:
            pass


    def addTable(self):


        if self.newTableEntryVariable.get():
            variable = self.newTableEntryVariable.get()
        else:
            tkinter.messagebox.showwarning('Create Table', 'No Table Name Specified')
            return

        if self.conn:
            self.cursor.execute('''CREATE TABLE {}(id INTEGER PRIMARY KEY)'''.format(variable))
            insertString = 'TABLE ' + variable + ' inserted into database ' + self.fileNameString + '\n'
            self.statusText.insert(tkinter.INSERT, insertString)
            self.updateTableList()
            self.newTableEntryVariable.set('')
        else:
            tkinter.messagebox.showerror('Create Table', 'No Active Database Connection')
            return
        pass

    def deleteTable(self):

        
        deleteOrder = self.deleteTableEntryVariable.get()

        if deleteOrder == '' and self.tableList.curselection():
            deleteOrder = self.tableList.get(self.tableList.curselection()[0])
            deleteOrder = deleteOrder[0]
                      
        if deleteOrder in self.masterTableList:
            response = tkinter.messagebox.askyesno('Delete Table?', 'Are you sure you want to delete TABLE {}'.format(deleteOrder))
            print(response)
            if(response) == False:
                return
        else:
            tkinter.messagebox.showwarning('Delete Table','TABLE {} not found!'.format(self.deleteTableEntryVariable.get()))
            return

        if self.conn:
            self.cursor.execute('''DROP TABLE {}'''.format(deleteOrder))
            updateString = 'TABLE ' + deleteOrder + ' removed from database '+self.fileNameString + '\n'
            self.statusText.insert(tkinter.INSERT, updateString)
            self.deleteTableEntryVariable.set('')
            self.updateTableList()
            self.tableSchemaString.set('No Table Selected')
        else:
            tkinter.messagebox.showerror('Delete Table', 'No Active Database Connection')
            return

        pass

    def addField(self):

        fieldToAdd = self.newFieldEntryVariable.get()

        if hasattr(self, 'conn'):
        
            if self.tableList.curselection() == ():
                tkinter.messagebox.showerror('Add COLUMN', 'No TABLE Selected!')
                self.newFieldEntry.delete(0, tkinter.END)
                return
        
            if fieldToAdd in self.schemaList:
                tkinter.messagebox.showerror('Add COLUMN', ('COLUMN '+fieldToAdd+' already exists!'))
                self.newFieldEntry.delete(0, tkinter.END)
                return

            tableSelected = self.tableList.curselection()

            tableString = self.tableList.get(tableSelected[0])

            tableString = tableString[0]

            executeString = "alter TABLE "+tableString+" add column '"+fieldToAdd+"' 'float'"
            self.cursor.execute(executeString)
            self.statusText.insert(tkinter.INSERT,('Inserted COLUMN '+fieldToAdd+' into TABLE '+tableString+'\n'))
            self.newFieldEntry.delete(0, tkinter.END)
            self.updateTableSchemaFrame(True)
            
            
        else:
            tkinter.messagebox.showerror('Add COLUMN', 'No Active Database Connection')
            self.newFieldEntry.delete(0, tkinter.END)
        

        pass

    def removeField(self):


        if hasattr(self, 'conn'):

            deleteOrder = self.removeFieldEntryVariable.get()
            tableSelected = self.tableList.curselection()
            tableString = self.tableList.get(tableSelected[0])
            tableString = tableString[0]

            if self.tableList.curselection() == ():
                tkinter.messagebox.showerror('Remove COLUMN', 'No TABLE Selected!')
                self.newFieldEntry.delete(0, tkinter.END)
                return
            
            
            if deleteOrder == '':
                tkinter.messagebox.showerror('Remove COLUMN', 'No COLUMN Specified!')
                self.removeFieldEntry.delete(0, tkinter.END)
                return
            else:
                if deleteOrder in self.schemaList:
                    response = tkinter.askyesno('Are you sure you wish to delete COLUMN {} from TABLE {}'.format(deleteOrder,tableString))
                    if response == True:
                        self.statusText.insert(tkinter.INSERT, 'Feature Not Yet Implemented')
                        self.newFieldEntry.delete(0, tkinter.END)
                    else:
                        self.newFieldEntry.delete(0, tkinter.END)

        pass

    def updateRecordListSelection(self,e):

        #selected
        pass
        
    def updateTableSchemaFrame(self,e):
        selectedTable = self.tableList.curselection()
        print(selectedTable)

        if not self.tableList.curselection():
            print('None Selected During Update!')
            if self.masterTableSelection:
                selectedTable = self.masterTableSelection
                selectedTableText = self.tableList.get(selectedTable[0])
                print('There is!', self.masterTableSelection)
            else:
                print('there never was')
        else:
            self.masterTableSelection = selectedTable
            selectedTableText = self.tableList.get(selectedTable[0])
        
        self.selectedTable = selectedTable
        
        self.fieldNames = self.cursor.execute("PRAGMA table_info({})".format(selectedTableText[0]))
        #print([row for row in self.fieldNames])
        self.columnData = [row for row in self.fieldNames]
        self.schemaList = [row[1] for row in self.cursor]
        schemaString = [row[1] for row  in self.cursor]
        
        self.tableSchemaString.set(self.schemaList)
        if hasattr(self.tableSchemaFrame, 'tableSchemaDisplayFrame'): self.tableSchemaDisplayFrame.destroy()
        self.tableSchemaDisplayFrame = tkinter.Frame(self.tableSchemaFrame, bd = 1, relief = 'sunken')
        self.tableSchemaDisplayFrame.grid(row = 1, column = 1, sticky = 'nesw')
        cidLabel = tkinter.Label(self.tableSchemaDisplayFrame, text = 'cid')
        cidLabel.grid(row = 0, column = 0)
        nameLabel = tkinter.Label(self.tableSchemaDisplayFrame, text = 'name')
        nameLabel.grid(row = 0, column = 1)
        typeLabel = tkinter.Label(self.tableSchemaDisplayFrame, text = 'type')
        typeLabel.grid(row = 0, column = 2)
        notNullLabel = tkinter.Label(self.tableSchemaDisplayFrame, text = 'notnull')
        notNullLabel.grid(row = 0, column = 3)
        dfltValueLabel = tkinter.Label(self.tableSchemaDisplayFrame, text = 'dflt_value')
        dfltValueLabel.grid(row = 0, column = 4)
        pkLabel = tkinter.Label(self.tableSchemaDisplayFrame, text = 'pk')
        pkLabel.grid(row = 0, column = 5)
        
        
        
        y = 1  
        for entry in self.columnData:

            x = 0
            for eachItem in entry:
                if isinstance(eachItem, str):
                    tkinter.Label(self.tableSchemaDisplayFrame, text = eachItem).grid(row = y, column = x)
                    
                else:
                    tkinter.Label(self.tableSchemaDisplayFrame, text = str(eachItem)).grid(row = y, column = x)
                    
                x+= 1
            y+=1

        self.updateRecordList()
        

    def listTableDeselect(self):
        print('List Table Deselected!')
    
    def updateTableList(self):

        self.tableNameList = self.conn.execute('''SELECT name FROM sqlite_master WHERE type='table';''')
        self.tableList.delete(0,tkinter.END)
        for name in self.tableNameList:
            self.masterTableList.append(name[0])
            insertString = name[0] + '\n'
            self.tableList.insert(tkinter.END, name)


    def addRecord(self):


        if hasattr(self, 'conn'):

            if self.tableList.curselection() == ():
                messagebox.showerror('Add RECORD', 'No TABLE Selected!')
                self.newFieldEntry.delete(0, tkinter.END)
                return
            
            self.win = tkinter.Toplevel()
            self.win.wm_title('Add RECORD')
            selectedTable = self.tableList.curselection()
            selectedTableText = self.tableList.get(selectedTable[0])
            
            self.win.selectedTable = selectedTableText[0]
            self.win.addFrame = tkinter.Frame(self.win)
            
            self.win.addLabel = tkinter.Label(self.win.addFrame, text = 'Add Record')

            self.recordFieldLabel = []
            self.recordFieldEntry = []
            self.recordFieldVariable = []
            self.recordFieldType = []
            self.columnName = []
            x = 0
            y = 0
            
            for entry in self.schemaList:
                
                self.recordFieldLabel.append(tkinter.Label(self.win.addFrame, text = entry))
                self.recordFieldLabel[y].grid(row = y, column = 0, sticky = 'e')
                self.recordFieldVariable.append(tkinter.StringVar())
                self.recordFieldVariable[y].set('')
                self.recordFieldEntry.append(tkinter.Entry(self.win.addFrame, textvariable = self.recordFieldVariable[y]))
                self.recordFieldEntry[y].grid(row = y, column = 1, sticky = 'w')
                                             
                y += 1
            self.win.addFrame.pack()
            self.win.addFrame.pack()
            
            selectedTable = self.tableList.curselection()
            selectedTableText = self.tableList.get(selectedTable[0])

            self.rows = self.cursor.execute("SELECT * FROM {}".format(self.win.selectedTable))
            self.rows = [row for row in self.rows]
            print(self.rows)
            self.curID = len(self.rows)
            print('real size:', self.curID)

            
            #Get Table Columns to prepare entry fields
            
        
            self.fieldNames = self.cursor.execute("PRAGMA table_info({})".format(self.win.selectedTable))
            
            self.columnData = [row for row in self.fieldNames]
            self.schemaList = [row[1] for row in self.cursor]
            schemaString = [row[1] for row  in self.cursor]
            #print('Self.columnData:', self.columnData)
            #print('Self.schemaList:', self.schemaList)
            #print('schemaString:', schemaString)
            
            
            x =0
            y = 0
            for columnField in range(1, (len(self.columnData))):
                
                self.columnName.append(self.columnData[columnField][1])
                labelString = self.columnData[columnField][1] + ' ('+self.columnData[columnField][2]+'):'
                self.recordFieldLabel.append(tkinter.Label(self.win.addFrame, text = labelString))
                self.recordFieldVariable.append(tkinter.StringVar())
                self.recordFieldEntry.append(tkinter.Entry(self.win.addFrame, textvariable = self.recordFieldVariable[y]))
                self.recordFieldLabel[y].grid(row  = y, column = 1)
                self.recordFieldEntry[y].grid(row = y, column = 2)
                y+=1
                
            submitButton = tkinter.Button(self.win.addFrame, text = 'Submit', command = self.submitRecord)
            cancelButton = tkinter.Button(self.win.addFrame, text = 'Cancel', command = self.win.destroy)
                      
            
                

            submitButton.grid(row = y+1, column = 0)
            cancelButton.grid(row = y+1, column = 1)






            
            
            self.win.addFrame.pack(expand = True, fill = tkinter.BOTH)

        else:
            tkinter.messagebox.showwarning('Add RECORD', 'No Active Database Connection')
            return

    def submitRecord(self):

        
        labelString = [string for string in self.columnName]
        
        variableValue = [var.get() for var in self.recordFieldVariable]
        variableValue.insert(0, self.curID)
        insertString = "INSERT INTO {} values ({})".format(self.win.selectedTable, variableValue)
            #print('self.recordFieldLabel', self.recordFieldLabel)
            #print(insertString)
            
        newInsertString = insertString.replace('[','')
        self.newRecordInsertString = newInsertString.replace(']', '')
        

        #print(self.newRecordInsertString)
        self.cursor.execute(self.newRecordInsertString)
        self.conn.commit()
        updateString = 'RECORD ' + str(self.curID) + ' added to TABLE '+self.win.selectedTable + '\n'
        self.statusText.insert(tkinter.INSERT, updateString)
        
        self.win.destroy()
        self.updateTableSchemaFrame('')
        pass

    def updateRecordList(self):

        selectedTable = self.tableList.curselection()
        if not self.tableList.curselection():
            #print('None Selected During Update!')
            if self.masterTableSelection:
                selectedTable = self.masterTableSelection
                selectedTableText = self.tableList.get(selectedTable[0])
                #print('There is!', self.masterTableSelection)
            else:
                #print('there never was')
                pass
        else:
            self.masterTableSelection = selectedTable
            selectedTableText = self.tableList.get(selectedTable[0])

        
        
        #print(selectedTableText)
        self.rows = self.cursor.execute("SELECT * FROM {}".format(selectedTableText[0]))
        self.rows = [row for row in self.rows]
        #print(self.rows)
        
        #Clear out the Record List
        self.recordList.delete(0,tkinter.END)

        #Iterate through the returned DB and generate a list of lists, each record being a list,
        #convert list to string and insert into Record list
        for row in self.rows:
            rowEntries = [entry for entry in row]
            rowString = []
            for each in rowEntries:
                #print(each)
                if isinstance(each, str):
                    
                    rowString.append(each + " | ")

                else:

                    each = str(each)
                    rowString.append(each + " | ")

            #print(rowString)
            entryListString = ''.join(rowString)
            #print(entryListString)
            self.recordList.insert(tkinter.END, entryListString)
            
            
        '''
            self.masterTableList.append(name[0])
            insertString = name[0] + '\n'
            self.tableList.insert(tkinter.END, name)'''
            

        pass

    
    def addRecordFrame(self):
    
        self.addColumnWin = tkinter.Toplevel()
        self.addColumnWin.tableSelected = self.tableList.curselection()
        self.addColumnWin.tableString = self.tableList.get(self.addColumnWin.tableSelected[0])
        self.addColumnWin.tableString = self.addColumnWin.tableString[0]
        self.addColumnWin.addRecordFrame = tkinter.Frame(self.addColumnWin)
    
        cIDLabel = tkinter.Label(self.addColumnWin.addRecordFrame, text = 'CID:')
        cIDLabel.grid(row = 0, column = 0, sticky = 'e')
    
        self.addColumnWin.cIDVariable = tkinter.StringVar()
        self.addColumnWin.cIDVariable.set('')
        self.addColumnWin.cIDDisplay = tkinter.Label(self.addColumnWin.addRecordFrame, textvariable = self.addColumnWin.cIDVariable)
        self.addColumnWin.cIDDisplay.grid(row = 0, column = 1)

        nameLabel = tkinter.Label(self.addColumnWin.addRecordFrame, text = 'name:')
        nameLabel.grid(row = 1, column = 0, sticky = 'e')

        self.ARFnameEntryVariable = tkinter.StringVar()
        self.ARFnameEntryVariable.set('')
        self.ARFnameEntry = tkinter.Entry(self.addColumnWin.addRecordFrame, textvariable = self.ARFnameEntryVariable)
        self.ARFnameEntry.grid(row = 1, column = 1, sticky = 'w')

        typeLabel = tkinter.Label(self.addColumnWin.addRecordFrame, text = 'type:')
        typeLabel.grid(row = 2, column = 0, sticky = 'e')

        self.addColumnWin.typeCombo = ttk.Combobox(self.addColumnWin.addRecordFrame)
        self.addColumnWin.typeCombo['values'] = ('INTEGER','TEXT', 'REAL', 'BLOB', 'NUMERIC')
        self.addColumnWin.typeCombo.current(0)

        self.addColumnWin.typeCombo.grid(row = 2, column = 1, sticky = 'w')

        isNullLabel = tkinter.Label(self.addColumnWin.addRecordFrame, text = 'notNull:')
        self.addColumnWin.isNullCombo = ttk.Combobox(self.addColumnWin.addRecordFrame)
        self.addColumnWin.isNullCombo['values'] = ('True', 'False')
        self.addColumnWin.isNullCombo.current(0)
        isNullLabel.grid(row = 3, column = 0, sticky = 'e')
        self.addColumnWin.isNullCombo.grid(row = 3, column = 1, sticky = 'w')

        defaultValueLabel = tkinter.Label(self.addColumnWin.addRecordFrame, text = 'dflt_value:')
        self.addColumnWin.defaultValueVariable = tkinter.StringVar()
        self.addColumnWin.defaultValueVariable.set('')
        self.addColumnWin.defaultValueEntry = tkinter.Entry(self.addColumnWin.addRecordFrame, textvariable = self.addColumnWin.defaultValueVariable)
        defaultValueLabel.grid(row = 4, column = 0, sticky = 'e')
        self.addColumnWin.defaultValueEntry.grid(row = 4, column = 1, sticky = 'w')
    

        isPrimaryLabel = tkinter.Label(self.addColumnWin.addRecordFrame, text = 'P_KEY:')
        self.addColumnWin.isPrimaryCombo = ttk.Combobox(self.addColumnWin.addRecordFrame)
        self.addColumnWin.isPrimaryCombo['values'] = ('True', 'False')
        self.addColumnWin.isPrimaryCombo.current(1)
        isPrimaryLabel.grid(row = 5, column = 0, sticky = 'e')
        self.addColumnWin.isPrimaryCombo.grid(row = 5, column = 1, sticky = 'w')
    
    
    
        self.addColumnWin.addRecordFrame.grid(row = 1, column = 1)
        self.addColumnWin.addButton = tkinter.Button(self.addColumnWin, text = 'Add', command = self.submitNewRecord)
        self.addColumnWin.addButton.grid(row = 6, column = 0, sticky = 'we')

        self.addColumnWin.cancelButton = tkinter.Button(self.addColumnWin, text = 'Cancel', command = self.addColumnWin.destroy)
        self.addColumnWin.cancelButton.grid(row = 6, column = 1, sticky = 'we')

    def submitNewRecord(self):


        self.ARFtypeValue = self.addColumnWin.typeCombo.get()

        if self.addColumnWin.isNullCombo.get() == 'True': iNull = 1
        if  self.addColumnWin.isNullCombo.get() == 'False': iNull = 0

        if self.addColumnWin.isPrimaryCombo.get() == 'False': pKey = 0
        if self.addColumnWin.isPrimaryCombo.get() == 'True': pKey = 1
        self.newColumn = [ self.ARFnameEntryVariable.get(), self.ARFtypeValue, iNull, self.addColumnWin.defaultValueVariable.get(),pKey]
        #print(self.newColumn)
        
        commandString = "alter TABLE {} add COLUMN '{}' '{}' '{}' '{}' '{}'".format(self.addColumnWin.tableString, self.newColumn[0], self.newColumn[1],
                                                                               self.newColumn[2], self.newColumn[3], self.newColumn[4])
        self.cursor.execute(commandString)
        self.statusText.insert(tkinter.INSERT, ('COLUMN '+self.newColumn[0]+' added to TABLE '+self.addColumnWin.tableString+'\n'))
        self.tableList.selection_set(self.addColumnWin.tableSelected)
        self.updateTableSchemaFrame('')
        self.addColumnWin.destroy()
        #print(commandString)
        pass

    def updateDBRecord(self, e = None):


        if hasattr(self, 'conn'):

            if self.recordList.curselection() == ():
                messagebox.showerror('Modify RECORD', 'No RECORD Selected!')
                
                return
            
            self.win = tkinter.Toplevel()
            self.win.wm_title('Modify RECORD')

            
            selectedTable = self.tableList.curselection()
            if selectedTable == ():
                selectedTableText = self.tableList.get(self.masterTableSelection[0])
            else:
                selectedTableText = self.tableList.get(selectedTable[0])
            
            self.win.selectedTable = selectedTableText[0]
            self.win.addFrame = tkinter.Frame(self.win)
            
            self.win.addLabel = tkinter.Label(self.win.addFrame, text = 'Modify Record')

            self.recordFieldLabel = []
            self.recordFieldEntry = []
            self.recordFieldVariable = []
            #Set Values for Record
            self.updateRowID = str(self.recordList.curselection()[0])
            exeString = "SELECT * from {} WHERE ROWID = {}".format(selectedTableText[0], self.updateRowID)
            print(exeString)
            self.recordToMod = self.conn.execute(exeString)
            self.recordFieldType = []
            self.columnName = []
            x = 0
            y = 0

            self.fieldNames = self.cursor.execute("PRAGMA table_info({})".format(self.win.selectedTable))
            print('FIELD NAMES:', self.fieldNames)
            #print([row for row in self.fieldNames])
            self.columnData = [row for row in self.fieldNames]
            print('Column DATA:', self.columnData)
            self.schemaList = [row[1] for row in self.columnData]
            print('SCHEMA LIST:',self.schemaList)
            del self.schemaList[0]
            schemaString = [row[1] for row  in self.cursor]
            self.recordFieldVariable = []
            print(schemaString)
            for entry in self.schemaList:
                
                self.recordFieldLabel.append(tkinter.Label(self.win.addFrame, text = entry))
                self.recordFieldLabel[y].grid(row = y, column = 0, sticky = 'e')
                self.recordFieldVariable.append(tkinter.StringVar())
                self.recordFieldVariable[y].set('')
                self.recordFieldEntry.append(tkinter.Entry(self.win.addFrame, textvariable = self.recordFieldVariable[y]))
                self.recordFieldEntry[y].grid(row = y, column = 1, sticky = 'w')
                                             
                y += 1
            counter = 0
            firstEntry = True
            for each in self.recordToMod:
                for entry in each:
                    print(entry)
                    print(self.recordFieldVariable)
                    if firstEntry == True:
                        firstEntry = False
                        continue
                    if isinstance(entry, str):
                        self.recordFieldVariable[counter].set(entry)
                        counter+=1
                    else:
                        newEach = str(entry)
                        self.recordFieldVariable[counter].set(newEach)
                        counter+=1
                    
            
            self.win.addFrame.pack()
            self.win.addFrame.pack()
            
            
            self.rows = self.cursor.execute("SELECT * FROM {}".format(self.win.selectedTable))
            self.rows = [row for row in self.rows]
            #print(self.rows)
            self.curID = len(self.rows)
            #print('real size:', self.curID)


            #Get Table Columns to prepare entry fields
            
        
            self.fieldNames = self.cursor.execute("PRAGMA table_info({})".format(self.win.selectedTable))
            #print([row for row in self.fieldNames])
            self.columnData = [row for row in self.fieldNames]
            self.schemaList = [row[1] for row in self.cursor]
            schemaString = [row[1] for row  in self.cursor]
            #print('Self.columnData:', self.columnData)
            #print('Self.schemaList:', self.schemaList)
            #print('schemaString:', schemaString)
            #self.tableSchemaString.set(self.schemaList)
            
            x =0
            y = 0
            for columnField in range(1, (len(self.columnData))):
                
                self.columnName.append(self.columnData[columnField][1])
                labelString = self.columnData[columnField][1] + ' ('+self.columnData[columnField][2]+'):'
                self.recordFieldLabel.append(tkinter.Label(self.win.addFrame, text = labelString))
                
                self.recordFieldEntry.append(tkinter.Entry(self.win.addFrame, textvariable = self.recordFieldVariable[y]))
                self.recordFieldLabel[y].grid(row  = y, column = 1)
                self.recordFieldEntry[y].grid(row = y, column = 2)
                y+=1
                
            submitButton = tkinter.Button(self.win.addFrame, text = 'Update', command = self.updateRecord)
            cancelButton = tkinter.Button(self.win.addFrame, text = 'Cancel', command = self.win.destroy)
                      
            
                

            submitButton.grid(row = y+1, column = 0)
            cancelButton.grid(row = y+1, column = 1)






            
            
            self.win.addFrame.pack(expand = True, fill = tkinter.BOTH)

        else:
            tkinter.messagebox.showwarning('Modify RECORD', 'No Active Database Connection')
            return
        
    def updateRecord(self):


        
        labelString = [string for string in self.columnName]
        variableValue = []
        
        variableValue = [var.get() for var in self.recordFieldVariable]
        variableValue.insert(0, self.updateRowID)
        insertString = "REPLACE INTO {} values ({})".format(self.win.selectedTable, variableValue)
            
            
        newInsertString = insertString.replace('[','')
        self.newRecordInsertString = newInsertString.replace(']', '')
        

        
        self.cursor.execute(self.newRecordInsertString)
        self.conn.commit()
        self.updateTableSchemaFrame('')
        

    def deleteRecord(self):

        doubleCheck = tkinter.messagebox.askyesno('Delete RECORD?','Are you sure you want to permenantly delete this record?')

        if doubleCheck == False:
            return

        exeString = "DELETE from {} WHERE ROWID = {}".format(self.tableList.get(self.masterTableSelection[0])[0], str(self.recordList.curselection()[0]))
        print(exeString)
        self.cursor.execute(exeString)
        self.conn.commit()
        self.updateTableSchemaFrame('')

    

myApp = tkinter.Tk()
myApp.geometry('800x500')
myApp.title('SQLite3 Manager v0.02A')
dbBrowser(myApp)
