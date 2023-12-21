import mysql.connector

def execute_query(connection, query, params=None):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()
    return result

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            database='dbt9', 
            user='root',
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def count_incidents_in_time_range(connection, start_date, end_date):
    query = '''
        SELECT COUNT(*) AS IncidentCount
        FROM Incidents
        WHERE RegistrationDate BETWEEN %s AND %s
    '''
    params = (start_date, end_date)
    result = execute_query(connection, query, params)
    print("Количество происшествий в указанный промежуток времени:")
    print(result[0]['IncidentCount'])

def count_incidents_for_person(connection, person_id):
    query = '''
        SELECT COUNT(*) AS IncidentCount
        FROM IncidentPersons
        WHERE PersonID = %s
    '''
    params = (person_id,)
    result = execute_query(connection, query, params)
    print("Количество происшествий для указанного лица:")
    print(result[0]['IncidentCount'])

def add_or_update_incident(connection, registration_number, registration_date, incident_type, decision):
    query = '''
        INSERT INTO Incidents (RegistrationNumber, RegistrationDate, IncidentType, Decision)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        RegistrationDate = VALUES(RegistrationDate),
        IncidentType = VALUES(IncidentType),
        Decision = VALUES(Decision)
    '''
    params = (registration_number, registration_date, incident_type, decision)
    execute_query(connection, query, params)
    print("Информация о происшествии добавлена или обновлена успешно.")

def add_or_update_person(connection, first_name, last_name, middle_name, address, criminal_records):
    query = '''
        INSERT INTO Persons (FirstName, LastName, MiddleName, Address, CriminalRecords)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        LastName = VALUES(LastName),
        MiddleName = VALUES(MiddleName),
        Address = VALUES(Address),
        CriminalRecords = VALUES(CriminalRecords)
    '''
    params = (first_name, last_name, middle_name, address, criminal_records)
    execute_query(connection, query, params)
    print("Информация о лице добавлена или обновлена успешно.")

# Подключаемся к базе данных
connection = connect_to_database()

if not connection:
    print("Не удалось подключиться к базе данных.")
else:
    try:
        # Запрос номера задания
        task_number = int(input("Введите номер задания (1-5): "))

        # Выполнение соответствующего действия
        if task_number == 1:
            start_date = input("Введите начальную дату (гггг-мм-дд): ")
            end_date = input("Введите конечную дату (гггг-мм-дд): ")
            count_incidents_in_time_range(connection, start_date, end_date)
        elif task_number == 2:
            person_id = int(input("Введите ID лица: "))
            count_incidents_for_person(connection, person_id)
        elif task_number == 3:
            registration_number = input("Введите регистрационный номер: ")
            registration_date = input("Введите дату регистрации (гггг-мм-дд): ")
            incident_type = input("Введите тип происшествия: ")
            decision = input("Введите решение: ")
            add_or_update_incident(connection, registration_number, registration_date, incident_type, decision)
        elif task_number == 4:
            first_name = input("Введите имя лица: ")
            last_name = input("Введите фамилию лица: ")
            middle_name = input("Введите отчество лица: ")
            address = input("Введите адрес лица: ")
            criminal_records = int(input("Введите количество судимостей лица: "))
            add_or_update_person(connection, first_name, last_name, middle_name, address, criminal_records)
        else:
            print("Некорректный номер задания. Введите число от 1 до 5.")
    finally:
        # Закрываем соединение с базой данных
        connection.close()
