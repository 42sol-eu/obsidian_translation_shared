from pathlib import Path                 #!md|[docs](https://docs.python.org/3/library/pathlib.html#Path)
from toml import *                       #!md|[docs](https://github.com/uiri/toml)

from logging import INFO,DEBUG           #!md|[docs](https://docs.python.org/3/library/logging.html?highlight=logging#module-logging)
from logging import basicConfig as config_logging
from logging import getLogger as Logger
import chevron  
#OLD              #!md|[docs](https://github.com/defunkt/pystache)

config_logging(level=INFO, filename='tembase_split.log',  
 format='%(asctime)s;%(name)s;%(levelname)s;%(message)s;[file;line]',  
 datefmt='%Y-%m-%d;CW%W;%H:%M:%S')  

app  = Logger('app.process')  
test = Logger('app.test')  

debug = False

test.info(f'"\nSTART\n"')  
app.info('started')

class Parameters:
    config_file_path= 'project_example.toml'


    def __init__(self):
        app.info('Parameters created')
        self.load(x_local=True)


    def load(self, x_config_file_path='', x_local=False):
        """
            load parameters from config
        """

        if x_config_file_path == '':
            x_config_file_path = Parameters.config_file_path
        
        script_path = Path(__file__).parent
        test.debug(script_path)
        config_file_path = Path(x_config_file_path)
        if x_local:
            config_file_path = script_path / x_config_file_path

        self.data = {}
        if config_file_path.exists():
            with open(config_file_path, 'r') as toml_file:
                toml_string = toml_file.read()
                toml_data   = loads(toml_string)
                if debug: print(toml_data)
                self.data = toml_data

        if self.data != {}:
            app.info('Parameters loaded successfull')
            
            active_section = 'setup'
            if active_section in self.data.keys():
                if 'language' in self.data[active_section].keys():
                    setattr(self, 'language', self.data[active_section]['language'])
                if 'project_path' in self.data[active_section].keys():
                    setattr(self, 'project_path', self.data[active_section]['project_path'])

            active_section= 'files'
            if active_section in self.data.keys():
                if 'termbase' in self.data[active_section].keys():
                    setattr(self, 'termbase_path', chevron.render(self.data[active_section]['termbase'], {'project_path': self.project_path,'language':self.language}))
            
        else:
            app.error('NO Parameters found!')

