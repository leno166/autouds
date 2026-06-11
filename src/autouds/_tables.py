"""
@文件: _tables.py
@作者: 雷小鸥
@日期: 2026/6/11 12:03
@许可: MIT License
@描述: UDS 服务标识符映射表，按 ISO 14229-1 分类。
@版本: Version 0.1
"""
SERVICE_MAP = {
    # ═══════════════════════════════════════
    # 诊断和通信管理类
    # ═══════════════════════════════════════
    '会话'                              : 0x10,
    'Diagnostic Session Control'        : 0x10,
    'session'                           : 0x10,

    'ECU 复位'                          : 0x11,
    'ECU Reset'                         : 0x11,
    'reset'                             : 0x11,

    '安全访问'                          : 0x27,
    'Security Access'                   : 0x27,
    'security_access'                   : 0x27,
    'unlock'                            : 0x27,

    '通讯控制'                          : 0x28,
    'Communication Control'             : 0x28,
    'communication_control'             : 0x28,
    'comm'                              : 0x28,

    '待机'                              : 0x3E,
    'Tester Present'                    : 0x3E,
    'tester_present'                    : 0x3E,
    'present'                           : 0x3E,

    '访问时间参数'                      : 0x83,
    'Access Timing Parameter'           : 0x83,
    'timing'                            : 0x83,

    '安全数据传输'                      : 0x84,
    'Secured Data Transmission'         : 0x84,
    'transmission'                      : 0x84,

    '控制DTC的设置'                     : 0x85,
    'Control DTC Setting'               : 0x85,
    'dtc_setting'                       : 0x85,

    '事件响应'                          : 0x86,
    'Response On Event'                 : 0x86,
    'event'                             : 0x86,

    '链路控制'                          : 0x87,
    'Link Control'                      : 0x87,
    'link'                              : 0x87,

    # ═══════════════════════════════════════
    # 数据传输类
    # ═══════════════════════════════════════
    '标识符读数据'                      : 0x22,
    'Read Data By Identifier'           : 0x22,
    'read_did'                          : 0x22,

    '地址读内存'                        : 0x23,
    'Read Memory By Address'            : 0x23,
    'read_memory'                       : 0x23,
    'read_mem'                          : 0x23,

    '标识符读比例数据'                  : 0x24,
    'Read Scaling Data By Identifier'   : 0x24,
    'scaling'                           : 0x24,

    '周期标识符读数据'                  : 0x2A,
    'Read Data By Periodic Identifier'  : 0x2A,
    'periodic'                          : 0x2A,

    '动态定义标识符'                    : 0x2C,
    'Dynamically Define Data Identifier': 0x2C,
    'define'                            : 0x2C,

    '标识符写数据'                      : 0x2E,
    'Write Data By Identifier'          : 0x2E,
    'write_did'                         : 0x2E,

    '地址写内存'                        : 0x3D,
    'Write Memory By Address'           : 0x3D,
    'write_mem'                         : 0x3D,

    # ═══════════════════════════════════════
    # 存储数据传输类
    # ═══════════════════════════════════════
    '清除诊断信息'                      : 0x14,
    'Clear Diagnostic Information'      : 0x14,
    'clear_dtc'                         : 0x14,

    '读取故障信息码'                    : 0x19,
    'Read DTC Information'              : 0x19,
    'read_dtc'                          : 0x19,

    # ═══════════════════════════════════════
    # 输入输出控制类
    # ═══════════════════════════════════════
    '通过标识符控制输入输出'            : 0x2F,
    'Input Output Control By Identifier': 0x2F,
    'io'                                : 0x2F,

    # ═══════════════════════════════════════
    # 例程功能类
    # ═══════════════════════════════════════
    '例行程序控制'                      : 0x31,
    'Routine Control'                   : 0x31,
    'routine'                           : 0x31,

    # ═══════════════════════════════════════
    # 上传下载类
    # ═══════════════════════════════════════
    '请求下载'                          : 0x34,
    'Request Download'                  : 0x34,
    'download'                          : 0x34,

    '请求上传'                          : 0x35,
    'Request Upload'                    : 0x35,
    'upload'                            : 0x35,

    '数据传输'                          : 0x36,
    'Transfer Data'                     : 0x36,
    'transfer'                          : 0x36,

    '请求退出传输'                      : 0x37,
    'Request Transfer Exit'             : 0x37,
    'exit_tf'                           : 0x37,

    '请求文件传输'                      : 0x38,
    'Request File Transfer'             : 0x38,
    'file'                              : 0x38,
}

# ── 子功能映射 ──
# 键为 service_id (int)，值为 { enable: bool, 中文/英文/短key: sub_fn 值 }
# enable=True 表示该服务支持子功能，子功能字段有效

