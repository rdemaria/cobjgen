import cobjgen as co

#Named types to generate API with additional methods can be addded

co.set_api_path("./api.so")

class StructA(co.Struct):
    """Fixed size struct

    fa: Double field
    fb: Signed Int64 field with default
    fc: Double array with default  default
    """
    fa: co.Double
    fb: co.Int64 = 3
    fc: co.Double[4] = [1,2,3,4]
    fd: co.Double[6] = 0

    def _set_fielda(self,value):
        """define setter"""
        pass

    def _get_fielde(self):
        """define getter"""
        pass


class StructB(co.Struct):
    """ Structure with flexible array

    fielda: Structure
    fieldb: Array of structure
    fieldc: Flexible size of structure
    """
    fsa: StructA
    fsb: StructA[3]
    fsc: StructA[None]

class StructC(co.Struct):
    """ Structure with flexible nested elements
    """
    fia: StructB
    fib: StructB[3]
    fic: StructB[None]

class UnionA(co.Union):
    _members: (StructA, StructB, StructC)

class Array1(co.Array):
    _element: UnionA
    _shape: 3

class Array2(co.SOA):
    _element: StructA

class Array3(co.SOA):
    _element: StructB

class Array4(co.SOA):
    _element: StructC


class StructE(co.Struct):
    """ Anonymous types not API exported no additional methods

    fielda: anonymous array
    fieldb: anonymous struct
    """
    fielda: co.array(co.Double,3)
    fieldb: co.struct(a=co.Double,b=co.Int64)
    fieldc: co.soa(StructA,2,2)
    fieldd: co.union(StructA,StructB)



