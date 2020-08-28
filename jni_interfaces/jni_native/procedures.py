import archinfo
from ..common import JNIProcedureBase as JPB
from ..common import JNIEnvMissingError
from ..record import Record


class GetClass(JPB):
    def run(self, env_ptr, cls_name_ptr):
        cls_name = self.load_string_from_memory(cls_name_ptr)
        return self.create_java_class(cls_name)


class DefineClass(GetClass):
    pass


class FindClass(GetClass):
    pass


class NewRef(JPB):
    def run(self, env_ptr, obj_ptr):
        return obj_ptr


class NewGlobalRef(NewRef):
    pass


class NewLocalRef(NewRef):
    pass


class AllocObject(NewRef):
    pass


class NewObject(NewRef):
    pass


class NewObjectV(NewRef):
    pass


class NewObjectA(NewRef):
    pass


class GetObjectClass(JPB):
    def run(self, env, obj_ptr):
        obj = self.get_ref(obj_ptr)
        if obj is None:
            desc = 'jclass obtained via "GetObjectClass" and cannot be parsed'
            return self.create_java_class(None, desc=desc)
        else:
            return obj_ptr


class GetMethodBase(JPB):
    def run(self, env, cls_ptr, method_name_ptr, sig_ptr):
        cls = self.get_ref(cls_ptr)
        method_name = self.load_string_from_memory(method_name_ptr)
        signature = self.load_string_from_memory(sig_ptr)
        return self.create_java_method_ID(cls, method_name,
                signature, self.is_static())

    def is_static(self):
        raise NotImplementedError('"is_static" need to be implemented!')


class GetStaticMethodID(GetMethodBase):
    def is_static(self):
        return True


class GetMethodID(GetMethodBase):
    def is_static(self):
        return False


class GetFieldID(JPB):
    def run(self, env_ptr, cls_ptr, field_name_ptr, sig_ptr):
        cls = self.get_ref(cls_ptr)
        name = self.load_string_from_memory(field_name_ptr)
        signature = self.load_string_from_memory(sig_ptr)
        return self.create_java_field_ID(cls, name, signature)


class GetStaticFieldID(GetFieldID):
    pass


class GetObjectField(JPB):
    def run(self, env_ptr, _, field_ptr):
        field = self.get_ref(field_ptr)
        return self.create_java_class(field.ftype.strip('L;').replace('/', '.'),
                                      init=True)


class GetStaticObjectField(GetObjectField):
    pass


class CallMethodBase(JPB):
    def run(self, env, _, method_ptr):
        method = self.get_ref(method_ptr)
        record = self.get_current_record()
        record.add_invokee(method)
        return_value = self.get_return_value(method)
        if return_value:
            return return_value

    def get_current_record(self):
        func_ptr = self.state.globals.get('func_ptr')
        return Record.RECORDS.get(func_ptr)

    def get_return_value(self, method):
        raise NotImplementedError('Extending CallMethodBase without implement get_return_value!')


class CallPrimaryMethod(CallMethodBase):
    def get_return_value(self, method):
        return self.state.solver.BVS('primary_value', self.arch.bits)

class CallBooleanMethod(CallPrimaryMethod):
    pass


class CallBooleanMethodV(CallPrimaryMethod):
    pass


class CallBooleanMethodA(CallPrimaryMethod):
    pass


class CallByteMethod(CallPrimaryMethod):
    pass


class CallByteMethodV(CallPrimaryMethod):
    pass


class CallByteMethodA(CallPrimaryMethod):
    pass


class CallCharMethod(CallPrimaryMethod):
    pass


class CallCharMethodV(CallPrimaryMethod):
    pass


class CallCharMethodA(CallPrimaryMethod):
    pass


class CallShortMethod(CallPrimaryMethod):
    pass


class CallShortMethodV(CallPrimaryMethod):
    pass


class CallShortMethodA(CallPrimaryMethod):
    pass


