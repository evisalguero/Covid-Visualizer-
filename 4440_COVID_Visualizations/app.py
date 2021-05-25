from flask import Flask, request, session, render_template, redirect, url_for, jsonify, Response

import json
import pymysql
import os
import re
import collections
import datetime
import random
import csv
import random


app = Flask(__name__, static_url_path="")
app.secret_key = os.urandom(24)

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='password', # replace your db password here
                             db='covid_db')

@app.route("/")
def index():
    return render_template("index.html")

def write_csv(base_name, fields, data_list):
    rand_num = str(random.randint(0,100000000000))
    file_name = 'static/' + base_name + rand_num + '.csv'
    pass_file_name = base_name + rand_num + '.csv'
    print(pass_file_name)
    # f = open(file_name, 'w', newline='')
    f = open(file_name, 'wb')
    writer = csv.writer(f)
    writer.writerow(fields)
    writer.writerows(data_list)
    f.close()
    return pass_file_name


@app.route('/view_cases_county', methods=['GET', 'POST'])
def view_cases_county(date='2020-05-01'):
    if request.method == 'GET':
        return render_template("view_cases_county.html")
    date = request.form['i_date']
    print(date)

    cursor = connection.cursor()
    cursor.execute('SELECT fips, county, cumul_cases FROM COUNTY_INFECTIONS WHERE submission_date = (%s);',
                        (date,))
    cases = cursor.fetchall()

    print(len(cases))
    fields = ['id', 'county', 'cases']
    cases_list = [
                [int(fips), county, int(cases)]
                for fips, county, cases
                in cases
            ]

    pass_file_name = write_csv('county_cases', fields, cases_list)
    return render_template("view_cases_county.html", file_name=pass_file_name, sel_date=date)

@app.route('/view_deaths_county', methods=['GET', 'POST'])
def view_deaths_county(date='2020-03-21'):
    if request.method == 'GET':
        return render_template("view_deaths_county.html")
    date = request.form['i_date']
    print(date)

    cursor = connection.cursor()
    cursor.execute('SELECT fips, county, deaths FROM COUNTY_INFECTIONS WHERE submission_date = (%s);',
                        (date,))
    deaths = cursor.fetchall()
    print(len(deaths))
    fields = ['id', 'county', 'deaths']
    deaths_list = [
                [int(fips), county, 0 if death == '' else int(death)]
                for fips, county, death
                in deaths
            ]

    pass_file_name = write_csv('county_deaths', fields, deaths_list)
    return render_template("view_deaths_county.html", file_name=pass_file_name, sel_date=date)

@app.route('/view_vac_dis', methods=['GET', 'POST'])
def view_vac_dis():
    cursor = connection.cursor()
    if request.method == 'POST':
        if 'filter' in request.form:
            filters = {
                'i_date' : request.form['i_date']
            }

            for filt_name, val in filters.items():
                filters[filt_name] = val if val else None


            cursor.callproc('covid_vaccine_distribution_date_state', tuple(filters.values()))
            connection.commit()
            cursor.execute('SELECT * FROM covid_vaccine_distribution_date_state_result;')
            vac_results = cursor.fetchall()

            # Create a list of results to display in the HTML
            fields = ['state_name', 'pop_vaccine']

            vac_list = [[
                state_name, pop_vaccine]
                for state_name, pop_vaccine
                in vac_results
            ]

            pass_file_name = write_csv('vac_state', fields, vac_list)
            return render_template("view_vac_dis.html", file_name=pass_file_name, filters = filters.values())

    return render_template("view_vac_dis.html")


@app.route('/view_vac_ratio', methods=['GET', 'POST'])
def view_vac_ratio():
    cursor = connection.cursor()
    if request.method == 'POST':
        if 'filter' in request.form:
            filters = {
                'i_date' : request.form['i_date']
            }
            for filt_name, val in filters.items():
                filters[filt_name] = val if val else None

            cursor.callproc('covid_vaccine_ratio', tuple(filters.values()))
            connection.commit()
            cursor.execute('SELECT * FROM covid_vaccine_ratio_result;')
            vac_results = cursor.fetchall()

            # Create a list of results to display in the HTML
            fields = ['state_name', 'pop_vaccine']

            vac_list = [[
                state_name, pop_vaccine]
                for state_name, pop_vaccine
                in vac_results
            ]


            pass_file_name = write_csv('vac_ratio', fields, vac_list)
            return render_template("view_vac_ratio.html", file_name = pass_file_name, filters = filters.values())

    return render_template("view_vac_ratio.html")

@app.route('/view_county_ratio', methods=['GET', 'POST'])
def view_county_ratio():
    cursor = connection.cursor()
    if request.method == 'POST':
        if 'filter' in request.form:
            filters = {
                'i_date' : request.form['i_date']
            }

            date = request.form['i_date']

            cursor.callproc('calculate_covid_cases_county_ratio', [filters['i_date']]);
            connection.commit()
            cursor.execute('SELECT * FROM county_cases_and_pop;')
            inf_results = cursor.fetchall()

            fields = ['id', 'county', 'cases', 'population']

            inf_list = [[
                fips, county_name, cases, population]
                for fips, county_name, cases, population
                in inf_results
            ]

            pass_file_name = write_csv('county_ratio', fields, inf_list)
            return render_template("view_county_ratio.html", file_name=pass_file_name, sel_date=date)

    return render_template("view_county_ratio.html")


@app.route('/view_daily_cases', methods=['GET', 'POST'])
def view_daily_cases():
    cursor = connection.cursor()
    if request.method == 'POST':
        if 'filter' in request.form:
            filters = {
                'i_date' : request.form['i_date']
            }

            date = request.form['i_date']

            cursor.execute('SELECT fips, county, daily_cases FROM COUNTY_INFECTIONS WHERE submission_date = (%s);',
                        (date,))
            inf_results = cursor.fetchall()

            fields = ['id', 'county', 'daily_cases']

            inf_list = [[
                fips, county_name, daily_cases]
                for fips, county_name, daily_cases
                in inf_results
            ]

            pass_file_name = write_csv('daily_cases', fields, inf_list)
            return render_template("view_daily_cases.html", file_name=pass_file_name, sel_date=date)

    return render_template("view_daily_cases.html")


