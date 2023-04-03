class Object:
    def __init__(self, name, detail='Default'):
        ''' # config the instance '''
        self.name = name
        self.detail = detail

    def __call__(self, a, b): 
        '''# make the instance callable  ::method  def __call__(): a + b
        instance(1, 2) == 3    return this function like primary by him istanse'''
        print( a + b)

    def __dir__(self):  
        '''  # set default name for class methods  --------
        ::method   dir(*arg)    give back a list of possible methods  '''
        return ['name', 'function']
    
    def __delattr__(self):
        ''' delete an attribute ... take the name in a string format
        if this function is empty can not delete the attributes   '''
        pass

    def __eq__(self, exemple):
        ''' set default attribute for mode to equiparate / confrontate 
        2 instance of this class. isinstance() can support checking if 
         exemple is an istance of the Object class in case of error return false'''
        if isinstance(exemple, Object):
            return self.name == exemple.name
        return False
    def __format__(self, __format_spec):
        
        return 'This is a {0} formatted sting'.format(0, 'DEFAULT' )

    def __getattribute__(self, name):
        ''' get an attribute value'''
        pass 
    
    def __hash__(self):
        ''' set default attribute for wich need to hash value'''
        return hash((self.name, self.detail))

    def __instancecheck__(self, __instance):
        ''' check if the value passed  is instance of this class
        or instancecheck( instance , [ list_of_classes ] )'''
        pass

    def __init_subclass__(cls):
        ''' cls = DEFAULT  this function will be call at the creation of the instance
        children of this class'''
        pass

    def __ne__(self, instance):
        ''' look at the diversity of 2 object or istance of this class
        this is like use:: if x != y:....'''
        pass

    def __new__(cls, iterable):
        ''' create a new instance from this class with same config from
          init file + some else here '''
        lower_iterable = (l.lower() for l in iterable) 
        pass# super().__new__(cls, lower_iterable)
    def __repr__(self):
        ''' return a string but it is not same to the str() method '''
        pass
    def __reduce_ex__(self, __protocol):
        ''' reduce the extencion of the python module for make it compatible
        for client.......?  '''
        pass
    def __subclasscheck__(self, __subclass):
        ''' ask if this self is parent of the subclass '''
        pass
    def __sizeof__(self):
        ''' return the site of the object in bit'''
        pass
    

g = Object('hh')

i = Object('ok')
K = Object('K')
print(isinstance(K, Object))
print(repr(i))