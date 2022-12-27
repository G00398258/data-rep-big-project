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

    def get_survey_stats(self):
        # method gets some stats from different tables in the DB
        # each query result is turned into a dict and stored in a separate list, these are combined at the end
        cursor = self.getcursor()

        # count responses
        sql = "SELECT COUNT(*) AS Responses FROM SurveyResults"
        cursor.execute(sql)
        resultsArray = []
        #numResponses = []
        result = cursor.fetchall()
        print(result)

        item = {}

        for r in result:
            value = r[0]
            item['NumResponses'] = value
        #numResponses.append(item)
        resultsArray.append(item)


        # calculate average scores
        sql = "SELECT AVG(IT_Overall_Score) AS IT_Overall, AVG(Laptop_Score) AS Laptops, \
            AVG(Accessories_Score) AS Accessories, AVG(Applications_Score) AS Applications, \
                AVG(Support_Score) AS Support FROM SurveyResults"
        cursor.execute(sql)
        #scores = []
        results = cursor.fetchall()
        print(results)

        item = {}
    
        for result in results:
            item['IT_Overall'] = result[0]
            item['Laptops'] = result[1]
            item['Accessories'] = result[2]
            item['Applications'] = result[3]
            item['Support'] = result[4]
            #scores.append(item)
            resultsArray.append(item)
        
        sql = "SELECT e.Department, COUNT(e.Department) AS Dept_Responses \
            FROM SurveyResults s LEFT JOIN Employees e ON s.EmployeeID = e.EmployeeID \
                GROUP BY e.Department"
        cursor.execute(sql)
        #depts = []
        results = cursor.fetchall()
        print(results)

        items = {}
        items['results'] = []

        for result in results:
            item = {}
            item['Department'] = result[0]
            item['Dept_Responses'] = result[1]
            items['results'].append(item)
        #depts.append(items['results'])
        resultsArray.append(items['results'])

        # laptop detractors (low scorers)
        sql = "SELECT d.DeviceModel, COUNT(d.DeviceModel) AS Negative_Scores \
            FROM SurveyResults s LEFT JOIN Laptops d ON s.EmployeeID = d.EmployeeID \
                WHERE s.Laptop_Score < 4 GROUP BY d.DeviceModel"
        cursor.execute(sql)
        #laptopDetractors = []
        results = cursor.fetchall()
        print(results)

        items = {}
        items['results'] = []

        for result in results:
            item = {}
            item['DeviceModel'] = result[0]
            item['Negative_Scores'] = result[1]
            items['results'].append(item)
        #laptopDetractors.append(items['results'])
        resultsArray.append(items['results'])

        # info for employees open to being contacted for follow up
        sql = "SELECT s.ResponseID, e.EmployeeID, CONCAT(e.FirstName,e.LastName,'@dell.com') AS Email, e.ManagerID, \
            e.Location, e.JobTitle, e.Department, d.DeviceModel, d.DeviceAgeMonths, s.Follow_Up, s.IT_Overall_Score, \
                s.Laptop_Score, s.Accessories_Score, s.Applications_Score, s.Support_Score \
                FROM Employees e LEFT JOIN SurveyResults s ON e.EmployeeID = s.EmployeeID \
                    LEFT JOIN Laptops d ON s.EmployeeID = d.EmployeeID WHERE Follow_Up = 'Yes'"

        cursor.execute(sql)
        #followUpInfo = []
        results = cursor.fetchall()
        print(results)

        items = {}
        items['results'] = []

        for result in results:
            item = {}
            item['ResponseID'] = result[0]
            item['EmployeeID'] = result[1]
            item['Email'] = result[2]
            item['ManagerID'] = result[3]
            item['Location'] = result[4]
            item['JobTitle'] = result[5]
            item['Dept'] = result[6]
            item['LaptopModel'] = result[7]
            item['LaptopAgeMths'] = result[8]
            item['FollowUp'] = result[9]
            item['ITOverall'] = result[10]
            item['LaptopScore'] = result[11]
            item['AccessoriesScore'] = result[12]
            item['AppsScore'] = result[13]
            item['SupportScore'] = result[14]
            items['results'].append(item)
        #followUpInfo.append(items['results'])
        resultsArray.append(items['results'])

        self.closeAll()

        '''
        resultsArray = []
        results.append(numResponses)
        results.append(scores)
        results.append(depts)
        results.append(laptopDetractors)
        results.append(followUpInfo)
        '''
        return resultsArray
        
        
    '''
    def create_tables(self):
        cursor = self.getcursor()
        sql = "create table vote (id int AUTO_INCREMENT NOT NULL PRIMARY KEY, bandname varchar(250), ipaddress varchar(250))"
        cursor.execute(sql)

        self.connection.commit()
        self.closeAll()

    
    def create_database(self):
        self.connection = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password   
        )
        self.cursor = self.connection.cursor()
        sql="create database "+ self.database
        self.cursor.execute(sql)

        self.connection.commit()
        self.closeAll()
    '''

survey_DAO = Survey_DAO()