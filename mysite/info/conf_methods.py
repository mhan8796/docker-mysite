import configparser
from .DbHandler import DbHandler

# get config information
config = configparser.ConfigParser()
config.read('./config.ini')

confdbUrl = config['confluence_db']['url']
confdbName = config['confluence_db']['db_name']
confdbUsername = config['confluence_db']['username']
confdbPassword = config['confluence_db']['password']
dbh = DbHandler(confdbUrl,confdbUsername,confdbPassword,confdbName)

def throw_admin(spaceId):
    admin_list = []
    # get admin users
    query = '''
    SELECT x.permusername FROM public.spacepermissions x
    WHERE x.permtype = 'SETSPACEPERMISSIONS' 
    AND spaceid = '%s' AND x.permusername IS NOT NULL
    ''' % spaceId
    ret = dbh.doQuery(query)
    for i in ret:
        query = '''
        SELECT LOWER(x.username) FROM public.user_mapping x
        WHERE x.user_key = '%s'
        ''' % i
        ret = dbh.doQuery(query)
        if ret:
        	admin_list.append(ret[0][0])

    # get admin groups
    query = '''
    SELECT x.permgroupname FROM public.spacepermissions x
    WHERE x.permtype = 'SETSPACEPERMISSIONS' 
    AND spaceid = '%s' AND x.permgroupname IS NOT NULL
    ''' % spaceId
    admin_groups = dbh.doQuery(query)
    for admin_group in admin_groups:
        query = '''
        SELECT x.id FROM public.cwd_group x
        WHERE LOWER(x.lower_group_name) = LOWER('{0}')
        '''.format(admin_group[0])
        group_id = dbh.doQuery(query)[0][0]
        print (group_id)
        query = '''
        SELECT x.child_user_id FROM public.cwd_membership x
        WHERE x.parent_id = '{0}'
        '''.format(group_id)
        user_ids = dbh.doQuery(query)
        for user_id in user_ids:
            query = '''
            SELECT LOWER(x.user_name) FROM public.cwd_user x
            WHERE x.id = '{0}'
            '''.format(user_id[0])
            user_name = dbh.doQuery(query)[0][0]
            if user_name not in admin_list:
                admin_list.append(user_name)

    return admin_list

def query_id(spaceId):
    query = '''
    SELECT x.spaceid FROM public.spaces x 
    WHERE x.spaceid = '{0}'
    '''.format(spaceId)
    ret = dbh.doQuery(query)
    return ret

def query_name(spaceName):
    query = '''
    SELECT x.spaceid FROM public.spaces x 
    WHERE LOWER(x.spacename) = LOWER('{0}') 
    '''.format(spaceName)
    ret = dbh.doQuery(query)
    return ret

def query_key(spaceKey):
    query = '''
    SELECT x.spaceid FROM public.spaces x 
    WHERE LOWER(x.spacekey) = LOWER('{0}')
    '''.format(spaceKey)
    ret = dbh.doQuery(query)
    return ret