SUB_FN_MAP = {
    # ── 诊断会话控制 (0x10) ──
    0x10: {
        'enable'             : True,

        '默认'               : 0x01,
        'default session'    : 0x01,
        'default'            : 0x01,

        '编程'               : 0x02,
        'programming session': 0x02,
        'program'            : 0x02,

        '拓展'               : 0x03,
        'extended session'   : 0x03,
        'extend'             : 0x03,

        '安全'               : 0x04,
        'security session'   : 0x04,
        'safety'             : 0x04,
    },

    # ── ECU 复位 (0x11) ──
    0x11: {
        'enable'                  : True,

        '硬'                      : 0x01,
        'hard reset'              : 0x01,
        'hard'                    : 0x01,

        '钥匙'                    : 0x02,
        'key off on'              : 0x02,
        'key'                     : 0x02,

        '软'                      : 0x03,
        'soft reset'              : 0x03,
        'soft'                    : 0x03,

        '启用快速断电'            : 0x04,
        'enable rapid power down' : 0x04,
        'on'                      : 0x04,

        '禁用快速断电'            : 0x05,
        'disable rapid power down': 0x05,
        'off'                     : 0x05,
    },

    # ── 安全访问 (0x27) ──
    0x27: {
        'enable'         : True,

        'L1'             : 0x01,
        'L1 Ex'          : 0x02,

        'level 1'        : 0x01,
        'level 1 extend' : 0x02,

        'L5'             : 0x05,
        'L5 Ex'          : 0x06,

        'level 5'        : 0x05,
        'level 5 extend' : 0x06,

        'L19'            : 0x19,
        'L19 Ex'         : 0x1A,

        'level 19'       : 0x19,
        'level 19 extend': 0x1A,
    },

    # ── 通讯控制 (0x28) ──
    0x28: {
        'enable'                       : True,

        '启用接收和发送'               : 0x00,
        'enable rx and tx'             : 0x00,
        'en_rx_tx'                     : 0x00,

        '启用接收禁用发送'             : 0x01,
        'enable rx disable tx'         : 0x01,
        'rx'                           : 0x01,

        '禁用接收启用发送'             : 0x02,
        'disable rx enable tx'         : 0x02,
        'tx'                           : 0x02,

        '禁用接收和发送'               : 0x03,
        'disable rx and tx'            : 0x03,
        'dis_rx_tx'                    : 0x03,

        '启用接收禁用发送增强'         : 0x04,
        'enable rx disable tx enhanced': 0x04,
        'rx_enhanced'                  : 0x04,

        '启用接收和发送增强'           : 0x05,
        'enable rx and tx enhanced'    : 0x05,
        'rx_tx_enhanced'               : 0x05,
    },

    # ── 待机握手 (0x3E) ──
    0x3E: {
        'enable'  : True,

        '响应'    : 0x00,
        'response': 0x00,
        'resp'    : 0x00,
    },

    # ── 控制 DTC 设置 (0x85) ──
    0x85: {
        'enable'            : True,

        '允许 DTC 更新'     : 0x01,
        'enable dtc update' : 0x01,
        'on'                : 0x01,

        '禁止 DTC 更新'     : 0x02,
        'disable dtc update': 0x02,
        'off'               : 0x02,
    },

    0x22: {'enable': False},
    0x23: {'enable': False},

    # ── 读取 DTC 信息 (0x19) ──
    0x14: {'enable': False},
    0x19: {
        'enable'                                                  : True,
        '通过状态掩码报告 DTC 数量'                               : 0x01,
        'report number of dtc by status mask'                     : 0x01,
        'count_by_mask'                                           : 0x01,

        '通过状态掩码报告 DTC'                                    : 0x02,
        'report dtc by status mask'                               : 0x02,
        'dtc_by_mask'                                             : 0x02,

        '获取 DTC 快照记录 ID'                                    : 0x03,
        'report dtc snapshot identification'                      : 0x03,
        'snapshot_id'                                             : 0x03,

        '请求指定 DTC 快照信息'                                   : 0x04,
        'report dtc snapshot record by dtc number'                : 0x04,
        'snapshot_by_dtc'                                         : 0x04,

        '通过记录 ID 报告 DTC 存储数据'                           : 0x05,
        'report dtc stored data by record number'                 : 0x05,
        'stored_data'                                             : 0x05,

        '通过 DTC 报告扩展数据'                                   : 0x06,
        'report dtc record by dtc number'                         : 0x06,
        'ext_data'                                                : 0x06,

        '通过严重性掩码报告 DTC 数量'                             : 0x07,
        'report number of dtc by severity mask record'            : 0x07,
        'count_by_severity'                                       : 0x07,

        '通过严重性掩码报告 DTC'                                  : 0x08,
        'report dtc by severity mask record'                      : 0x08,
        'dtc_by_severity'                                         : 0x08,

        '报告 DTC 严重性信息'                                     : 0x09,
        'report severity information of dtc'                      : 0x09,
        'severity_info'                                           : 0x09,

        '读取支持的所有 DTC 列表'                                 : 0x0A,
        'report supported dtc'                                    : 0x0A,
        'supported_dtc'                                           : 0x0A,

        '报告第一次测试失败的 DTC'                                : 0x0B,
        'report first test failed dtc'                            : 0x0B,
        'first_test_failed'                                       : 0x0B,

        '报告第一次确认的 DTC'                                    : 0x0C,
        'report first confirmed dtc'                              : 0x0C,
        'first_confirmed'                                         : 0x0C,

        '报告最近一次测试失败的 DTC'                              : 0x0D,
        'report most recent test failed dtc'                      : 0x0D,
        'recent_test_failed'                                      : 0x0D,

        '报告最近一次确认的 DTC'                                  : 0x0E,
        'report most recent confirmed dtc'                        : 0x0E,
        'recent_confirmed'                                        : 0x0E,

        '报告 DTC 故障检测计数器'                                 : 0x14,
        'report dtc fault detection counter'                      : 0x14,
        'fault_counter'                                           : 0x14,

        '用户定义内存 DTC 扩展数据'                               : 0x19,
        'report user def memory dtc ext data record by dtc number': 0x19,
        'user_def_memory'                                         : 0x19,
    },

    0x2F: {'enable': False},
    0x34: {'enable': False},
    0x35: {'enable': False},
    0x36: {'enable': False},
    0x37: {'enable': False},

    # ── 例行程序控制 (0x31) ──
    0x31: {
        'enable'                 : True,
        '启动程序'               : 0x01,
        'start routine'          : 0x01,
        'start'                  : 0x01,

        '停止程序'               : 0x02,
        'stop routine'           : 0x02,
        'stop'                   : 0x02,

        '请求运行结果'           : 0x03,
        'request routine results': 0x03,
        'result'                 : 0x03,
    },

}

