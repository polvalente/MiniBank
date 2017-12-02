from MiniBank import app
from MiniBank.Config import config
from sys import argv

#if argv[1] exists, is will be a filename 
if len(argv) == 2:
    l = argv[1].split('.')
    if (l[-1] == '.py' or os.path.isdir(argv[1])): 
        print "Won't overwrite .py files or directories"
        exit(1)

    repo_data['filename'] = argv[1]
    repo_data['type'] = 'in memory'
else:
    repo_data{
            'dbname':config.db_name,
            'address':config.db_address,
            'port':config.db_port,
            'user':config.db_user,
            'pass':config.db_pass
            }

app.run(repo_data)
