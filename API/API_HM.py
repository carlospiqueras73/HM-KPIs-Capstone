"""
API H&M DATASETS
"""

from flask import Flask, jsonify
from sqlalchemy import create_engine
from flask_restx import Api, Namespace, Resource

user = ""
passw = ""
host = ""
database = ""

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = host

api = Api(app, version = '1.0',
    title = 'Rest API for H&M Capstone data - Carlos Piqueras, MCSBT',
    description = """
        This RESTS API is an API built with FLASK
        and FLASK-RESTX libraries for the CAPSTONE
        PROJECT of the MCSBT @ IE UNIVERSITY
        """,
    contact = "carlos.piqueras@student.ie.edu",
    endpoint = "/api/v1"
)

def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    connect_args = {'connect_timeout': 10})
    conn = db.connect()
    return conn

def disconnect(conn):
    conn.close()

# ---------------------
# FOR THE ARTICLES DATA
# ---------------------

articles = Namespace('articles',
    description = 'All information related to articles',
    path='/api/v1')
api.add_namespace(articles)

# Retrieve the first 1000 entries from the articles dataframe
@articles.route("/articles")
class get_all_articles(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM articles
            LIMIT 1000;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

# ----------------------
# FOR THE CUSTOMERS DATA
# ----------------------

customers = Namespace('customers',
    description = 'All information related to customers',
    path='/api/v1')
api.add_namespace(customers)

# Retrieve the first 1000 entries from the customers dataframe
@customers.route("/customers")
class get_all_customers(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM customers
            LIMIT 1000;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

# -------------------------
# FOR THE TRANSACTIONS DATA
# -------------------------

transactions = Namespace('transactions',
    description = 'All information related to transactions',
    path='/api/v1')
api.add_namespace(transactions)

# Retrieve first 1000 transactions entries with all their corresponding information
@transactions.route("/transactions")
class get_all_transactions(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM transactions
            LIMIT 1000;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

if __name__ == '__main__':
    app.run(host = '0.0.0.0', 
            port = 8080,
            debug = True)