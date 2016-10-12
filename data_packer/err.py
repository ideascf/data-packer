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
    pass

class DataPackerSrcKeyNotFoundError(DataPackerError):
    """
    未在源字典中找到需要的字段
    """
    pass


class DataPackerLackFieldError(DataPackerError):
    """
    缺少字段错误,用于SelectorField
    """
    pass


class DataPackerCheckError(DataPackerError):
    """
    字段校验失败
    """
    pass


#### 内部使用异常 ####
class _DataPackerInterruptError(DataPackerError):
    """
    内部流程中断异常，该field获取失败
    """
    pass