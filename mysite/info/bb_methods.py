import configparser
from .DbHandler import DbHandler

# get config information
config = configparser.ConfigParser()
config.read('./config.ini')

bbdbUrl = config['bitbucket_db']['url']
bbdbName = config['bitbucket_db']['db_name']
bbdbUsername = config['bitbucket_db']['username']
bbdbPassword = config['bitbucket_db']['password']
dbh = DbHandler(bbdbUrl,bbdbUsername,bbdbPassword,bbdbName)

# return admin list using given project id
def throw_admin(projectId):
    admin_list = []
    # get admin users
    query = '''
    SELECT x.user_id FROM public.sta_project_permission x 
    WHERE x.project_id = '{0}' AND x.perm_id = 4 AND x.user_id IS NOT NULL
    '''.format(projectId)
    ret = dbh.doQuery(query)
    for i in ret:
        query = '''
        SELECT LOWER(x.name) FROM public.sta_normal_user x
        WHERE x.user_id = '{0}'
        '''.format(i[0])
        ret = dbh.doQuery(query)
        if ret:
        	admin_list.append(ret[0][0])

    # get admin groups
    query = '''
    SELECT x.group_name FROM public.sta_project_permission x 
    WHERE x.project_id = '{0}' AND x.perm_id = 4 AND x.group_name IS NOT NULL
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
    SELECT x.id FROM public.project x 
    WHERE LOWER(x.project_key) = LOWER('{0}')
    '''.format(projectKey)
    ret = dbh.doQuery(query)
    return ret