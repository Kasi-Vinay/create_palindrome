
class InvalidField(Exception):
    pass

class DoesNotExist(Exception):
    pass

class MultipleObjectsReturned(Exception):
    pass



class Student:
    def __init__(self, name, age, score):
        self.name = name
        self.student_id = None
        self.age = age
        self.score = score
    
    def __repr__(self):
        return "Student(student_id={0}, name={1}, age={2}, score={3})".format(
            self.student_id,
            self.name,
            self.age,
            self.score)
    
    
    @classmethod
    def get(cls,**kwargs):
        for k,v in kwargs.items():
            cls.x=k
            cls.y=v
        
            if str(k) not in ('student_id','name','age','score'):
                raise InvalidField
            
        
        res = read_data(" SELECT * FROM STUDENT WHERE {} = '{}' ".format(cls.x,cls.y) )
        
        if len(res)==0:
            raise DoesNotExist
        elif len(res) > 1:
            raise MultipleObjectsReturned
            
        out=Student(res[0][1],res[0][2],res[0][3])
        out.student_id = res[0][0]
        return out
    
    
    def save(self):
        if self.student_id is None:
            write_data( "INSERT INTO STUDENT (name,age,score) VALUES('{}',{},{})".format(self.name,self.age,self.score) )
            query=read_data( "SELECT student_id FROM STUDENT WHERE name='{}' AND age={} AND score={}".format(self.name,self.age,self.score) )
            self.student_id=query[0][0]
            
        elif(f" SELECT {self.student_id} NOT IN (SELECT student_id FROM STUDENT) FROM STUDENT "):
            write_data(f"REPLACE INTO STUDENT (student_id,name,age,score) VALUES( {self.student_id},'{self.name}',{self.age},{self.score} )")
            
        else:
            write_data( "UPDATE STUDENT SET name='{}',age={},score={}".format(self.name,self.age,self.score) )
        
        
    
    def delete(self):
        write_data(f"DELETE FROM STUDENT WHERE student_id={self.student_id}")




    @classmethod
    def filter(cls,**kwargs):
        
        cls.condition_list = []
        cls.condition_operators = { 'lt' : '<','lte':'<=','gt':'>','gte':'>=','neq':'<>','in':'in','contain':''}  
        
        
        if(len(kwargs))>=1:
            append_list = []
            for k,v in kwargs.items():
                    cls.x=k
                    cls.y=v
            
                    condition = cls.x            
                    condition = k.split('__')        
            
                    if condition[0]  not in ('student_id','name','age','score'):
                        raise InvalidField
        
                    if (len(condition)) == 1:
                        query=(f"{cls.x}={cls.y}")
                        
                    elif condition[1] == 'in':
                        query=(f"{condition[0]} {cls.condition_operators[condition[1]]} {tuple(cls.y)}")
                   
                    elif condition[1] == 'contains':
                        query=(f"{condition[0]} LIKE '%{cls.y}%'")
                        
                    else:
                        query=(f"{condition[0]} {cls.condition_operators[condition[1]]} '{cls.y}'  ")
                
                    append_list.append(query)
            
        
            joining_list=" and ".join(tuple(append_list))  
            query="SELECT * FROM STUDENT WHERE"+joining_list


        output_query=read_data(query)
        for i in range(len(output_query)):
            output=Student(i[1],i[2],i[3])
            output.student_id=output_query[i][0]
            cls.condition_list.append(output)
        return cls.condition_list       
        

def write_data(sql_query):
	import sqlite3
	connection = sqlite3.connect("selected_students.sqlite3")
	crsr = connection.cursor() 
	crsr.execute("PRAGMA foreign_keys=on;") 
	crsr.execute(sql_query) 
	connection.commit() 
	connection.close()

def read_data(sql_query):
	import sqlite3
	connection = sqlite3.connect("selected_students.sqlite3")
	crsr = connection.cursor() 
	crsr.execute(sql_query) 
	ans= crsr.fetchall()  
	connection.close() 
	return ans
