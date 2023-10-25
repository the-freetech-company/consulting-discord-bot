from jira import JIRA

jira = JIRA(server='https://the-freetech-company.atlassian.net', basic_auth=('chase@freetech.co', 'ATATT3xFfGF0P6pkfbYIxrxTpR0d4kt-XGboqRjsCDprG9ccanO5B4u0UklRxQ5b3IG-x1BqH0BRTwMQ2KI8TNkzZ6qnc5IYJCGO6IJQ2G56oGti5MTcdAM6PuROVIPQhWWrhWpR1zBfEMZmKF6X7eJjcosZkXeGTmN9fSdEv4gqButMjEk6nyY=EF964A05'))


def updateIssueStatus(issueKey, status):
    issue = jira.issue(issueKey)
    transitions = jira.transitions(issue)
    for t in transitions:
        if t['name'] == status:
            jira.transition_issue(issue, t['id'])
            return True
    return False
