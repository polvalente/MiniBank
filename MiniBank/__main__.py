import sys
sys.path = [''] + sys.path
from MiniBank import app
from MiniBank.Config import config

#if argv[1] exists, is will be a filename 
if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "in_memory":
        repo_data = {}
        repo_data['type'] = 'in memory'
    else:
        repo_data = {
                'type':config.db_type,
                'dbname':config.db_name,
                'address':config.db_address,
                'port':config.db_port,
                'user':config.db_user,
                'pass':config.db_pass
                }

    app.run(repo_data)
