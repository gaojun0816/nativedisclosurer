
class Invokee:
    def __init__(self, method):
        self.cls_name = method.cls.name if method.cls is not None else None
        self.desc = method.cls.desc if method.cls is not None else None
        self.method_name = method.name
        self.signature = method.signature
        self._static = method.static

    def __str__(self):
        s = f'{self.cls_name}, {self.method_name}, {self.signature}, {self._static}'
        if self.desc:
            s += f', {self.desc}'
        return s


class Record:
    # global records, indexed by the address of corresponding JNI function pointer
    RECORDS = dict()

    def __init__(self, cls_name, method_name, signature, func_ptr, symbol_name,
             static_method=None, obfuscated=None, static_export=False):
        self.cls = cls_name
        self.method_name = method_name
        self.signature = signature
        self.func_ptr = func_ptr
        self.symbol_name = symbol_name
        self.static_method = static_method
        self.obfuscated = obfuscated
        self.static_export = static_export
        self._invokees = None # list of method invoked by current native method
        Record.RECORDS.update({func_ptr: self}) # add itself to global record

    def add_invokee(self, param):
        """Add the Java invokee method information
        The invokee is a Java method invoked by current native function.

        Args:
        *param: should be either an instance of class Invokee or 3 strings
                describing invokee's class name, method name and the signature
                of the method.
        """
        invokee = None
        if isinstance(param, Invokee):
            invokee = param
        else:
            invokee = Invokee(param)
        if self._invokees is None:
            self._invokees = list()
        self._invokees.append(invokee)

    def is_invoker(self):
        return self._invokees is not None

    def get_num_invokees(self):
        num = 0
        if self._invokees is not None:
            num = len(self._invokees)
        return num

    def __str__(self):
        result = ''
        invoker = f'{self.cls}, {self.method_name}, {self.signature}, {self.symbol_name}, {self.static_export}'
        if self._invokees is None:
            result = invoker
        else:
            for invokee in self._invokees:
                result += invoker + ', ' + str(invokee) + '\n'
        return result.strip()


class RecordNotFoundError(Exception):
    pass

