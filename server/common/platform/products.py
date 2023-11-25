class _Chatbot:
    def __init__(self) -> None:
        self.__name = 'CHATBOT'
        self.__types = ('QNA', 'AI')
        self.__types_desc = {
            'QNA': 'Questions & Answers',
            'AI': 'AI Language Model'
        }
        self.__engines = ('C-QnA', 'OpenAI-ChatGPT', 'Google-Bard')
        self.__models = {
            'C-QnA': ('C-QnA'),
            'OpenAI-ChatGPT': ('gpt-3.5-turbo'),
            'Google-Bard': ('Palm-2')
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
    
    @property
    def engines(self) -> tuple:
        return self.__engines
    
    @property
    def models(self) -> dict:
        return self.__models

    @property
    def types_model_choices(self) -> tuple:
        choices = []
        for type, desc in self.types_desc.items():
            choices.append((type, desc))
        return tuple(choices)
    
    @property
    def engines_model_choices(self) -> tuple:
        choices = []
        for engine in self.engines:
            choices.append((engine, engine))
        return tuple(choices)

    @property
    def models_model_choices(self) -> tuple:
        models = []
        for engine in self.engines:
            models.append(self.models.get(engine))
        choices = [(model, model) for model in models]
        return tuple(choices)


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
    
    @property
    def types_model_choices(self) -> tuple:
        choices = []
        for type, desc in self.types_desc.items():
            choices.append((type, desc))
        return tuple(choices)



    

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
        return Product.chatbot.types_model_choices + Product.emforms.types_model_choices
    
    @staticmethod
    def is_product_type_valid(product, type):
        return (product == Product.chatbot.name and type in Product.chatbot.types) or (product == Product.emforms.name and type in Product.emforms.types)
            