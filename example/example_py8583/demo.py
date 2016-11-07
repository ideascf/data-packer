# coding=utf-8
import datetime

from py8583.spec import Py8583Spec
from py8583.py8583 import Py8583
from data_packer import RequiredField, OptionalField, DefaultField, PlaceholderField
from data_packer.converter import ConverterWrapper
from data_packer.checker import TypeChecker, ReChecker, text_checker
from data_packer.container import DictContainer
from data_packer import DataPacker

from container_py8583 import Py8583Container


def syssn2trace_num(sk, dk, value):
    return value[2:]


def trace_num2syssn(sk, dk, value):
    return '20' + value

# 请求字段
f_req_pan = RequiredField('pan', 2, checker=text_checker)
f_req_process_code = RequiredField('process_code', 3)
f_req_sys_dtm = RequiredField('sysdtm', 7, )
f_req_syssn = RequiredField('syssn', 11, converter=ConverterWrapper(syssn2trace_num))
f_req_mcc = RequiredField('mcc', 18, checker=ReChecker(r'^[0-9]{4}$'))
f_req_txamt = RequiredField('txamt', 4, checker=TypeChecker(int))
f_req_date_expire = OptionalField('date_expire', 14)
f_req_currcd = DefaultField('156', 'currcd', 49)
f_req_acq_reserved = DefaultField('nothing', 'acq_reserved', 122)

# 返回字段
f_resp_pan = RequiredField(2, 'pan')
f_resp_txamt = RequiredField(4, 'txamt')
f_resp_syssn = RequiredField(7, 'syssn', converter=ConverterWrapper(trace_num2syssn))
f_resp_respcd = RequiredField(39, 'respcd')
f_resp_reserved = PlaceholderField(60, 'reserved')


req_balance_dp = DataPacker([f_req_pan, f_req_process_code, f_req_sys_dtm, f_req_syssn, f_req_mcc, f_req_txamt,
                      f_req_date_expire, f_req_currcd, f_req_acq_reserved])
resp_balance_dp = DataPacker([f_resp_pan, f_resp_txamt, f_resp_syssn, f_resp_respcd, f_resp_reserved])


def main():
    # 准备请求数据字典
    req_dict = {
        'pan': 'primary_acct_num',
        'process_code': '123456',
        'sysdtm': datetime.datetime.now(),
        'syssn': '20161101987654',
        'mcc': '9876',
        'txamt': 100,
        # 'date_expire': ''
        'f_req_currcd': '156',
    }
    req_py8583 = Py8583(Py8583Spec())
    # 将字典数据打包为8583协议数据包
    req_balance_dp.run(
        DictContainer(req_dict),
        Py8583Container(req_py8583)
    )
    print req_py8583.bitmap_info()
    print req_py8583.field_info()
    print '\n\n\n'


    resp_dict = {}
    resp_py8583 = Py8583(Py8583Spec())
    # 构建测试8583协议响应数据
    resp_py8583.set_bit(2, 'primary_acct_num')
    resp_py8583.set_bit(4, 100)
    resp_py8583.set_bit(7, '161101987654')
    resp_py8583.set_bit(39, '00')
    resp_py8583.set_bit(60, 'reserved value test.')
    # 解析8583协议数据 为字典
    resp_balance_dp.run(
        Py8583Container(resp_py8583),
        DictContainer(resp_dict)
    )
    print resp_dict
    print

if __name__ == '__main__':
    main()