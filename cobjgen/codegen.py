import os


"""
struct <name> [(<name> <type> <default>),...]
array <name> <type> <length>
soa   <name> <type> <length>
union <name> [ type, ...]

"""

def get_size(typ):
    if typ=='double':
        return 8
    elif typ=='int64':
        return 8
    elif isinstance(typ,tuple):
        if typ[0]=='struct':
            return get_size_struct(typ)
        elif typ[0]=='array':
            return get_size_array(typ)

def struct_gen_methods(top, names, idx, typ):
    if isinstance(typ,tuple):
        if typ[0]=='struct':
            for name,ftyp,default in typ[2]:
                for out in struct_gen_methods(top,names+[name],idx, ftyp):
                    yield out
        elif typ[0]=='array':
            if typ[1] is None:
               iname='size_t i'+str(len(idx))
            else :
               iname='size_t i'+typ[1]
            for out in struct_gen_methods(top,names,idx+[iname], typ[2]):
                yield out
    elif typ=='double':
        yield top,names, idx,'double'
    elif typ=='int64':
        yield top,names, idx,'int64'

def format_method_get(method):
    top,names,idx,typ=method
    fields='_'.join(names)
    indexes=', '.join([f'{top} *ptr']+idx)
    return f"{typ:7} {top}_get_{fields}({indexes});"

def format_method_set(method):
    top,names,idx,typ=method
    fields='_'.join(names)
    indexes=', '.join([f'{top} *ptr']+idx)
    return f"void {top}_set_{fields}({indexes}, {typ} value);"

def write_struct_api(name,basedir,definition):
    apiname=os.path.join(basedir,name+'.h')
    print('struct',apiname)
    #print(definition)
    methods=list(struct_gen_methods(name,[],[],definition))
    for method in methods:
        print(format_method_get(method))
    for method in methods:
        print(format_method_set(method))
    print()


def write_array_api(name,basedir,definition):
    apiname=os.path.join(basedir,name+'.h')
    print('array',apiname,definition)
    print()

def write_union_api(name,basedir,members):
    print("union",name,basedir)
    print(element,length)
    print()

def write_soa_api(name,basedir,element,length):
    print("soa",name,basedir)
    print(element,length)
