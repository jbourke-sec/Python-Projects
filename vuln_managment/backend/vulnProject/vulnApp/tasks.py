from celery import Celery
from celery import app
#imports needed for the functions
app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task(name='vulnApp.tasks.update')
def main():
    from .models import CveEntry
    CveEntry.main()