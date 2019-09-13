from flask import render_template, url_for, flash, redirect, request, Response, session
from tool import app
from tool.forms import QueryForm
# from flaskblog.forms import RegistrationForm, LoginForm
# from flaskblog.models import User, Post
import pandas as pd
from datetime import datetime
import os
from io import StringIO
# Designate routes
# Routes direct you to different pages
# Don't forget to set an enviornment variable "export FLASK_APP=flaskblog.py"
# in BASH write "flask run" to launch
# Run in debug mode for rapid development "export FLASK_DEBUG=1"
# Debug mode updates changes in real time.

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST']) # directs to hello with either url.
def home():
    # Generate the search form. Comes from forms.py
    form = QueryForm(request.form)
    # When the user posts, collect the data and validate.
    if request.method == 'POST':
        content = form.data
        # prints to terminal. For dev and debugging purposes
        print(content)
        # Generate a session variable to generate the download dataframe
        session['content'] = content
        print(form.validate_on_submit())
        logged = content
        with open('log.txt', 'w+') as log_file:
            log_file.write(str(datetime.now()))
            log_file.write('\n\n\n')
            for k, v in logged.items():
                log_file.write(str(k) + ' : ' + str(v))
                log_file.write('\n')

        if form.validate_on_submit():
            # Load master dataset
            data = pd.read_csv('wds_gaia_master.csv', index_col=0)
            # Check if user chose to search by WDS disc
            # if content['by_des_or_coord'] == 'By WDS discoverer code':
            if content['WDS_name']:
                # Gather the system and components from the master set
                data = data[data['WDSName'] == content['WDS_name']]
                # Flash the number of system components found.
                flash(f'This system has {len(data) + 1} components.')

                # For a system with only AB components
                if len(data) == 1:
                    # rename the dataset. For consistency
                    data_ab_comp = data
                    # The overall system snapshot
                    sys_info = data_ab_comp[['WDSNum' , 'WDSName', 'WDS_RA',
                        'WDS_Dec']]
                    # Info for the A component
                    a_comp = data_ab_comp[['WDS_disc', 'components', 'NOBS',
                        'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA' 'gaia_PMRA1', 'gaia_PMDEC1',
                        'gaia_mag_1', 'delta_mag_GAIA', 'STYPE', 'NOTES', 'd_pri', 'PM_prob', 'binary_prob', 'physical?',
                         'px_prob', 'dist_prob']]
                    # Info for the B component
                    b_comp = data_ab_comp[['WDS_disc', 'components', 'NOBS',
                        'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA', 'gaia_PMRA2', 'gaia_PMDEC2',
                        'gaia_mag_2', 'delta_mag_GAIA', 'STYPE', 'NOTES', 'd_sec', 'PM_prob', 'binary_prob', 'physical?',
                         'px_prob', 'dist_prob']]


                    # Convert dataframes to html and then render as a list of tables
                    return render_template('results.html',
                        tables=[sys_info.to_html(classes='wdsgaia table'),
                            a_comp.to_html(classes='wdsgaia table'),
                            b_comp.to_html(classes='wdsgaia table')],
                        titles=['na', 'System Info', 'Primary Info',
                         'Secondary Info'])
                # For systems with AC component
                if len(data) == 2:
                    # Split the data into AB and AC components
                    data_ab_comp = data[data['components'] == 'AB']
                    data_c_comp = data[data['components'] == 'AC']
                    # System snapshot
                    sys_info = data_ab_comp[['WDSNum' , 'WDSName', 'WDS_RA',
                        'WDS_Dec']]
                    # Info for the A component
                    a_comp = data_ab_comp[['WDS_disc', 'components', 'NOBS',
                        'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA', 'gaia_PMRA1', 'gaia_PMDEC1',
                        'gaia_mag_1', 'delta_mag_GAIA', 'STYPE', 'NOTES', 'd_pri', 'PM_prob', 'binary_prob', 'physical?',
                         'px_prob', 'dist_prob']]
                    # Info for the B component
                    b_comp = data_ab_comp[['WDS_disc', 'components', 'NOBS',
                        'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA', 'gaia_PMRA2', 'gaia_PMDEC2',
                        'gaia_mag_2', 'delta_mag_GAIA', 'STYPE', 'NOTES', 'd_sec', 'PM_prob', 'binary_prob', 'physical?',
                         'px_prob', 'dist_prob']]
                    # Rename the C component columns to more meaninful names
                    c_comp = data_c_comp.rename(columns={
                         'gaia_PMRA2': 'gaia_PMRA3',
                         'gaia_PMDEC2': 'gaia_PMDEC3',
                         'gaia_mag_2': 'gaia_mag_3',
                         'd_sec': 'd_3'}, inplace=True)
                    # C component
                    c_comp = data_c_comp[['WDS_disc', 'components', 'NOBS',
                        'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA', 'gaia_PMRA3', 'gaia_PMDEC3',
                        'gaia_mag_3', 'delta_mag_GAIA', 'STYPE', 'NOTES', 'd_3', 'PM_prob', 'binary_prob', 'physical?',
                         'px_prob', 'dist_prob']]
                    # Convert to html and render as list of tables
                    return render_template('results.html',
                        tables=[sys_info.to_html(classes='wdsgaia table'),
                            a_comp.to_html(classes='wdsgaia table'),
                            b_comp.to_html(classes='wdsgaia table'),
                            c_comp.to_html(classes='wdsgaia table')],
                        titles=['na', 'System Info', 'A Component Info',
                         'B Component Info', 'C Component Info'])
                # For systems with AD component
                if len(data) == 3:
                    # Split the data into AB and AC components
                    data_ab_comp = data[data['components'] == 'AB']
                    data_c_comp = data[data['components'] == 'AC']
                    data_d_comp = data[data['components'] == 'AD']
                    # System snapshot
                    sys_info = data_ab_comp[['WDSNum' , 'WDSName', 'WDS_RA',
                        'WDS_Dec']]
                    # Info for the A component
                    a_comp = data_ab_comp[['WDS_disc', 'components', 'NOBS',
                        'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA', 'gaia_PMRA1', 'gaia_PMDEC1',
                        'gaia_mag_1', 'delta_mag_GAIA', 'STYPE', 'NOTES', 'd_pri', 'PM_prob', 'binary_prob', 'physical?',
                         'px_prob', 'dist_prob']]
                    # Info for the B component
                    b_comp = data_ab_comp[['WDS_disc', 'components', 'NOBS',
                        'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA', 'gaia_PMRA2', 'gaia_PMDEC2',
                        'gaia_mag_2', 'delta_mag_GAIA', 'STYPE', 'NOTES', 'd_sec', 'PM_prob', 'binary_prob', 'physical?',
                         'px_prob', 'dist_prob']]
                    # Rename the C component columns to more meaninful names
                    c_comp = data_c_comp.rename(columns={
                         'gaia_PMRA2': 'gaia_PMRA3',
                         'gaia_PMDEC2': 'gaia_PMDEC3',
                         'gaia_mag_2': 'gaia_mag_3',
                         'd_sec': 'd_3'}, inplace=True)
                    # C component
                    c_comp = data_c_comp[['WDS_disc', 'components', 'NOBS',
                        'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA', 'gaia_PMRA3', 'gaia_PMDEC3',
                        'gaia_mag_3', 'delta_mag_GAIA', 'STYPE', 'NOTES', 'd_3', 'PM_prob', 'binary_prob', 'physical?',
                         'px_prob', 'dist_prob']]
                    # Rename the D component columns to more meaningful names
                    d_comp = data_d_comp.rename(columns={
                         'gaia_PMRA2': 'gaia_PMRA4',
                         'gaia_PMDEC2': 'gaia_PMDEC4',
                         'gaia_mag_2': 'gaia_mag_4',
                         'd_sec': 'd_4'}, inplace=True)
                    # D component
                    d_comp = data_d_comp[['WDS_disc', 'components', 'NOBS',
                        'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA', 'gaia_PMRA4', 'gaia_PMDEC4',
                        'gaia_mag_4', 'delta_mag_GAIA', 'STYPE', 'NOTES', 'd_4', 'PM_prob', 'binary_prob', 'physical?',
                         'px_prob', 'dist_prob']]
                     # Convert to html and render as list of tables
                    return render_template('results.html',
                        tables=[sys_info.to_html(classes='wdsgaia table'),
                            a_comp.to_html(classes='wdsgaia table'),
                            b_comp.to_html(classes='wdsgaia table'),
                            c_comp.to_html(classes='wdsgaia table'),
                            d_comp.to_html(classes='wdsgaia table')],
                        titles=['na', 'System Info', 'A Component Info',
                        'B Component Info', 'C Component Info', 'D Component Info'])
                # For systems with AE component
                if len(data) == 4:
                    # Split the data into AB, AC, AD, AE components
                    data_ab_comp = data[data['components'] == 'AB']
                    data_c_comp = data[data['components'] == 'AC']
                    data_d_comp = data[data['components'] == 'AD']
                    data_e_comp = data[data['components'] == 'AE']
                    # System snapshot
                    sys_info = data_ab_comp[['WDSNum' , 'WDSName', 'WDS_RA',
                        'WDS_Dec']]
                    # Info for the A component
                    a_comp = data_ab_comp[['WDS_disc', 'components', 'NOBS',
                        'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA', 'gaia_PMRA1', 'gaia_PMDEC1',
                        'gaia_mag_1', 'delta_mag_GAIA', 'STYPE', 'NOTES', 'd_pri', 'PM_prob', 'binary_prob', 'physical?',
                         'px_prob', 'dist_prob']]
                    # Info for the B component
                    b_comp = data_ab_comp[['WDS_disc', 'components', 'NOBS',
                        'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA', 'gaia_PMRA2', 'gaia_PMDEC2',
                        'gaia_mag_2', 'delta_mag_GAIA', 'STYPE', 'NOTES', 'd_sec', 'PM_prob', 'binary_prob', 'physical?',
                         'px_prob', 'dist_prob']]
                    # Rename the C component columns to more meaninful names
                    c_comp = data_c_comp.rename(columns={
                         'gaia_PMRA2': 'gaia_PMRA3',
                         'gaia_PMDEC2': 'gaia_PMDEC3',
                         'gaia_mag_2': 'gaia_mag_3',
                         'd_sec': 'd_3'}, inplace=True)
                    # C component
                    c_comp = data_c_comp[['WDS_disc', 'components', 'NOBS',
                        'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA', 'gaia_PMRA3', 'gaia_PMDEC3',
                        'gaia_mag_3', 'delta_mag_GAIA', 'STYPE', 'NOTES', 'd_3', 'PM_prob', 'binary_prob', 'physical?',
                         'px_prob', 'dist_prob']]
                    # Rename the D component columns to more meaningful names
                    d_comp = data_d_comp.rename(columns={
                         'gaia_PMRA2': 'gaia_PMRA4',
                         'gaia_PMDEC2': 'gaia_PMDEC4',
                         'gaia_mag_2': 'gaia_mag_4',
                         'd_sec': 'd_4'}, inplace=True)
                    # D component
                    d_comp = data_d_comp[['WDS_disc', 'components', 'NOBS',
                        'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA', 'gaia_PMRA4', 'gaia_PMDEC4',
                        'gaia_mag_4', 'delta_mag_GAIA', 'STYPE', 'NOTES', 'd_4', 'PM_prob', 'binary_prob', 'physical?',
                         'px_prob', 'dist_prob']]
                    # Rename the E component columns to more meaningful names
                    e_comp = data_e_comp.rename(columns={
                         'gaia_PMRA2': 'gaia_PMRA5',
                         'gaia_PMDEC2': 'gaia_PMDEC5',
                         'gaia_mag_2': 'gaia_mag_5',
                         'd_sec': 'd_5'}, inplace=True)
                    # E component
                    e_comp = data_e_comp[['WDS_disc', 'components', 'NOBS',
                        'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA', 'gaia_PMRA5', 'gaia_PMDEC5',
                        'gaia_mag_5', 'delta_mag_GAIA', 'STYPE', 'NOTES', 'd_5', 'PM_prob', 'binary_prob', 'physical?',
                         'px_prob', 'dist_prob']]
                     # Convert to html and render as list of tables
                    return render_template('results.html',
                        tables=[sys_info.to_html(classes='wdsgaia table'),
                            a_comp.to_html(classes='wdsgaia table'),
                            b_comp.to_html(classes='wdsgaia table'),
                            c_comp.to_html(classes='wdsgaia table'),
                            d_comp.to_html(classes='wdsgaia table'),
                            e_comp.to_html(classes='wdsgaia table')],
                        titles=['na', 'System Info', 'A Component Info',
                        'B Component Info', 'C Component Info', 'D Component Info',
                        'E Component Info'])
                # For systems with AF component
                if len(data) == 5:
                        # Split the data into AB, AC, AD, AE, AF components
                        data_ab_comp = data[data['components'] == 'AB']
                        data_c_comp = data[data['components'] == 'AC']
                        data_d_comp = data[data['components'] == 'AD']
                        data_e_comp = data[data['components'] == 'AE']
                        data_f_comp = data[data['components'] == 'AF']
                        # System snapshot
                        sys_info = data_ab_comp[['WDSNum' , 'WDSName', 'WDS_RA',
                            'WDS_Dec']]
                        # Info for the A component
                        a_comp = data_ab_comp[['WDS_disc', 'components', 'NOBS',
                            'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA', 'gaia_PMRA1', 'gaia_PMDEC1',
                            'gaia_mag_1', 'delta_mag_GAIA', 'STYPE', 'NOTES', 'd_pri', 'PM_prob', 'binary_prob', 'physical?',
                             'px_prob', 'dist_prob']]
                        # Info for the B component
                        b_comp = data_ab_comp[['WDS_disc', 'components', 'NOBS',
                            'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA', 'gaia_PMRA2', 'gaia_PMDEC2',
                            'gaia_mag_2', 'delta_mag_GAIA', 'STYPE', 'NOTES', 'd_sec', 'PM_prob', 'binary_prob', 'physical?',
                             'px_prob', 'dist_prob']]
                        # Rename the C component columns to more meaninful names
                        c_comp = data_c_comp.rename(columns={
                             'gaia_PMRA2': 'gaia_PMRA3',
                             'gaia_PMDEC2': 'gaia_PMDEC3',
                             'gaia_mag_2': 'gaia_mag_3',
                             'd_sec': 'd_3'}, inplace=True)
                        # C component
                        c_comp = data_c_comp[['WDS_disc', 'components', 'NOBS',
                            'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA', 'gaia_PMRA3', 'gaia_PMDEC3',
                            'gaia_mag_3', 'delta_mag_GAIA', 'STYPE', 'NOTES', 'd_3', 'PM_prob', 'binary_prob', 'physical?',
                             'px_prob', 'dist_prob']]
                        # Rename the D component columns to more meaningful names
                        d_comp = data_d_comp.rename(columns={
                             'gaia_PMRA2': 'gaia_PMRA4',
                             'gaia_PMDEC2': 'gaia_PMDEC4',
                             'gaia_mag_2': 'gaia_mag_4',
                             'd_sec': 'd_4'}, inplace=True)
                        # D component
                        d_comp = data_d_comp[['WDS_disc', 'components', 'NOBS',
                            'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA', 'gaia_PMRA4', 'gaia_PMDEC4',
                            'gaia_mag_4', 'delta_mag_GAIA', 'STYPE', 'NOTES', 'd_4', 'PM_prob', 'binary_prob', 'physical?',
                             'px_prob', 'dist_prob']]
                        # Rename the E component columns to more meaningful names
                        e_comp = data_e_comp.rename(columns={
                             'gaia_PMRA2': 'gaia_PMRA5',
                             'gaia_PMDEC2': 'gaia_PMDEC5',
                             'gaia_mag_2': 'gaia_mag_5',
                             'd_sec': 'd_5'}, inplace=True)
                        # E component
                        e_comp = data_e_comp[['WDS_disc', 'components', 'NOBS',
                            'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA', 'gaia_PMRA5', 'gaia_PMDEC5',
                            'gaia_mag_5', 'delta_mag_GAIA', 'STYPE', 'NOTES', 'd_5', 'PM_prob', 'binary_prob', 'physical?',
                             'px_prob', 'dist_prob']]
                        # Rename the F component columns to more meaningful names
                        f_comp = data_f_comp.rename(columns={
                             'gaia_PMRA2': 'gaia_PMRA6',
                             'gaia_PMDEC2': 'gaia_PMDEC6',
                             'gaia_mag_2': 'gaia_mag_6',
                             'd_sec': 'd_6'}, inplace=True)
                        # F component
                        f_comp = data_e_comp[['WDS_disc', 'components', 'NOBS',
                            'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA', 'gaia_PMRA6', 'gaia_PMDEC6',
                            'gaia_mag_6', 'delta_mag_GAIA', 'STYPE', 'NOTES', 'd_6', 'PM_prob', 'binary_prob', 'physical?',
                             'px_prob', 'dist_prob']]
                         # Convert to html and render as list of tables
                        return render_template('results.html',
                            tables=[sys_info.to_html(classes='wdsgaia table'),
                                a_comp.to_html(classes='wdsgaia table'),
                                b_comp.to_html(classes='wdsgaia table'),
                                c_comp.to_html(classes='wdsgaia table'),
                                d_comp.to_html(classes='wdsgaia table'),
                                e_comp.to_html(classes='wdsgaia table'),
                                f_comp.to_html(classes='wdsgaia table')],
                            titles=['na', 'System Info', 'A Component Info',
                            'B Component Info', 'C Component Info', 'D Component Info',
                            'E Component Info', 'F Component Info'])

            # Check that max_ra is greater than min_ra. If not, then add 2hrs to min
            if content['min_ra'] and content['max_ra']:
                if not content['max_ra'] > content['min_ra']:
                    content['max_ra'] = content['min_ra'] + 200000
            # Check that max_dec is greater than min_dec. If not, add 10 degress
            if content['min_dec'] and content['max_dec']:
                if not content['max_dec'] > content['min_dec']:
                    content['max_dec'] = content['min_dec'] + 100000
            # Check that min_mag is greater than max_mag. If not, add 3 to min_mag
            if content['min_mag'] and content['max_mag']:
                if not content['min_mag'] > content['max_mag']:
                    content['min_mag'] = content['max_mag'] + 3
            # Check that max_sep is greater than min_sep. If not, add 5 arcseconds
            if content['min_sep'] and content['max_sep']:
                if not content['max_sep'] > content['min_sep']:
                    content['max_sep'] = content['min_sep'] + 5
            # Update session['content']
            session['content'] = content
            # by min RA
            if content['min_ra']:
                data = data[data['WDS_RA'] >= content['min_ra']]
            # By max RA
            if content['max_ra']:
                data = data[data['WDS_RA'] <= content['max_ra']]
            # By min Dec
            if content['min_dec']:
                data = data[data['WDS_Dec'] >= content['min_dec']]
            # By max Dec
            if content['max_dec']:
                data = data[data['WDS_Dec'] <= content['max_dec']]
            # By min mag
            if content['min_mag']:
                data = data[data['gaia_mag_1'] <= content['min_mag']]
            # By max mag
            if content['max_mag']:
                data = data[data['gaia_mag_1'] >= content['max_mag']]
            # by min separation
            if content['min_sep']:
                data = data[data['LSTSEP'] >= content['min_sep']]
            # By max separation
            if content['max_sep']:
                data = data[data['LSTSEP'] <= content['max_sep']]
            # By delta magnitude
            if content['max_delta_mag']:
                data = data[data['delta_mag_GAIA'] <= content['max_delta_mag']]
            # By Number Observations
            if content['nobs']:
                data = data[data['NOBS'] <= content['nobs']]
            # By last observation year
            if content['last_obs']:
                data = data[data['LSTDATE'] <= content['last_obs']]
            # Flash the number of results found
            flash(f'Search returned {len(data)} results.')
            # Save the result to a csv for download later
            # data.to_csv('result.csv', index=False)
            # Info for the Primary component
            a_comp = data.head(20)[['WDSName', 'components', 'NOBS',
                'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA', 'gaia_mag_1', 'delta_mag_GAIA', 'STYPE',
                'NOTES', 'd_pri', 'd_sec', 'px_prob', 'dist_prob', 'PM_prob',
                'binary_prob', 'physical?']]
            # Info for the Secondary component
            b_comp = data.head(20)[['WDSName', 'components', 'NOBS',
                'LSTDATE', 'LSTSEP', 'delta_sep', 'delta_PA','gaia_mag_2', 'delta_mag_GAIA', 'STYPE',
                'NOTES', 'd_pri', 'd_sec', 'px_prob', 'dist_prob', 'PM_prob',
                'binary_prob', 'physical?']]

        # Return a list of tables to be rendered
            return render_template('results.html',
                tables=[a_comp.to_html(classes='wdsgaia table'),
                    b_comp.to_html(classes='wdsgaia table')],
                titles=['na', 'Primary Info', 'Secondary Info']
                )

    return render_template('home.html', form=form)

