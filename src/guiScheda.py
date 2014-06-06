# -*- encoding: utf-8 -*-
'''
Nikko31
'''

from PySide import QtCore, QtUiTools
from PySide.QtGui import QMessageBox, QDialog

class guiScheda(QDialog):
    def __init__(self, inParent = None, inField = []):
        super(guiScheda, self).__init__(inParent)
        
        loader = QtUiTools.QUiLoader()
        f = QtCore.QFile("guiScheda.ui")
        f.open(QtCore.QFile.ReadOnly)
        self.myWidget = loader.load(f, self)
        f.close()
        
        # Class builtin function
        self.setGeometry( 100, 100, 640, 211 )
        self.setWindowTitle('Conoscere Linux - Qubrica - Scheda')
        self.campi = inField
        
        if(self.campi):
            self.myWidget.txtNome.setText(self.campi[0])
            self.myWidget.txtCognome.setText(self.campi[1]) 
            self.myWidget.txtNumero.setText(self.campi[2])
        
        self.InitEvents()
        
    def InitEvents(self):
        self.myWidget.cmdConferma.clicked.connect(self.cmdConferma_click)
        self.myWidget.cmdAnnulla.clicked.connect(self.cmdAnnulla_click)

    def GetDialog(self):
        return self.myWidget
    
    def cmdConferma_click(self):
        self.campi = [self.myWidget.txtNome.text(), self.myWidget.txtCognome.text(), self.myWidget.txtNumero.text()]
        self.myWidget.accept()
    
    def cmdAnnulla_click(self):
        self.myWidget.reject()
        
        
        