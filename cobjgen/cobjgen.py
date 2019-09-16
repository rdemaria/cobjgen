"""

Named type defined by subclassing base class.
Base class cannot be instantiate.

Wnen a class is defined the API is written.

"""
import os

from .codegen import write_struct_api

_apifn='.'

def set_api_path(filename):
    _apifn=filename

def get_apidir():
    return os.path.dirname(_apifn)


### Utils

def _to_abs(el):
    if hasattr(el,'_to_abs'):
        return el._to_abs()
    else:
        return el

class MetaGeneric(type):
    def __getitem__(cls,shape):
        return mkarray(None,cls,shape)
    def __repr__(cls):
        return f"<{cls.__name__}>"

### Struct
def mkstruct(name,fields,defaults):
    """make structure"""
    afields=[(k,_to_abs(v),defaults.get(k)) for k,v in fields.items()]
    return "struct",name,afields

def struct(**fields):
    """make anonynous structure"""
    return "struct",None,[(k,_to_abs(v),None) for k,v in fields.items()]

class MetaStruct(MetaGeneric):
    def __new__(cls, clsname, bases, dct):
        if len(bases)>0: #is subclass of struct
            #print(f"Struct `{clsname}` bases: ",bases)
            #print(f"Struct `{clsname}` dct: ",dct)
            try:
                ann=dct['__annotations__']
            except KeyError:
                msg=f"Struct `{clsname}` does not have annotation"
                raise TypeError(msg)
            defaults={}
            for k in ann:
               if k in dct:
                 defaults[k]=dct[k]
                 del dct[k]
            dct['_fields']=ann
            dct['_defaults']=defaults
            newcls=type.__new__(cls, clsname, bases, dct)
            apidir=get_apidir()
            if apidir is not None:
               write_struct_api(clsname,apidir,newcls._to_abs())
            return newcls
        else:
            return type.__new__(cls, clsname, bases, dct)
    def _to_abs(cls):
        return mkstruct(cls.__name__,cls._fields,cls._defaults)

class Struct(metaclass=MetaStruct):
    pass


### Array

class MetaArray(type):
    def __new__(cls, clsname, bases, dct):
        if len(bases)>0: #is subclass of struct
            #print(f"Struct `{clsname}` bases: ",bases)
            #print(f"Struct `{clsname}` dct: ",dct)
            try:
                ann=dct['__annotations__']
                eltype=ann['_element']
                shape=ann.get('_shape')
            except KeyError:
                msg=f"Array `{clsname}` does not have element type"
                raise TypeError(msg)
        return super().__new__(cls, clsname, bases, dct)
    def _to_abs(cls):
        ann=cls.__annotations__
        return mkarray(cls.__name__,ann['_element'],ann['_shape'])


class Array(metaclass=MetaArray):
    pass

def mkarray(name,element,shape):
    element=_to_abs(element)
    if isinstance(shape,tuple):
        if len(shape)>1:
            return 'array',name,mkarray(None,element,shape[1:]),shape[0]
        else:
            return 'array',name,element,shape[0]
    else:
        return 'array',name,element,shape

def array(element,*shape):
    return mkarray(None,element,shape)


### SOA
def mksoa(name,element,shape):
    from collections import OrderedDict
    element=_to_abs(element)
    if element[0]!='struct':
        raise TypeError("SOA not from struct")
    fields=OrderedDict()
    defaults={}
    for k,v,d in element[2]:
        fields[k]=array(None,v,shape)
        defaults[k]=d
    return mkstruct(name,fields,defaults)

def soa(element,*shape):
    """make anonynous structure"""
    return mksoa(None,element,shape)

class MetaSoa(type):
    def __new__(cls, clsname, bases, dct):
        if len(bases)>0: #is subclass of struct
            #print(f"Struct `{clsname}` bases: ",bases)
            #print(f"Struct `{clsname}` dct: ",dct)
            try:
                ann=dct['__annotations__']
                eltype=ann['_element']
                shape=ann.get('_shape')
            except KeyError:
                msg=f"Array `{clsname}` does not have element type"
                raise TypeError(msg)
        return super().__new__(cls, clsname, bases, dct)
    def _to_abs(cls):
        ann=cls.__annotations__
        return mksoa(cls.__name__,ann['_element'],ann['_shape'])

class SOA(metaclass=MetaSoa):
    pass


### Union
def mkunion(name,members):
    """make anonynous structure"""
    return 'union',name,members

def union(*members):
    """make anonynous structure"""
    return mkunion(None,members)

class Union(metaclass=MetaGeneric):
    pass

### Scalars

class Double(metaclass=MetaGeneric):
    @classmethod
    def _to_abs(cls):
        return 'double'

class Int64(metaclass=MetaGeneric):
    @classmethod
    def _to_abs(cls):
        return 'int64'

### List and Dict...

class List(metaclass=MetaGeneric):
    pass

class Dict(metaclass=MetaGeneric):
    pass






