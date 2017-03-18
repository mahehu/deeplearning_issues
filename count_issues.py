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
    
    GITHUB_TOKEN = 'add yours here'
    
    repos = [('dmlc', 'mxnet'),
             ('fchollet', 'keras'),
             ('tensorflow', 'tensorflow'),
             ('BVLC', 'caffe'),
             #('PaddlePaddle', 'Paddle'),
             ('pytorch', 'pytorch'),
             #('torch', 'torch7'),
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

    for org, repo in repos:

        issues = dict()
            
        for i in gh.iter_repo_issues(org, repo, state='all'):
            year = i.created_at.year
            month = i.created_at.month
            quarter = int(np.ceil(month / 3.0))

            #if year == current_year and quarter == current_quarter:
            #    # Skip current quarter issues as it is not complete.
            #    continue
        
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
        
        order = np.argsort(issues.keys())
        dates    = [issues.keys()[k] for k in order]
        activity = [issues.values()[k] for k in order]
        ax.plot(dates, activity, label = "{}/{}".format(org, repo))
        
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
    plt.show()
