import mysql.connector
import db_config as cfg

class Survey_DAO:
    connection = ''
    cursor = ''
    host = ''
    user = ''
    password = ''
    database = ''
    port = 0
    
    def __init__(self):
        self.host = cfg.mysql['host']
        self.user = cfg.mysql['user']
        self.password = cfg.mysql['password']
        self.database = cfg.mysql['database']
        self.port = cfg.mysql['port']

    def getcursor(self): 
        self.connection = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def closeAll(self):
        self.connection.close()
        self.cursor.close()
         
    def create(self, values):
        cursor = self.getcursor()
        sql = "INSERT INTO SurveyResults (EmployeeID, IT_Overall_Score, Laptop_Score, Accessories_Score,\
            Applications_Score, Support_Score, Positive_Feedback, Negative_Feedback, Follow_Up) \
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        self.closeAll()
        return newid

    def getAll(self):
        cursor = self.getcursor()
        sql = "SELECT * FROM SurveyResults"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray

    def findByResponseID(self, id):
        cursor = self.getcursor()
        sql = "SELECT * FROM SurveyResults WHERE ResponseID = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue

    def update(self, values):
        cursor = self.getcursor()
        sql = "UPDATE SurveyResults SET EmployeeID = %s, IT_Overall_Score = %s, Laptop_Score = %s, Accessories_Score = %s,\
             Applications_Score = %s, Support_Score = %s, Positive_Feedback = %s, Negative_Feedback = %s, \
                Follow_Up = %s WHERE ResponseID = %s"
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()
        
    def delete(self, id):
        cursor = self.getcursor()
        sql = "DELETE FROM SurveyResults WHERE ResponseID = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.connection.commit()
        self.closeAll()
        
        print("Record for ResponseID", values, "has been deleted")

    def convertToDictionary(self, result):
        colnames = ['ResponseID', 'EmployeeID', 'IT_Overall_Score', 'Laptop_Score', 'Accessories_Score',
            'Applications_Score', 'Support_Score', 'Positive_Feedback', 'Negative_Feedback', 'Follow_Up']
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
        
survey_DAO = Survey_DAO()