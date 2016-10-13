# coding=utf-8

class DataPackerError(Exception):
    pass


class DataPackerProgramError(DataPackerError):
    """
    程序编写有误
    """
    pass



####  业务相关异常  ####
class DataPackerDstKeyDupError(DataPackerError):
    """
    在填充目标字典时，key已经存在
    """

    def __init__(self, dst_name, *args, **kwargs):
        super(DataPackerDstKeyDupError, self).__init__(*args, **kwargs)

        self.dst_name = dst_name

    def __str__(self):
        return 'key({}) ALREADY in dst container!'.format(self.dst_name)


class DataPackerSrcKeyNotFoundError(DataPackerError):
    """
    未在源字典中找到需要的字段
    """

    def __init__(self, src_name, *args, **kwargs):
        super(DataPackerSrcKeyNotFoundError, self).__init__(*args, **kwargs)

        self.src_name = src_name

    def __str__(self):
        return 'key({}) NOT foud in src container!'.format(self.src_name)


class DataPackerLackFieldError(DataPackerError):
    """
    缺少字段错误,用于SelectorField
    """
    pass


class DataPackerCheckError(DataPackerError):
    """
    字段校验失败
    """

    def __init__(self, src_name, dst_name, value, ck, *args, **kwargs):
        super(DataPackerCheckError, self).__init__(*args, **kwargs)
        self.src_name = src_name
        self.dst_name = dst_name
        self.value = value
        self.ck = ck

    def __str__(self):
        return 'check FAILED!!!' \
               ' \n\t src_name: {}' \
               ' \n\t dst_name: {}' \
               ' \n\t value: {}' \
               ' \n\t checker: {}'.format(
            self.src_name, self.dst_name, self.value, self.ck
        )


#### 内部使用异常 ####
class _DataPackerInterruptError(DataPackerError):
    """
    内部流程中断异常，该field获取失败
    """
    pass