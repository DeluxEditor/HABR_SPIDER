# Функция обработки поискового запроса
def db_process_request(self, request):
    request = request.lower()
    wordlist = request.split(' ')

    query, wordids = sql_query_compile(self, wordlist)
    print(query)

    query_result = self.cursor.execute(query)
    row = [i for i in query_result]
    return row, wordids


# Составление SQL-запроса для поиска id страниц, где встречаются искомые слова, в БД
def sql_query_compile(self, wordlist):
    query = str()

    wordids = get_word_id(self, wordlist)
    columnname = compile_columnname(wordids)
    join = compile_join(wordids)
    condition = compile_condition(wordids)

    query += "SELECT"
    query += querypart_compile(columnname)

    query += "\nFROM wordLocation word0"
    query += querypart_compile(join)
    query += querypart_compile(condition)

    return query ,wordids


# Нахождение id искомых слов
def get_word_id(self, wordlist):
    wordids = list()
    for word in wordlist:
        word_id = self.connection.execute(f"SELECT wordId from wordList where word = '{word}'").fetchone()
        if word_id is None:
            continue
        else:
            id = word_id[0]
            wordids.append(id)
    return wordids


def querypart_compile(querypart):
    compiled_part = str()
    for string in querypart:
        compiled_part += str(f"\n{string}")
    return compiled_part


# Составление SQL - столбцы (SELECT ...)
def compile_columnname(wordids):
    columnname = list()
    for idx in range(len(wordids)):
        if idx == 0:
            columnname.append("word0.fk_urlId urlid")
        columnname.append(f", word{idx}.location word{idx}_location")
    return columnname


# Составление SQL - джоины (INNER JOIN ... ON ...)
def compile_join(wordids):
    join = list()
    for idx in range(len(wordids)):
        if idx == 0:
            continue
        join.append(f"INNER JOIN wordLocation word{idx} on word0.fk_urlId=word{idx}.fk_urlId")
    return join


# Составление SQL - условия (WHERE ... AND ...)
def compile_condition(wordids):
    condition = list()
    for idx in range(len(wordids)):
        id = wordids[idx]
        if idx == 0:
            condition.append(f"WHERE word0.fk_wordId={id}")
            continue
        condition.append(f"AND word{idx}.fk_wordId={id}")
    return condition
