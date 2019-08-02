import random
import json

class Faker:
    """
        Faker of VNegmas produce load demo data that used for shown at the conference IJCAI.
        .. versionadd:: v0.2.1
            functions produce_offline_demo and load_offline_demo are added
    """
    products = [                
                "Product 1",
                "Product 2",
                "Product 3",
                "Product 4",
                "Product 5",
                "Product 6"
                ]
    factories = [
        "Factory 1",
        "Factory 2",
        "Factory 3",
        "Factory 4",
        "Factory 5",
        "Factory 6"
    ]
    products_factories_produce_data = [
         [random.randint(0, 100) for p in range(6)] for f in range(6)
    ]
    total_step = 100
    activations_level_data = []
    buy_and_sell_data = [[], []]

    @staticmethod
    def get_activations_level(factories=None, total_step=None):
        data = [(i, j, random.randint(0, 0)) 
                        for i in range(len(Faker.factories if factories is None else factories)) 
                        for j in range(Faker.total_step if total_step is None else total_step)
                    ]
        return data

    @ staticmethod
    def get_product_factories_produce(products=None, factories=None):
        return [
                        [ random.randint(0, 10) 
                        for p in (Faker.products if products is None else products)] 
                        for f in (Faker.factories if factories is None else factories)
                        ]

    @staticmethod
    def get_buy_and_sell_data(factories=None, products=None):
        data = {"seller":[
                            [ random.randint(0, 3) 
                            for f in  (Faker.factories if factories is None else factories)] 
                            for p in (Faker.products if products is None else products)
                        ], 
                        "buyer":[
                            [ random.randint(0, 3) 
                            for f in (Faker.factories if factories is None else factories)] 
                            for p in (Faker.products if products is None else products)
                            ]
                        }
        return data

    @ staticmethod
    def get_product_factories_produce_dynamic(products=None, factories=None):
        data = {f: [random.randint(0, 5) 
                        for p in (Faker.products if products is None else products)] 
                        for f in (Faker.factories if factories is None else factories)
                    }
        return data
    
    @staticmethod
    def get_buy_and_sell_data_dynamic(products=None, factories=None):
        factories = Faker.factories if factories is None else factories
        products = Faker.products if products is None else products

        data = {"seller":{
                                            p:[ random.randint(0, 50) 
                                            for f in factories] 
                                            for p in products
                                        },
                        "buyer":{
                                            p:[ random.randint(0, 20) 
                                            for f in factories] 
                                            for p in products
                                }
                        }
        return data
    
    @staticmethod
    def get_activations_level_dynamic(total_step=None, factories=None):
        data = [random.randint(0, 2)
                for i in range(len(Faker.factories if factories is None else factories)) 
            ]
        return data

    def produce_offline_demo(self, file_name="offline_demo.json"):
        """
            Use this function to create a json file obtain the demo information that will be used for shown at the conference IJCAI
            data structure is `[ 
                {"step":1, "agents":[["m_1", "m_2" , "m_3"] , ["my@1_1","greedy@1_2","greedy@2_1"], ["c_1", "c_2", "c_3"]], 
                 "contract_signed":[], "product_produce":{}, "buyer_and_seller":{}
                },
                {"step":2, "agents":[["m_1", "m_2" , "m_3"] , ["my@1_1","greedy@1_2","greedy@2_1"], ["c_1", "c_2", "c_3"]], 
                "contract_signed":[["c_2", "greedy@2_1"], ["c_1", "greedy@2_1"], ["greedy@1_2", "greedy@2_1"], ["my@1_1", "greedy@2_1"], ["m_1", "my@1_1"]], "product_produce":{}, "buyer_and_seller":{}
                },
                {
                }, 
                {   
                }
             ]` 
        """
        total_step = 100
        total_data = []
        max_miners = 10
        max_consumers = 10
        # startswith my or greedy
        max_factories = 15
        current_step_data = {}

        for current_step in range(total_step):
            current_step_data["step"] = current_step + 1
            if current_step == 0:
                current_step_data["agents"] = [[], [], []]
            elif current_step <5:
                current_step_data["contract_signed"] = [[], [], [], []]
            else:
                pass
            total_data.append(current_step_data)
            
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(total_data, f, ensure_ascii=False, indent=4)
    
    @staticmethod
    def load_offline_demo():
        pass

if __name__ == "__main__":
    print(Faker.get_activations_level())