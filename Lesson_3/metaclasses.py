import dis


class ServerVerifier(type):
    def __init__(cls, class_name, bases, class_dict):
        methods = []
        attrs = []
        for func in class_dict:
            try:
                ret = dis.get_instructions(class_dict[func])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            attrs.append(i.argval)
        if 'connect' in methods:
            raise TypeError('You can not use CONNECT method in Server class ')
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Incorrect socket initialization')
        super().__init__(class_name, bases, class_dict)


class ClientVerifier(type):
    def __init__(cls, class_name, bases, class_dict):
        methods = []
        for func in class_dict:
            try:
                ret = dis.get_instructions(class_dict[func])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
        for command in ('accept', 'listen', 'socket'):
            if command in methods:
                raise TypeError('Incorrect method for CLIENT class')
        if 'get_msg' in methods:
            pass
        else:
            raise TypeError('Miss socket functions')
        super().__init__(class_name, bases, class_dict)
