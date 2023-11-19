class _Chatbot:
    def __init__(self) -> None:
        self.__name = 'CHATBOT'
        self.__types = ('QNA', 'CHATGPT')
        self.__types_desc = {
            'QNA': 'Questions & Answers',
            'CHATGPT': 'ChatGPT'
        }
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def types(self) -> tuple:
        return self.__types
    
    @property
    def types_desc(self) -> dict:
        return self.__types_desc
    

class _Emforms:
    def __init__(self) -> None:
        self.__name = 'EMFORMS'
        self.__types = ('JSON', 'MULTIPART')
        self.__types_desc = {
            'JSON': 'Json Body',
            'MULTIPART': 'Multipart Body'
        }
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def types(self) -> tuple:
        return self.__types
    
    @property
    def types_desc(self) -> dict:
        return self.__types_desc
    

class Product:
    chatbot = _Chatbot()
    emforms = _Emforms()

    @staticmethod
    def products():
        return (Product.chatbot.name, Product.emforms.name)
    
    @staticmethod
    def products_model_choices():
        return ((Product.chatbot.name, Product.chatbot.name), (Product.emforms.name, Product.emforms.name))
    
    @staticmethod
    def product_types():
        return Product.chatbot.types + Product.emforms.types
    
    @staticmethod
    def product_types_model_choices():
        choices = []
        types_desc = {**Product.chatbot.types_desc, **Product.emforms.types_desc}
        for type, desc in types_desc.items():
            choices.append((type, desc))
        return tuple(choices)
    
    @staticmethod
    def is_product_type_valid(product, type):
        return (product == Product.chatbot.name and type in Product.chatbot.types) or (product == Product.emforms.name and type in Product.emforms.types)
            