from flask import Flask, jsonify, abort, request, render_template
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = '104.198.163.126'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'yEBpALG6zHDoCFLn'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = 'project'

mysql = MySQL(app)
import flask_mysql as db


@app.route('/', methods=['GET'])
def home():
    return "Home for backend Education Today"


@app.route('/search', methods=['GET'])
def get_professor_ranked_list():
    professor_name = request.args.get('professor')
    institution_name = request.args.get('institution')
    if not db.get_professor_info(professor_name, institution_name):
        db.scrape_professor_info(professor_name, institution_name)
    data = db.get_professor_ranked_list(professor_name, institution_name)

    # return jsonify([]), 200
    return jsonify(data), 200


@app.route('/page', methods=['GET'])
def get_specific_professor_info():
    professor_name = request.args.get('professor')
    institution_name = request.args.get('institution')
    data = db.get_professor_info(professor_name, institution_name)
    # print((professor_name, institution_name), data)
    return jsonify(data[0]), 200


@app.route('/publication', methods=['GET'])
def get_professor_publications():
    professor_name = request.args.get('professor')
    institution_name = request.args.get('institution')
    data = db.get_professor_publications(professor_name, institution_name)
    return jsonify(data), 200


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response
