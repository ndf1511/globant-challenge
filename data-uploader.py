from flask import Flask
from flask_restful import Api, Resource, reqparse
from sqlalchemy import create_engine
from flask_jsonpify import jsonpify
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

conf ={
    'host':"globant-test.ckoljx3ba7ss.us-east-1.rds.amazonaws.com",
    'port':'5432',
    'database':"testdb",
    'user':"nicolas",
    'password':"12345678" #if this was anything important i would use a secret manager
}

class Departments(Resource):
    def post(self):
        engine = create_engine("postgresql://{user}:{password}@{host}:{port}/{database}".format(**conf))
        df = pd.read_csv('data/departments.csv', header=None, names=['id', 'department'])
        df.to_sql('departments', con=engine, if_exists='append', index=False)
        return {'data': df.to_dict()}, 201
        
class Employees(Resource):
    def post(self):
        engine = create_engine("postgresql://{user}:{password}@{host}:{port}/{database}".format(**conf))
        df = pd.read_csv('data/hired_employees.csv', header=None, names=['id', 'name', 'datetime', 'department_id', 'job_id'], delimiter=',')
        df.to_sql('employees', con=engine, if_exists='append', index=False)
        return {'data': df.to_dict()}, 201

class Jobs(Resource):
    def post(self):
        engine = create_engine("postgresql://{user}:{password}@{host}:{port}/{database}".format(**conf))
        df = pd.read_csv('data/jobs.csv', header=None, names=['id', 'job'])
        df.to_sql('jobs', con=engine, if_exists='append', index=False)
        return {'data': df.to_dict()}, 201
    
class EmployeesHiredByDepartmentAndJob(Resource):
    def get(self):
        engine = create_engine("postgresql://{user}:{password}@{host}:{port}/{database}".
                               format(**conf))
        df = pd.read_sql_query(open('hires_by_department_job.sql', 'r').read(), engine)
        return jsonpify(df.to_dict(orient='records'))
    
class HiresByDepartmentOverMean(Resource):
    def get(self):
        engine = create_engine("postgresql://{user}:{password}@{host}:{port}/{database}".
                               format(**conf))
        df = pd.read_sql_query(open('hires_by_department_over_mean.sql', 'r').read(), engine)
        return jsonpify(df.to_dict(orient='records'))

api.add_resource(Departments, '/departments') 
api.add_resource(Employees, '/employees')
api.add_resource(Jobs, '/jobs')
api.add_resource(EmployeesHiredByDepartmentAndJob, '/hires_by_department_and_job')
api.add_resource(HiresByDepartmentOverMean, '/hires_by_department_over_mean')

if __name__ == '__main__':
    app.run(debug=True)