NRC_MAP = {
    # ── 0x01 ~ 0x0F 暂时保留 ──

    # ── 0x10 ~ 0x14 通用错误 ──
    0x10: '未知错误，服务暂时被拒绝',
    0x11: '不支持该服务请求',
    0x12: '不支持子功能',
    0x13: '消息长度或格式错误',
    0x14: '请求长度超出',

    # ── 0x15 ~ 0x20 暂时保留 ──

    # ── 0x21 ~ 0x26 条件/顺序错误 ──
    0x21: '服务端正忙',
    0x22: '条件不满足',

    # 0x23 暂时保留

    0x24: '请求顺序错误',
    0x25: '指令已被接收，但是未被执行',
    0x26: '失败的操作导致当前操作无法执行',

    # ── 0x27 ~ 0x30 暂时保留 ──

    # ── 0x31 ~ 0x36 参数/安全错误 ──
    0x31: '参数错误',

    # 0x32 暂时保留

    0x33: '安全校验未通过',

    # 0x34 暂时保留

    0x35: '密钥不匹配',
    0x36: '已达到解锁最大错误次数',
    0x37: '请求延时未过期，请稍后再试',

    # ── 0x38 ~ 0x4F 为扩展数据链路安全性文档暂时保留 ──
    # ── 0x50 ~ 0x6F 暂时保留 ──

    # ── 0x70 ~ 0x73 上传下载错误 ──
    0x70: '不允许上传下载',
    0x71: '数据传输中断',
    0x72: '擦除或烧写内存错误',
    0x73: '块序列计数错误',

    # ── 0x74 ~ 0x77 暂时保留 ──

    0x78: '收到请求，延迟响应',

    # ── 0x79 ~ 0x7D 暂时保留 ──

    0x7E: '当前会话下子功能不支持',
    0x7F: '当前会话下子服务不支持',

    # 0x80 暂时保留

    # ── 0x81 ~ 0x93 条件不满足类 ──
    0x81: '每分钟转速（RPM）太高',
    0x82: '每分钟转速太低',
    0x83: '当前引擎正在运行',
    0x84: '当前引擎未运行',
    0x85: '截止当前时间引擎运行时间太短',
    0x86: '温度过高',
    0x87: '温度过低',
    0x88: '车速过高',
    0x89: '车速过低',
    0x8A: '油门/踏板过高（超过了当前要求的最大阈值）',
    0x8B: '油门/踏板过低',
    0x8C: '变速器档位不在空挡',
    0x8D: '变速器档位不在排档',

    # 0x8E 暂时保留

    0x8F: '制动开关没有关闭',
    0x90: '换挡杆不在驻车档',
    0x91: '变矩器离合器锁定',
    0x92: '电压过高',
    0x93: '电压过低',

    # ── 0x94 ~ 0xEF 为"条件不满足"类错误码扩展暂时保留 ──
    # ── 0xF0 ~ 0xFE 为汽车制造商保留 ──
    # ── 0xFF 暂时保留 ──
}
