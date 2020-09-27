# Omnifocus-GoogleDocs
Automatically generates agendas on Google Docs from pre-existing Omnifocus Projects. Extracts a series of Projects and Tasks from Omnifocus (Standard)'s local DB, writes them to a Google Doc, formats, and shares the created file with specified users. 

## About
If you're a user of Omnifocus (Standard), you probably already know that it's a pretty robust project management system. Only problem is - it's not easy to export the data out of Omnifocus and into any other program, which makes integration with other systems cumbersome, and difficult. Here we present a quick-and-dirty solution in Python,  which may be customized to suit your needs. 

## Omnifocus Specifics
How information is mapped between Omnifocus & Google Docs: 
- The Pro version of Omnifocus supports direct API access, but the Standard version does not
- This mod is designed for Standard, and roots your local Omnifocus database to fetch information
- Script only pulls project names, and top-level tasks (no sub-tasks, though you can customize)
- In the OmniFocus database structure, the `Task` table holds all task data, including project names

## Setup / Directions
(1) Sign up/into Google's Developer Console: https://console.developers.google.com/

(2) Create a project, and enable Docs and Drive APIs.
- In project settings, for redirect URIs, setting to `localhost` for this purpose
- See tutorial here: https://developers.google.com/docs/api/quickstart/python for more info

(3) Download credentials.json and store in project root folder.

(4) Edit config.py `params` to fit your needs:

- `db_path` = path to your OmniFocus database (usually some variation of `/Users/{user}/Library/...`)
**Note: the path will depend on your OmniFocus version, and whether you downloaded it direct, or through the App Store**

- `projects` = list of project names you want to pull tasks from

- `agenda_title` = desired name of document when you publish agenda to Google Docs
**Note: today's date is automatically appended to the end of any title string**

- `share_with` = list of email address(es) you would like to share the finished agenda with

(5) Run `python3 create_agenda.py` to run through the whole flow, end-to-end.
To further customize text formatting, refer to: https://developers.google.com/docs/api/concepts/structure

(6) Set local cronjob on `create_agenda.py` so it fires daily, weekly, or whatever works best for you. 

## Design Note
I didn't write any sophisticated instance or class methods for this mod, simply because I wanted to make it easy to import freestanding functions and build additional layers (e.g., for Asana users, or other). Mod design has been kept super simple and only uses one top-level folder. 

## Application / Business Use Case
Every Sunday evening, I have been writing out our Team Agenda for our Full Circle-Up meetings, which are held on Monday mornings. Previously, I was doing this manually, and often found myself just copying items from my local OmniFocus to Google Docs. I figured it would be nice to get that time back every Sunday, so I spun up this quick program to automate the generation of our weekly agendas, end-to-end. Hopefully it helps someone else, too!  