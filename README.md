# ToDo: A Project Management App
## Video Demo: https://youtu.be/1SM5OvVQWGQ
## Description: 
The project was created after being internally motivated by my regular use of task management apps like Todoist and Notion. I chose the web as the platform because of how vast it really is - allowing users of different platforms - be it Linux, macOS, Windows, iOS, Android or any other user using any other operating system - to access the same web application. 

The project is a task management app allowing the user to create tasks with proper headings, descriptions, deadlines and urgency systems (task priority).

The app has been created using HTML, Bootstrap(CSS and JavaScript) and a little bit of JavaScript for the front-end. I used SQLite as the database. Flask, a Python framework was used to handle the back-end code.

The project I have created is honestly not that surprising or inspiring, but I view it as a stepping stone - a small key to access and develop a greater skill-set through developing other projects of a more advanced and technical nature, after acquiring sufficient knowledge from other online courses. 

With that said, let's start understanding, through a brief summary, what each file is about.

### main.py
This file is what runs the whole app. Running the command 'python .\main.py' in the root of the project runs the server. 

### __init__.py
This initializes the app. Setting the app's secret key, creating the blueprints for 'auth.py' and 'views.py' which are Python files responsible for managing authorization and user content respectively, telling 'flask_login' the default page to revert to if a user is not signed in and lastly, loading the logged in user's data.

### models.py
This stores the structure of the database. The 'Task' table, for example, has an 'id', a primary key to uniquely identify each task. The 'heading' refers to the main text used to describe the task. The 'description' is further explanation of the task, expanding on the 'heading' text to clarify, in detail (if needed), what needs to be done. 'due_date' means when the task is due. 'priority' refers to the urgency of the task; the lower the number, the greater the importance. 'date_of_creation' stores the time when the task was originally created. 'user_id' acts as a foreign key, linking with the 'User' table's 'id' key. 
Moving to the 'User' table, we have the 'id' key, a primary key used to uniquely identify each user in the database. 'username' is a unique name which each user can assign to themselves, with the 'password' acting as protection to block users who do not own the username from accessing said user's data. 'date_created' refers to the time when the user account was created. 'tasks' establishes a one-to-many relationship with the 'Task' table: one user can have many tasks.

### auth.py
This file is responsible for managing everything related to user accounts. So logging in, creating a new account, changing the user's password and deleting the user's account is all managed in this file. 

### views.py
This file is responsible for managing the user's content. In the context of this project, that "user's content" refers to the different tasks the user has created. For example, this file manages the job of creating a task, editing it, deleting it or showing different tasks to the user based on the URL. If 'today' is in the URL, that means load all the tasks from the database that the user created which have a deadline of 1 day or less. If 'upcoming' is in the URL, that means load all the tasks which have a deadline of a week or less later, but greater than 1 day. If 'inbox' is in the URL, that means loading all the tasks of the user, without any time parameter.

### helpers.py
Although it contains only a single function right now (it first had two functions but a simplification of code resulted in that function being removed), I created this file in hopes that, should development continue in the future, I can write functions in this file to reduce repetitive code. The function 'show_tasks()' is responsible for showing the different tasks of the user based on the time parameter set (which is determined by which page is currently open). The functionality has been explained in my text related to 'views.py'.

### /templates (folder)
This folder stores all the HTML files. The folder also contains another folder, called 'includes', which stores some more HTML files, which aren't entire pages, but small parts of the website which cannot be rendered independently. For example, the sidebar, if rendered alone, would be meaningless without other parts of HTML. This folder is essentially to store HTML code that would be repetitive, if written in many HTML files.
