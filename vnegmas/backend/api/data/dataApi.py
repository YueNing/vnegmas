from typing import Union

class   NegmasDataBridge:
    """
        class used between Negmass and Data,
        :param receive_data_type: For online file use a class monitor to detect and receive data from NEGMAS,
                                                                For online memory `serial mode` receive data from a world call back function of NEGMAS
                                                                For online memory `parallel` receive data from api of NEGMAS (still in development)
                                                                For offline receive data from a simple analyse Class
        :param data: the data that receive form NEGMAS
    """
    def __init__(self,  receive_data_type=None):
        self.data = {}
        self.receive_data_type = receive_data_type

    def get_data(self, tp: Union[st, list]=None):
        """
            get the data from negmas
            .. versionadd:: v0.2.1
                the tp paramters is added
            
            : param tp: type of data that you want to get, 
        """
        if tp is not None:
            if type(tp) is str:
                self.setup_data(tp)
            elif type(tp) is list:
                self.setup_data_from_list(tp)
            return self.selected_data

    def setup_data_from_list(self, tp: "['breach', 'total_market_size']"=None):
        """
            The data that receive from NEGMAS is list, perhaps need to process some data, so separate this with just one type of data
            
            .. versionadd:: v0.2.1
                the parameter tp is added
            :param tp: data type of list

        """
        self.data_type  = type
        self.selected_data =  {t:self.data[t] for t in self.data_type}
    
    def setup_data(self, tp: 'breach'=None):
        """
            .. versionadd:: v0.2.1
                the parameter tp is added
            :param tp: one data type of str
        """
        self.data_type = type
        self.selected_data = self.data[self.data_type]
    
    def update_data(self, data: dict = None, mode: str="full"):
        """
            .. versionadd:: v0.2.1
                the data and mode paramters are added
            
            :param data: the data receive from NEGMAS that need to update to the cls
            :param mode: the mode of update data, full or increment
                                            full means, every step receive full data from NEGMAS
                                            increment means, every step increment receive data from NEGMAS 
        """
        if data is not None:
            if mode == 'full':
                self.data = data
            if mode == 'increment':
                for data_type, data_value in data.items():
                    if data_type in self.data:
                        self.data[data_type] += data_value
                    else:
                        self.data[data_type] = data_value


class DataVNegmasBridge:
    """
        Class used for combination of Data and VNegmas
        .. versionadd:: v0.2.1
            functions produce, register and __init__ are added,
    """
    def __init__(self):
        pass
    
    def register(self,  
                    data:dict =None, 
                    data_title: str=None,
                    chart_type: str="Bar",
                    processFunc = None
                ):
        """
            used for register new charts type that defined by data analyser, for example, use Bar to show the average of breach of NEGMAS
            .. versionadd:: v0.2.1
                parameters data, data_title, chart_type, processFunc are added
            
            : param data: the data received form NEGMAS that needed to process with processFunc, type dict
            : data_title: title of data, used shown at the charts in website, such as  `average`, mainly describe the function of processFunc 
        """
        self.data = data
        self.data_title = data_title
        self.chart_type = chart_type
        self.processFunc = processFunc

    def produce(self):
        """
            use this function to produce the data from NEGMAS with processFunc, and finally return data that will be used by pyecharts
            .. versionadd:: v0.2.1

        """
        return {data_type:self.processFunc(data_value) for data_type, data_value in self.data.items()}