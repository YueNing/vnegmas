import configparser

def get_config(filepath):
    config = configparser.ConfigParser()
    config.read(filepath)
    # print(config._sections['system_general'])
    def remove_character(data):
        if '(' and ')' in data: 
            return tuple(data.replace(" ", "").replace('(', '').replace(')', '').split(','))
        return data
    for section in config._sections:
        for key in config._sections[section]:
            # import pdb; pdb.set_trace()
            config._sections[section][key] = remove_character(config._sections[section][key])
    # import pdb; pdb.set_trace()
    return config

if __name__ == "__main__":
    get_config('./config.ini')