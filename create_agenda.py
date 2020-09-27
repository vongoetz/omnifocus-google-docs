from datetime import date

# Import local mods
from omni import get_omnifocus_tasks
from gdocs import docs_authenticate
from config import params
import json
import os

def agenda_title():
    today = date.today()
    formatted = today.strftime("%m/%d/%y")
    agenda_title = params['agenda_title'] + ' ' + formatted
    return agenda_title

def build_agenda_body(task_data):
    requests = []
    cur_index = 1
    for each in task_data:
        # First, format projects:
        project_name = each.get('project')
        start_index, end_index = calc_indices(cur_index, project_name)
        print(project_name, start_index, end_index)

        project_text = {
            'insertText': {
                'location': {
                    'index': start_index,
                },
                # Important: Insert line break AFTER each item to create new paragraph
                'text': project_name + '\n'
            }
        }
        requests.append(project_text)

        project_formatting = {
            'updateParagraphStyle': {
                'range': {
                    'startIndex': start_index,
                    'endIndex':  end_index
                },
                'paragraphStyle': {
                    'namedStyleType': 'HEADING_1',
                    'spaceAbove': {
                        'magnitude': 10.0,
                        'unit': 'PT'
                    },
                    'spaceBelow': {
                        'magnitude': 10.0,
                        'unit': 'PT'
                    }
                },
                'fields': 'namedStyleType,spaceAbove,spaceBelow'
            }
        }
        requests.append(project_formatting)
        cur_index = end_index

        # If there are sub-task items, loop through them here
        if each.get('tasks') != None:
            tasks = each.get('tasks')
            for task in tasks:
                task_name = task.get('task')
                start_index, end_index = calc_indices(cur_index, task_name)

                task_text = {
                'insertText': {
                    'location': {
                        'index': start_index,
                    },
                    # Important: Insert line break AFTER each item to create new paragraph
                    'text': task_name + '\n'
                    }}
                print("Task is located at {}, {}.".format(start_index, end_index))
                requests.append(task_text)

                bullets = {
                'createParagraphBullets': {
                    'range': {
                        'startIndex': start_index,
                        'endIndex':  end_index
                    },
                    'bulletPreset': 'BULLET_ARROW_DIAMOND_DISC',
                    }
                }
                print("Bullets created at {}, {}.".format(start_index, end_index))
                requests.append(bullets)
                # Update index for loop
                cur_index = end_index
    
    return requests

def calc_indices(cur_index, string):
    str_len = len(string)
    start_index = cur_index
    end_index = cur_index + str_len + 1
    # Add one because of line break
    return start_index, end_index

def create_weekly_agenda(service):
    # Execute creation of new Google Document
    return service.documents().create(body={'title': agenda_title()}).execute()

def write_weekly_agenda(task_data, document_id, service):
    # Update created Google Document with text content, formatting
    requests = build_agenda_body(task_data)
    return service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()

def grant_permissions_to_file(file_id, service, role):
    def callback(request_id, response, exception):
        if exception:
            # Handle error
            print(exception)
        else:
            print("Permission Id: %s" % response.get('id'))

    batch = service.new_batch_http_request(callback=callback)

    share_list = params['share_with']
    for email in share_list:
        user_permission = {
            'type': 'user',
            'role': role,
            'emailAddress': email
        }
        batch.add(service.permissions().create(
                fileId=file_id,
                body=user_permission,
                fields='id',
        ))
    batch.execute()
    return batch


def main():
    # First, get tasks from Omnifocus local DB
    task_data = get_omnifocus_tasks()

    # Then, authenticate to Google Docs, Google Drive
    gdocs_service, gdrive_service = docs_authenticate()

    # Create the agenda on Google Docs
    agenda = create_weekly_agenda(gdocs_service)
    # Grab the document ID
    document_id = agenda.get('documentId')

    # Insert agenda text
    write_weekly_agenda(task_data, document_id, gdocs_service)

    # Finally, adjust permissions on the document by ID (Google Drive API)
    grant_permissions_to_file(document_id, gdrive_service, 'writer')
    print("Agenda shared with %s" %params['share_with'])


if __name__ == "__main__":
    main()