import configparser
import os 

class ManagerChart:
    """
       Class that used for manager the modal, click from setting.
       read the config of mode and charts that can be drawn in the page.
       config file is real_time.

       .. versioninitial:: 0.2.1
          The `config_file_path` paramete is added
       
       :param config_file_path: tell class where the real time config file is stored
    """
    def __init__(self, config_file_path="/home/naodongbanana/Document/vnegmas/vnegmas/backend/src/configs/real_time.ini"):
        self.config_file_path = config_file_path
        self.config = configparser.ConfigParser()
        self.absolute_path = config_file_path
        self.config.read(self.absolute_path )
    
    def register(self, charts=None, modes=None):
        """ Register new charts into config file
        .. versionadded:: 0.2.1
        """
        if charts is not None:
            old_charts = self.config._sections['charts']
            for chart in charts:
                self.config.set("charts", chart, charts[chart])
        if modes is not None:
            old_mode = self.config._sections["mode"]
            for mode in modes:
                self.config.set("mode", mode, modes[mode])
        with open(self.config_file_path , "w+") as f:
            self.config.write(f)
    
    def delete(self):
        pass
    
    def update(self, content):
        """ Update the stats of negmas running mode and charts.
        
        .. versionadded:: 0.2.1
        """
        for section in self.config.sections():
            for _ in self.config[section]:
                if _ in content or  _ == content['realtimemode']:
                    if _ == content['realtimemode']:
                        self.config.set(section, content['realtimemode'], 'True')
                    else:
                        self.config.set(section, _, 'True')
                else:
                    self.config.set(section, _, 'False')
        with open(self.absolute_path, "w+") as f:
            self.config.write(f)
    

if __name__ == "__main__":
    charts = {"contract_signed":"False", "product_produce":"False", "Buyer_and_Seller":"False", "Negmas-Agents_Activation_Level":"True"}
    modes = {"onlineSerial":"True", "onlineFileParallel":"False"}
    mc = ManagerChart("./configs/real_time.ini")
    mc.register(charts, modes)