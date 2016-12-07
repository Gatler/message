import json

from utils import log


def db_save(data, path):
    """
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    # data 是要序列化的字典或者 list
    # indent 是生成的字符串的格式缩进
    # ensure_ascii = False 可以保证中文不被转码
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def db_load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        # s 是一个字符串
        log('load', s)
        # json.loads 可以把字符串转为 dict 或者 list
        # 取决于你是什么
        return json.loads(s)


class Model(object):
    """
    Model 是所有 model 的基类
    @classmethod 是一个套路用法
    例如
    user = User()
    user.db_path() 返回 User.txt
    """
    @classmethod
    def db_path(cls):
        """
        cls 是类名, 谁调用的类名就是谁的
        classmethod 有一个参数是 class(这里我们用 cls 这个名字)
        所以我们可以得到 class 的名字
        """
        classname = cls.__name__
        # cls 相当于 User 或者 Message
        path = 'dbfiles/{}.txt'.format(classname)
        return path

    @classmethod
    def all(cls):
        """
        all 方法(类里面的函数叫方法)使用 load 函数得到所有的 models
        """
        path = cls.db_path()
        models = db_load(path)
        # models 是一个包含了 dict 的 list
        # 这里用了列表推导生成一个包含所有 实例 的 list
        # m 是 dict, 用 cls(m) 可以初始化一个 cls 的实例
        # 不明白就 log 大法看看这些都是啥
        # cls(m) 相当于 User(m)
        ms = [cls(m) for m in models]
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        """
        用法是
        User.find_by(username='gua')
        返回一个 list， 包含了所有符合条件的 User 实例

        在 find_by 函数里面， kwargs 是
        {
            'username': 'gua',
        }

        如果不存在，返回 []

        有了这个函数，可以极大地简化编码
        比如，可以这样验证登录和注册
        def validate_login
            us = User.find_by(username=self.username)
            if len(us) > 0:
                if us[0].password == self.password:
                    return True

        def validate_register
            us = User.find_by(username=self.username)
            unique_name = len(us) == 0
        """
        pass

    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)

    def save(self):
        """
        用 all 方法读取文件中的所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        log('debug save')
        models = self.all()
        log('models', models)
        models.append(self)
        # __dict__ 是一个魔法属性
        # 它包含的是所有对象的属性和值组成的字典
        l = [m.__dict__ for m in models]
        path = self.db_path()
        db_save(l, path)


class User(Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        # return self.username == 'gua' and self.password == '123'
        us = self.all()
        for u in us:
            if u.username == self.username:
                if u.password == self.password:
                    return True
        return False

    def validate_register(self):
        valid_length = len(self.username) > 2 and len(self.password) > 2
        # 要求名字不重复
        unique_name = True
        us = self.all()
        for u in us:
            if u.username == self.username:
                unique_name = False
                break
        # 返回结果
        log('用户注册校验', valid_length, unique_name)
        return valid_length and unique_name

class Message(Model):
    """
    Message 是用来保存留言的 model
    """
    def __init__(self, form):
        self.author = form.get('author', '')
        self.message = form.get('message', '')


if __name__ == '__main__':
    # log('db path', User.db_path(), Message.db_path())
    # log('all', User.all())
    # log('all', Message.all())
    form = {
        'author': 'gua',
        'message': '你好',
    }
    m = Message(form)
    m.save()
    log(Message.all())