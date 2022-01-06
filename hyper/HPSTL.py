

class Atom:
    def __init__ (self,id,Atom):
        self._id = id
        self._atom = Atom

    def __str__ (self):
        return f"({self._id}#{self._atom})"

class Conj:
    def __init__ (self,left,right):
        self._left = left
        self._right = right

    def __str__ (self):
        return f"({self._left } && {self._right})"



class Disj:
    def __init__ (self,left,right):
        self._left = left
        self._right = right

    def __str__ (self):
        return f"({self._left } || {self._right})"



class Until:
    def __init__ (self,left,right,lbound, rbound):
        self._left = left
        self._right = right
        self._lbound = lbound
        self._rbound = rbound
        
    def __str__ (self):
        return f"({self._left } U[{self._lbound},{self._rbound}] {self._right})"
    

class Release:
    def __init__ (self,left,right,lbound, rbound):
        self._left = left
        self._right = right
        self._lbound = lbound
        self._rbound = rbound
        
    def __str__ (self):
        return f"({self._left } R[{self._lbound},{self._rbound}]s {self._right})"
    

class Diamond:
    def __init__ (self,left,lbound, rbound):
        self._left = left
        self._lbound = lbound
        self._rbound = rbound
        
    def __str__ (self):
        return f"(<>[{self._lbound},{self._rbound}] {self._left})"
    

class Box:
    def __init__ (self,left,lbound, rbound):
        self._left = left
        self._lbound = lbound
        self._rbound = rbound
        
    def __str__ (self):
        return f"(<>[{self._lbound},{self._rbound}] {self._left})"
    


