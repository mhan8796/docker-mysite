import configparser
from .DbHandler import DbHandler

# get config information
config = configparser.ConfigParser()
config.read('./config.ini')

jrdbUrl = config['jira_db']['url']
jrdbName = config['jira_db']['db_name']
jrdbUsername = config['jira_db']['username']
jrdbPassword = config['jira_db']['password']
dbh = DbHandler(jrdbUrl,jrdbUsername,jrdbPassword,jrdbName)

# return admin list
def throw_admin(projectId, projectKey):
    admin_list = []
    # get project lead using projectKey
    query = '''
    SELECT x.lead FROM public.project x 
    WHERE LOWER(x.pkey) = LOWER('{0}')
    '''.format(projectKey)
    ret = dbh.doQuery(query)
    if ret:
        admin_list.append(ret[0][0])

    # get admin users using projectId
    query = '''
    SELECT x.roletypeparameter FROM public.projectroleactor x 
    WHERE x.pid = '{0}' AND x.roletypeparameter IS NOT NULL 
    AND x.roletype = 'atlassian-user-role-actor'
    AND x.projectroleid = 10002
    '''.format(projectId)
    ret = dbh.doQuery(query)
    for i in ret:
        if i[0] not in admin_list:
            admin_list.append(i[0])

    # get admin groups
    query = '''
    SELECT x.roletypeparameter FROM public.projectroleactor x 
    WHERE x.pid = '{0}' AND x.roletypeparameter IS NOT NULL 
    AND x.roletype = 'atlassian-group-role-actor'
    AND x.projectroleid = 10002
    '''.format(projectId)
    groups = dbh.doQuery(query)
    for group in groups:
        query = '''
        SELECT LOWER(x.child_name) FROM public.cwd_membership x 
        WHERE LOWER(x.lower_parent_name) = LOWER('{0}') AND x.child_name IS NOT NULL
        '''.format(group[0])
        admins_from_group = dbh.doQuery(query)
        for admin in admins_from_group:
            if admin[0] not in admin_list:
                admin_list.append(admin[0])
                 
    return admin_list

# return project id using given project key
def query_key(projectKey):
    query = '''
    SELECT x.project_id FROM public.project_key x 
    WHERE LOWER(x.project_key) = LOWER('{0}')
    '''.format(projectKey)
    ret = dbh.doQuery(query)
    return ret