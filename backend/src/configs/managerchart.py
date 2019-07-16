import configparser
import os 

class ManagerChart:
    def __init__(self, configFilePath):
        self.configFilePath = configFilePath
        self.config = configparser.ConfigParser()
        self.absolute_path = os.path.dirname(__file__) + configFilePath
        self.config.read(os.path.join(os.path.dirname(__file__) + configFilePath))
    
    def register(self, charts=None, modes=None):
        if charts is not None:
            old_charts = self.config._sections['charts']
            for chart in charts:
                self.config.set("charts", chart, charts[chart])
        if modes is not None:
            old_mode = self.config._sections["mode"]
            for mode in modes:
                self.config.set("mode", mode, modes[mode])
        with open(self.configFilePath , "w+") as f:
            self.config.write(f)
    
    def delete(self):
        pass
    
    def update(self, content):
        print(content)
        for section in self.config.sections():
            for _ in self.config[section]:
                if _ in content or  _ == content['realtimemode']:
                    print(f'key {_}')
                    print('test')
                    if _ == content['realtimemode']:
                        self.config.set(section, content['realtimemode'], 'True')
                    else:
                        self.config.set(section, _, 'True')
                else:
                    self.config.set(section, _, 'False')
        print(f"befor write{ self.config._sections}")
        with open(self.absolute_path, "w+") as f:
            self.config.write(f)
    

if __name__ == "__main__":
    charts = {"contract_signed":"False", "product_produce":"False", "Buyer_and_Seller":"False", "Negmas-Agents_Activation_Level":"True"}
    modes = {"onlineSerial":"True", "onlineFileParallel":"False"}
    mc = ManagerChart("./configs/real_time.ini")
    mc.register(charts, modes)