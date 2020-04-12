from flask import Flask, render_template, jsonify, request
from flask_wtf import FlaskForm
from wtforms import SelectField
import requests, json, ast, datetime
''' ------------- HELPER FUNCTIONS FOR API ROUTES BELOW THIS LINE ------------- '''
def get_table_name(year):
    return str(year)+'_vehicles'
# ----------------------
def mappify_row(row):
    # Parse row object to return a dictionary with {key : value} mapping
    map = dict()
    map['Year'] = row[1]
    map['Make'] = row[2]
    map['Model'] = row[3]
    map['Styles'] = ast.literal_eval(row[4])
    map['Trims'] = ast.literal_eval(row[5])
    map['Images'] = ast.literal_eval(row[6])

    # Return a dictionary for a result object
    return map
# ----------------------
def parse_results(results):
    # Parse results
    list = []
    for result in results:
        map = mappify_row(result)
        list.append(map)
    return list
# ----------------------
def compile_response(list):
    response = dict()
    response['Count'] = len(list)
    if len(list) > 0:
        response['Message'] = 'Results returned successfully'
    else:
        response['Message'] = 'No results found for this request'
    response['Results'] = list
    return response
# ----------------------
def default_response():
    response = dict()
    response['Count'] = 0
    response['Message'] = 'No results found for this request'
    response['Results'] = []
    return response
