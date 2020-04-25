class Products(object): 
    def __init__(self, name, link, country, category, audPrice, quantity, otherPrice, otherCurrency, customer, image): 
        self._name = name
        self._link = link
        self._country = country
        self._category = category
        self._audPrice = audPrice
        self._otherPrice = otherPrice
        self._quantity = quantity
        self._otherCurrency = otherCurrency
        self._customer = customer
        self._image = image

    @property
    def name(self):
        return self._name
        
    @property
    def link(self):
        return self._link
        
    @property
    def country(self):
        return self._country
        
    @property
    def category(self):
        return self._category
       
    @property
    def audPrice(self):
        return self._audPrice
        
    @property
    def quantity(self):
        return self._quantity
        
    @property
    def otherPrice(self):
        return self._otherPrice
    
    @property
    def otherCurrency(self):
        return self._otherCurrency
        
    @property
    def customer(self):
        return self._customer
        
    @property
    def image(self):
        return self._image
'''for testing        
    def __str__(self):
        return f'Product: {self._name}, {self._link}, {self._country}, {self._category}, {self._audPrice}, {self._quantity}, {self._otherPrice}, {self._otherCurrency}' '''
