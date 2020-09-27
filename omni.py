import os
import sqlite3
from config import params
from datetime import date, timedelta

def get_omnifocus_tasks():
    # Connect to the database locally stored
    db_path = params['db_path']

    # Create connection to local Omnifocus DB
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Get projects to extract from Omnifocus
    projects = params['projects']
    
    final_data = []
    for project in projects: 
        result = get_project_identifier(c, project)

        # Grab project_id from tuple
        project_id = result[0]

        # Calculate end of week
        eow = calculate_eow()

        # Now, look for all tasks that are children of the project_id
        # Where parent == project_id; only top-level tasks, no sub-items
        children = get_all_project_tasks(c, project_id, eow)

        # Create list of dicts of task information
        tasks = []
        for child in children: 
            task = {
                'task': child[0]
            }
            tasks.append(task)
        
        # Finally, create final data for each project
        project_data = {
            'project': project,
            'tasks': tasks
        }

        final_data.append(project_data)
    
    return final_data

def calculate_eow():
    """Calculates end of this week"""
    now = date.today()
    eow = now + timedelta(days=5)
    return eow

def get_project_identifier(c, project_name):
    t = (project_name,)
    # Query pulls all tasks where the project id is the same as the task id; means it's a project
    c.execute('SELECT persistentIdentifier FROM Task WHERE name=? AND containingProjectInfo = persistentIdentifier', t)
    result = c.fetchone()
    return result

def get_all_project_tasks(c, project_id, eow):
    t = (eow, project_id, project_id)
    # Build query for tasks NOT completed AND the due date is within one work week AND the task is not a project listing (it is a child item) AND the parent == project_id (meaning, it is a top level task only with no sub-items)
    c.execute('SELECT name, dateDue, parent, containingProjectInfo FROM Task WHERE dateCompleted IS NULL AND dateDue <= ? AND containingProjectInfo=? AND parent = ? AND containingProjectInfo != persistentIdentifier', t)
    results = c.fetchall()
    return results