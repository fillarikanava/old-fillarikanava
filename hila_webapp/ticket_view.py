from roundup import instance


def show_tickets():
    returnstring = ""
    
    tracker = instance.open('/projects/shared/roundup-1.4.6/demo')
    db = tracker.open('admin')
    issues = db.issue.list()
    resolved_id = db.status.lookup('resolved')

    for i in issues:
        issue = db.issue.getnode(i)
        if issue.status != resolved_id:
            returnstring += "<br>" + issue.id + "<br>2" + issue
    
    return returnstring
