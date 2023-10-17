from jira import JIRA

jira = JIRA(server='https://the-freetech-company.atlassian.net', basic_auth=('chase@freetech.co', 'ATATT3xFfGF0nkLWP6HWa7Kk7sT5MwGmSHgIcijZnAF7prSTHH-FgziGF_WNeBecuHqGAELGQRwpTFLFU3q-hhxgKb-QfdwhjwzNhq0EprkUEXHiti4NhrWCTcWVs8sCY8cW46PwqZLwbVMvfiU04YmlR9uzk45mqdHuImzpKtI5EWGseVmrjDI=E2F9EEE2'))


def updateIssueStatus(issueKey, status):
    issue = jira.issue(issueKey)
    transitions = jira.transitions(issue)
    for t in transitions:
        if t['name'] == status:
            jira.transition_issue(issue, t['id'])
            return True
    return False
