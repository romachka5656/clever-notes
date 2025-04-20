#начни тут создавать приложение с умными заметками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QPushButton, 
    QApplication, 
    QWidget, 
    QLabel, 
    QListWidget, 
    QLineEdit, 
    QTextEdit,
    QInputDialog, 
    QHBoxLayout, 
    QVBoxLayout, 
    QFormLayout
)
import json
notes = {
    'Добро пожаловать!' :
        {
        'текст' : 'Это самое лучшое приложение для заметок',
        'теги' : ['добро', 'инструкция']
        }



}
# with open('f.json', 'w') as file:
#     json.dump(notes, file)







app = QApplication([])
notes_win = QWidget()
notes_win.setWindowTitle('Умные заметки')

list_notes = QListWidget() #создаёт список заметок
list_notes_label = QLabel('Список заметок') 
button_note_del = QPushButton('Удалить заметку')
button_note_create = QPushButton('Создать заметку')
button_note_save = QPushButton('Сохранить заметку')
field_tag = QLineEdit('') #Поле для ввода тега
field_tag.setPlaceholderText('Введите тег...') #Подсказка в поле ввода тега
field_text = QTextEdit() #многострочное текстовое поле для заметки
button_tag_add = QPushButton('Добавить к заметке')
button_tag_del = QPushButton('Открепить от заметки')
button_tag_search = QPushButton('Искать заметки по тегу')
list_tags = QListWidget() #список для отображения тегов
list_tags_label = QLabel('список тегов') #метка для списка тегов

layout_notes = QHBoxLayout() #главный комплектовщик
col_1 = QVBoxLayout() #Вертикальная компоновка для первой колонки / 1 столбец слева
col_1.addWidget(field_text)
layout_notes.addLayout(col_1)


col_2 = QVBoxLayout() #Вертикальная компоновка для второй колонки / 2 столбец справа
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)



row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)

row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)


col_2.addLayout(row_1)
col_2.addLayout(row_2)
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)

row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)



layout_notes.addLayout(col_2)
notes_win.setLayout(layout_notes)

def search_tag():
    print(button_tag_search.text())
    tag = field_tag.text()
    if button_tag_search.text() == 'Искать заметки по тегу' and tag:
        print(tag)
        notes_filtered = {} #тут будут заметки с выделенным тегом
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note]=notes[note]
        button_tag_search.setText('Сбросить поиск')
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        print(button_tag_search.text())
    elif button_tag_search.text() == 'Сбросить поиск':
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText('Искать заметки по тегу')
        print(button_tag_search.text())
    else:
        pass

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open('f.json', 'w') as file:
            json.dump(notes, file,sort_keys=True ,ensure_ascii=False)
        print(notes)
    else:
        print('Заметка для удаления не выбрана')

def add_notes():
    note_name, ok = QInputDialog.getText(
        notes_win, 'Добавить заметку', 'Название заметки: '
    )
    if ok and note_name != '':
        notes[note_name] = {'текст' : '', 'теги' : []}
        list_notes.addItem(note_name)
        #list_tags.addItems(notes[note_name]['теги'])

def show_note():
    name = list_notes.selectedItems()[0].text() #выбор заметки😒
    field_text.setText(notes[name]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[name]['теги'])


def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['текст'] = field_text.toPlainText() #получение текста
        with open('f.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('заметка не найдена')
            

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        print('Заметка для добавления тега не выбрана!')

def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]['теги'])
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Заметка для добавления тега не выбрана!')

#list_notes.itemClicked.connect(search_tag)
button_tag_search.clicked.connect(search_tag)
button_tag_add.clicked.connect(add_tag)
button_note_create.clicked.connect(add_notes)
list_notes.itemClicked.connect(show_note)


button_note_create.clicked.connect(add_notes)
list_notes.itemClicked.connect(show_note)
button_note_save.clicked.connect(save_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_note_del.clicked.connect(del_note)
#button_tags_search.clicked.connect(search_tag)
with open('f.json', 'r') as file:
    notes = json.load(file)
list_notes.addItems(notes)
notes_win.show()
app.exec_()