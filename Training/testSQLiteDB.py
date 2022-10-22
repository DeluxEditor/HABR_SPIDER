"""
Демонстрация работы с базой данных

Для работы необходима библиотека sqlite3.
Команда для устанкови - "pip.exe install db-sqlite3"
"""
import sqlite3 # подключить библиотеку для работы с SQLite


# Создать соединение с файл-БД при заданном имени ---------------------------------------------------------------------------
fileName = "DB_filename.db"
conn = sqlite3.connect(fileName)

# Получить курсор для выполнения операций
curs = conn.cursor()


## Удалить все прежние данные из таблицы  wordlist --------------------------------------------------------------------------
curs.execute("""DROP TABLE IF EXISTS wordlist""")

# Создать таблицу в БД
curs.execute("""CREATE TABLE IF NOT EXISTS wordlist  (
                                    rowid INTEGER PRIMARY KEY AUTOINCREMENT,  -- первичный ключ
                                    word TEXT NOT NULL, -- слово
                                    isFiltred INTEGER NOT NULL -- флаг фильрации
                ); """
            )


# Добавить строки. Способ 1. По одной записи  -------------------------------------------------------------------------------
curs.execute("INSERT INTO wordlist (word, isFiltred) VALUES ('Четверг', 0)")
curs.execute("INSERT INTO wordlist (word, isFiltred) VALUES ('Пятница', 0)")
curs.execute("INSERT INTO wordlist (word, isFiltred) VALUES ('Суббота', 0)")


# Добавить строки. Способ 2. По несколько строк -----------------------------------------------------------------------------
insertList = [  ('Понедельник', 0),
                ('Вторник', 0),
                ('Среда', 0),
            ]
print (type( insertList ),  len(  insertList ),  insertList )
curs.executemany('INSERT INTO wordlist (word, isFiltred) VALUES (?,?)', insertList)

# Сохранить (commit) изменения в БД -----------------------------------------------------------------------------------------
conn.commit()




# Получение данных из БД и вывод в консоль ----------------------------------------------------------------------------------
print("\n===SQL=== 1. Получение данных из БД. Вывод всех элементов таблицы wordlist =========================================")
resultRows = curs.execute("SELECT * FROM wordlist").fetchall()
print("Ответ от БД содержит строк: ", len(resultRows))
for item in resultRows:
    print(item)




print("\n===SQL=== 2. Получение данных из БД. Запрос строк таблицы wordlist подходящих под условие ==========================")
searchedWord = 'Суббота'
searchedList = [searchedWord]
# различие в типах данных
print( "Данные:", searchedWord, "; Тип данных=", type( searchedWord ), "; Длинна=", len( searchedWord ) ) # тип данных Строка "str"
print( "Данные:", searchedList, "; Тип данных=", type( searchedList ), "; Длинна=", len( searchedList ) ) # упаковка в список "list"

resultRows  = curs.execute("SELECT * FROM wordlist WHERE word=?; ",searchedList ).fetchall() # передача параметра в виде
#resultRows  = curs.execute("SELECT * FROM wordlist WHERE word=?; ",  ['Суббота',]  ).fetchall() # эквивалентный вид команды

print("Ответ от БД содержит строк: ", len(resultRows))
for item in resultRows:
    print(item)




print("\n===SQL=== 3. Получение данных из БД. Запрос строк таблицы wordlist подходящих под условие . Именованые параметры ===")
searchedWord = 'Суббота'
resultRows = curs.execute(  "SELECT * FROM wordlist WHERE word=:srchdWrd AND isFiltred=:filtredFlaf",
                            {"srchdWrd": searchedWord, "filtredFlaf":0}
                          ).fetchall()

print("Ответ от БД содержит строк: ",len(resultRows))
for item in resultRows:
    print(item)




