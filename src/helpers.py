from flask_login import current_user
from datetime import datetime

from . import db

def show_tasks(time):
    
    """ Shows the tasks to the user by going through the current user's tasks, 
      checking to see if the deadline is within a day, a week or no deadline at all,
      and then adds them to a separate list which is rendered.
    """

    tasks = []
    def sort_tasks_by_priority(e):
            return e.priority

    for task in reversed(current_user.tasks):
        if task.due_date:
            difference_in_time = task.due_date - datetime.now()
            task.due_date = task.due_date.date()
            if time is None:
                tasks.append(task)
            elif time == 7:    
                if difference_in_time.days > 1 and difference_in_time.days <= time:
                    tasks.append(task)
            elif time == 1:
                if difference_in_time.days < time:
                    tasks.append(task)
        else:
            if time is None:
                tasks.append(task)

        tasks.sort(key=sort_tasks_by_priority)

    return tasks