@app.route('/download', methods=['GET', 'POST'])
def download():
    # Get the query to build a dataset for download
    content = session.get('content')
    # Load the master dataset to build the results from
    data = pd.read_csv('wds_gaia_master.csv', index_col=0)

    # Query by WDS Name
    if content['WDS_name']:
        # Gather the system and components from the master set
        data = data[data['WDSName'] == content['WDS_name']]
        # Buffer object for csv data
        output = StringIO()
        data.to_csv(output)
        # Send the file
        return Response(output.getvalue(),
            mimetype="text/csv",
            headers={"Content-disposition":
            "attachment; filename=results.csv"})

    # Following are parameters for a target discovery query
    # by min RA
    if content['min_ra']:
        data = data[data['WDS_RA'] >= content['min_ra']]
    # By max RA
    if content['max_ra']:
        data = data[data['WDS_RA'] <= content['max_ra']]
    # By min Dec
    if content['min_dec']:
        data = data[data['WDS_Dec'] >= content['min_dec']]
    # By max Dec
    if content['max_dec']:
        data = data[data['WDS_Dec'] <= content['max_dec']]
    # By min mag
    if content['min_mag']:
        data = data[data['gaia_mag_1'] <= content['min_mag']]
    # By max mag
    if content['max_mag']:
        data = data[data['gaia_mag_1'] >= content['max_mag']]
    # by min separation
    if content['min_sep']:
        data = data[data['LSTSEP'] >= content['min_sep']]
    # By max separation
    if content['max_sep']:
        data = data[data['LSTSEP'] <= content['max_sep']]
    # By delta magnitude
    if content['max_delta_mag']:
        data = data[data['delta_mag_GAIA'] <= content['max_delta_mag']]
    # By Number Observations
    if content['nobs']:
        data = data[data['NOBS'] <= content['nobs']]
    # By last observation year
    if content['last_obs']:
        data = data[data['LSTDATE'] <= content['last_obs']]

    output = StringIO()
    data.to_csv(output)

    return Response(output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition":
        "attachment; filename=test.csv"}
    )
    
