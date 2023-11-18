class Product:
    CHATBOT = 'CHATBOT'
    EMFORMS = 'EMFORMS'

    @staticmethod
    def products():
        return (Product.CHATBOT, Product.EMFORMS)
    
    @staticmethod
    def products_model_choices():
        return ((Product.CHATBOT, Product.CHATBOT), (Product.EMFORMS, Product.EMFORMS))