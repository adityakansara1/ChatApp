import mysql.connector
import json


with open('config.json', 'r') as c:
    params = json.load(c)['params']

app_db = mysql.connector.connect (
    host=params['db_data']['host'],
    user=params['db_data']['user'],
    password=params['db_data']['password'],
    database=params['db_data']['database']
)


class NewUser:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


    def insertUser(self):
        try:
            mycursor = app_db.cursor()
            sql = f"""insert into users (username, email, password) values ('{self.username}', '{self.email}', '{self.password}')"""
            mycursor.execute(sql)
            app_db.commit()
        except Exception as e:
            print(e)

class NewDP:
    def __init__(self, uid, dp):
        self.uid = uid
        self.dp = dp

    def insertDp(self):
        try:
            mycursor = app_db.cursor()
            sql = f"""update users set dp='{self.dp}' where uid = {self.uid}"""
            mycursor.execute(sql)
            app_db.commit()
        except Exception as e:
            print(e)


class SignIn:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def checkUser(self):
        try: 
            mycursor = app_db.cursor()
            sql_user_data = f"""select * from users where username='{self.username}'"""
            mycursor.execute(sql_user_data)
            user_data = mycursor.fetchone()

            if self.username == user_data[1] and self.password == user_data[3]:
                sql_friends_data = f"""select * from users left outer join friends on users.uid = friends.uid2 where uid1={user_data[0]}"""
                mycursor.execute(sql_friends_data)
                friends_data = mycursor.fetchall()

                sql_groups_data = f"""select * from users left outer join users_groups on users.uid = users_groups.uid where gid in (select gid from users_groups where uid = {user_data[0]})"""
                mycursor.execute(sql_groups_data)
                groups_data = mycursor.fetchall()
                for i in groups_data:
                    if i[0] != user_data[0]:
                        print(i)

                a_file = open('config.json', 'r')
                json_obj = json.load(a_file)
                a_file.close()

                json_obj["params"]["user_data"]["uid"] = user_data[0]
                json_obj["params"]["user_data"]["username"] = user_data[1]
                json_obj["params"]["user_data"]["email"] = user_data[2]
                json_obj["params"]["user_data"]["dp"] = user_data[4]

                if json_obj["params"]["user_data"]["friends"] != None:
                    json_obj["params"]["user_data"]["friends"] = []

                for i in friends_data:
                    json_obj["params"]["user_data"]["friends"].append({"friend_uid": i[0], "friend_name": i[1], "friend_email": i[2], "friend_dp": i[4]})


                a_file = open('config.json', 'w')
                json.dump(json_obj, a_file)
                a_file.close()

                return True
            else: 
                return False
        except Exception as e:
            print(e)
            return False