class Requests(object):
    def __init__(self, name, customer, quantity, totalAudPrice, totalOtherPrice, otherCurrency, status, traveller, country):
        self._name  = name
        self._customer = customer
        self._totalAudPrice = totalAudPrice
        self._totalOtherPrice = totalOtherPrice
        self._quantity  = quantity
        self._otherCurrency = otherCurrency
        self._status = status
        #a boolean value 0 = pending, 1 = accepted
        #pending when no traveller has selected or when a traveller has offered help but the customer has not accepted it in their inbox
        self._traveller = traveller
        #either be a username or 0
        self._country = country
    
    @property
    def name(self):
        return self._name
    
    @property
    def customer(self):
        return self._customer
    
    @property
    def totalAudPrice(self):
        return self._totalAudPrice
            
    @property
    def quantity(self):
        return self._quantity  
    
    @property
    def totalOtherPrice(self):
        return self._totalOtherPrice    
        
    @property
    def country(self):
        return self._country     

'''for testing  
    def __str__(self):
        return f'request by: {self._customer}, {self._quantity},  {self._name}, {self._totalAudPrice}, {self._totalOtherPrice}' '''

