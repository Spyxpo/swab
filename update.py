import time
import git

def update():
    try:
        print('Updating SWAB...')
        git.Git().pull()
        print('Updated successfully.')
        time.sleep(5)
        exit()
    except:
        print('Error updating SWAB.')
        time.sleep(5)
        exit()

update()