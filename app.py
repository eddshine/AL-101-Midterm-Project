from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
# from pdf2image import convert_from_path
# from pdf2image.exceptions import (
#     PDFInfoNotInstalledError,
#     PDFPageCountError,
#     PDFSyntaxError
# )

import fitz
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
import sys, re #, random
# from collections import defaultdict
from automata.fa.dfa import DFA
from visual_automata.fa.dfa import VisualDFA
from automata.fa.nfa import NFA
from visual_automata.fa.nfa import VisualNFA


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        ui_dir = "resources/ui/widget.ui" # UI File directory
        self.ui = uic.loadUi(ui_dir, self) # Load the .ui file
        self.setWindowIcon(QtGui.QIcon('resources/ico/market_icon.ico')) # Icon for the applications
        self.show() # Show the GUI

        # Variables
        self.finiteStates = []
        self.finiteInputs = []
        self.initialState = None
        self.finalState = {}
        self.transitionFlow = {} #defaultdict(list)
        self.transitions = {}
        self.languages = []
        self.digraph = {}
        self.dfa = None
        self.nfa = None

        # Table widget
        self.ui.tableWidget.setColumnCount(1)
        self.ui.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Transitions"))
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        # Button Clicks
        self.ui.btn_submit.clicked.connect(self.submitAction)
        self.ui.btn_clear.clicked.connect(self.clearAction)
        self.ui.btn_add.clicked.connect(self.addToTable)
        self.ui.btn_reset.clicked.connect(self.clearTable)
        self.ui.btn_langSubmit.clicked.connect(self.languageAcceptance)

        # ComboBox Widget
        self.ui.btn_fType.activated.connect(self.fType)

        # Report Errors
        self.ui.in_fset.textChanged.connect(self.fsets_errors)
        self.ui.in_fset_Sym.textChanged.connect(self.fsets_alpha_errors)
        self.ui.in_initial.textChanged.connect(self.initial_states_errors)
        self.ui.in_finalSet.textChanged.connect(self.final_state_errors)


    # FUNCTION TO SUMBIT USER'S ANSWER
    def submitAction(self):
        try:
            if self.verifyInputs() and len(self.transitionFlow) !=0:
                if self.ui.btn_fType.currentText() == "DFA":
                    self.dfa=DFA(
                            states=set(self.finiteStates),
                            input_symbols=set(self.finiteInputs),
                            transitions=self.transitionFlow,
                            initial_state=self.initialState,
                            final_states=self.finalState,
                            )
                    

                    self.dfa = VisualDFA(self.dfa)
                    self.ui.tableView.setText(str(self.dfa.table))
                    #print(dfa.table)
                    self.dfa.show_diagram(view=True)
                    pdffile = "Digraph.gv.pdf"
                    doc = fitz.open(pdffile)
                    page = doc.load_page(0)
                    pix = page.get_pixmap()
                    output = "fsm.png"
                    pix.save(output)
                    pixmap = QPixmap("fsm.png")
                    self.ui.imageView.setPixmap(pixmap)
                    self.ui.imageView.resize(pixmap.width(),pixmap.height())


                elif self.ui.btn_fType.currentText() == "NFA":
                    nfa=NFA(
                            states=set(self.finiteStates),
                            input_symbols=set(self.finiteInputs),
                            transitions=self.transitionFlow,
                            initial_state=self.initialState,
                            final_states=self.finalState,
                            )
                    nfa = VisualNFA(nfa)
                    self.ui.tableView.setText(str(nfa.table))
                    #print(nfa.table)
                    nfa.show_diagram(view=True)
                    pdffile = "Digraph.gv.pdf"
                    doc = fitz.open(pdffile)
                    page = doc.load_page(0)
                    pix = page.get_pixmap()
                    output = "fsm.png"
                    pix.save(output)
                    pixmap = QPixmap("fsm.png")
                    self.ui.imageView.setPixmap(pixmap)
                    self.ui.imageView.resize(pixmap.width(),pixmap.height())
        except:
            self.ui.submitError.setText("ERROR!")

        
    # INPUT - PROMPT AN ERROR IF SOMETHING IS NOT MET
    def fsets_errors(self):
         if len(self.ui.in_fset.text().split(",")) > 1 and self.ui.in_fset.text().split(",")[len(self.ui.in_fset.text().split(","))-1] != "":
            self.ui.warn1.setText("")
            self.finiteStates = set([i for i in self.ui.in_fset.text().split(',')])
            if self.verifyInputs():
                self.ui.btn_states.clear()
                self.ui.btn_transitions.clear()
                self.addToComboBox()
         else:
            self.ui.btn_states.clear()
            self.ui.btn_transitions.clear()
            self.ui.in_initial.clear()
            self.ui.in_finalSet.clear()
            self.ui.tableWidget.setRowCount(0)
            self.transitionFlow = {}
            self.ui.submitError.clear()
            self.ui.imageView.clear()
            self.ui.tableView.clear()
            self.ui.acceptanceReturn.clear()
            self.ui.warn1.setText("Required 2 or more")
    
    # INPUT - PROMPT AN ERROR IF SOMETHING IS NOT MET
    def fsets_alpha_errors(self):
         if len(self.ui.in_fset_Sym.text()) != 0 and self.ui.in_fset_Sym.text().split(",")[len(self.ui.in_fset_Sym.text().split(","))-1] != "":
            self.ui.warn2.setText("")
            self.finiteInputs = set([i for i in self.ui.in_fset_Sym.text().split(',')])
            if self.verifyInputs():
                self.ui.btn_states.clear()
                self.ui.btn_transitions.clear()
                self.addToComboBox()
         else:
            self.ui.btn_states.clear()
            self.ui.btn_transitions.clear()
            self.ui.in_initial.clear()
            self.ui.in_finalSet.clear()
            self.ui.tableWidget.setRowCount(0)
            self.transitionFlow = {}
            self.ui.imageView.clear()
            self.ui.tableView.clear()
            self.ui.acceptanceReturn.clear()
            self.ui.warn2.setText("Required")

    # INPUT - PROMPT AN ERROR IF SOMETHING IS NOT MET
    def initial_states_errors(self):
         if len(self.ui.in_initial.text()) == 0:
            self.initialState = None
            self.ui.btn_states.clear()
            self.ui.btn_transitions.clear()
            self.ui.tableWidget.setRowCount(0)
            self.transitionFlow = {}
            self.ui.warn3.setText("Required")
         elif self.ui.btn_fType.currentText() == "DFA":
            if len(self.ui.in_initial.text().split(",")) > 1:
                self.initialState = None
                self.ui.btn_states.clear()
                self.ui.btn_transitions.clear()
                self.ui.tableWidget.setRowCount(0)
                self.transitionFlow = {}
                self.ui.imageView.clear()
                self.ui.tableView.clear()
                self.ui.acceptanceReturn.clear()
                self.ui.warn3.setText("DFA: Initiial shouldn't be more then 2")
            elif self.ui.in_initial.text() not in self.finiteStates:
                self.initialState = None
                self.ui.btn_states.clear()
                self.ui.btn_transitions.clear()
                self.ui.tableWidget.setRowCount(0)
                self.ui.imageView.clear()
                self.ui.tableView.clear()
                self.ui.acceptanceReturn.clear()
                self.transitionFlow = {}
                self.ui.warn3.setText("Pick from Finite Set of States")
            else:
                self.ui.warn3.setText("")
                self.initialState = self.ui.in_initial.text()
                if self.verifyInputs():
                    self.ui.btn_states.clear()
                    self.ui.btn_transitions.clear()
                    self.addToComboBox()
         elif self.ui.btn_fType.currentText() == "NFA":
            if not set(self.ui.in_initial.text().split(",")).issubset(set(self.finiteStates)):
                self.initialState = None
                self.ui.btn_states.clear()
                self.ui.btn_transitions.clear()
                self.ui.tableWidget.setRowCount(0)
                self.transitionFlow = {}
                self.ui.imageView.clear()
                self.ui.tableView.clear()
                self.ui.acceptanceReturn.clear()
                self.ui.warn3.setText("Pick from Finite Set of States")
            else:
                self.ui.warn3.setText("")
                self.initialState = self.ui.in_initial.text()
                if self.verifyInputs():
                    self.ui.btn_states.clear()
                    self.ui.btn_transitions.clear()
                    self.addToComboBox()

    # INPUT - PROMPT AN ERROR IF SOMETHING IS NOT MET
    def final_state_errors(self):
        if len(self.ui.in_finalSet.text()) == 0:
            self.finalState = {}
            self.ui.btn_states.clear()
            self.ui.btn_transitions.clear()
            self.ui.tableWidget.setRowCount(0)
            self.transitionFlow = {}
            self.ui.imageView.clear()
            self.ui.tableView.clear()
            self.ui.acceptanceReturn.clear()
            self.ui.warn4.setText("Required")
            
        elif not set(self.ui.in_finalSet.text().split(",")).issubset(set(self.finiteStates)):
            self.finalState = {}
            self.ui.btn_states.clear()
            self.ui.btn_transitions.clear()
            self.ui.tableWidget.setRowCount(0)
            self.transitionFlow = {}
            self.ui.imageView.clear()
            self.ui.tableView.clear()
            self.ui.acceptanceReturn.clear()
            self.ui.in_langAccept.clear()
            self.ui.warn4.setText("Pick from Finite Set of States")
        else:
            self.ui.warn4.setText("")
            self.finalState = set([i for i in self.ui.in_finalSet.text().split(",")])
            if self.verifyInputs():
                self.ui.btn_states.clear()
                self.ui.btn_transitions.clear()
                self.addToComboBox()

    # FUNCTION TO CHECK IF ALL POSSIBLE INPUTS ARE MET.
    def verifyInputs(self):
        if len(self.finiteStates) <= 1 or len(self.finiteInputs) == 0 or self.initialState is None or  len(self.finalState) == 0:
            return False
        else:
            return True

    # FUNCTION TO CLEAR ALL INPUTS.
    def clearAction(self):
        self.finiteStates = []
        self.finiteInputs = []
        self.initialState = None
        self.finalState = {}
        self.transitionFlow = {}
        self.languages = []
        self.ui.tableWidget.setRowCount(0)
        self.ui.imageView.clear()
        self.ui.tableView.clear()
        self.ui.acceptanceReturn.clear()
        self.ui.in_langAccept.clear()
        [i.clear() for i in [self.ui.in_finalSet, self.ui.in_fset, self.ui.in_fset_Sym, self.ui.in_initial]]
        [i.setText("") for i in [self.ui.warn1, self.ui.warn2, self.ui.warn3, self.ui.warn4]]

    # FUNCTION TO ADD ALL POSSIBLE COMBINATION OF STATE AND ALPHABET AND PUT INTO COMBO BOX.
    def addToComboBox(self):
        for i in self.finiteStates:
            for x in self.finiteInputs:
                self.ui.btn_states.addItem(f"{i} ➜ {x} ➜ Q?")
            
            self.transitionFlow[f"{i}"] = {}
            self.ui.btn_transitions.addItem(i)
            
    # FUNCTION TO GET USER'S CHOICES.
    def addToTable(self):
        if self.verifyInputs():
            # GET USER'S ANSWER FROM COMBO BOX
            getTrans = self.ui.btn_states.currentText().split(" ")
            getState = self.ui.btn_transitions.currentText()
            #self.transitionFlow[(getTrans[0], getTrans[2])] = getState
            self.transitionFlow[getTrans[0]].update({getTrans[2]: getState})
            #print(self.transitionFlow)

            # PUSH TO TABLE FOR DISPLAY
            rowPosition = self.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)
            self.ui.tableWidget.setItem(rowPosition , 0, QTableWidgetItem(f"{getTrans[0]} ➜ {getTrans[2]} ➜ {getState}"))


    # RESET/CLEAR TABLE
    def clearTable(self):
        self.transitionFlow = {}
        for i in self.finiteStates:
            self.transitionFlow[f"{i}"] = {}
        self.ui.tableWidget.setRowCount(0)
        self.ui.imageView.setText("")
        self.ui.submitError.setText("")
        self.ui.imageView.clear()
        self.ui.tableView.clear()
        self.ui.acceptanceReturn.clear()
        self.ui.in_langAccept.clear()


    # CLEAR THINGS UP WHENEVER FINITE TYPE BUTTON CHANGES (DFA/NFA)
    def fType(self):
            self.ui.btn_states.clear()
            self.ui.btn_transitions.clear()
            self.ui.in_initial.clear()
            self.ui.in_finalSet.clear()
            self.ui.tableWidget.setRowCount(0)
            self.transitionFlow = {}
            self.ui.warn3.setText("")
            self.ui.warn4.setText("")
            self.ui.imageView.clear()
            self.ui.tableView.clear()
            self.ui.acceptanceReturn.clear()
            self.ui.in_langAccept.clear()
    
    # CHECK IF A CERTAIN LANGUAGE IS ACCEPTABLE OR REJEACTBALE BY THE AUTOMATA
    def languageAcceptance(self):
        try:
            if self.ui.in_langAccept.text() != "" and self.verifyInputs and len(self.transitionFlow) != 0:
                if self.ui.btn_fType.currentText() == "DFA":
                    #print(self.dfa.input_check(self.ui.in_langAccept.text()))
                    res = re.findall(r'\[.*?\]', str(self.dfa.input_check(self.ui.in_langAccept.text())))
                    getRes = str(res).replace("[","").replace("]","").replace("'","")
                    if getRes == "Accepted":
                        self.ui.acceptanceReturn.setText(f"{getRes}!")
                    else:
                        self.ui.acceptanceReturn.setText(f"{getRes}!")
                elif self.ui.btn_fType.currentText() == "NFA":
                    res = re.findall(r'\[.*?\]', str(self.nfa.input_check(self.ui.in_langAccept.text())))
                    getRes = str(res).replace("[","").replace("]","").replace("'","")
                    if getRes == "Accepted":
                        self.ui.acceptanceReturn.setText(f"{getRes}!")
                    else:
                        self.ui.acceptanceReturn.setText(f"{getRes}!")
        except:
            self.ui.acceptanceReturn.setText("ERROR!")
# =========================================================================================================== #
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