class CallIntMethod(CallPrimaryMethod):
    pass


class CallIntMethodV(CallPrimaryMethod):
    pass


class CallIntMethodA(CallPrimaryMethod):
    pass


class CallLongMethod(CallPrimaryMethod):
    pass


class CallLongMethodV(CallPrimaryMethod):
    pass


class CallLongMethodA(CallPrimaryMethod):
    pass


class CallFloatMethod(CallPrimaryMethod):
    pass


class CallFloatMethodV(CallPrimaryMethod):
    pass


class CallFloatMethodA(CallPrimaryMethod):
    pass


class CallDoubleMethod(CallPrimaryMethod):
    pass


class CallDoubleMethodV(CallPrimaryMethod):
    pass


class CallDoubleMethodA(CallPrimaryMethod):
    pass


class CallStaticBooleanMethod(CallPrimaryMethod):
    pass


class CallStaticBooleanMethodV(CallPrimaryMethod):
    pass


class CallStaticBooleanMethodA(CallPrimaryMethod):
    pass


class CallStaticByteMethod(CallPrimaryMethod):
    pass


class CallStaticByteMethodV(CallPrimaryMethod):
    pass


class CallStaticByteMethodA(CallPrimaryMethod):
    pass


class CallStaticCharMethod(CallPrimaryMethod):
    pass


class CallStaticCharMethodV(CallPrimaryMethod):
    pass


class CallStaticCharMethodA(CallPrimaryMethod):
    pass


class CallStaticShortMethod(CallPrimaryMethod):
    pass


class CallStaticShortMethodV(CallPrimaryMethod):
    pass


class CallStaticShortMethodA(CallPrimaryMethod):
    pass


class CallStaticIntMethod(CallPrimaryMethod):
    pass


class CallStaticIntMethodV(CallPrimaryMethod):
    pass


class CallStaticIntMethodA(CallPrimaryMethod):
    pass


class CallStaticLongMethod(CallPrimaryMethod):
    pass


class CallStaticLongMethodV(CallPrimaryMethod):
    pass


class CallStaticLongMethodA(CallPrimaryMethod):
    pass


class CallStaticFloatMethod(CallPrimaryMethod):
    pass


class CallStaticFloatMethodV(CallPrimaryMethod):
    pass


class CallStaticFloatMethodA(CallPrimaryMethod):
    pass


class CallStaticDoubleMethod(CallPrimaryMethod):
    pass


class CallStaticDoubleMethodV(CallPrimaryMethod):
    pass


class CallStaticDoubleMethodA(CallPrimaryMethod):
    pass


class CallVoidMethod(CallMethodBase):
    def get_return_value(self, method):
        return None


class CallVoidMethodV(CallVoidMethod):
    pass


class CallVoidMethodA(CallVoidMethod):
    pass


class CallStaticVoidMethod(CallMethodBase):
    pass


class CallStaticVoidMethodV(CallVoidMethod):
    pass


class CallStaticVoidMethodA(CallVoidMethod):
    pass


class CallObjectMethod(CallMethodBase):
    def get_return_value(self, method):
        rtype = method.get_return_type().strip('L;').replace('/', '.')
        return self.create_java_class(rtype, init=True)


class CallObjectMethodV(CallObjectMethod):
    pass


class CallObjectMethodA(CallObjectMethod):
    pass


class CallStaticVoidMethod(CallVoidMethod):
    pass


class CallStaticVoidMethodV(CallVoidMethod):
    pass


class CallStaticVoidMethodA(CallVoidMethod):
    pass


class NewObjectArray(JPB):
    def run(self, env_ptr, size, cls_ptr, obj_ptr):
        # simply use the one of the element
        return obj_ptr


class GetObjectArrayElement(JPB):
    def run(self, env_ptr, array_ptr, index):
        # As we simplied, the array is the element
        return array_ptr


