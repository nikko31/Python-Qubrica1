# -*- encoding: utf-8 -*-
'''
Nikko31 uno
'''

# Importo alcuni moduli fondamentali di Qt
from PySide import QtGui, QtCore, QtUiTools
from PySide.QtSql import QSqlDatabase, QSqlTableModel
from PySide.QtGui import QMessageBox, QFileDialog

import guiMain_rc

from guiScheda import guiScheda

class guiMain(QtGui.QMainWindow):
    def __init__(self, *args):
        apply(QtGui.QMainWindow.__init__, (self,) + args)
        
        loader = QtUiTools.QUiLoader()
        f = QtCore.QFile("guiMain.ui")
        f.open(QtCore.QFile.ReadOnly)
        self.myWidget = loader.load(f, self)
        f.close()
        
        # Class builtin function
        self.setCentralWidget(self.myWidget)
        self.setGeometry( 100, 100, 640, 480 )
        self.setWindowTitle('Conoscere Linux - Qubrica - Lista')
        
        # Custom function
        self.InitEvents()
                
    def InitEvents(self):
        """Funzione che inizializza gli eventi dei pulsanti"""
        self.myWidget.cmdNuovo.clicked.connect(self.cmdNuovo_click)
        self.myWidget.cmdModifica.clicked.connect(self.cmdModifica_click)
        self.myWidget.cmdElimina.clicked.connect(self.cmdElimina_click)
        self.myWidget.cmdSfoglia.clicked.connect(self.cmdSfoglia_click)

    def cmdSfoglia_click(self):
        """Evento che gestisce il tasto per sfogliare il percorso"""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setNameFilter("SQLite db (*.db)")
        dialog.setViewMode(QFileDialog.Detail)
        
        if dialog.exec_():
            fileNames = dialog.selectedFiles()
            self.myWidget.txtPercorso.setText( fileNames[0] )
            self.InitTable()
    
    def cmdNuovo_click(self):
        """Evento che gestisce il tasto di modifica"""
        
        tmpDialog = guiScheda(self, [])
        tmpScheda = tmpDialog.GetDialog() 
        tmpScheda.exec_()
        if(tmpScheda.result() == 1):
            rec = self.tableModel.record()
            
            for i in range(3):
                rec.setValue(i, tmpDialog.campi[i])
                
            self.tableModel.insertRecord(-1, rec)
            self.tableModel.submitAll()
           
    def cmdModifica_click(self):
        """Evento che gestisce il tasto di modifica"""
        
        if self.myWidget.lstRubrica.currentIndex():
            index = self.myWidget.lstRubrica.currentIndex().row()
            rec = self.tableModel.record(index)
            nome = rec.value("nome")
            cognome = rec.value("cognome")
            telefono = rec.value("telefono")
            
            tmpDialog = guiScheda(self, [nome, cognome, telefono])
            tmpScheda = tmpDialog.GetDialog() 
            tmpScheda.exec_()
            if(tmpScheda.result() == 1):    
                for i in range(3):
                    rec.setValue(i, tmpDialog.campi[i])
                
                self.tableModel.setRecord(index, rec)
                self.tableModel.submitAll()
        else:
            msgBox = QMessageBox()
            msgBox.setText("Occorre selezionare un elemento!")
            msgBox.exec_()            
           
    def cmdElimina_click(self):
        """Evento che gestisce il tasto di elimina"""

        msgBox = QMessageBox()
                
        if self.myWidget.lstRubrica.currentIndex():
            index = self.myWidget.lstRubrica.currentIndex().row()
            rec = self.tableModel.record(index)
            nome = rec.value("nome")
            cognome = rec.value("cognome")
            
            msgBox.setText("Si conferma l'eliminazione del contatto %s %s?" % (nome, cognome))
            msgBox.setInformativeText("Se si procede con l'eliminazione il contatto verrà eliminato definitivamente.")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            ret = msgBox.exec_()
            
            if(ret == QMessageBox.Ok):
                self.tableModel.removeRow(index)
                self.tableModel.submitAll()                
        else:
            msgBox.setText("Occorre selezionare un elemento!")
            msgBox.exec_()            
           
    def InitTable(self):
        """Funzione che accede al database ed imposta il data model"""
        db = QSqlDatabase.addDatabase("QSQLITE")

        db.setDatabaseName(self.myWidget.txtPercorso.text())
        db.open()
        
        model =  QSqlTableModel()
        model.setTable("contatti")
        model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        model.select()
        model.setHeaderData(0, QtCore.Qt.Horizontal, "Nome")
        model.setHeaderData(1, QtCore.Qt.Horizontal, "Cognome")
        model.setHeaderData(2, QtCore.Qt.Horizontal, "Telefono")
                
        self.tableModel = model
        self.myWidget.lstRubrica.setModel(model)

if __name__ == '__main__':
    import sys
    import os
    print("Running in " + os.getcwd() + " .\n")

    app = QtGui.QApplication(sys.argv)

    mainWindow = guiMain()
    mainWindow.show()

    app.connect(app, QtCore.SIGNAL("lastWindowClosed()"),app, QtCore.SLOT("quit()"))
    app.exec_()