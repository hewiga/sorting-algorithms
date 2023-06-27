from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QListWidget, QCheckBox, QLabel
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import QtTest
import random

ALGORITHMS = ["Bubble Sort", "Insertion Sort", "Selection Sort", "Quick Sort", "Merge Sort"]
NUMBER_OF_ELEMENTS = 100
ELEMENTS_WIDTH = 10

class Sorting:
    def __init__(self, window):
        
        self.all_algorithms = {
            "Quick Sort" : self.quick_sort,
            "Bubble Sort": self.bubble_sort,
            "Selection Sort": self.selection_sort,
            "Insertion Sort": self.insertion_sort,
            "Merge Sort": self.merge_sort
        }

        self.window = window
        self.sorting_speed = 0

    def refresh_screen(self):
        self.window.update()
        QApplication.processEvents()  
        QtTest.QTest.qWait(self.sorting_speed)

    def sort(self, algorithm, elements):

        random.shuffle(elements)
        self.refresh_screen()
        self.all_algorithms[algorithm](elements)


    def bubble_sort(self, elements):
        was_change = False
        number_of_elements = len(elements)
                
        while number_of_elements > 1:
            i = 0
            while i < number_of_elements - 1:
                if elements[i] > elements[i + 1]:
                    buf = elements[i]
                    elements[i] = elements[i + 1]
                    elements[i + 1] = buf

                    self.refresh_screen()
                    was_change = True
                i += 1
            
            if not was_change:
                    break
            
            number_of_elements -= 1

    def insertion_sort(self, elements):

        for i in range(1, NUMBER_OF_ELEMENTS):
            element = elements[i]
            j = i - 1
            while j >= 0:
                if element <= elements[j] or j < 0:
                    elements[j + 1], elements[j] = elements[j], elements[j + 1]
                    self.refresh_screen()
                    j -= 1
                elif element > elements[j]:
                    break

    def selection_sort(self, elements):
        
        for i in range(NUMBER_OF_ELEMENTS):
            min_element = elements[i]
            min_element_index = i
            for j in range(i, NUMBER_OF_ELEMENTS):
                if elements[j] < min_element:
                    min_element = elements[j]
                    min_element_index = j
            elements[min_element_index], elements[i] = elements[i], elements[min_element_index]
            self.refresh_screen()
        return elements
    
    def quick_sort(self, elements, start=0, end=None):

        if end == None:
            end = len(elements)

        if (end - start) < 2:
            return 
        partition = start

        for i in range(start + 1, end):
            if elements[i] < elements[start]:
                partition += 1
                elements[i], elements[partition] = elements[partition], elements[i]
                self.refresh_screen()

        elements[partition], elements[start] = elements[start], elements[partition]

        self.refresh_screen()
        self.quick_sort(elements, start, partition)
        self.quick_sort(elements, partition + 1, end)
    
    def merge_sort(self, elements, begin = 0, end = None):

        if end == None:
            end = len(elements)
            
        if len(elements[begin:end]) < 2:
            return
        
        middle = int(len(elements[begin:end]) / 2) + begin
        
        self.merge_sort(elements, begin, middle)
        self.merge_sort(elements, middle, end)

        left = elements[begin:middle]
        right = elements[middle:end]

        i = j = 0
        k = begin
        
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                elements[k] = left[i]
                i += 1
            else:
                elements[k] = right[j]
                j += 1
            self.refresh_screen()
            k += 1
        
        while i < len(left):
            elements[k] = left[i]
            i += 1
            k += 1
            self.refresh_screen()
        
        while j < len(right):
            elements[k] = right[j]
            j += 1
            k += 1        
            self.refresh_screen()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("Sorting")
        self.setGeometry(200, 200, 1200, 700)
        self.set_widgets()
        
        self.sorting = Sorting(self)

        self.elements = list(range(1, NUMBER_OF_ELEMENTS + 1))

    def set_widgets(self):
        #tworzenie i pozycjonowanie elementów

        self.list_of_algorithms = QListWidget(self)
        self.list_of_algorithms.setGeometry(1000, 100, 200, 600)
        self.list_of_algorithms.addItems(ALGORITHMS)
        self.list_of_algorithms.setCurrentRow(0)

        self.start_button = QPushButton("START", self)
        self.start_button.setGeometry(1000, 650, 200, 50)
        self.start_button.clicked.connect(self.start_sorting)

        self.speed_text = QLabel(self)
        self.speed_text.setText("Animation Speed")
        self.speed_text.setGeometry(1000, 0, 200, 30)

        self.speed1= QCheckBox("100%", self)
        self.speed1.setGeometry(1030, 20, 50, 50)

        self.speed2= QCheckBox("50%", self)
        self.speed2.setGeometry(1100, 20, 50, 50)

        self.speed3= QCheckBox("25%", self)
        self.speed3.setGeometry(1030, 50, 50, 50)

        self.speed4= QCheckBox("10%", self)
        self.speed4.setGeometry(1100, 50, 50, 50)

        self.speed1.setChecked(True)
        self.speed1.stateChanged.connect(self.uncheck)
        self.speed2.stateChanged.connect(self.uncheck)
        self.speed3.stateChanged.connect(self.uncheck)
        self.speed4.stateChanged.connect(self.uncheck)

    def uncheck(self, state):
        #umożliwia oznaczenie tylko jednego checkboxa prędkości sortowania

        if state == Qt.Checked:

            if self.sender() == self.speed1:
                self.sorting.sorting_speed = 0
                self.speed2.setChecked(False)
                self.speed3.setChecked(False)
                self.speed4.setChecked(False)
            
            if self.sender() == self.speed2:
                self.sorting.sorting_speed = 20
                self.speed1.setChecked(False)
                self.speed3.setChecked(False)
                self.speed4.setChecked(False)

            if self.sender() == self.speed3:
                self.sorting.sorting_speed = 40
                self.speed2.setChecked(False)
                self.speed1.setChecked(False)
                self.speed4.setChecked(False)
            
            if self.sender() == self.speed4:
                self.sorting.sorting_speed = 100
                self.speed2.setChecked(False)
                self.speed3.setChecked(False)
                self.speed1.setChecked(False)


    def start_sorting(self):
        #określa który algorytm został wybrany i rozpoczyna sortowanie

        algoritm = self.list_of_algorithms.currentItem().text()
        self.sorting.sort(algoritm, self.elements)

    def paintEvent(self, event):
        #rysowanie elementów

        painter = QPainter(self)
        painter.setBrush(QBrush(Qt.red))
        painter.setPen(Qt.black)
        x = 0
        for element in self.elements:
            painter.drawRect(x, 700 - element * 7, 10, element * 7)
            x += ELEMENTS_WIDTH

        painter.end()        

def main():

    app = QApplication([])
    window = MainWindow()
    window.show()

    app.exec()

if __name__ == "__main__":
    main()