class SetObjectArrayElement(JPB):
    def run(self, env_ptr, array_ptr, index, elememt_ptr):
        # to simplify, nothing need to be done.
        pass


class RegisterNatives(JPB):
    def run(self, env, cls_ptr, methods, method_num):
        cls_name = self.get_ref(cls_ptr).name
        num = self.state.solver.eval(method_num)
        methods_ptr = self.state.solver.eval(methods)
        for i in range(num):
            ptr = methods_ptr + i * 3 * self.arch.bits // 8
            method = self.state.mem[ptr].struct.JNINativeMethod
            name = method.name.deref.string.concrete
            signature = method.signature.deref.string.concrete
            fn_ptr = method.fnPtr.long.concrete
            symbol = self.func_ptr_2_symbol_name(fn_ptr)
            c, m, s, static, obfuscated = self._dex_heuristic(cls_name,
                    name.decode('utf-8', 'ignore'),
                    signature.decode('utf-8', 'ignore'))
            Record(c, m, s, fn_ptr, symbol, static, obfuscated)
        return self.JNI_OK

    def func_ptr_2_symbol_name(self, func_ptr):
        name = None
        for s in self.state.project.loader.symbols:
            if s.rebased_addr == func_ptr:
                name = s.name
        return name

    def _dex_heuristic(self, cls_name, method_name, signature):
        """Use the heuristic way to get more information about the JNI function
        and try to deobfucate by checking with cooresponding method in Dex.
        """
        # is the native method is a static method
        is_static_method = None
        obfuscated = False
        dex = self.state.globals.get('dex')
        if dex is None:
            obfuscated = None
        ms = list(dex.find_methods(f'L{cls_name};', method_name))
        if len(ms) == 0:
            # cls or/and method name are obfuscated situation
            obfuscated = True
            cs = dex.find_classes(f'L{cls_name};')
            ms = dex.find_methods(methodname=method_name)
            if len(cs) == 0 and len(ms) == 0:
                # all obfuscated, nothing can be improved.
                pass
            elif len(cs) == 0:
                # class name obfuscated
                if len(ms) == 1:
                    cls_name = ms[0].get_method().get_class_name()
                    signature = ms[0].descriptor
                    if 'static' in ms[0].access:
                        is_static_method = True
                    else:
                        is_static_method = False
                else:
                    # more than one method found base on method name
                    classes = set()
                    sigs = set()
                    static_count = 0
                    for m in ms:
                        classes.add(m.get_method().get_class_name())
                        sigs.add(m.descriptor)
                        if 'static' in m.access:
                            static_count += 1
                    if len(classes) == 1:
                        # all in one class, so we can sure the class name
                        cls_name, = classes
                    if len(sigs) == 1:
                        # all have same signature, so we can sure the signature
                        signature, = sigs
                    if static_count == 0:
                        is_static_method = False
                    elif static_count == len(ms):
                        is_static_method = True
            else:
                # method name obfuscated
                pass
        elif len(ms) == 1:
            if signature != ms[0].descriptor:
                obfuscated = True
                signature = ms[0].descriptor
            if 'static' in ms[0].access:
                is_static_method = True
            else:
                is_static_method = False
        else:
            # method overload situation
            found = False
            static_count = 0
            for m in ms:
                if m.descriptor == signature:
                    found = True
                    break
                if 'static' in m.access:
                    static_count += 1
            if found:
                if 'static' in m.access:
                    is_static_method = True
                else:
                    is_static_method = False
            else:
                # Since signature is obfuscated and we are not sure the exact one
                # So the obfuscated signature will be returned.
                obfuscated = True
                if static_count == 0:
                    # since no method is static so we can sure
                    is_static_method = False
                elif static_count == len(ms):
                    # since all methods are static so we can sure
                    is_static_method = True
        cls_name = cls_name.strip('L;').replace('/', '.')
        return cls_name, method_name, signature, is_static_method, obfuscated



