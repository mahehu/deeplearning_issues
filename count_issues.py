#!/usr/bin/env python

from __future__ import print_function
import github3
import json
import os.path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np

if __name__ == "__main__":

    GITHUB_TOKEN = 'e5151b6f7059ebb9628018024f096c8330ff646d'
    
    repos = [('dmlc', 'mxnet'),
             ('fchollet', 'keras'),
             ('tensorflow', 'tensorflow'),
             ('BVLC', 'caffe'),
             #('PaddlePaddle', 'Paddle'),
             ('pytorch', 'pytorch'),
             ('vlfeat', 'matconvnet'),
             ('torch', 'torch7')
             #('deeplearning4j', 'deeplearning4j'),
             #('Microsoft', 'CNTK'),
             #('Theano', 'Theano')
             ]
            
    gh = github3.login(token=GITHUB_TOKEN)

    current_year  = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    current_quarter = np.ceil(current_month / 3.0)
    
    years = mdates.YearLocator()   # every year
    months = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')

    fig, ax = plt.subplots()

    # Store numbers of issues in the current quarter here
    current_issues = dict()

    for org, repo in repos:

        issues = dict()
            
        for i in gh.iter_repo_issues(org, repo, state='all'):
            year = i.created_at.year
            month = i.created_at.month
            quarter = int(np.ceil(month / 3.0))
            
            if year == 2014:
                break
            
            key = datetime.datetime(year, 3*quarter, 01).toordinal()
            
            if issues.has_key(key):
                issues[key] += 1
                print("{}/{}: collecting issues for Q{}/{}: {}...".format(org,
                      repo, quarter, year, issues[key]), end = "\r")
            else:
                issues[key] = 1
                print("\n{}/{}: collecting issues for Q{}/{}: {}...".format(org, 
                      repo, quarter, year, issues[key]), end = "\r")

            if year == current_year and quarter == current_quarter:
                # Store number of issues this quarter
                current_issues[org + "/" + repo] = issues[key]
                
        order = np.argsort(issues.keys())
        dates    = [issues.keys()[k] for k in order]
        activity = [issues.values()[k] for k in order]
        ax.plot(dates, activity, label = "{}/{}".format(org, repo), linewidth = 2)
        
        # format the ticks
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.xaxis.set_minor_locator(months)

    plt.legend(loc = "best")
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.grid(True)
    
    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()
    plt.ylabel('Quarterly Issues')
    plt.title("Graph updated %s" % datetime.datetime.now().strftime("%B %d, %Y"))
    plt.savefig("deeplearning_issues.pdf", bbox_inches = "tight")
    plt.savefig("deeplearning_issues.png", bbox_inches = "tight")
    
    # List current situation:
    print("\n" + "-" * 20)
    print("Share of issues:")
    
    total_curr_issues = np.sum(current_issues.values())
    for key in current_issues.keys():
        print("{:21} {:4.1f} %".format(key, 100.0 * current_issues[key] / 
             total_curr_issues))
    
    plt.show()

