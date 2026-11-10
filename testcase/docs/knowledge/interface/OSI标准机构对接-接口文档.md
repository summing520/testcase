# 标准机构对接-接口文档

> **来源**：本地 Word《[新版] 乐享借机构合作标准接口文档260417.docx》（乐享借机构合作标准接口说明）  
> **转换**：`skills/word-doc-parser/parse_word_to_md.py`（python-docx，段落与表格按文档顺序）

---

## 文档导航

> **一级**：各大章（一、二、三、四、五）；**二级**：如「1. 机构合作方提供接口」「2. 借款相关接口」；**三级**：如「1.1 准入撞库」等具体接口。

- [一、概述](#nav-l1-yi)
  - [1. 文档简介](#nav-yi-s1)
  - [2. 版本变更记录](#nav-yi-s2)
- [二、对接说明](#nav-l1-er)
  - [1. 回调环境说明](#nav-er-s1)
  - [2. 接入说明](#nav-er-s2)
  - [3. 数据安全](#nav-er-s3)
  - [4. 参数结构](#nav-er-s4)
    - [4.1 说明](#nav-er-4-1)
    - [4.2 请求参数结构](#nav-er-4-2)
    - [4.3 响应参数结构](#nav-er-4-3)
    - [4.4 公用响应码](#nav-er-4-4)
  - [5. 接口总览](#nav-er-s5)
- [三、联机接口](#nav-l1-san)
  - [1. 机构合作方提供接口](#nav-san-partner)
    - [1. 准入授信相关接口](#nav-san-biz-1)
      - [1.1 准入撞库](#nav-org-1-1)
      - [1.2 实名注册](#nav-org-1-2)
      - [1.3 预授信申请提交](#nav-org-1-3)
      - [1.4 授信申请提交](#nav-org-1-4)
      - [1.5 查询授信申请结果](#nav-org-1-5)
    - [2. 借款相关接口](#nav-san-biz-2)
      - [2.1 借款试算](#nav-org-2-1)
      - [2.2 借款申请提交](#nav-org-2-2)
      - [2.3 查询放款结果](#nav-org-2-3)
      - [2.4 查询借据及还款计划](#nav-org-2-4)
      - [2.5 查询权益订单及还款计划](#nav-org-2-5)
      - [2.6 获取借款下一步增验信息](#nav-org-2-6)
      - [2.7 查询AMC订单及还款计划](#nav-org-2-7)
    - [3. 还款相关接口](#nav-san-biz-3)
      - [3.1 查询待还款列表](#nav-org-3-1)
      - [3.2 还款试算](#nav-org-3-2)
      - [3.3 还款申请提交](#nav-org-3-3)
      - [3.4 查询还款结果](#nav-org-3-4)
      - [3.5 权益还款试算](#nav-org-3-5)
      - [3.6 权益还款申请提交](#nav-org-3-6)
      - [3.7 查询权益还款结果](#nav-org-3-7)
    - [4. 绑卡相关接口](#nav-san-biz-4)
      - [4.1 查询用户已绑卡列表](#nav-org-4-1)
      - [4.2 查询支持银行列表](#nav-org-4-2)
      - [4.3 银行卡绑定申请](#nav-org-4-3)
      - [4.4 银行卡绑定短信验证](#nav-org-4-4)
      - [4.5 查询绑卡结果](#nav-org-4-5)
    - [5. 通用接口](#nav-san-biz-5)
      - [5.1 查询用户额度](#nav-org-5-1)
      - [5.2 查询用户协议](#nav-org-5-2)
      - [5.3 查询场景页面地址](#nav-org-5-3)
      - [5.4 发送短信验证码](#nav-org-5-4)
      - [5.5 短信验证](#nav-org-5-5)
      - [5.6 提交补充资料](#nav-org-5-6)
  - [2. 平台方提供接口](#nav-san-platform)
    - [2.1 推送授信结果](#nav-plat-2-1)
    - [2.2 推送额度变更](#nav-plat-2-2)
    - [2.3 推送放款结果](#nav-plat-2-3)
    - [2.4 推送借据及还款计划](#nav-plat-2-4)
    - [2.5 推送权益订单信息及还款计划](#nav-plat-2-5)
    - [2.6 推送还款结果](#nav-plat-2-6)
    - [2.7 推送绑卡结果](#nav-plat-2-7)
    - [2.8 推送权益还款结果](#nav-plat-2-8)
    - [2.9 推送AMC订单信息及还款计划](#nav-plat-2-9)
- [四、批量文件【根据实际需要对接】](#nav-l1-si)
  - [1. T-1日新增授信申请信息](#nav-si-chunk-1)
  - [2. T-1日新增借据信息](#nav-si-chunk-2)
  - [3. T-1日新增还款计划信息](#nav-si-chunk-3)
  - [4. T-1日变更借据信息](#nav-si-chunk-4)
  - [5. T-1日变更还款计划信息](#nav-si-chunk-5)
  - [6. T-1日放款交易流水](#nav-si-chunk-6)
  - [7. T-1日还款交易流水](#nav-si-chunk-7)
  - [8. T-1日代偿交易流水](#nav-si-chunk-8)
- [五、附录](#nav-l1-wu)
  - 正文内 [1. 婚姻状况](#nav-wu-1) … [12. 银行编码映射](#nav-wu-12) 等附录小节均可锚点跳转

---

[新版] 乐享借机构合作标准接口文档

<h2 id="nav-l1-yi">一、概述</h2>

<h3 id="nav-yi-s1">1. 文档简介</h3>

此文档作为乐享借平台与助贷机构合作方进行互联网信贷业务合作的对接文档，详细描述了乐享借平台与机构合作方之间的标准交互流程。

<h3 id="nav-yi-s2">2. 版本变更记录</h3>

| 版本号 | 修订时间 | 修订内容 | 修订人 |
| --- | --- | --- | --- |
| V 1.0 | 2024.1.15 | 初版 |  |
| V 1.1 | 2024.3.11 | 5.3 查询场景页面地址，其中场景字段增加类型：DOWN | 但明冬 |
| V1.2 | 2024.10.9 | 2.2 推送额度变更接口，增加“可用额度”字段 | 张一楠 |
| V1.3 | 2024.11.4 | 5.6 提交补充资料接口，入参bizNo改为必传 | 张一楠 |
| V1.3.1 | 2024.11.8 | 增加2.3查询放款结果接口入参描述 | 张一楠 |
| V1.4 | 2024.11.26 | authIdInfo对象中IdCardAddress改为idCardAddress<br>jobInfo对象中，jobCatagory改为jobCategory<br>4.3银行卡绑定申请接口返参，fundBindReqNo必传<br>2.6 推送还款结果接口，repayReqNo参数说明更新 | 张一楠 |
| V1.5 | 2025.03.18 | 2.2借款申请提交接口，银行卡信息对象增加参数<br>4.3银行卡绑定申请接口，返参增加字段<br>5.2 查询用户协议，入参增加字段<br>额度变更接口，入参增加字段 | 张一楠 |
| V1.5.1 | 2025.04.07 | 以下接口增加违约金字段（提前还款手续费）：<br>3.2 还款试算<br>2.4 查询借据及还款计划<br>2.4 推送借据及还款计划 | 张一楠 |
| V1.5.2 | 2025.04.23 | 查询用户已绑卡列表，增加入参：bindScene、fundDrawNo | 张一楠 |
| V1.5.3 | 2025.05.28 | 以下新增首贷、复贷标识<br>2.3 查询放款结果<br>2.3 推送放款结果 | 曹玏 |
| V1.5.4 | 2025.06.26 | 借款试算接口新增出参：discountAmt权益优惠金额，非必传<br>新增2.7 权益查询接口<br>5.3 查询场景页面地址入参新增：DRAW_PRIVILEGE_REDEEM H5权益兑换地址<br>2.5 查询权益订单及还款计划新增：privilegeExpireTime过期时间<br>2.5 推送权益订单信息及还款计划新增：privilegeExpireTime过期时间<br>借款试算接口新增出参privilegeDiscountAmt，有权益必传 | 曹玏 |
| V1.5.5 | 2025.07.15 | 2.3查询放款结果、2.3推送放款结果，响应参数，删除权益相关字段<br>isPrivilegeProcess，fundPrivilegeOrderNo，privilegeAmt，privilegeTerm，privilegePurchaseTime<br>2.5查询权益订单及还款计划、2.5推送权益订单信息及还款计划，<br>请求参数，删除fundPrivilegeOrderNo<br>privilegeStatus 状态，增加 05 - 已关单<br>2.7 权益查询接口 删除<br>2.1 借款试算响应参数增加supportPrivilege，响应参数，删除discountAmt、privilegeDiscountAmt<br>5.2 查询用户协议请求参数，scene查询场景，增加 PRIVILEGE<br>2.6 获取借款下一步增验信息，出参增加smsType<br>2.5查询权益订单及还款计划和2.5 推送权益订单信息及还款计划新增privilegeName 权益名称 | 赵鑫 |
| V1.5.6 | 2025.08.05 | 1.4授信申请提交新增拓展对象extraData对象<br>2.2借款申请提交新增拓展对象extraData对象<br>2.3放款结果查询新增出资机构编码capitalCode<br>2.3推送放款结果新增出资机构编码capitalCode | 曹玏 |
| V1.5.7 | 2025.09.25 | 2.1 借款试算<br>请求参数新增：loanType借款类型<br>响应参数新增：totalDebtConsultationFeeAmt应还债务咨询顾问服务费、loanType借款类型、amcInfo AMC借款对象<br>2.2 借款申请提交<br>请求参数新增：loanType借款类型<br>新增2.7 查询AMC订单及还款计划<br>新增2.9 推送AMC订单及计划机构<br>3.2 还款试算<br>请求参数新增：orderType还款订单类型<br>响应参数新增：deserveDebtConsultationFeeAmt应还债务咨询顾问服务费、deserveDebtConsultationPenaltyAmt应还债务咨询顾问服务违约金<br>3.3 还款申请提交<br>请求参数新增：orderType还款订单类型 |  |
| V1.5.8 | 2026.03.25 | 2.5查询权益订单及还款计划接口更新过期时间回传场景 |  |

<h2 id="nav-l1-er">二、对接说明</h2>

<h3 id="nav-er-s1">1. 回调环境说明</h3>

开发环境：https://test2.xurongwl.com/cbg/goa/api/p/平台分配的机构编码/接口名

测试环境：https://test3.xurongwl.com/cbg/goa/api/p/平台分配的机构编码/接口名

生产环境：https://a.loloabz.com/cbg/goa/api/p/平台分配的机构编码/接口名

<h3 id="nav-er-s2">2. 接入说明</h3>

使用 HTTPS 协议进行数据通信

使用 POST json 方式发送请求，数据类型为application/json

使用 UTF-8 字符集编码

双方交换RSA公钥，乐享借提供机构编码、md5Salt给合作方

<h3 id="nav-er-s3">3. 数据安全</h3>

使用对称加密+非对称加密+签名保证安全，流程：

双方生成 RSA 的公私钥，交换 RSA 公钥

请求方生成随机的 AES 密钥，对明文进行加密，然后使用对方的RSA 的公钥对这个随机密钥进行加密

最后将 AES 加密后的数据、RSA 加密后的随机密钥、当前时间戳、md5盐值拼在一起，用 MD5 算法生成签名

接受方校验签名后，RSA 解密得到随机密钥，然后再做 AES 解密得到明文

demo

[api-demo.zip]

<h3 id="nav-er-s4">4. 参数结构</h3>

<h4 id="nav-er-4-1">4.1 说明</h4>

| - | 符号 | 说明 |
| --- | --- | --- |
| 是否必须 | Y | 必须 |
| 是否必须 | N | 非必须 |
| 是否必须 | O | 一定情况下必须 |

<h4 id="nav-er-4-2">4.2 请求参数结构</h4>

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| timestamp | 时间戳 | long | Y | 时间戳，毫秒值 |
| sign | 数据签名 | string | Y |  |
| key | 随机密钥 | string | Y |  |
| content | 请求业务数据 | string | Y | json加密后的string 详见各接口定义 |

请求参数示例：

```json
{
"timestamp":1705484734000,
"key":"xxxxx",
"sign":"xxxx",
"content":"json加密后的值"
}
```

<h4 id="nav-er-4-3">4.3 响应参数结构</h4>

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| timestamp | 时间戳 | long | Y | 时间戳，毫秒值 |
| sign | 数据签名 | string | Y |  |
| key | 随机密钥 | string | Y |  |
| content | 响应业务数据 | string | Y | json加密后的string |

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| code | 响应码 | string | Y | 详见4.4公用响应码定义 |
| msg | 响应信息 | string | O | code 不为 200时，必传 |
| bizData | 业务数据 | object | O | 详见各接口定义 |

响应参数示例：

```json
{
"timestamp":1705484736000,
"key":"xxxxx",
"sign":"xxxx",
"content":"json加密后的值"
}
```

<h4 id="nav-er-4-4">4.4 公用响应码</h4>

| 响应码 / code | 说明 |
| --- | --- |
| 200 | 响应成功 |
| 1001 | 系统异常（内部系统异常或网络异常） |
| 1002 | 参数错误 |
| 1003 | 签名错误 |
| 1100 | 其他 |

<h3 id="nav-er-s5">5. 接口总览</h3>

| 接口类型 | 业务环节 | 对接接口 | 是否必须 | 备注说明 |
| --- | --- | --- | --- | --- |
| 机构合作方提供接口 | 准入授信 | 1.1 准入撞库 | Y |  |
| 机构合作方提供接口 | 准入授信 | 1.2 实名注册（可选） | N | 根据实际需要对接 |
| 机构合作方提供接口 | 准入授信 | 1.3 预授信申请提交（可选） | N | 根据实际需要对接 |
| 机构合作方提供接口 | 准入授信 | 1.4 授信申请提交 | Y |  |
| 机构合作方提供接口 | 准入授信 | 1.5 查询授信申请结果 | Y |  |
| 机构合作方提供接口 | 借款 | 2.1 借款试算 | O | 借款为API模式时，需对接 |
| 机构合作方提供接口 | 借款 | 2.2 借款申请提交 | O | 借款为API模式时，需对接 |
| 机构合作方提供接口 | 借款 | 2.3 查询放款结果 | Y |  |
| 机构合作方提供接口 | 借款 | 2.4 查询借据及还款计划 | Y |  |
| 机构合作方提供接口 | 借款 | 2.5 查询权益订单信息及还款计划 | O | 有权益订单信息时，需对接 |
| 机构合作方提供接口 | 借款 | 2.6 获取借款下一步增验信息 | N | 根据实际需要对接（有人脸/短信等借款增验时，需对接） |
| 机构合作方提供接口 | 借款 | 2.7 权益查询接口 | N | 根据实际需要对接 |
| 机构合作方提供接口 | 还款 | 3.1 查询待还款列表 | N | 根据实际需要对接 |
| 机构合作方提供接口 | 还款 | 3.2 还款试算 | O | 还款为API模式时，需对接 |
| 机构合作方提供接口 | 还款 | 3.3 还款申请提交 | O | 还款为API模式时，需对接 |
| 机构合作方提供接口 | 还款 | 3.4 查询还款结果 | O | 还款为API模式时，需对接 |
| 机构合作方提供接口 | 绑卡 | 4.1 查询用户已绑卡列表 | Y |  |
| 机构合作方提供接口 | 绑卡 | 4.2 查询支持银行列表 | O | 绑卡为API模式时，需对接 |
| 机构合作方提供接口 | 绑卡 | 4.3 银行卡绑定申请 | O | 绑卡为API模式时，需对接 |
| 机构合作方提供接口 | 绑卡 | 4.4 银行卡绑定短信验证 | O | 绑卡为API模式时，需对接 |
| 机构合作方提供接口 | 绑卡 | 4.5 查询绑卡结果 | O | 绑卡为H5模式时，需对接 |
| 机构合作方提供接口 | 通用 | 5.1 查询用户额度 | Y |  |
| 机构合作方提供接口 | 通用 | 5.2 查询用户协议 | Y |  |
| 机构合作方提供接口 | 通用 | 5.3 获取场景页面地址（可选） | N | 根据实际需要对接 |
| 机构合作方提供接口 | 通用 | 5.4 获取短信验证码（可选） | N | 根据实际需要对接（有借款短信增验时，需对接） |
| 机构合作方提供接口 | 通用 | 5.5 短信验证（可选） | N | 根据实际需要对接（有借还款短信增验时，需对接） |
| 机构合作方提供接口 | 通用 | 5.6 提交补充资料（可选） | N | 根据实际需要对接（有借款人脸增验时，需对接） |
| 平台方提供接口 | - | 6.1 推送授信结果 | Y |  |
| 平台方提供接口 | - | 6.2 推送额度变更 | Y |  |
| 平台方提供接口 | - | 6.3 推送放款结果 | Y |  |
| 平台方提供接口 | - | 6.4 推送借据和还款计划 | Y |  |
| 平台方提供接口 | - | 6.5 推送权益订单信息及还款计划 | O | 机构合作方有权益时，需对接 |
| 平台方提供接口 | - | 6.6 推送还款结果 | Y |  |
| 平台方提供接口 | - | 6.7 推送绑卡结果 | O | 绑卡为H5模式时，需对接 |

<h2 id="nav-l1-san">三、联机接口</h2>

<h3 id="nav-san-partner">1. 机构合作方提供接口</h3>

<h4 id="nav-san-biz-1">1. 准入授信相关接口</h4>

<h4 id="nav-org-1-1">1.1 准入撞库</h4>

1.1.1 调用场景

平台方请求机构合作方接口，合作方对用户进行前置准入检查、并返回准入结果，准入成功则可进行后续申请。

1.1.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/userAccess

1.1.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| mobileNoMd5 | 手机号md5 | string(64) | Y | 32位md5小写 |
| idNoMd5 | 身份证号md5 | string(64) | N | 32位md5小写 |
| mobileIdNoMd5 | ⼿机号+⾝份证号md5 | string(64) | N | 32位md5小写 |
| userName | 用户姓名 | string(64) | N | 明文 |

*手机号md5为必传，其他参数按照双方约定以实际需要传输

请求参数示例：

```json
{
"mobileNoMd5": "77a8b9df79de0206dc622a74288e81a6",
"idNoMd5": "2441abbcd153c7778ff2852552c494b8"
}
```

1.1.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 准入结果 | integer(2) | Y | 1 - 准入通过；2 - 准入拒绝 |
| reasonDesc | 拒绝原因描述 | string(256) | O | 结果2时必传 |

响应参数示例：

```json
// 准入通过
{
"result": 1
}
// 准入拒绝
{
"result": 2,
"reasonDesc": "黑名单用户"
}
```

<h4 id="nav-org-1-2">1.2 实名注册</h4>

1.2.1 调用场景

根据机构合作方流程及产品要求，可选择对接此接口。平台方请求机构合作方接口，提供用户明文的实名信息，合作方进行用户注册、并告知注册结果，成功则可进行后续申请。

1.2.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/userRegister

1.2.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userNo | 平台用户号 | string(64) | Y | 平台用户对外唯一标识 |
| userName | 用户姓名 | string(64) | Y | 明文 |
| mobileNo | 用户手机号 | string(15) | Y | 明文 |
| idNo | 用户身份证号 | string(30) | Y | 明文 |

请求参数示例：

```json
{
"userNo": "U1703648207",
"userName": "张三",
"mobileNo": "13366663333",
"idNo": "430381200012121212"
}
```

1.2.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 注册结果 | integer(2) | Y | 1 - 注册成功；2 - 注册失败 |
| fundUserNo | 机构用户号 | string(32) | N | 结果1时可传，机构方用户唯一标识 |
| reasonDesc | 失败原因描述 | string(256) | O | 结果2时必传 |

响应参数示例：

```json
// 注册成功
{
"result": 1,
"fundUserNo": "1703648219"
}
// 注册失败
{
"result": 2,
"reasonDesc": "黑名单用户"
}
```

<h4 id="nav-org-1-3">1.3 预授信申请提交</h4>

1.3.1 调用场景

根据机构合作方流程及产品要求，可选择对接此接口。平台方请求机构合作方接口，提供用户的申请信息，合作方进行用户授信资格检查申请、并告知申请结果，成功则可进行后续申请。

1.3.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/preCreditApply

1.3.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userNo | 平台用户号 | string(64) | Y | 平台用户对外唯一标识 |
| fundUserNo | 机构方用户号 | string(64) | N | 机构方用户唯一标识 |
| authIdInfo | 用户身份证信息 | object | Y | 详见下表 |
| authFaceInfo | 用户活体信息 | object | Y | 详见下表 |
| deviceInfo | 设备信息 | object | Y | 详见下表 |
| geoInfo | 定位信息 | object | Y | 详见下表 |

authIdInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| idCardFrontImgUrl | 身份证人像面照片地址 | string(500) | Y | 示例：https://private-sit.oss-cn-shanghai.aliyuncs.com/private-sit/ocr/hub/UR0707901830361083904/1703128526347/92pceu/1703128526483.png |
| idCardBackImgUrl | 身份证国徽面照片地址 | string(500) | Y | 示例：https://private-sit.oss-cn-shanghai.aliyuncs.com/private-sit/ocr/hub/UR0707901830361083904/1703128537134/m3gtqa/1703128537036.png |
| idCardHandImgUrl | 手持身份证照片地址 | string(500) | N |  |
| idCardFrontImgBase64 | 身份证人像面照片base64 | string(200000) | N |  |
| idCardBackImgBase64 | 身份证国徽面照片base64 | string(200000) | N |  |
| idCardHandImgBase64 | 手持身份证照片base64 | string(200000) | N |  |
| idCardNo | 用户身份证号 | string(32) | Y | 身份证正面身份证号 |
| idCardSex | 用户性别 | string(2) | Y | 0-男，1-女 |
| idCardBirthday | 用户生日 | string(32) | Y | 格式：1979-08-23 |
| idCardEthnicity | 用户民族 | string(2) | Y | 汉 |
| idCardAddress | 身份证地址 | string(100) | Y | 身份证详细地址 |
| idCardStartDate | 身份证有效期始期 | string(32) | Y | 格式示例：20080314 |
| idCardEndDate | 身份证有效期止期 | string(32) | Y | 若为长期则传29991231 |
| idCardAuthority | 签发机关 | string(32) | Y |  |

authFaceInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| faceSource | 活体供应商 | integer(2) | Y | 1 - 旷视；2 -微众；3 -阿里 |
| faceImg1Url | 活体照片1地址 | string(500) | Y | 示例：http://private-sit.oss-cn-shanghai.aliyuncs.com/private-sit/live/hub/UR0710959998205427712/1703584077691/5eek3g/HUB_LIVE.jpeg |
| faceImg1Base64 | 活体照片1base64 | string(200000) | N |  |
| faceImg2Url | 活体照片2地址 | string(500) | N |  |
| faceImg2Base64 | 活体照片2base64 | string(200000) | N |  |
| faceOriginData | 活体检测原始数据 | string(3000) | N |  |
| faceScore | 活体分 | decimal | N |  |
| faceCollectTime | 活体采集时间 | string(32) | N | 格式：2023-10-13 12:03:13 |

deviceInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| ip | Ip地址 | string(32) | Y |  |
| gps | gps地址 | string(500) | Y |  |
| os | 系统 | string(32) | Y | android, ios |

geoInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| latitude | 纬度 | decimal | N |  |
| longitude | 经度 | decimal | N |  |

请求参数示例：

```json
{
"userNo": "U1703648207",
"fundUserNo": "1703648219",
"authIdInfo": {
"idFrontImgUrl": "http://example.com/身份证/正面照片.jpg",
"idBackImgUrl": "http://example.com/身份证/背面照片.jpg",
"idAddress": "广东省深圳市福田区上梅林中康路卓越城一期4栋608室",
"idValidFrom": "2015-08-11",
"idValidTo": "2025-08-11",
"idIssueOrg": "深圳市公安局"
},
"authFaceInfo": {
"faceSource": 1,
"faceImg1Url": "http://example.com/活体照片1.jpg",
"faceImg2Url": "http://example.com/活体照片2.jpg",
"faceScore": 95.5,
"faceCollectTime": "2023-12-26 10:30:00"
},
"deviceInfo": {
"ip": "192.168.0.1",
"gps": {
"x": 30.23,
"y": 140.24
},
"os": "ios"
},
"geoInfo": {
"latitude": "35.359542",
"longitude": "117.455610"
}
}
```

1.3.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 受理结果 | integer(2) | Y | 1 - 预授信成功；2 - 预授信拒绝 |
| reasonDesc | 失败原因描述 | string(256) | O | 结果2时必传 |

响应参数示例：

```json
// 预授信成功
{
"result": 1
}
// 预授信拒绝
{
"result": 2,
"reasonDesc":"黑名单用户"
}
```

<h4 id="nav-org-1-4">1.4 授信申请提交</h4>

1.4.1 调用场景

平台方请求机构合作方接口，提供用户授信申请详细信息、向机构方进件，机构方返回申请受理成功和失败的结果。受理成功，则可继续调用查询授信结果接口。

1.4.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/creditApply

1.4.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| creditReqNo | 平台授信申请号 | string(64) | Y |  |
| userNo | 平台用户号 | string(64) | Y | 平台用户对外唯一标识 |
| fundUserNo | 机构方用户号 | string(64) | N | 机构方用户唯一标识 |
| userBaseInfo | 用户基本信息 | object | Y | 详见下表 |
| userProfileInfo | 用户详细信息 | object | Y | 详见下表 |
| cardInfo | 用户银行卡信息 | object | O | 绑卡在授信环节时，必传 |
| authIdInfo | 用户身份证信息 | object | O | 与机构约定，如已在预授信接口提供，则该接口不用再次提供 |
| authFaceInfo | 用户活体信息 | object | O | 与机构约定，如已在预授信接口提供，则该接口不用再次提供 |
| jobInfo | 用户公司信息 | object | Y | 详见下表 |
| contactInfo | 用户联系人信息 | object | Y | 详见下表 |
| deviceInfo | 设备信息 | object | O | 与机构约定，如已在预授信接口提供，则该接口不用再次提供 |
| geoInfo | 定位信息 | object | O | 与机构约定，如已在预授信接口提供，则该接口不用再次提供 |
| extraData | 拓展信息 | object | O | 与机构约定是否必传 |

userBaseInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userName | 用户姓名 | string(32) | Y |  |
| mobileNo | 用户手机号 | string(32) | Y |  |

userProfileInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| marriage | 婚姻状况 | string(10) | N | 根据合作方要求配置是否必传。枚举值见附录 |
| monthIncome | 收入情况 | string(10) | N | 同上 |
| education | 最高学历 | string(10) | N | 同上 |
| loanPurpose | 借款用途 | string(10) | N | 同上 |
| expectedLoanAmt | 期望借款金额 | decimal | N | 根据合作方要求配置是否必传。单位：元(小数点后保留两位) |
| expectedLoanTerm | 期望借款期数 | integer | N | 根据合作方要求配置是否必传。1，3，6，9，12，24，36 |
| residentialType | 住宅类型 | string(10) | N | 同上 |
| address | 居住地址（省-市-区） | string(64) | N | 根据合作方要求配置是否必传。示例：上海市-上海市辖区-徐汇区 |
| addressDetail | 详细地址 | string(100) | N | 根据合作方要求配置是否必传。 |
| residentialProvince | 居住地省份 | string(64) | N | 同上 |
| residentialCity | 居住地城市 | string(64) | N | 同上 |
| residentialDistrict | 居住地区县 | string(64) | N | 同上 |
| residentialProvinceCode | 居住地省份代码 | string(10) | N | 同上 |
| residentialCityCode | 居住地市代码 | string(10) | N | 同上 |
| residentialDistrictCode | 居住地区代码 | string(10) | N | 同上 |
| email | 邮箱 | string(64) | N | 同上 |

cardInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| cardNo | 银行卡号 | string(32) | N | 卡号明文 |
| bankCode | 银行编码 | string(32) | N | 银行编码与银行名称，详见附录 |
| bankName | 银行名称 | string(64) | N | 银行编码与银行名称，详见附录 |
| bankMobile | 银行预留手机号 | string(32) | N | 银行预留手机号明文 |

authIdInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| idCardFrontImgUrl | 身份证人像面照片地址 | string(500) | Y | 示例：https://private-sit.oss-cn-shanghai.aliyuncs.com/private-sit/ocr/hub/UR0707901830361083904/1703128526347/92pceu/1703128526483.png |
| idCardBackImgUrl | 身份证国徽面照片地址 | string(500) | Y | 示例：https://private-sit.oss-cn-shanghai.aliyuncs.com/private-sit/ocr/hub/UR0707901830361083904/1703128537134/m3gtqa/1703128537036.png |
| idCardNo | 用户身份证号 | string(32) | Y | 身份证正面身份证号 |
| idCardSex | 用户性别 | string(2) | Y | 0-男，1-女 |
| idCardBirthday | 用户生日 | string(32) | Y | 格式：1979-08-23 |
| idCardEthnicity | 用户民族 | string(2) | Y | 汉 |
| idCardAddress | 身份证地址 | string(100) | Y | 身份证详细地址 |
| idCardStartDate | 身份证有效期始期 | string(32) | Y | 格式示例：20080314 |
| idCardEndDate | 身份证有效期止期 | string(32) | Y | 若为长期则传29991231 |
| idCardAuthority | 签发机关 | string(32) | Y |  |

authFaceInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| faceSource | 活体供应商 | integer(2) | Y | 1 - 旷视；2 -微众；3 -阿里 |
| faceImg1Url | 活体照片1地址 | string(500) | Y | 示例：http://private-sit.oss-cn-shanghai.aliyuncs.com/private-sit/live/hub/UR0710959998205427712/1703584077691/5eek3g/HUB_LIVE.jpeg |
| faceImg1Base64 | 活体照片1base64 | string(200000) | N |  |
| faceImg2Url | 活体照片2地址 | string(500) | N |  |
| faceImg2Base64 | 活体照片2base64 | string(200000) | N |  |
| faceOriginData | 活体检测原始数据 | string(3000) | N |  |
| faceScore | 活体分 | decimal | Y |  |
| faceCollectTime | 活体采集时间 | string(32) | Y | 格式：2023-10-13 12:03:13 |

jobInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| jobIndustry | 行业 | string(10) | N | 根据合作方要求传输，枚举值见附录 |
| jobCategory | 职业类别 | string(10) | N | 同上 |
| incomeType | 收入类型 | string(10) | N | 同上 |
| companyName | 公司名称 | string(64) | N | 根据合作方要求传输 |
| companyType | 公司类型 | string(10) | N | 根据合作方要求传输，枚举值见附录 |
| companyAddress | 公司地址 | string(64) | N | 同上 |
| companyAddressDetail | 公司详细地址 | string(100) | N | 同上 |
| companyProvince | 公司地址省份 | string(64) | N | 同上 |
| companyCity | 公司地址城市 | string(64) | N | 同上 |
| companyDistrict | 公司地址区县 | string(64) | N | 同上 |
| companyProvinceId | 公司地址省份代码 | string(10) | N | 同上 |
| companyCityId | 公司地址城市代码 | string(10) | N | 同上 |
| companyDistrictId | 公司地址区县代码 | string(10) | N | 同上 |
| companyTel | 公司电话 | string(32) | N | 同上 |

contactInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| contactOneName | 第一联系人姓名 | string(32) | Y |  |
| contactOneTel | 第一联系人电话 | string(32) | Y |  |
| contactOneRel | 第一联系人关系 | string(10) | Y | 枚举值见附录 |
| contactTwoName | 第二联系人姓名 | string(32) | Y |  |
| contactTwoTel | 第二联系人电话 | string(32) | Y |  |
| contactTwoRel | 第二联系人关系 | string(10) | Y | 枚举值见附录 |

deviceInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| ip | Ip地址 | string(32) | Y |  |
| os | 系统类型 | string(32) | Y | android, ios |
| deviceId | 设备Id | string(200) | N | 有则传 |
| mac | 设备mac地址 | string(32) | N | 有则传 |
| isSimulator | 设备是否模拟器 | Integer | N | 0.否，1.是，2.未知。有则传 |
| isRoot | 设备是否越狱 | Integer | N | 0.否，1.是，2.未知。有则传 |
| os_version | 系统版本号 | string(32) | N | 有则传 |
| duid | 设备诶一标识 | string(32) | N | 有则传 |
| deviceModel |  | string(32) | N | IOS:设备类型名称：iphone/ipod/ipad<br>Android：设备型号：PBEM00。有则传 |
| deviceBrand | 设备品牌 | string(32) | N | 设备品牌：OPPO（仅Android有）。有则传 |
| memory | MB设备内存 | float | N | 有则传 |
| storage | MB设备总存储 | float | N | 有则传 |
| unuseStorage | MB设备剩余存储 | float | N | 有则传 |
| deviceResolution | 设备屏幕分辨率 | string(32) | N | 有则传 |
| bettary | 设备当前电量百分比 | float | N | 有则传 |
| isProxy | 省呗是否使用代理 | int | N | 0.否  1.是 2.未知。有则传 |
| simCount | SIM的个数 | int | N | 0,1,2。有则传 |
| withSim | 是否有SIM | int | N | 0.否  1.是 2.未知。有则传 |
| teleNum | 运营商编码 | string(32) | N | 中国移动、中国联通、中国电信。有则传 |
| deviceUa | 浏览器 | string(32) | N | 浏览器UA。有则传 |
| debugState | 手机是否调试状态 | int | N | 0.否  1.是 2.未知。有则传 |
| isPpn | 是否使用VPN | int | N | 0.否  1.是 2.未知。有则传 |
| isUsbDebug | 是否开启USB调试 | int | N | 0.否  1.是 2.未知。有则传 |
| androidId | 设备唯一id | string(32) | N | 设备唯一id(仅Android设备有) |
| imei | 设备唯一id | string(32) | N | 设备唯一id(仅Android设备有) |
| oaid | 安全联盟统一id | string(32) | N | 仅Android设备有 |
| network | 网络类型 | int | N | 0.移动网络 1.WiFi   2.无网络 -1.未知网络（仅Android设备有） |
| mac | 设备mac地址 | string(32) | N | 仅Android设备有 |
| idfa | 设备IDFA标识 | string(32) | N | 仅IOS设备有 |
| idfv | 设备IDFV标识 | string(32) | N | 仅IOS设备有 |
| deviceName | 设备用户名称 | string(32) | N | 仅IOS设备有 |
| deviceInfo | 设备机型 | string(32) | N | 仅IOS设备有 |

geoInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| latitude | 纬度 | decimal | N | 有则传 |
| longitude | 经度 | decimal | N | 有则传 |

extraData对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| businessType | 业务模式 | string(20) | N | 乐小融-够享借模式必传：0-代运营 |
| platformAmt | 平台额度 | decimal | N | 乐小融-够享借模式必传，单位元 |
| partnerCode | 合作方编码 | string(20) | N | 乐小融-够享借模式必传：fundloan |

请求参数示例：

```json
{
"creditReqNo": "CR07103777521223233233380",
"userNo": "U1703648207",
"fundUserNo": "1703648219",
"userBaseInfo": {
"userName": "小张",
"mobileNo": "12344434444"
},
"userProfileInfo": {
"marriage": "01",
"monthIncome": "01",
"education": "01",
"debtSituation": "01",
"expectedLoanAmt": 3000.00,
"expectedLoanTerm": 12,
"residentialType": "02",
"autoAddress": "上海市-上海市辖区-浦东新区",
"addressDetail": "上海市浦东新区花木街道杨高南路辅路中国石化上海浦东科研信息办公综合基地",
"residentialProvince": "上海市",
"residentialCity": "上海市辖区",
"residentialDistrict": "浦东新区",
"email": "4543949w899@163.com"
},
"cardInfo": {
"cardNo": "6230183543234564333333",
"bankCode": "0001",
"bankName": "中国银行",
"bankMobile": "134271364934"
},
"authIdInfo": {
"idCardFrontImgUrl": "http://example.com/身份证/正面照片.jpg",
"idCardBackImgUrl": "http://example.com/身份证/背面照片.jpg",
"idCardNo": "2343224422234094494",
"idCardSex": "0",
"idCardBirthday": "1979-08-23",
"idCardEthnicity": "汉",
"idCardAddress": "上海市浦东新区花木街道杨高南路辅路中国石化上海浦东科研信息办公综合基地",
"idCardStartDate": "20080314",
"idCardEndDate": "20180314",
"idCardAuthority": "深圳市公安局"
},
"authFaceInfo": {
"faceSource": 1,
"faceImg1Url": "http://example.com/活体照片1.jpg",
"faceImg2Url": "http://example.com/活体照片2.jpg",
"faceScore": 95.5,
"faceCollectTime": "2023-12-26 10:30:00"
},
"jobInfo": {
"jobIndustry": "01",
"jobCategory": "01",
"incomeType": "02",
"companyName": "天益传媒有限公司",
"companyType": "02",
"companyAddress": "西藏自治区张家港兴山澳门街G座",
"companyAddressDetail": "西藏自治区张家港兴山澳门街G座陈路B座",
"companyTel": "021-54722222"
},
"contactInfo": {
"contactOneName": "张大",
"contactOneTel": "13918239292",
"contactOneRel": "01",
"contactTwoName": "张大",
"contactTwoTel": "13918232312",
"contactTwoRel": "03"
},
"deviceInfo": {
"ip": "192.168.0.1",
"os": "ios"
},
"geoInfo": {
"latitude": "35.359542",
"longitude": "117.455610"
}
}
```

1.4.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 受理结果 | integer | Y | 1 - 受理成功；2 - 受理失败 |
| reasonDesc | 失败原因描述 | string(200) | O | 结果2时必传 |
| fundCreditNo | 机构授信申请号 | string(64) | N | 结果1时可传 |

响应参数示例：

```json
// 受理成功
{
"result": 1,
"fundCreditNo":"43848959939599495959"
}
// 受理失败
{
"result": 2,
"reasonDesc":"OCR姓名不符合规范"
}
```

<h4 id="nav-org-1-5">1.5 查询授信申请结果</h4>

1.5.1 调用场景

平台方请求机构合作方接口，查询用户授信申请结果。

1.5.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/creditResultQuery

1.5.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| creditReqNo | 平台授信申请号 | string(64) | Y |  |
| fundCreditNo | 机构授信申请号 | string(64) | N |  |

请求参数示例：

```json
{
"creditReqNo": "AP0710324673086914560",
"fundCreditNo": "123412341234"
}
```

1.5.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 授信结果 | string(8) | Y | CR101 - 授信成功（可继续调用额度查询接口）<br>CR102 - 授信拒绝<br>CR103 - 授信申请取消<br>CR104 - 待补件【暂不支持】<br>CR105 - 授信中<br>CR106 - 无记录（如因网络等问题，授信申请未实际提交到合作方，导致合作方查询不到对应流水号的申请结果，需返回CR106无记录） |
| fundCreditNo | 机构授信申请号 | string(64) | O | 结果CR101时必传 |
| reasonCode | 拒绝码 | string(8) | O | 结果CR102时必传<br>C1010 内部处理失败<br>C1011 资料缺失<br>C1021 风控审核拒绝<br>C1022 资方审核拒绝<br>C2001 其他 |
| reasonDesc | 拒绝原因描述 | string(256) | O | 结果CR102时必传 |
| creditFailTime | 授信拒绝时间 | string(32) | O | 结果CR102时必传，yyyy-mm-dd hh:mm:ss |
| creditFailFrozenTime | 授信被拒封禁期 | string(32) | O | 结果CR102时必传，yyyy-mm-dd hh:mm:ss |
| creditSuccTime | 授信成功时间 | string(32) | O | 结果CR101时必传，yyyy-mm-dd hh:mm:ss |
| creditAmt | 授信额度 | decimal(32) | O | 结果CR101时必传，单位元 |
| annualRate | 年利率 | string(16) | O | 结果CR101时必传，年利率 |
| creditCancelTime | 授信申请取消时间 | string(32) | O | 结果CR103时必传，yyyy-mm-dd hh:mm:ss |
| supplyType | 补件类型 | string(16) | O | 结果CR104时必传，ID / FACE / CONTACT / CARD |

响应参数示例：

```json
// 成功
{
"result": "CR101",
"creditSuccTime": "2023-12-27 11:11:11",
"creditAmt": "5000",
"annualRate": "4.35"
}
// 拒绝
{
"result": "CR102",
"reasonCode": "C1011",
"creditFailTime": "2023-12-27 11:11:11",
"reasonDesc": "身份证资料缺失"
}
// 取消
{
"result": "CR103",
"creditCancelTime": "2023-12-27 11:11:11"
}
// 待补件
{
"result": "CR104",
"reasonDesc": "需要补充资料",
"supplyType": "CONTACT"
}
// 授信申请中
{
"result": "CR105"
}
```

<h4 id="nav-san-biz-2">2. 借款相关接口</h4>

<h4 id="nav-org-2-1">2.1 借款试算</h4>

2.1.1 调用场景

平台方请求机构合作方接口，在借款申请提交前，进行借款试算，获取试算还款计划。

2.1.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/drawTrial

2.1.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| creditReqNo | 平台授信申请号 | string(64) | Y |  |
| fundCreditNo | 机构授信申请号 | string(64) | N |  |
| loanAmt | 试算借款金额 | decimal | Y | 单位：元(小数点后保留两位) |
| loanTerm | 试算借款期数 | integer | Y | 不支持传多个期数 |
| interestMethod | 计息方式 | integer | N | 1 - 按日计息；2 - 按月计息。默认为2 |
| repayMethod | 还款方式 | integer | N | 1 - 等本等息；2 - 等额本息；3 - 等额本金；4 - 先息后本；05 - 随借随还；6 - 到期还本；7 - 锁期。默认为2 |
| isPrivilegeTrial | 是否走权益试算 | string(1) | N | Y - 带权益试算；N - 不带权益试算。默认为Y |
| loanType | 借款类型 | string(2) | N | 1 - 普通借款；2 - 权益以外的非普通借款。  默认为1 |

请求参数示例：

```json
{
"creditReqNo": "AP0710324673086914560",
"loanAmt": 3 000.00,
"loanTerm": 3
}
```

2.1.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 试算结果 | integer(2) | Y | 1 - 试算成功<br>2 - 试算失败<br>结果为1时，业务数据才有值 |
| reasonDesc | 失败原因描述 | string(256) | O | 结果2时必传 |
| loanTerm | 借款期数 | integer | Y |  |
| loanAmt | 借款金额 | decimal | Y | 单位：元(小数点后保留两位) |
| loanYearRate | 借款年利率 | string(16) | Y | 0.154 |
| interestMethod | 计息方式 | integer | Y | 1 - 按日计息；2 - 按月计息 |
| repayMethod | 还款方式 | integer | Y | 1 - 等本等息；2 - 等额本息；3 - 等额本金；4 - 先息后本；05 - 随借随还；6 - 到期还本；7 - 锁期 |
| totalAmt | 应还总金额 | decimal | Y | 单位：元(小数点后保留两位) |
| totalPrinAmt | 应还总本金 | decimal | Y | 单位：元(小数点后保留两位) |
| totalIntAmt | 应还总利息 | decimal | Y | 单位：元(小数点后保留两位) |
| totalFeeAmt | 应还总费用 | decimal | Y | 单位：元(小数点后保留两位) |
| totalDebtConsultationFeeAmt | 应还债务咨询顾问服务费 | decimal | O | 单位：元(小数点后保留两位)<br>响应参数的loanType = 2 时必传 |
| loanRepayPlanList | 还款计划 | array[] | Y | 详见下表 |
| supportPrivilege | 支持权益 | string(1) | O | Y - 支持  N - 不支持 |
| privilegeName | 权益名称 | string(200) | O | 走权益流程时必传 |
| privilegeTotalAmt | 权益总金额 | decimal | O | 支持权益时必传<br>单位：元(小数点后保留两位) |
| privilegeTerm | 权益期数 | integer | O | 走权益流程时必传 |
| privilegeDesc | 权益说明 | string(256) | N | 权益包的介绍 |
| privilegeData | 权益包数据 | object | O | 权益内容 |
| privilegeDetailUrl | 权益详情展示 | string | N | 权益详情url |
| loanType | 借款类型 | string(2) | N | 1 - 普通借款；2 - AMC借款。默认为1 |
| amcInfo | AMC借款对象 | object（amcInfo） | O | loanType = 2 时有值 |

LoanRepayPlan对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| periodNo | 期数 | integer | Y |  |
| repayDate | 本期还款日 | string(10) | Y | 格式：yyyy-MM-dd |
| totalAmt | 本期应还总金额 | decimal | Y | 单位：元(小数点后保留两位) |
| prinAmt | 本期应还本金 | decimal | Y | 单位：元(小数点后保留两位) |
| intAmt | 本期应还利息 | decimal | Y | 单位：元(小数点后保留两位) |
| feeAmt | 本期应还费用 | decimal | Y | 单位：元(小数点后保留两位) |
| remark | 描述 | string(256) | N | 备注信息 |

privilegeData对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| name | 权益标题 | string（10） | Y | 单位：元(小数点后保留两位) |
| value | 权益价值 | string（10） | N | 单位：元(小数点后保留两位) |
| count | 权益次数 | string（10） | N | 单位： |
| unit | 权益次数单位 | string（10） | N | 单位：个，次，张等 |

amcInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| supportAmc | 是否支持amc | string(1) | Y | Y - 支持  N - 不支持<br>不管入参的loanType为何值，只要机构支持amc就要为Y |
| amcRepayPlanList | amc还款计划 | array[amcRepayPlan] | Y | supportAmc = Y 且  出参的loanType=2，则一定有值 |

amcRepayPlan对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| periodNo | 期数 | integer | Y |  |
| repayDate | 本期还款日 | string(10) | Y | 格式：yyyy-MM-dd |
| totalAmt | 本期应还总金额 | decimal | Y | 单位：元(小数点后保留两位) |
| debtConsultationFeeAmt | 本期应还债务咨询顾问服务费 | decimal | Y | 单位：元(小数点后保留两位) |

响应参数示例：

```json
{
"result": 1,
"loanTerm": 3,
"loanAmt": 3000,
"loanYearRate": "0.055",
"interestMethod": 1,
"repayMethod": 1,
"totalAmt": 3300,
"totalPrinAmt": 3000,
"totalIntAmt": 300,
"totalFeeAmt": 0,
"loanRepayPlanList": [
{
"periodNo": 1,
"repayDate": "2024-02-01",
"totalAmt": 1100,
"prinAmt": 1000,
"intAmt": 100,
"feeAmt": 0,
"remark": ""
},
{
"periodNo": 2,
"repayDate": "2024-03-01",
"totalAmt": 1100,
"prinAmt": 1000,
"intAmt": 100,
"feeAmt": 0,
"remark": ""
},
{
"periodNo": 3,
"repayDate": "2024-04-01",
"totalAmt": 1100,
"prinAmt": 1000,
"intAmt": 100,
"feeAmt": 0,
"remark": ""
}
],
"isPrivilegeProcess": "Y",
"privilegeName": "星星卡套餐",
"privilegeTotalAmt": 330,
"privilegeTerm": 3,
"privilegeRepayPlanList": [
{
"periodNo": 1,
"repayDate": "2024-02-01",
"totalAmt": 110,
"prinAmt": 100,
"intAmt": 10,
"feeAmt": 0,
"remark": ""
},
{
"periodNo": 2,
"repayDate": "2024-03-01",
"totalAmt": 110,
"prinAmt": 100,
"intAmt": 10,
"feeAmt": 0,
"remark": ""
},
{
"periodNo": 3,
"repayDate": "2024-04-01",
"totalAmt": 110,
"prinAmt": 100,
"intAmt": 10,
"feeAmt": 0,
"remark": ""
}
],
"privilegeData": [
{
"name": "话费抵充券",
"value": 39,
"count": 3,
"unit": "张"
}
]
}
```

<h4 id="nav-org-2-2">2.2 借款申请提交</h4>

2.2.1 调用场景

平台方请求机构合作方接口，提交借款申请。

2.2.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/drawSubmit

2.2.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| drawReqNo | 平台借款申请号 | string(64) | Y | 平台借款申请请求号。需要根据drawReqNo支持幂等。 |
| creditReqNo | 平台授信申请号 | string(64) | Y |  |
| userNo | 平台用户号 | string(64) | Y | 平台用户对外唯一标识 |
| fundUserNo | 机构方用户号 | string(64) | N | 机构方用户唯一标识 |
| drawApplyInfo | 用户借款申请信息 | object | Y | 详见下表 |
| deviceInfo | 设备信息 | object | N | 详见下表 |
| authFaceInfo | 用户活体信息 | object | N | 详见下表 |
| cardInfo | 用户银行卡信息 | object | N | 详见下表 |
| isPrivilegeProcess | 是否含权益 | string(1) | O | Y - 走权益流程；N - 不走权益流程<br>默认为N |
| extraData | 拓展信息 | object | O | 乐小融-够享借模式必传 |
| loanType | 借款类型 | string(2) | N | 1 - 普通借款；2 - AMC借款。默认为1 |

drawApplyInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| drawApplyTime | 申请时间 | string(20) | Y | 格式：yyyy-MM-dd HH:mm:ss |
| loanPurpose | 借款用途 | string(8) | N | 枚举值见附录 |
| loanAmt | 借款申请金额 | decimal | Y | 单位：元(小数点后保留两位) |
| loanTerm | 借款申请期数 | integer(2) | Y | 1，3，6，9，12，24，36 |
| interestMethod | 计息方式 | integer(2) | N | 1 - 按日计息；2 - 按月计息<br>默认为2 |
| repayMethod | 还款方式 | integer(2) | N | 1 - 等本等息；2 - 等额本息；3 - 等额本金；4 - 先息后本；05 - 随借随还；6 - 到期还本；7 - 锁期<br>默认为2 |

authFaceInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| faceSource | 活体供应商 | integer(2) | Y | 1 - 旷视；2 -微众；3 -阿里 |
| faceImg1Url | 活体照片1地址 | string(500) | Y | 示例：http://private-sit.oss-cn-shanghai.aliyuncs.com/private-sit/live/hub/UR0710959998205427712/1703584077691/5eek3g/HUB_LIVE.jpeg |
| faceImg1Base64 | 活体照片1base64 | string(200000) | N |  |
| faceImg2Url | 活体照片2地址 | string(500) | N |  |
| faceImg2Base64 | 活体照片2base64 | string(200000) | N |  |
| faceOriginData | 活体检测原始数据 | string(3000) | N |  |
| faceScore | 活体分 | decimal | N |  |
| faceCollectTime | 活体采集时间 | string(20) | N | 格式：yyyy-MM-dd HH:mm:ss |

cardInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| cardNo | 银行卡号 | string(32) | Y | 卡号明文 |
| bankCode | 银行编码 | string(32) | Y | 银行编码与银行名称，详见附录 |
| bankName | 银行名称 | string(64) | Y | 银行编码与银行名称，详见附录 |
| bankMobile | 银行预留手机号 | string(32) | Y | 银行预留手机号明文 |
| userName | 用户姓名 | string(64) | Y | 明文 |
| idNo | 用户身份证号 | string(30) | Y | 明文 |

deviceInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| ip | Ip地址 | string(32) | Y |  |
| os | 系统 | string(32) | Y | android, ios |
| deviceId | 设备号 | String | N | 有则传 |
| mac | mac地址 | String | N | 有则传 |
| isSimulator | 设备是否模拟器 | Integer | N | 0.否，1.是，2.未知。有则传 |
| isRoot | 设备是否越狱 | Integer | N | 0.否，1.是，2.未知。有则传 |

extraData对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| businessType | 业务模式 | string(20) | N | 乐小融-够享借模式必传：0-代运营 |
| partnerCode | 合作方编码 | string(20) | N | 乐小融-够享借模式必传：fundloan |

请求参数示例：

```json
{
"drawReqNo":"CR0716595246214803456",
"creditReqNo":"AP0710324673086914560",
"userNo":"UR0716595073412812800",
"fundUserNo":"FUR0716595073412812811",
"drawApplyInfo":{
"drawApplyTime":"2024-01-17 13:39:41",
"loanPurpose":"01",
"loanAmt":3000.00,
"loanTerm":3,
"interestMethod":2,
"repayMethod":2
},
"authFaceInfo":{
"faceSource":1,
"faceImg1Url":"http://example.com/活体照片1.jpg",
"faceImg1Base64":"base64-encoded-face-image1",
"faceImg2Url":"http://example.com/活体照片2.jpg",
"faceImg2Base64":"base64-encoded-face-image2",
"faceScore":95.5,
"faceCollectTime":"2024-01-17 13:39:41"
},
"isPrivilegeProcess":"Y"
}
```

2.2.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 受理结果 | integer(2) | Y | 1 - 受理成功；2 - 受理失败；3 - 需补充验证 |
| reasonDesc | 失败原因描述 | string(256) | O | 结果2时必传 |
| fundDrawNo | 机构借款申请号 | string(64) | N | 结果1时可传 |
| checkType | 验证类型 | array[integer] | O | 结果3时必传，需配合2.6获取下一步增验信息接口使用<br>1 - 活体（使用补充资料提交接口提交）<br>2 - 短信（机构验证，调用短信验证相关接口，需主动调用5.4发送验证码）<br>3 - 短信（机构验证，调用短信验证相关接口，机构静默发送短信，只需调用5.5验证验证码）<br>4 - 绑卡短信（机构资方验证，调用4.3、4.4绑卡验证相关接口）【暂不支持】<br>如需验证多项，按顺序给，默认先验证返回的第一项。 |
| smsType | 短信类型 | string(64) | O | checkType为2，3，4时，必传<br>1.资方绑卡短信<br>2.权益绑卡短信 |

响应参数示例：

```json
{
"result":3,
"fundDrawNo":"FCR0716595246214803456",
"checkType":[
1,
2
]
}
```

<h4 id="nav-org-2-3">2.3 查询放款结果</h4>

2.3.1 调用场景

平台方请求机构合作方接口，查询用户借款申请的放款结果。此接口可用于查询用户在平台侧发起的借款申请结果，也可以用于查询用户在机构合作方侧发起的借款申请结果（如：半流程机构，授信出额后，在机构APP发生的借款）。

2.3.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/drawResultQuery

2.3.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| drawReqNo | 平台借款申请号 | string(64) | N | 平台借款申请请求号。如带该参数请求，则只返回该笔信息。如未带该参数，则使用授信申请号，查授信申请下的所有借款（包括不在平台发生的借款）API借款该字段不为空优先使用该字段查询。 |
| fundDrawNo | 机构借款申请号 | string(64) | N | 机构借款申请号。如带该参数请求，则只返回该笔信息。如未带该参数，则使用授信申请号，查授信申请下的所有借款（包括不在平台发生的借款）H5借款该字段不为空优先使用该字段查询。 |
| creditReqNo | 平台授信申请号 | string(64) | Y |  |
| fundCreditNo | 机构授信申请号 | string(64) | N |  |

请求参数示例：

```json
{
"drawReqNo":"CR0716595246214803456",
"creditReqNo":"AP0710324673086914560"
}
```

2.3.4 响应参数

list形式返回（如需返回多笔放款，则list中有多笔；如只有一笔，则list中只有一笔；如果为空则按照空数组返回）

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| drawResultList | 放款结果数组 | 数组<DrawResult> | Y |  |

DrawResult对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 放款结果 | string(8) | Y | DR101 - 放款成功（可继续调用查询借据及还款计划接口）<br>DR102 - 放款失败<br>DR103 - 放款拒绝<br>DR104 - 放款申请取消<br>DR105 - 待补件【暂不支持】<br>DR106 - 需重新匹配资金方（需验证短信）<br>DR107 - 需重新匹配资金方（无需验证，直接发起新申请）【暂不支持】<br>DR108 - 放款中<br>DR109 - 无记录（查无记录；或者半流程机构，授信通过未放款；如因网络等问题，借款申请未实际提交到合作方，导致合作方查询不到对应流水号的申请结果，需返回DR109无记录） |
| drawStatusUpdateTime | 放款状态变更时间 | string(20) | Y | 状态变更时必传，格式：yyyy-MM-dd HH:mm:ss |
| fundDrawNo | 机构借款申请号 | string(64) | O | 结果非DR109时必传 |
| drawReqNo | 平台借款申请号 | string(64) | O | 结果非DR109时，如果从平台发起的借款必传 |
| loanAmt | 放款金额 | decimal | O | 结果为DR101时必传，单位元 |
| loanTerm | 放款期数 | integer | O | 结果为DR101时必传 |
| reasonCode | 失败原因码 | string(8) | O | 结果为DR102、DR103时必传<br>D1010 内部处理失败<br>D1011 资料缺失<br>D1021 风控拒绝<br>D1022 资方审核拒绝<br>D2001 其他 |
| reasonDesc | 失败原因描述 | string(256) | O | 结果为DR102、DR103时必传 |
| drawFreezeEndTime | 放款冻结结束时间 | string(20) | O | 结果为DR102、DR103、DR104 时可传<br>格式：yyyy-MM-dd HH:mm:ss |
| supplyType | 补件类型 | string(10) | O | 结果为DR105时必传，ID / FACE / CONTACT / PROFILE / CARD |
| isReloan | 首复贷标识 | integer | O | 结果为DR101-放款成功时可传<br>0-首贷，1-复贷 |
| capitalCode | 出资机构编码 | string(64) | N | 乐小融-够享借模式必传 |

响应参数示例：

```json
{
"drawResultList": [
{
"result": "DR101",
"drawStatusUpdateTime": "2024-01-17 13:39:41",
"fundDrawNo": "FCR0716595246214803456",
"drawReqNo": "CR0716595246214803456",
"loanAmt": 3000,
"loanTerm": 3,

},
{
"result": "DR101",
"drawStatusUpdateTime": "2024-01-17 13:39:41",
"fundDrawNo": "FCR0716595246214803456",
"drawReqNo": "CR0716595246214803457",
"loanAmt": 3000,
"loanTerm": 6,

}
]
}
```

<h4 id="nav-org-2-4">2.4 查询借据及还款计划</h4>

2.4.1 调用场景

平台方请求机构合作方接口，在放款结果变更、发生还款后，查询用户的借据和还款计划信息。

2.4.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/loanPlanQuery

2.4.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| drawReqNo | 平台借款申请号 | string(64) | N | 平台借款申请请求号 |
| fundDrawNo | 机构借款申请号 | string(64) | Y |  |

请求参数示例：

```json
{
"drawReqNo":"CR0716595246214803456",
"fundDrawNo": "FCR0716595246214803456"
}
```

2.4.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| loanAmt | 放款金额 | decimal | Y | 单位：元(小数点后保留两位) |
| loanTerm | 放款期数 | integer | Y |  |
| loanYearRate | 放款年利率 | string(16) | Y | 默认传IRR计算方式下的年利率。传0.154代表IRR年利率15.4% |
| loanSuccTime | 放款成功时间 | string(20) | Y | 格式：yyyy-MM-dd HH:mm:ss |
| interestMethod | 计息方式 | integer | Y | 1 - 按日计息；2 - 按月计息 |
| repayMethod | 还款方式 | integer | Y | 1 - 等本等息；2 - 等额本息；3 - 等额本金；4 - 先息后本；5 - 随借随还；6 - 到期还本；7 - 锁期 |
| cardNo | 放款银行卡号 | string(32) | N | 卡号明文 |
| bankCode | 放款银行编码 | string(32) | N | 银行编码与银行名称，详见附录 |
| bankName | 放款银行名称 | string(64) | N | 银行编码与银行名称，详见附录 |
| bankMobile | 放款银行预留手机号 | string(32) | N | 银行预留手机号明文 |
| loanStatus | 借据状态 | string(2) | Y | 01 - 还款中；02 - 逾期中；03 - 已结清；04 - 已退贷 |
| loanSettleTime | 结清时间 | string(20) | O | 借据状态03时必传，格式：yyyy-MM-dd HH:mm:ss |
| loanCancelTime | 退贷时间 | string(20) | O | 借据状态04时必传，格式：yyyy-MM-dd HH:mm:ss |
| loanOverdueDays | 逾期天数 | integer | O | 借据状态02时必传 |
| loanRepayPlanList | 借据还款计划 | array[LoanRepayPlan] | Y |  |

LoanRepayPlan对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| periodNo | 当期期数 | integer | Y |  |
| dateDue | 应还款日 | string(10) | Y | 格式：yyyy-MM-dd |
| timeRepayEarliest | 最早可还款时间 | string(20) | O | 支持提前还当期时必传。如不传，默认最早可还款时间和应还款日一样。<br>格式：yyyy-MM-dd HH:mm:ss |
| deserveTotalAmt | 应还总金额 | decimal | Y | 还款计划生成后不再变化。单位元，支持小数点后两位。下同。 |
| deservePrinAmt | 应还本金 | decimal | Y |  |
| deserveIntAmt | 应还利息 | decimal | Y |  |
| deserveOintAmt | 应还罚息 | decimal | Y |  |
| deserveLateFeeAmt | 应还滞纳金 | decimal | N |  |
| deservePenaltyAmt | 应还违约金 | decimal | N |  |
| deserveOtherFeeAmt | 应还其他费用 | decimal | N |  |
| actTotalAmt | 已还总金额 | decimal | Y | 单位元，支持小数点后两位。下同。 |
| actPrinAmt | 已还本金 | decimal | Y |  |
| actIntAmt | 已还利息 | decimal | Y |  |
| actOintAmt | 已还罚息 | decimal | Y |  |
| actLateFeeAmt | 已还滞纳金 | decimal | N |  |
| actPenaltyAmt | 已还违约金 | decimal | N |  |
| actOtherFeeAmt | 已还其他费用 | decimal | N |  |
| actDeductTotalAmt | 已减免总金额 | decimal | N |  |
| actDeductPrinAmt | 已减免本金 | decimal | N |  |
| actDeductIntAmt | 已减免利息 | decimal | N |  |
| actDeductOintAmt | 已减免罚息 | decimal | N |  |
| actDeductLateFeeAmt | 已减免滞纳金 | decimal | N |  |
| actDeductPenaltyAmt | 已减免违约金 | decimal | N |  |
| actDeductOtherFeeAmt | 已减免其他费用 | decimal | N |  |
| payType | 当期扣款方式 | string(2) | N | 01 - 系统批量扣款；02 - 客户主动还款 |
| status | 当期状态 | string(2) | Y | 01 - 待还款；02 - 逾期中；03 - 当期已结清 |
| overdueDays | 当期逾期天数 | integer | O | 当期状态为02时必传，每一期的逾期天数 |
| settleTime | 当期结清时间 | string(20) | O | 当期状态为03时必传，格式：yyyy-MM-dd HH:mm:ss |
| remark | 描述 | string(256) | N | 备注信息 |

响应参数示例：

```json
{
"loanAmt":1000.00,
"loanTerm":3,
"loanYearRate":"0.055",
"loanSuccTime":"2024-01-17 13:39:41",
"interestMethod":2,
"repayMethod":2,
"cardNo":"1234567890123456",
"bankCode":"1234",
"bankName":"Example Bank",
"bankMobile":"1234567890",
"loanStatus":"01",
"loanSettleTime":null,
"loanCancelTime":null,
"loanOverdueDays":0,
"loanRepayPlanList":[
{
"periodNo":1,
"dateDue":"2024-01-17",
"timeRepayEarliest":"2024-01-17 13:39:41",
"deserveTotalAmt":1000,
"deservePrinAmt":800,
"deserveIntAmt":200,
"deserveOintAmt":0,
"deserveLateFeeAmt":0,
"deserveOtherFeeAmt":0,
"actTotalAmt":0,
"actPrinAmt":0,
"actIntAmt":0,
"actOintAmt":0,
"actLateFeeAmt":0,
"actOtherFeeAmt":0,
"actDeductTotalAmt":0,
"actDeductPrinAmt":0,
"actDeductIntAmt":0,
"actDeductOintAmt":0,
"actDeductLateFeeAmt":0,
"actDeductOtherFeeAmt":0,
"payType":"01",
"status":"01",
"overdueDays":0,
"settleTime":0,
"remark":""
},
{
"periodNo":2,
"dateDue":"2024-02-17",
"timeRepayEarliest":"2024-01-27 13:39:41",
"deserveTotalAmt":1000,
"deservePrinAmt":800,
"deserveIntAmt":200,
"deserveOintAmt":0,
"deserveLateFeeAmt":0,
"deserveOtherFeeAmt":0,
"actTotalAmt":0,
"actPrinAmt":0,
"actIntAmt":0,
"actOintAmt":0,
"actLateFeeAmt":0,
"actOtherFeeAmt":0,
"actDeductTotalAmt":0,
"actDeductPrinAmt":0,
"actDeductIntAmt":0,
"actDeductOintAmt":0,
"actDeductLateFeeAmt":0,
"actDeductOtherFeeAmt":0,
"payType":"01",
"status":"01",
"overdueDays":0,
"settleTime":0,
"remark":""
},
{
"periodNo":3,
"dateDue":"2024-03-17",
"timeRepayEarliest":"2024-03-17 13:39:41",
"deserveTotalAmt":1000,
"deservePrinAmt":800,
"deserveIntAmt":200,
"deserveOintAmt":0,
"deserveLateFeeAmt":0,
"deserveOtherFeeAmt":0,
"actTotalAmt":0,
"actPrinAmt":0,
"actIntAmt":0,
"actOintAmt":0,
"actLateFeeAmt":0,
"actOtherFeeAmt":0,
"actDeductTotalAmt":0,
"actDeductPrinAmt":0,
"actDeductIntAmt":0,
"actDeductOintAmt":0,
"actDeductLateFeeAmt":0,
"actDeductOtherFeeAmt":0,
"payType":"01",
"status":"01",
"overdueDays":0,
"settleTime":0,
"remark":""
}
]
}
```

<h4 id="nav-org-2-5">2.5 查询权益订单及还款计划</h4>

2.5.1 调用场景

平台方请求机构合作方接口，在放款成功带独立的权益信息、权益订单状态变更、权益发生还款后，查询用户的权益订单和还款计划信息。

2.5.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/privilegePlanQuery

2.5.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| drawReqNo | 平台借款申请号 | string(64) | N | 平台借款申请请求号 |
| fundDrawNo | 机构借款申请号 | string(64) | Y |  |

请求参数示例：

```json
{
"drawReqNo":"CR0716595246214803456",
"fundDrawNo": "FCR0716595246214803456"
}
```

2.5.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| fundPrivilegeOrderNo | 机构权益订单号 | string(64) | N |  |
| privilegeName | 权益名称 | string(20) | Y |  |
| privilegeAmt | 权益金额 | decimal | Y | 单位元 |
| privilegeTerm | 权益期数 | integer | Y |  |
| privilegePurchaseTime | 权益购买时间 | string(20) | Y | 格式：yyyy-MM-dd HH:mm:ss |
| privilegeActivateTime | 权益激活时间 | string(20) | Y | 格式：yyyy-MM-dd HH:mm:ss |
| privilegeStatus | 权益订单状态 | string(2) | Y | 00 - 处理中；01 - 还款中；02 - 逾期中；03 - 已结清；04 - 已退贷 ；05-已关单 |
| paidAmount | 支付金额 | string(20) | O | 权益订单状态03时必传 |
| privilegeSettleTime | 结清时间 | string(20) | O | 权益订单状态03时必传，格式：yyyy-MM-dd HH:mm:ss |
| privilegeCancelTime | 退贷时间 | string(20) | O | 权益订单状态04时必传，格式：yyyy-MM-dd HH:mm:ss |
| refundAmount | 退贷金额 | string(20) | O | 权益订单状态04时必传 |
| privilegeExpireTime | 过期时间 | string(20) | N | 可行权时必传<br>格式：yyyy-MM-dd HH:mm:ss |
| privilegeOverdueDays | 逾期天数 | integer | O | 权益订单状态02时必传 |
| privilegeRepayPlanList | 权益还款计划 | array[PrivilegeRepayPlan] | Y |  |

PrivilegeRepayPlan对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| periodNo | 当期期数 | integer | Y |  |
| dateDue | 应还款日 | string(10) | Y | 格式：yyyy-MM-dd |
| timeRepayEarliest | 最早可还款时间 | string(20) | O | 支持提前还当期时必传。如不传，默认最早可还款时间和应还款日一样。<br>格式：yyyy-MM-dd HH:mm:ss |
| deserveTotalAmt | 应还总金额 | decimal | Y | 还款计划生成后不再变化。单位元，支持小数点后两位。下同。 |
| deservePrinAmt | 应还本金 | decimal | N |  |
| deserveIntAmt | 应还利息 | decimal | N |  |
| deserveOintAmt | 应还罚息 | decimal | N |  |
| deserveLateFeeAmt | 应还滞纳金 | decimal | N |  |
| deserveOtherFeeAmt | 应还其他费用 | decimal | N |  |
| actTotalAmt | 已还总金额 | decimal | Y | 单位元，支持小数点后两位。下同。 |
| actPrinAmt | 已还本金 | decimal | N |  |
| actIntAmt | 已还利息 | decimal | N |  |
| actOintAmt | 已还罚息 | decimal | N |  |
| actLateFeeAmt | 已还滞纳金 | decimal | N |  |
| actOtherFeeAmt | 已还其他费用 | decimal | N |  |
| actDeductTotalAmt | 已减免总金额 | decimal | N |  |
| actDeductPrinAmt | 已减免本金 | decimal | N |  |
| actDeductIntAmt | 已减免利息 | decimal | N |  |
| actDeductOintAmt | 已减免罚息 | decimal | N |  |
| actDeductLateFeeAmt | 已减免滞纳金 | decimal | N |  |
| actDeductOtherFeeAmt | 已减免其他费用 | decimal | N |  |
| payType | 当期扣款方式 | string(2) | N | 01 - 系统批量扣款；02 - 客户主动还款 |
| status | 当期状态 | string(2) | Y | 01 - 待还款；02 - 逾期中；03 - 当期已结清 |
| overdueDays | 当期逾期天数 | integer | O | 当期状态为02时必传，每一期的逾期天数 |
| settleTime | 当期结清时间 | string(20) | O | 当期状态为03时必传，格式：yyyy-MM-dd HH:mm:ss |
| remark | 描述 | string(256) | N | 备注信息 |

响应参数示例：

```json
{
"privilegeAmt":5000,
"privilegeTerm":3,
"privilegePurchaseTime":"2024-01-17 13:39:41",
"privilegeActivateTime":"2024-01-17 13:39:41",
"privilegeStatus":"01",
"privilegeSettleTime":0,
"privilegeCancelTime":0,
"privilegeOverdueDays":0,
"privilegeRepayPlanList":[
{
"periodNo":1,
"dateDue":"2024-01-17",
"timeRepayEarliest":"2024-01-17 13:39:41",
"deserveTotalAmt":1000,
"deservePrinAmt":800,
"deserveIntAmt":200,
"deserveOintAmt":null,
"deserveLateFeeAmt":null,
"deserveOtherFeeAmt":null,
"actTotalAmt":0,
"actPrinAmt":0,
"actIntAmt":0,
"actOintAmt":0,
"actLateFeeAmt":0,
"actOtherFeeAmt":0,
"actDeductTotalAmt":0,
"actDeductPrinAmt":0,
"actDeductIntAmt":0,
"actDeductOintAmt":0,
"actDeductLateFeeAmt":0,
"actDeductOtherFeeAmt":0,
"payType":"01",
"status":"01",
"overdueDays":0,
"settleTime":0,
"remark":""
},
{
"periodNo":2,
"dateDue":"2024-02-17",
"timeRepayEarliest":"2024-02-17 13:39:41",
"deserveTotalAmt":1000,
"deservePrinAmt":800,
"deserveIntAmt":200,
"deserveOintAmt":null,
"deserveLateFeeAmt":null,
"deserveOtherFeeAmt":null,
"actTotalAmt":0,
"actPrinAmt":0,
"actIntAmt":0,
"actOintAmt":0,
"actLateFeeAmt":0,
"actOtherFeeAmt":0,
"actDeductTotalAmt":0,
"actDeductPrinAmt":0,
"actDeductIntAmt":0,
"actDeductOintAmt":0,
"actDeductLateFeeAmt":0,
"actDeductOtherFeeAmt":0,
"payType":"01",
"status":"01",
"overdueDays":0,
"settleTime":0,
"remark":""
},
{
"periodNo":3,
"dateDue":"2024-03-17",
"timeRepayEarliest":"2024-03-17 13:39:41",
"deserveTotalAmt":1000,
"deservePrinAmt":800,
"deserveIntAmt":200,
"deserveOintAmt":null,
"deserveLateFeeAmt":null,
"deserveOtherFeeAmt":null,
"actTotalAmt":0,
"actPrinAmt":0,
"actIntAmt":0,
"actOintAmt":0,
"actLateFeeAmt":0,
"actOtherFeeAmt":0,
"actDeductTotalAmt":0,
"actDeductPrinAmt":0,
"actDeductIntAmt":0,
"actDeductOintAmt":0,
"actDeductLateFeeAmt":0,
"actDeductOtherFeeAmt":0,
"payType":"01",
"status":"01",
"overdueDays":0,
"settleTime":0,
"remark":""
}
]
}
```

<h4 id="nav-org-2-6">2.6 获取借款下一步增验信息</h4>

2.6.1 调用场景

平台方请求机构合作方接口，查询用户在借款申请提交后续验证步骤中的当前验证信息。

2.6.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/drawStepQuery

2.6.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| drawReqNo | 平台借款申请号 | string(64) | Y | 平台借款申请请求号 |
| creditReqNo | 平台授信申请号 | string(64) | Y |  |

请求参数示例：

```json
{
"drawReqNo":"CR0716595246214803456",
"creditReqNo":"AP0710324673086914560",
"userNo":"UR0716595073412812800",
"fundUserNo":"FUR0716595073412812811",
}
```

2.6.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 是否需要继续验证 | integer(2) | Y | 1 - 无需验证；2  - 需继续验证 |
| fundDrawNo | 机构借款申请号 | string(64) | Y | 结果为1时可传 |
| nextStep | 下一步验证信息 | string(64) | O | 结果2时必传<br>1 - 活体（使用补充资料提交接口提交）<br>2 - 短信（机构验证，调用短信验证相关接口，需主动调用5.4发送验证码）<br>3 - 短信（机构验证，调用短信验证相关接口，机构静默发送短信，只需调用5.5验证验证码）<br>4 - 绑卡短信（机构验证，调用4.3、4.4绑卡验证相关接口）【暂不支持】<br>如需验证多项，按顺序给。 |
| validTime | 验证截止时间 | string(20) | N | 格式：yyyy-MM-dd HH:mm:ss<br>过期后需要重新发起借款申请 |
| smsType | 短信类型 | string(64) | O | nextStep为2，3，4时，必传<br>1 资方绑卡短信<br>2权益绑卡短信 |

响应参数示例：

```json
{
"fundDrawNo":"FCR0716595246214803456",
"result":"2",
"nextStep": "2",
"validTime": "2024-01-01 12:00:00"，
"smsType":"1"
}
```

<h4 id="nav-org-2-7">2.7 查询AMC订单及还款计划</h4>

2.7.1 调用场景

平台方请求机构合作方接口，在放款成功带独立的AMC信息、AMC订单状态变更、AMC发生还款后，查询用户的AMC订单和还款计划信息。

2.7.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/amcPlanQuery

2.7.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| drawReqNo | 平台借款申请号 | string(64) | N | 平台借款申请请求号 |
| fundDrawNo | 机构借款申请号 | string(64) | Y |  |

请求参数示例：

| JSON |
| --- |

2.7.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| fundOrderNo | 机构AMC订单号 | string(64) | Y |  |
| amt | AMC金额 | decimal | Y | 单位：元(小数点后保留两位) |
| term | AMC期数 | integer | Y |  |
| status | AMC订单状态 | string(2) | Y | 00 - 处理中；01 - 还款中；02 - 逾期中；03 - 已结清；04 - 已退贷 ；05-已关单 |
| settleTime | 结清时间 | string(20) | O | AMC订单状态03时必传，格式：yyyy-MM-dd HH:mm:ss |
| cancelTime | 退贷时间 | string(20) | O | AMC订单状态04时必传，格式：yyyy-MM-dd HH:mm:ss |
| refundAmount | 退贷金额 | string(20) | O | AMC订单状态04时必传 |
| overdueDays | 逾期天数 | integer | O | 权益订单状态02时必传 |
| repayPlanList | AMC还款计划 | array[amcRpayPlan] | Y |  |

amcRpayPlan对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| periodNo | 当期期数 | integer | Y |  |
| dateDue | 应还款日 | string(10) | Y | 格式：yyyy-MM-dd |
| timeRepayEarliest | 最早可还款时间 | string(20) | O | 支持提前还当期时必传。如不传，默认最早可还款时间和应还款日一样。<br>格式：yyyy-MM-dd HH:mm:ss |
| deserveTotalAmt | 应还总金额 | decimal | Y | 还款计划生成后不再变化。单位元，支持小数点后两位。下同。 |
| deserveDebtConsultationFeeAmt | 应还债务咨询顾问服务费 | decimal | Y |  |
| deserveDebtConsultationPenaltyAmt | 应还债务咨询顾问服务违约金 | decimal | N |  |
| actTotalAmt | 已还总金额 | decimal | Y | 单位元，支持小数点后两位。下同。 |
| actDebtConsultationFeeAmt | 已还债务咨询顾问服务费 | decimal | N |  |
| actDebtConsultationPenaltyAmt | 已还债务咨询顾问服务违约金 | decimal | N |  |
| actDeductTotalAmt | 已减免总金额 | decimal | N |  |
| actDeductDebtConsultationFeeAmt | 已减免债务咨询顾问服务费 | decimal | N |  |
| actDeductDebtConsultationPenaltyAmt | 已减免债务咨询顾问服务违约金 | decimal | N |  |
| payType | 当期扣款方式 | string(2) | N | 01 - 系统批量扣款；02 - 客户主动还款 |
| status | 当期状态 | string(2) | Y | 01 - 待还款；02 - 逾期中；03 - 当期已结清 |
| overdueDays | 当期逾期天数 | integer | O | 当期状态为02时必传，每一期的逾期天数 |
| settleTime | 当期结清时间 | string(20) | O | 当期状态为03时必传，格式：yyyy-MM-dd HH:mm:ss |
| remark | 描述 | string(256) | N | 备注信息 |

响应参数示例：

| JSON |
| --- |

<h4 id="nav-san-biz-3">3. 还款相关接口</h4>

<h4 id="nav-org-3-1">3.1 查询待还款列表</h4>

3.1.1 调用场景

平台方请求机构合作方接口，查询用户在机构合作方的所有未还款借据的待还款列表。

3.1.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/repayListQuery

3.1.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userNo | 平台用户号 | string(64) | Y | 平台用户对外唯一标识 |
| fundUserNo | 机构方用户号 | string(64) | N | 机构方用户唯一标识 |

请求参数示例：

```json
{
"userNo":"UR0696455066729598976",
"fundUserNo":"HL1729873129873129"
}
```

3.1.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userNo | 平台用户号 | string(64) | Y | 平台用户对外唯一标识 |
| fundUserNo | 机构方用户号 | string(64) | N | 机构方用户唯一标识 |
| repayInfoList | 待还信息 | array[RepayInfo] | Y | 机构待还信息 |

RepayInfo

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| drawReqNo | 平台借款申请号 | string(64) | Y | 平台借款申请请求号 |
| fundDrawNo | 机构借款申请号 | string(64) | N |  |
| creditReqNo | 机构授信号 | string(64) | Y |  |
| dateLoan | 借款申请时间 | string(20) | Y | 格式：yyyy-MM-dd HH:mm:ss |
| repayPlanList | 待还列表 | array[RepayPlan] | Y |  |
| privilegeRepayPlanList | 权益待还列表 | array[PrivilegeRepayPlan] | Y |  |

RepayPlan

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| periodNo | 期数 | integer | Y |  |
| dateDue | 应还款日 | string | Y | 格式：yyyy-MM-dd |
| overdueDays | 逾期天数 | integer | Y |  |
| deserveTotalAmt | 应还总金额 | decimal | Y | 单位（元） |
| deservePrinAmt | 应还本金 | decimal | Y | 单位（元） |
| deserveIntAmt | 应还利息 | decimal | Y | 单位（元） |
| deserveOintAmt | 应还罚息 | decimal | Y | 单位（元） |
| deserveLateFeeAmt | 应还滞纳金 | decimal | N | 逾期状态必传，单位（元） |
| deserveOtherFeeAmt | 应还其他费用 | decimal | N | 单位（元） |

PrivilegeRepayPlan

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| periodNo | 期数 | integer | Y |  |
| dateDue | 应还款日 | string | Y | 格式：yyyy-MM-dd |
| overdueDays | 逾期天数 | integer | Y |  |
| deserveTotalAmt | 应还总金额 | decimal | Y | 单位（元） |
| deservePrinAmt | 应还本金 | decimal | Y | 单位（元） |
| deserveIntAmt | 应还利息 | decimal | Y | 单位（元） |
| deserveOintAmt | 应还罚息 | decimal | Y | 单位（元） |
| deserveLateFeeAmt | 应还滞纳金 | decimal | N | 逾期状态必传，单位（元） |
| deserveOtherFeeAmt | 应还其他费用 | decimal | N | 单位（元） |

响应参数示例：

```json
{
"userNo":"UR12789312798311231",
"fundUserNo":"FUR0716595073412812811",
"repayInfoList":[
{
"drawReqNo":"CR0716595246214803456",
"fundDrawNo":"FCR0716595246214803456",
"creditReqNo":"AP0710324673086914560",
"dateLoan":"2024-01-10 12:30:00",
"repayPlanList":[
{
"periodNo":1,
"dateDue":"2024-01-17",
"overdueDays":0,
"deserveTotalAmt":1000,
"deservePrinAmt":800,
"deserveIntAmt":200,
"deserveOintAmt":0,
"deserveLateFeeAmt":0,
"deserveOtherFeeAmt":0
},
{
"periodNo":2,
"dateDue":"2024-02-17",
"overdueDays":0,
"deserveTotalAmt":1000,
"deservePrinAmt":800,
"deserveIntAmt":200,
"deserveOintAmt":0,
"deserveLateFeeAmt":0,
"deserveOtherFeeAmt":0
},
{
"periodNo":3,
"dateDue":"2024-03-17",
"overdueDays":0,
"deserveTotalAmt":1000,
"deservePrinAmt":800,
"deserveIntAmt":200,
"deserveOintAmt":0,
"deserveLateFeeAmt":0,
"deserveOtherFeeAmt":0
}
]
}
]
}
```

<h4 id="nav-org-3-2">3.2 还款试算</h4>

3.2.1 调用场景

平台方请求机构合作方接口，在还款申请提交前，进行还款试算，获取应还金额信息。可区分不同类型试算。

3.2.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/repayTrial

3.2.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userNo | 平台用户号 | string(64) | Y |  |
| drawReqNo | 平台借款申请号 | string(64) | N | 平台借款申请号和机构借款申请号，必须传一个 |
| fundDrawNo | 机构借款申请号 | string(64) | N |  |
| trialType | 试算还款类型 | integer(2) | Y | 1 - 当期还款（必须按顺序，不能跳期）<br>2 - 逾期还款（单期）【2和3仅支持其中一种】<br>3 - 逾期还款（多期合并）【2和3仅支持其中一种】<br>4 - 整笔提前结清 |
| trialPeriods | 试算还款期数 | array[integer] | Y | 多期试算用逗号隔开 |
| orderType | 试算还款订单类型 | string(2) | O | 1 - 借据+AMC（必须按顺序，不能跳期）<br>2 - AMC（必须按顺序，不能跳期）<br>3 - 借据（必须按顺序，不能跳期）<br>借款为AMC模式必传 |

请求参数示例：

```json
{
"userNo": "UR0696455066729598976",
"drawReqNo": "DR718293712983712",
"fundDrawNo": "FDR81209381093810",
"trialType": 1,
"trialPeriods": [1]
}
```

3.2.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 试算结果 | integer(2) | Y | 1 - 试算成功<br>2 - 试算失败<br>结果为1时，业务数据才有值 |
| reasonDesc | 失败原因描述 | string(256) | O | 结果2时必传，尽量详细，我方会透传给用户 |
| userNo | 平台用户号 | string(64) | Y | 平台用户号 |
| drawReqNo | 平台借款申请号 | string(64) | N | 平台借款申请号 |
| deserveTotalAmt | 应还总金额 | decimal | Y | 单位（元） |
| deservePrinAmt | 应还本金 | decimal | Y | 单位（元） |
| deserveIntAmt | 应还利息 | decimal | Y | 单位（元） |
| deserveOintAmt | 应还罚息 | decimal | Y | 单位（元） |
| deserveLateFeeAmt | 应还滞纳金 | decimal | N | 单位（元） |
| deservePenaltyAmt | 应还违约金 | decimal | N | 单位（元） |
| deserveOtherFeeAmt | 应还其他费用 | decimal | N | 单位（元） |
| deserveDebtConsultationFeeAmt | 应还债务咨询顾问服务费 | decimal | O | 单位（元）<br>orderType=1或2时必传 |
| deserveDebtConsultationPenaltyAmt | 应还债务咨询顾问服务违约金 | decimal | O | 单位（元）<br>orderType=1或2时必传 |

响应参数示例：

```json
{
"result":1,
"userNo":"UR0696455066729598976",
"drawReqNo":"DR718293712983712",
"deserveTotalAmt":1000.00,
"deservePrinAmt":800.00,
"deserveIntAmt":200.00,
"deserveOintAmt":0,
"deserveLateFeeAmt":0,
"deserveOtherFeeAmt":0
}
```

<h4 id="nav-org-3-3">3.3 还款申请提交</h4>

3.3.1 调用场景

平台方请求机构合作方接口，完成各种必要的前置校验后，提交还款申请。

3.3.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/repaySubmit

3.3.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| repayReqNo | 平台还款申请号 | string(64) | Y | 平台还款申请请求号 |
| drawReqNo | 平台借款申请号 | string(64) | N | 平台借款申请号和机构借款申请号，必须传一个 |
| fundDrawNo | 机构借款申请号 | string(64) | N |  |
| repayType | 还款方式 | integer(2) | N | 1 - 当期还款（必须按顺序，不能跳期）<br>2 - 逾期还款（单期）<br>3 - 逾期还款（多期合并）<br>4 - 整笔提前结清 |
| repayApplyTime | 还款申请时间 | string | Y | 用户还款申请提交时间 yyyy-MM-dd HH:mm:ss |
| repayApplyAmt | 还款申请金额 | decimal | Y | 还款申请金额，单位（元） |
| periods | 还款期数 | array[integer] | Y | 多期[1,2,3,4] |
| cardNo | 银行卡号 | string(32) | Y | 还款银行卡号 |
| bankMobile | 银行预留手机号 | string(32) | Y |  |
| orderType | 试算还款订单类型 | string(2) | O | 1 - 借据+AMC（必须按顺序，不能跳期）<br>2 - AMC（必须按顺序，不能跳期）<br>3 - 借据（必须按顺序，不能跳期）<br>AMC模式必传 |

请求示例

```json
{
"repayReqNo": "RR182093812093812",
"drawReqNo": "DR718293712983712",
"fundDrawNo": "FD71298371298371",
"repayType": 1,
"repayApplyTime": "2024-01-10 14:30:00",
"repayApplyAmt": "1000.00",
"cardNo": "622202132385058530",
"bankMobile": "13781319899",
"periods": [1, 2, 3]
}
```

3.3.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 受理结果 | integer(2) | Y | 1 - 受理成功；2 - 受理失败；3 - 需补充验证 |
| fundRepayNo | 机构还款申请号 | string(64) | N | 结果1时可传 |
| reasonDesc | 失败原因描述 | string | O | 结果2时必传 |
| checkType | 验证类型 | array[integer] | O | 1 - 短信（机构验证，调用短信验证相关接口，需<br>主动调用5.4发送验证码）<br>2 - 短信（机构验证，调用短信验证相关接口，机构静默发送短信，只需调用5.5验证验证码） |

响应参数示例：

```json
{
"result":1,
"fundRepayNo":"FRP81902380192381",
"reasonDesc":null,
"checkType":[
1
]
}
```

<h4 id="nav-org-3-4">3.4 查询还款结果</h4>

3.4.1 调用场景

平台方请求机构合作方接口，查询用户还款结果。

3.4.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/repayResultQuery

3.4.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| repayReqNo | 平台还款申请号 | string(64) | Y | 平台还款申请请求号 |
| fundRepayNo | 机构还款申请号 | string(64) | N |  |

请求参数示例：

```json
{
"repayReqNo": "RR182093812093812",
"fundRepayNo": "FRP81902380192381"
}
```

3.4.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| repayReqNo | 平台还款申请号 | string(64) | Y |  |
| fundRepayNo | 机构还款申请号 | string(64) | N |  |
| result | 还款结果 | integer(2) | Y | 1 - 还款成功（可继续调用查询借据及还款计划接口）<br>2 - 还款失败<br>3 - 还款处理中<br>4 - 无记录 |
| payType | 支付方式 | integer(2) | Y | 1 - 主动还款，2-批扣， 3 - 线下还款， 4 - 其他 |
| repayDesc | 还款描述 | string | O | 结果2时必传 |
| repayDetailInfo | 还款成功详情 | object | O | 结果1时必传 |

repayDetailInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| repaySuccTime | 还款成功时间 | string(20) | Y | yyyy-MM-dd HH:mm:ss |
| repayAmt | 还款总金额 | decimal | Y | 单位（元） |
| repayTerm | 还款期数 | array[integer] | Y | 如为多期还款，用逗号隔开 |
| cardNo | 还款银行卡号 | string(32) | N | 卡号明文 |
| bankCode | 还款银行编码 | string(32) | N | 银行编码与银行名称，详见附录 |
| bankName | 还款银行名称 | string(64) | N | 银行编码与银行名称，详见附录 |
| bankMobile | 还款银行预留手机号 | string(32) | N | 银行预留手机号明文 |

响应参数示例：

```json
{
"result":1,
"payType":1,
"reasonDesc":"还款成功",
"repayDetailInfo":{
"repaySuccTime":"2024-01-15 10:30:00",
"repayAmt":1000,
"repayTerm":[
1
],
"cardNo":"6224567890123456",
"bankCode":"1234",
"bankName":"中国工商银行",
"bankMobile":"13812345678"
}
}
```

<h4 id="nav-org-3-5">3.5 权益还款试算</h4>

3.5.1 调用场景

平台方请求机构合作方接口，在权益还款申请提交前，进行权益还款试算，获取应还金额信息。可区分不同类型试算。

3.5.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/privilegeRepayTrial

3.5.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userNo | 平台用户号 | string(64) | Y |  |
| drawReqNo | 平台借款申请号 | string(64) | Y | 平台借款申请号和机构借款申请号，必须传一个 |
| fundDrawNo | 机构借款申请号 | string(64) | N |  |
| trialType | 试算还款类型 | integer(2) | Y | 1 - 当期还款（必须按顺序，不能跳期）<br>2 - 逾期还款（单期）<br>3 - 逾期还款（多期合并）<br>4 - 整笔提前结清<br><br>权益为1期时，默认传1-当期还款 |
| trialPeriods | 试算还款期数 | array[integer] | Y | 多期试算用逗号隔开 |

请求参数示例：

```json
{
"userNo": "UR0696455066729598976",
"drawReqNo": "DR718293712983712",
"fundDrawNo": "FDR81209381093810",
"trialType": 1,
"trialPeriods": [1]
}
```

3.5.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 试算结果 | integer(2) | Y | 1 - 试算成功<br>2 - 试算失败<br>结果为1时，业务数据才有值 |
| reasonDesc | 失败原因描述 | string(256) | O | 结果2时必传 |
| userNo | 平台用户号 | string(64) | Y | 平台用户号 |
| drawReqNo | 平台借款申请号 | string(64) | N | 平台借款申请号 |
| deserveTotalAmt | 应还总金额 | decimal | Y | 单位（元） |
| deservePrinAmt | 应还本金 | decimal | Y | 单位（元） |
| deserveIntAmt | 应还利息 | decimal | Y | 单位（元） |
| deserveOintAmt | 应还罚息 | decimal | Y | 单位（元） |
| deserveLateFeeAmt | 应还滞纳金 | decimal | N | 单位（元） |
| deserveOtherFeeAmt | 应还其他费用 | decimal | N | 单位（元） |

响应参数示例：

```json
{
"result":1,
"userNo":"UR0696455066729598976",
"drawReqNo":"DR718293712983712",
"deserveTotalAmt":1000.00,
"deservePrinAmt":800.00,
"deserveIntAmt":200.00,
"deserveOintAmt":0,
"deserveLateFeeAmt":0,
"deserveOtherFeeAmt":0
}
```

<h4 id="nav-org-3-6">3.6 权益还款申请提交</h4>

3.6.1 调用场景

平台方请求机构合作方接口，完成各种必要的前置校验后，提交权益还款申请。

3.6.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/privilegeRepaySubmit

3.6.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| privilegeRepayReqNo | 平台权益还款申请号 | string(64) | Y | 平台权益还款申请请求号 |
| drawReqNo | 平台借款申请号 | string(64) | Y | 平台借款申请号和机构借款申请号，必须传一个 |
| fundDrawNo | 机构借款申请号 | string(64) | N |  |
| cardNo | 银行卡号 | string(32) | Y | 卡号明文 |
| bankMobile | 银行预留手机号 | string(32) | Y | 银行预留手机号明文 |
| repayType | 还款方式 | integer(2) | N | 1 - 当期还款（必须按顺序，不能跳期）<br>2 - 逾期还款（单期）<br>3 - 逾期还款（多期合并）<br>4 - 整笔提前结清<br><br>权益为1期时，默认传1-当期还款 |
| repayApplyTime | 还款申请时间 | string | Y | 用户还款申请提交时间 yyyy-MM-dd HH:mm:ss |
| repayApplyAmt | 还款申请金额 | decimal | Y | 还款申请金额，单位（元） |
| periods | 还款期数 | array[integer] | Y | 多期[1,2,3,4] |

请求参数示例：

```json
{
"privilegeRepayReqNo": "RR182093812093812",
"drawReqNo": "DR718293712983712",
"fundDrawNo": "FD71298371298371",
"repayType": 1,
"repayApplyTime": "2024-01-10 14:30:00",
"repayApplyAmt": "1000.00",
"periods": [1, 2, 3]
}
```

3.6.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 受理结果 | integer(2) | Y | 1 - 受理成功；2 - 受理失败；3 - 需补充验证 |
| fundPrivilegeRepayNo | 机构权益还款申请号 | string(64) | N | 结果1时可传 |
| reasonDesc | 失败原因描述 | string | O | 结果2时必传 |
| checkType | 验证类型 | array[integer] | O | 1 - 短信（机构验证，调用短信验证相关接口，需<br>主动调用5.4发送验证码）<br>2 - 短信（机构验证，调用短信验证相关接口，机构静默发送短信，只需调用5.5验证验证码） |

响应参数示例：

```json
{
"result":1,
"fundPrivilegeRepayNo":"FRP81902380192381",
"reasonDesc":null,
"checkType":[1]
}
```

<h4 id="nav-org-3-7">3.7 查询权益还款结果</h4>

3.7.1 调用场景

平台方请求机构合作方接口，查询用户权益还款结果。

3.7.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/privilegeRepayResultQuery

3.7.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| privilegeRepayReqNo | 平台权益还款申请号 | string(64) | Y | 平台权益还款申请请求号 |
| fundPrivilegeRepayNo | 机构权益还款申请号 | string(64) | N |  |

请求参数示例：

```json
{
"privilegeRepayReqNo": "RR182093812093812",
"fundPrivilegeRepayNo": "FRP81902380192381"
}
```

3.7.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| privilegeRepayReqNo | 平台权益还款申请号 | string(64) | Y |  |
| fundPrivilegeRepayNo | 机构权益还款申请号 | string(64) | N |  |
| result | 还款结果 | integer(2) | Y | 1 - 还款成功（可继续调用查询借据及还款计划接口）<br>2 - 还款失败<br>3 - 还款处理中<br>4 - 无记录 |
| payType | 支付方式 | integer(2) | Y | 1 - 主动还款，2-批扣， 3 - 线下还款， 4 - 其他 |
| repayDesc | 还款描述 | string | O | 结果2时必传 |
| repayDetailInfo | 还款成功详情 | object | O | 结果1时必传 |

repayDetailInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| repaySuccTime | 还款成功时间 | string(20) | Y | yyyy-MM-dd HH:mm:ss |
| repayAmt | 还款总金额 | decimal | Y | 单位（元） |
| repayTerm | 还款期数 | array[integer] | Y | 如为多期还款，用逗号隔开 |
| cardNo | 还款银行卡号 | string(32) | N | 卡号明文 |
| bankCode | 还款银行编码 | string(32) | N | 银行编码与银行名称，详见附录 |
| bankName | 还款银行名称 | string(64) | N | 银行编码与银行名称，详见附录 |
| bankMobile | 还款银行预留手机号 | string(32) | N | 银行预留手机号明文 |

响应参数示例：

```json
{
"result":1,
"payType":1,
"reasonDesc":"还款成功",
"repayDetailInfo":{
"repaySuccTime":"2024-01-15 10:30:00",
"repayAmt":1000,
"repayTerm":[1],
"cardNo":"6224567890123456",
"bankCode":"1234",
"bankName":"中国工商银行",
"bankMobile":"13812345678"
}
```

<h4 id="nav-san-biz-4">4. 绑卡相关接口</h4>

<h4 id="nav-org-4-1">4.1 查询用户已绑卡列表</h4>

4.1.1 调用场景

平台方请求机构合作方接口，查询用户在机构合作方侧已绑定的银行卡列表。

4.1.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/userCardQuery

4.1.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userNo | 平台用户号 | string(64) | Y | 平台用户对外唯一标识 |
| fundUserNo | 机构方用户号 | string(64) | N | 机构方用户唯一标识 |
| bindScene | 绑卡场景 | string(32) | N | CREDIT - 授信绑卡；DRAW - 借款绑卡；REPAY - 还款换绑卡 |
| fundDrawNo | 机构借款申请号 | string(64) | N | 还款换绑卡场景下，可传 |

请求参数示例：

```json
{
"userNo":"UR0710379035226226688",
"fundUserNo":"xxxx"
}
```

4.1.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| cardList | 机构方已绑卡列表 | array[object] | N | 详见下表 |

cardList

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| cardNo | 银行卡号 | string(32) | Y | 卡号明文 |
| bankCode | 银行编码 | string(32) | Y | 银行编码与银行名称，详见附录 |
| bankName | 银行名称 | string(128) | Y | 银行编码与银行名称，详见附录 |
| bankMobile | 银行预留手机号 | string(32) | Y | 银行预留手机号明文 |
| isLoanCard | 是否必须使用此卡收款 | string(16) | N | 该已绑定银行卡是否必须作为放款银行卡。Y - 是；N - 否 |
| cardId | 银行卡ID | string(64) | N | 目前业务上不使用 |

响应参数示例：

```json
{
"cardList":[
{
"cardNo":"622031001036123456",
"bankCode":"0001",
"bankName":"中国银行",
"bankMobile":"18888888888",
"isLoanCard":"N"
}
]
}
```

<h4 id="nav-org-4-2">4.2 查询支持银行列表</h4>

4.2.1 调用场景

平台方请求机构合作方接口，查询机构合作方支持银行列表。

4.2.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/bankListQuery

4.2.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userNo | 平台用户号 | string(64) | Y | 平台用户对外唯一标识 |
| bindScene | 绑卡场景 | string(16) | N | CREDIT - 授信绑卡；DRAW - 借款绑卡；REPAY - 还款换绑卡 |

请求参数示例：

```json
{
"bindScene": "CREDIT"
}
```

4.2.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| bankList | 支持银行列表 | array[object] | Y | 详见下表 |

bankList对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| bankCode | 银行编码 | string(16) | N | 银行编码与银行名称，详见附录 |
| bankName | 银行名称 | string(32) | N | 银行编码与银行名称，详见附录 |

响应参数示例：

```json
{
"bankList": [
{
"bankCode": "0001",
"bankName": "中国银行"
},
{
"bankCode": "0002",
"bankName": "农业银行"
},
{
"bankCode": "0003",
"bankName": "工商银行"
}
]
}
```

<h4 id="nav-org-4-3">4.3 银行卡绑定申请</h4>

4.3.1 调用场景

平台方请求机构合作方接口，提交用户银行卡信息、并做绑定申请。

4.3.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/cardBind

4.3.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| bindReqNo | 平台绑卡请求号 | string(32) | Y |  |
| userNo | 平台用户号 | string(32) | Y | 平台用户对外唯一标识 |
| fundUserNo | 机构方用户号 | string(32) | N | 机构方用户唯一标识 |
| cardNo | 银行卡号 | string(32) | N | 卡号明文 |
| bankCode | 银行编码 | string(16) | N | 银行编码与银行名称，详见附录 |
| bankName | 银行名称 | string(32) | N | 银行编码与银行名称，详见附录 |
| bankMobile | 银行预留手机号 | string(16) | N | 银行预留手机号明文 |
| creditReqNo | 平台授信申请号 | string(64) | O | bindScene=DRAW时必传 |
| drawReqNo | 平台借款申请号 | string(64) | O | bindScene=REPAY时必传 |
| bindScene | 绑卡节点 | string(32) | O | 节点：CREDIT - 授信绑卡；DRAW - 借款绑卡；REPAY - 还款换绑卡 |
| cardId | 银行卡ID | string(64) | N | 机构返回卡ID，绑定机构返回老卡时必传 |
| idCardNo | 用户身份证号 | string(32) | Y | 用户身份证号 |
| userName | 用户姓名 | string(32) | Y | 用户姓名 |

请求参数示例：

```json
{
"bindReqNo": "BBC0671347062377410567",
"userNo": "UR0670381649694875678",
"fundUserNo": "100159059",
"cardNo": "621660990898353160",
"bankCode": "0001",
"bankName": "中国银行",
"bankMobile": "15012345678"
}
```

4.3.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 受理结果 | integer(2) | Y | 1 - 绑定成功，无需短信验证；<br>2 - 受理失败；<br>3 - 受理成功，已发送验证码； |
| reasonDesc | 失败原因描述 | string(256) | O | 结果失败时必传 |
| fundBindReqNo | 机构绑卡请求号 | string(32) | Y | 机构方绑卡请求唯一标识 |

响应参数示例：

```json
// 短信验证
{
"result": 1,
"reasonDesc": "验证码已发送"
}

// 无需验证
{
"result": 2,
"reasonDesc": "成功"
}

// 失败
{
"result": 3,
"reasonDesc": "银行卡不支持"
}
```

<h4 id="nav-org-4-4">4.4 银行卡绑定短信验证</h4>

4.4.1 调用场景

平台方请求机构合作方接口，在需要验证短信的情况下，提交验证码，完成绑卡短信验证。

4.4.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/cardBindSms

4.4.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| bindReqNo | 平台绑卡请求号 | string(32) | Y |  |
| userNo | 平台用户号 | string(32) | Y | 平台用户对外唯一标识 |
| fundUserNo | 机构方用户号 | string(32) | N | 机构方用户唯一标识 |
| smsCode | 短信验证码 | string(16) | Y | 绑卡短信验证码 |
| fundBindReqNo | 机构绑卡请求号 | string(32) | Y | 机构方绑卡请求唯一标识 |

请求参数示例：

```json
{
"bindReqNo": "BBC0671347062377410567",
"userNo": "UR0670381649694875678",
"fundUserNo": "100159059",
"smsCode": "123456"
}
```

4.4.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 受理结果 | integer(2) | Y | 1 - 验证成功；<br>2 - 验证失败；<br>3 - 重新发送验证码； |
| reasonDesc | 失败原因描述 | string(256) | O | 结果失败时必传 |

响应参数示例：

```json
// 成功
{
"result": 1,
"reasonDesc": "成功"
}

// 失败
{
"result": 2,
"reasonDesc": "验证码错误"
}

//重新发送
{
"result": 3,
"reasonDesc": "验证码已失效，请重新获取"
}
```

<h4 id="nav-org-4-5">4.5 查询绑卡结果</h4>

4.5.1 调用场景

平台方请求机构合作方接口，查询银行卡绑定结果。适用于H5绑卡场景。API绑卡无需对接。

4.5.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/cardBindResultQuery

4.5.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userNo | 平台用户号 | string(64) | Y | 平台用户对外唯一标识 |
| fundUserNo | 机构方用户号 | string(64) | N | 机构方用户唯一标识 |
| cardNo | 银行卡号 | string(32) | Y | 卡号明文 |

请求参数示例：

```json
{
"userNo":"UR0710379035226226688",
"fundUserNo":"xxxx",
"cardNo":"622031001036123456"
}
```

4.5.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 受理结果 | integer(2) | Y | 1 - 绑卡成功<br>2 - 绑卡失败<br>3 - 受理成功，已发送验证码<br>4 - 重新发送验证码 |
| cardNo | 银行卡号 | string(32) | O | 结果1时必传，卡号明文 |
| bankCode | 银行编码 | string(32) | O | 结果1时必传，银行编码与银行名称，详见附录 |
| bankName | 银行名称 | string(128) | O | 结果1时必传，银行编码与银行名称，详见附录 |
| bankMobile | 银行预留手机号 | string(32) | O | 结果1时必传，银行预留手机号明文 |
| bindTime | 绑定成功时间 | string(32) | O | 结果1时必传，时间格式：yyyy-MM-dd HH:mm:ss |
| reasonDesc | 失败原因描述 | string(256) | O | 结果2时必传 |

响应参数示例：

```json
{
"result":1,
"cardNo":"622031001036123456",
"bankCode":"0001",
"bankName":"中国银行",
"bankMobile":"18888888888",
"bindTime":"2023-12-01 10:00:00"
}
```

5. 通用接口

<h4 id="nav-org-5-1">5.1 查询用户额度</h4>

5.1.1 调用场景

平台方请求机构合作方接口，在授信成功后，查询用户额度、定价等相关信息。

5.1.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/accountInfoQuery

5.1.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userNo | 平台用户号 | string(64) | Y | 平台用户对外唯一标识 |
| fundUserNo | 机构方用户号 | string(64) | N | 机构方用户唯一标识 |
| creditReqNo | 平台授信申请号 | string(64) | Y |  |
| fundCreditNo | 机构授信申请号 | string(64) | N |  |

请求参数示例：

```json
{
"creditReqNo": "AP0710324673086914560",
"userNo": "UR0722566261684408320"
}
```

5.1.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| status | 额度状态 | integer(2) | Y | 1 - 可用（有可用额度，用户可发起借款申请）<br>2 - 失效（无可用额度，需重新授信）<br>3 - 锁定（额度已使用，借款审核中）【暂不支持】 |
| creditAmt | 授信额度 | decimal | Y | 单位元 |
| availableAmt | 可用额度 | decimal | Y | 单位元。<br>如存在额度临时冻结场景，可传额度状态=1，可用额度=0；额度恢复后再传更新后的可用额度。<br>额度失效情况下，可用额度=0。 |
| maxAvailableAmt | 最大可用额度 | decimal | Y | 单位元 |
| minAvailableAmt | 最小可用额度 | decimal | Y | 单位元 |
| step | 额度步长 | decimal | N | 单位元 |
| creditValidTime | 额度生效时间 | string(20) | Y | 格式：yyyy-MM-dd HH:mm:ss |
| creditExpireTime | 额度失效时间 | string(20) | Y | 格式：yyyy-MM-dd HH:mm:ss。<br>说明：变更额度状态/授信额度/可用额度时涉及更新<br>额度状态变更为额度失效时，需给小于当前时间的额度失效时间（否则无法触发我方额度失效逻辑）。<br>授信额度/可用额度更新时，根据实际需要更新额度失效时间。 |
| repayMethod | 还款方式 | integer | Y | 1 - 等本等息；2 - 等额本息；3 - 等额本金；4 - 先息后本；5 - 随借随还；6 - 到期还本；7 - 锁期 |
| rateType | 利率类型 | string(8) | Y | APR / IRR |
| rateUnit | 利率单位 | string(8) | Y | DAY - 日；MONTH - 月；YEAR - 年 |
| rate | 利率 | string(16) | Y | 如0.15，表示利率15.4% |
| availableTerms | 可借期数 | list[integer] | Y | 以此返回为准，对客展示 |
| capitalCode | 资方 | string(20) | N |  |

响应参数示例：

```json
{
"status": 1,
"creditAmt": 10000.00,
"maxAvailableAmt": 8000.00,
"minAvailableAmt": 1000.00,
"step": 1000.00,
"creditValidTime": "2024-01-17 13:39:41",
"creditExpireTime": "2024-01-17 13:39:41",
"repayMethod": 1,
"rateType": "APR",
"rateUnit": "DAY",
"rate": "0.55",
"availableTerms": [6, 12, 18, 24],
"capitalCode": "ABC123XYZ"
}
```

<h4 id="nav-org-5-2">5.2 查询用户协议</h4>

5.2.1 调用场景

平台方请求机构合作方接口，在授信、借款、绑卡等不同场景下调用，获取不同对客展示协议。

5.2.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/agreementList

5.2.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userNo | 平台用户号 | string(64) | Y | 平台用户对外唯一标识（scene为REGISTER，非必传） |
| scene | 查询场景 | string(32) | Y | REGISTER - 注册【暂不支持】<br>CREDIT - 授信<br>DRAW - 借款（非权益）<br>PRIVILEGE_DRAW-借款（权益）<br>BIND - 绑卡<br>LOAN - 借据详情【暂不支持】<br>REPAY - 还款【暂不支持】<br>PRIVILEGE - 权益 |
| creditReqNo | 授信申请号 | string(64) | N | scene为DRAW，必传 |
| drawReqNo | 借款申请号 | string(64) | N | scene为REPAY，必传 |
| loanAmt | 试算借款金额 | decimal | O | 单位：元(小数点后保留两位)。scene为DRAW，必传。<br>如需填充对客协议，可使用。 |
| loanTerm | 试算借款期数 | integer | O | 不支持传多个期数。scene为DRAW，必传。<br>如需填充对客协议，可使用。 |
| userName | 用户姓名 | string(64) | N | 明文。scene为CREDIT，有则传。<br>如需填充对客协议，可使用。 |
| idNo | 用户身份证号 | string(30) | N | 明文。scene为CREDIT，有则传。<br>如需填充对客协议，可使用。 |

请求参数示例：

```json
{
"userNo": null,
"fundUserNo": null,
"scene": "REGISTER",
"creditReqNo": null，
"drawReqNo": null
}
```

5.2.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| agreements | 合同列表 | array | Y | 详见下表。如有展示顺序，按照顺序返回 |
| isDefaultselect | 是否默认勾选 | string(16) | N | Y - 是；N - 否。默认为N |
| isForceRead | 是否强制阅读 | string(16) | N | Y - 是；N - 否。默认为N |
| forceReadTime | 强制阅读时间 | integer | N | 单位 - 秒。当isForceRead为Y时，可以有值 |

agreements合同列表

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| agreementName | 协议名称 | string(256) | Y |  |
| agreementUrl | 协议地址 | string(500) | Y |  |

响应参数示例：

```json
{
"agreements": [
{
"agreementName": "用户隐私协议",
"agreementUrl": "https://mswl.info/protocol/content/direct/t_lxj_ys_KHF7YD"
},
{
"agreementName": "用户服务协议",
"agreementUrl": "https://stc.xurongwl.com/protocol/register/fuwu.html"
}
],
"isDefaultselect": "N",
"isForceRead": "N",
"forceReadTime": null
}
```

<h4 id="nav-org-5-3">5.3 查询场景页面地址</h4>

5.3.1 调用场景

根据机构合作方流程和产品要求，可选择对接此接口。平台方请求机构合作方接口，在授信、借款、绑卡等不同场景下调用，获取机构H5页面跳转地址。

5.3.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/sceneUrlQuery

5.3.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userNo | 平台用户号 | string(64) | Y | 平台用户对外唯一标识 |
| scene | 查询场景 | string(64) | Y | DRAW - H5借款地址<br>DRAW_PRIVILEGE_ORDER1 - H5权益购买地址1（介绍）<br>DRAW_PRIVILEGE_ORDER2- H5权益购买地址2（购买）<br>DRAW_PRIVILEGE_REDEEM- H5权益兑换地址<br>REPAY - H5还款地址<br>REPAY_PRIVILEGE - H5权益还款地址<br>BIND - H5绑卡地址<br>SIGN - H5签约地址<br>SUPPLY - H5补充资料地址<br>DOWN - H5下载地址 |
| creditReqNo | 平台授信申请号 | string(64) | N |  |
| fundDrawNo | 机构借款申请号 | string(64) | N | 获取还款地址时，必传 |
| returnUrl | 回跳地址 | string(512) | N |  |

请求参数示例：

```json
{
"userNo":"UR0710379035226226688",
"scene":"BIND",
"creditReqNo":"CR0673827201381298176",
"fundDrawNo":"Fund0673827201381298175",
"returnUrl":"https://xxxx.com/xxxx",
}
```

5.3.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| url | 页面地址 | string(512) | Y |  |

响应参数示例：

```json
{
"url":"https://xxxx/bindcardurl/xxxx"
}
```

<h4 id="nav-org-5-4">5.4 发送短信验证码</h4>

5.4.1 调用场景

根据机构合作方流程和产品要求，可选择对接此接口。平台方请求机构合作方接口，在借款、还款等不同场景需要使用短信验证的时候调用，发送短信验证码。

5.4.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/sendSmsCode

5.4.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userNo | 平台用户号 | string(64) | Y | 平台用户对外唯一标识 |
| scene | 场景 | string(2) | Y | 01 - 借款提交验证短信；<br>02 - 还款提交验证短信； |
| bizNo | 业务编号 | string(64) | N | 01时传drawReqNo，02时传repayReqNo |

请求参数示例：

```json
{
"userNo":"UR0716595073412812800",
"scene":"01",
"bizNo":"AP0710324673086914560"
}
```

5.4.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 结果 | integer(2) | Y | 1 - 发送成功；2 - 发送失败 |
| reasonDesc | 失败原因描述 | string(256) | O | 结果2时必传 |

响应参数示例：

```json
{
"result":1
}
```

<h4 id="nav-org-5-5">5.5 短信验证</h4>

5.5.1 调用场景

根据机构合作方流程和产品要求，可选择对接此接口。平台方请求机构合作方接口，在借款、还款等不同场景需要使用短信验证的时候调用，提交短信验证码。

5.5.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/sendSms

5.5.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userNo | 平台用户号 | string(64) | Y | 平台用户对外唯一标识 |
| scene | 场景 | string(2) | Y | 01 - 借款提交验证短信；<br>02 - 还款提交验证短信； |
| bizNo | 业务编号 | string(64) | N | 01时传drawReqNo，02时传repayReqNo |
| smsCode | 短信验证码 | string(10) | Y |  |

请求参数示例：

```json
{
"userNo":"UR0716595073412812800",
"scene":"01",
"bizNo":"AP0710324673086914560",
"smsCode":"111111"
}
```

5.5.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 结果 | integer(2) | Y | 1 - 验证成功；2 - 验证失败 |
| reasonDesc | 失败原因描述 | string(256) | O | 结果2时必传 |

响应参数示例：

```json
{
"result":1
}
```

<h4 id="nav-org-5-6">5.6 提交补充资料</h4>

5.6.1 调用场景

根据机构合作方流程和产品要求，可选择对接此接口。平台方请求机构合作方接口，在授信、借款等不同场景需要补充资料的时候调用，用于提交补充的资料项。

5.6.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/supplySubmit

5.6.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userNo | 平台用户号 | string(64) | Y | 平台用户对外唯一标识 |
| fundUserNo | 机构方用户号 | string(64) | N | 机构方用户唯一标识 |
| scene | 场景 | string(16) | Y | CREDIT - 授信补件；<br>DRAW - 借款补件； |
| bizNo | 业务编号 | string(64) | Y | 场景为CREDIT时传creditReqNo，场景为DRAW时传drawReqNo |
| supplyInfo | 补充资料项 | array[object] | Y |  |

supplyInfo对象

cardInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| cardNo | 银行卡号 | string | N | 卡号明文 |
| bankCode | 银行编码 | string | N | 银行编码与银行名称，详见附录 |
| bankName | 银行名称 | string | N | 银行编码与银行名称，详见附录 |
| bankMobile | 银行预留手机号 | string | N | 银行预留手机号明文 |

authIdInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| idCardFrontImgUrl | 身份证人像面照片地址 | string(500) | Y | 示例：https://private-sit.oss-cn-shanghai.aliyuncs.com/private-sit/ocr/hub/UR0707901830361083904/1703128526347/92pceu/1703128526483.png |
| idCardBackImgUrl | 身份证国徽面照片地址 | string(500) | Y | 示例：https://private-sit.oss-cn-shanghai.aliyuncs.com/private-sit/ocr/hub/UR0707901830361083904/1703128537134/m3gtqa/1703128537036.png |
| idCardNo | 用户身份证号 | string(32) | Y | 身份证正面身份证号 |
| idCardSex | 用户性别 | string(2) | Y | 0-男，1-女 |
| idCardBirthday | 用户生日 | string(32) | Y | 格式：1979-08-23 |
| idCardEthnicity | 用户民族 | string(2) | Y | 汉 |
| idCardAddress | 身份证地址 | string(100) | Y | 身份证详细地址 |
| idCardStartDate | 身份证有效期始期 | string(32) | Y | 格式示例：20080314 |
| idCardEndDate | 身份证有效期止期 | string(32) | Y | 若为长期则传29991231 |
| idCardAuthority | 签发机关 | string(32) | Y |  |

authFaceInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| faceSource | 活体供应商 | integer(2) | Y | 1 - 旷视；2 -微众；3 -阿里 |
| faceImg1Url | 活体照片1地址 | string(500) | Y | 示例：http://private-sit.oss-cn-shanghai.aliyuncs.com/private-sit/live/hub/UR0710959998205427712/1703584077691/5eek3g/HUB_LIVE.jpeg |
| faceScore | 活体分 | decimal | N |  |
| faceCollectTime | 活体采集时间 | string(32) | N | 格式：2023-10-13 12:03:13 |
| faceOriginData | 活体检测原始数据 | string(3000) | N |  |

contactInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| contactOneName | 第一联系人姓名 | string(32) | Y |  |
| contactOneTel | 第一联系人电话 | string(32) | Y |  |
| contactOneRel | 第一联系人关系 | string(10) | Y | 枚举值见附录 |
| contactTwoName | 第二联系人姓名 | string(32) | Y |  |
| contactTwoTel | 第二联系人电话 | string(32) | Y |  |
| contactTwoRel | 第二联系人关系 | string(10) | Y | 枚举值见附录 |

请求参数示例：

```json
{
"userNo": "U1703648207",
"scene": "CREDIT",
"supplyInfo": [
{
"userBaseInfo": {
"userName": "小张",
"mobileNo": "12344434444"
},
"cardInfo": {
"cardNo": "6230183543234564333333",
"bankCode": "0001",
"bankName": "中国银行",
"bankMobile": "134271364934"
},
"authIdInfo": {
"idCardFrontImgUrl": "http://example.com/身份证/正面照片.jpg",
"idCardBackImgUrl": "http://example.com/身份证/背面照片.jpg",
"idCardNo": "2343224422234094494",
"idCardSex": "0",
"idCardBirthday": "1979-08-23",
"idCardEthnicity": "汉",
"idCardAddress": "上海市浦东新区花木街道杨高南路辅路中国石化上海浦东科研信息办公综合基地",
"idCardStartDate": "20080314",
"idCardEndDate": "20180314",
"idCardAuthority": "深圳市公安局"
},
"authFaceInfo": {
"faceSource": 1,
"faceImg1Url": "http://example.com/活体照片1.jpg",
"faceImg2Url": "http://example.com/活体照片2.jpg",
"faceScore": 95.5,
"faceCollectTime": "2023-12-26 10:30:00"
}
}
]
}
```

5.6.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 结果 | integer(2) | Y | 1 - 受理成功；2 - 受理失败 |
| reasonDesc | 失败原因描述 | string(256) | O | 结果2时必传 |

响应参数示例：

```json
{
"result": 2,
"reasonDesc":"上传接口信息字段缺失"
}
```

<h3 id="nav-san-platform">2. 平台方提供接口</h3>

<h4 id="nav-plat-2-1">2.1 推送授信结果</h4>

2.1.1 调用场景

机构合作方请求平台方接口，推送授信结果。

2.1.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/creditResultPush

2.1.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| creditReqNo | 平台授信申请号 | string(64) | Y |  |
| fundCreditNo | 机构授信申请号 | string(64) | N |  |
| result | 授信结果 | string(8) | Y | CR101 - 授信成功（可继续调用额度查询接口）<br>CR102 - 授信拒绝<br>CR103 - 授信申请取消<br>CR104 - 待补件【暂不支持】<br>CR105 - 授信中<br>CR106 - 无记录（如因网络等问题，授信申请未实际提交到合作方，导致合作方查询不到对应流水号的申请结果，需返回CR106无记录） |
| reasonCode | 拒绝码 | string(8) | O | 结果CR102时必传<br>C1010 内部处理失败<br>C1011 资料缺失<br>C1021 风控审核拒绝<br>C1022 资方审核拒绝<br>C2001 其他 |
| reasonDesc | 拒绝原因描述 | string(256) | O | 结果CR102时必传 |
| creditFailTime | 授信拒绝时间 | string(32) | O | 结果CR102时必传，yyyy-mm-dd hh:mm:ss |
| creditSuccTime | 授信成功时间 | string(32) | O | 结果CR101时必传，yyyy-mm-dd hh:mm:ss |
| creditAmt | 授信额度 | decimal(32) | O | 结果CR101时必传，单位元 |
| annualRate | 年利率 | string(16) | O | 结果CR101时必传，年利率 |
| creditCancelTime | 授信申请取消时间 | string(32) | O | 结果CR103时必传，yyyy-mm-dd hh:mm:ss |
| supplyType | 补件类型 | string(16) | O | 结果CR104时必传，ID / FACE / CONTACT / CARD |
| creditFailFrozenTime | 授信被拒封禁期 | string(32) | O | 结果CR102时必传，yyyy-mm-dd hh:mm:ss |

请求参数示例：

```json
// 成功
{
"creditReqNo": "AP0710324673086914560",
"fundCreditNo": "123412341234",
"result": "CR101",
"creditSuccTime": "2023-12-27 11:11:11",
"creditAmt": "5000"
}

// 拒绝
{
"creditReqNo": "AP0710324673086914560",
"fundCreditNo": "123412341234",
"result": "CR102",
"reasonDesc": "身份证信息不合法"
}

// 待补件
{
"creditReqNo": "AP0710324673086914560",
"fundCreditNo": "123412341234",
"result": "CR104",
"reasonDesc": "需要补充资料",
"supplyType": "CONTACT"
}

// 取消
{
"creditReqNo": "AP0710324673086914560",
"fundCreditNo": "123412341234",
"result": "CR103",
"creditCancelTime": "2023-12-27 11:11:11"
}
```

<h4 id="nav-plat-2-2">2.2 推送额度变更</h4>

2.2.1 调用场景

机构合作方请求平台方接口，在授信成功后，推送用户额度、定价等相关信息。有额度状态及额度的变化时，也通过该接口推送。

2.2.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/accountInfoPush

2.2.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userNo | 平台用户号 | string(64) | Y | 平台用户对外唯一标识 |
| fundUserNo | 机构方用户号 | string(64) | N | 机构方用户唯一标识 |
| creditReqNo | 平台授信申请号 | string(64) | Y |  |
| fundCreditNo | 机构授信申请号 | string(64) | N |  |
| status | 额度状态 | integer(2) | Y | 1 - 可用（有可用额度，用户可发起借款申请）<br>2 - 失效（无可用额度，需重新授信）<br>3 - 锁定（额度已使用，借款审核中）【暂不支持】 |
| creditAmt | 授信额度 | decimal | Y | 单位元 |
| availableAmt | 可用额度 | decimal | Y | 单位元。<br>如存在额度临时冻结场景，可传额度状态=1，可用额度=0；额度恢复后再传更新后的可用额度。<br>额度失效情况下，可用额度=0。 |
| maxAvailableAmt | 最大可用额度 | decimal | Y | 单位元 |
| minAvailableAmt | 最小可用额度 | decimal | Y | 单位元 |
| step | 额度步长 | decimal | N | 单位元 |
| creditValidTime | 额度生效时间 | string(20) | Y | 格式：yyyy-MM-dd HH:mm:ss |
| creditExpireTime | 额度失效时间 | string(20) | Y | 格式：yyyy-MM-dd HH:mm:ss。<br>说明：变更额度状态/授信额度/可用额度时涉及更新<br>额度状态变更为额度失效时，需给小于当前时间的额度失效时间（否则无法触发我方额度失效逻辑）。<br>授信额度/可用额度更新时，根据实际需要更新额度失效时间。 |
| repayMethod | 还款方式 | integer | Y | 1 - 等本等息；2 - 等额本息；3 - 等额本金；4 - 先息后本；5 - 随借随还；6 - 到期还本；7 - 锁期 |
| rateType | 利率类型 | string(8) | Y | APR / IRR |
| rateUnit | 利率单位 | string(8) | Y | DAY - 日；MONTH - 月；YEAR - 年 |
| rate | 利率 | string(16) | Y | 如0.15，表示利率15.4% |
| availableTerms | 可借期数 | list[integer] | Y |  |
| capitalCode | 资方 | string(20) | N |  |
| changeType | 变更类型 | integer(2) | N | 1 - 提额（触发短信营销）<br>2 - 降息 |

请求参数示例：

```json
{
"creditReqNo":"AP0710324673086914560",
"userNo":"UR0722566261684408320",
"status":1,
"creditAmt":10000,
"maxAvailableAmt":8000,
"minAvailableAmt":1000,
"step":1000,
"creditValidTime":"2024-01-17 13:39:41",
"creditExpireTime":"2024-01-17 13:39:41",
"repayMethod":1,
"rateType":"APR",
"rateUnit":"DAY",
"rate":"0.55",
"availableTerms":[
6,
12,
18,
24
],
"capitalCode":"ABC123XYZ"
}
```

<h4 id="nav-plat-2-3">2.3 推送放款结果</h4>

2.3.1 调用场景

机构合作方请求平台方接口，推送用户借款申请的放款结果。该接口可用于推送不在平台侧发起的借款信息。

2.3.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/drawResultPush

2.3.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| creditReqNo | 平台授信申请号 | string(64) | Y |  |
| fundCreditNo | 机构授信申请号 | string(64) | N |  |
| result | 放款结果 | string(8) | Y | DR101 - 放款成功（可继续调用查询借据及还款计划接口）<br>DR102 - 放款失败<br>DR103 - 放款拒绝<br>DR104 - 放款申请取消<br>DR105 - 待补件【暂不支持】<br>DR106 - 需重新匹配资金方（需验证短信）<br>DR107 - 需重新匹配资金方（无需验证，直接发起新申请）<br>DR108 - 放款中<br>DR109 - 无记录（如因网络等问题，借款申请未实际提交到合作方，导致合作方查询不到对应流水号的申请结果，需返回DR109无记录） |
| drawStatusUpdateTime | 放款状态变更时间 | string(20) | Y | 状态变更时必传，格式：yyyy-MM-dd HH:mm:ss |
| fundDrawNo | 机构借款申请号 | string(64) | O | 结果非DR109时必传 |
| drawReqNo | 平台借款申请号 | string(64) | O | 结果非DR109时，如果从平台发起的借款必传 |
| loanAmt | 放款金额 | decimal | O | 结果为DR101时必传，单位元 |
| loanTerm | 放款期数 | integer | O | 结果为DR101时必传 |
| reasonCode | 失败原因码 | string(8) | O | 结果为DR102、DR103时必传<br>D1010 内部处理失败<br>D1011 资料缺失<br>D1021 风控拒绝<br>D1022 资方审核拒绝<br>D2001 其他 |
| reasonDesc | 失败原因描述 | string(256) | O | 结果为DR102、DR103时必传 |
| drawFreezeEndTime | 放款冻结结束时间 | string(20) | O | 结果为DR102、DR103、DR104 时可传<br>格式：yyyy-MM-dd HH:mm:ss |
| supplyType | 补件类型 | string(10) | O | 结果为DR105时必传，ID / FACE / CONTACT / PROFILE / CARD |
| isReloan | 首复贷标识 | integer | O | 结果为DR101-放款成功时可传<br>0-首贷，1-复贷 |
| capitalCode | 出资机构编码 | string(64) | N | 乐小融-够享借模式必传 |

请求参数示例：

```json
{
"creditReqNo":"AP0710324673086914560",
"result":"DR101",
"drawStatusUpdateTime":"2024-01-17 13:39:41",
"fundDrawNo":"FCR0716595246214803456",
"drawReqNo":"CR0716595246214803456",
"loanAmt":3000,
"loanTerm":3,
}
```

<h4 id="nav-plat-2-4">2.4 推送借据及还款计划</h4>

2.4.1 调用场景

机构合作方请求平台方接口，在放款成功、借据状态变更、发生还款后，推送用户的借据状态。

2.4.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/loanPlanPush

2.4.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| drawReqNo | 平台借款申请号 | string(64) | O | 平台发起的提现一定要有值<br>平台借款申请请求号 |
| fundDrawNo | 机构借款申请号 | string(64) | Y |  |
| loanAmt | 放款金额 | decimal | Y | 单位：元(小数点后保留两位) |
| loanTerm | 放款期数 | integer | Y |  |
| loanYearRate | 放款年利率 | string(16) | Y | 默认传IRR计算方式下的年利率。传0.154代表IRR年利率15.4% |
| loanSuccTime | 放款成功时间 | string(20) | Y | 格式：yyyy-MM-dd HH:mm:ss |
| interestMethod | 计息方式 | integer | Y | 1 - 按日计息；2 - 按月计息 |
| repayMethod | 还款方式 | integer | Y | 1 - 等本等息；2 - 等额本息；3 - 等额本金；4 - 先息后本；5 - 随借随还；6 - 到期还本；7 - 锁期 |
| cardNo | 放款银行卡号 | string(32) | N | 卡号明文 |
| bankCode | 放款银行编码 | string(32) | N | 银行编码与银行名称，详见附录 |
| bankName | 放款银行名称 | string(64) | N | 银行编码与银行名称，详见附录 |
| bankMobile | 放款银行预留手机号 | string(32) | N | 银行预留手机号明文 |
| loanStatus | 借据状态 | string(2) | Y | 01 - 还款中；02 - 逾期中；03 - 已结清；04 - 已退贷 |
| loanSettleTime | 结清时间 | string(20) | O | 借据状态03时必传，格式：yyyy-MM-dd HH:mm:ss |
| loanCancelTime | 退贷时间 | string(20) | O | 借据状态04时必传，格式：yyyy-MM-dd HH:mm:ss |
| loanOverdueDays | 逾期天数 | integer | O | 借据状态02时必传 |
| loanRepayPlanList | 借据还款计划 | array[LoanRepayPlan] | Y |  |

LoanRepayPlan对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| periodNo | 当期期数 | integer | Y |  |
| dateDue | 应还款日 | string(10) | Y | 格式：yyyy-MM-dd |
| timeRepayEarliest | 最早可还款时间 | string(20) | O | 支持提前还当期时必传。如不传，默认最早可还款时间和应还款日一样。<br>格式：yyyy-MM-dd HH:mm:ss |
| deserveTotalAmt | 应还总金额 | decimal | Y | 还款计划生成后不再变化。单位元，支持小数点后两位。下同。 |
| deservePrinAmt | 应还本金 | decimal | Y |  |
| deserveIntAmt | 应还利息 | decimal | Y |  |
| deserveOintAmt | 应还罚息 | decimal | Y |  |
| deserveLateFeeAmt | 应还滞纳金 | decimal | N |  |
| deservePenaltyAmt | 应还违约金 | decimal | N |  |
| deserveOtherFeeAmt | 应还其他费用 | decimal | N |  |
| actTotalAmt | 已还总金额 | decimal | Y | 单位元，支持小数点后两位。下同。 |
| actPrinAmt | 已还本金 | decimal | Y |  |
| actIntAmt | 已还利息 | decimal | Y |  |
| actOintAmt | 已还罚息 | decimal | Y |  |
| actLateFeeAmt | 已还滞纳金 | decimal | N |  |
| actPenaltyAmt | 已还违约金 | decimal | N |  |
| actOtherFeeAmt | 已还其他费用 | decimal | N |  |
| actDeductTotalAmt | 已减免总金额 | decimal | N |  |
| actDeductPrinAmt | 已减免本金 | decimal | N |  |
| actDeductIntAmt | 已减免利息 | decimal | N |  |
| actDeductOintAmt | 已减免罚息 | decimal | N |  |
| actDeductLateFeeAmt | 已减免滞纳金 | decimal | N |  |
| actDeductPenaltyAmt | 已减免违约金 | decimal | N |  |
| actDeductOtherFeeAmt | 已减免其他费用 | decimal | N |  |
| payType | 当期扣款方式 | string(2) | O | 01 - 系统批量扣款；02 - 客户主动还款<br>(当前状态为03时必传) |
| status | 当期状态 | string(2) | Y | 01 - 待还款；02 - 逾期中；03 - 当期已结清 |
| overdueDays | 当期逾期天数 | integer | O | 当期状态为02时必传，每一期的逾期天数 |
| settleTime | 当期结清时间 | string(20) | O | 当期状态为03时必传，格式：yyyy-MM-dd HH:mm:ss |
| remark | 描述 | string(256) | N | 备注信息 |

请求参数示例：

```json
{
"fundDrawNo":"FCR0716595246214803456",
"drawReqNo":"CR0716595246214803456",
"loanAmt":1000.00,
"loanTerm":3,
"loanYearRate":"0.055",
"loanSuccTime":"2024-01-17 13:39:41",
"interestMethod":2,
"repayMethod":2,
"cardNo":"1234567890123456",
"bankCode":"1234",
"bankName":"Example Bank",
"bankMobile":"1234567890",
"loanStatus":"01",
"loanSettleTime":null,
"loanCancelTime":null,
"loanOverdueDays":0,
"loanRepayPlanList":[
{
"periodNo":1,
"dateDue":"2024-01-17",
"timeRepayEarliest":"2024-01-17 13:39:41",
"deserveTotalAmt":1000,
"deservePrinAmt":800,
"deserveIntAmt":200,
"deserveOintAmt":0,
"deserveLateFeeAmt":0,
"deserveOtherFeeAmt":0,
"actTotalAmt":0,
"actPrinAmt":0,
"actIntAmt":0,
"actOintAmt":0,
"actLateFeeAmt":0,
"actOtherFeeAmt":0,
"actDeductTotalAmt":0,
"actDeductPrinAmt":0,
"actDeductIntAmt":0,
"actDeductOintAmt":0,
"actDeductLateFeeAmt":0,
"actDeductOtherFeeAmt":0,
"payType":"01",
"status":"01",
"overdueDays":0,
"settleTime":0,
"remark":""
},
{
"periodNo":2,
"dateDue":"2024-02-17",
"timeRepayEarliest":"2024-01-27 13:39:41",
"deserveTotalAmt":1000,
"deservePrinAmt":800,
"deserveIntAmt":200,
"deserveOintAmt":0,
"deserveLateFeeAmt":0,
"deserveOtherFeeAmt":0,
"actTotalAmt":0,
"actPrinAmt":0,
"actIntAmt":0,
"actOintAmt":0,
"actLateFeeAmt":0,
"actOtherFeeAmt":0,
"actDeductTotalAmt":0,
"actDeductPrinAmt":0,
"actDeductIntAmt":0,
"actDeductOintAmt":0,
"actDeductLateFeeAmt":0,
"actDeductOtherFeeAmt":0,
"payType":"01",
"status":"01",
"overdueDays":0,
"settleTime":0,
"remark":""
},
{
"periodNo":3,
"dateDue":"2024-03-17",
"timeRepayEarliest":"2024-03-17 13:39:41",
"deserveTotalAmt":1000,
"deservePrinAmt":800,
"deserveIntAmt":200,
"deserveOintAmt":0,
"deserveLateFeeAmt":0,
"deserveOtherFeeAmt":0,
"actTotalAmt":0,
"actPrinAmt":0,
"actIntAmt":0,
"actOintAmt":0,
"actLateFeeAmt":0,
"actOtherFeeAmt":0,
"actDeductTotalAmt":0,
"actDeductPrinAmt":0,
"actDeductIntAmt":0,
"actDeductOintAmt":0,
"actDeductLateFeeAmt":0,
"actDeductOtherFeeAmt":0,
"payType":"01",
"status":"01",
"overdueDays":0,
"settleTime":0,
"remark":""
}
]
}
```

<h4 id="nav-plat-2-5">2.5 推送权益订单信息及还款计划</h4>

2.5.1 调用场景

机构合作方请求平台方接口，在放款成功带独立的权益信息、权益订单状态变更、权益发生还款后，推送用户的权益订单相关信息，包括权益还款计划。

2.5.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/privilegePlanPush

2.5.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| fundPrivilegeOrderNo | 机构权益订单号 | string(64) | N |  |
| drawReqNo | 平台借款申请号 | string(64) | O | 平台发起的提现一定要有值<br>平台借款申请请求号 |
| fundDrawNo | 机构借款申请号 | string(64) | Y |  |
| privilegeName | 权益名称 | string(20) | Y |  |
| privilegeAmt | 权益金额 | decimal | Y | 单位元 |
| privilegeTerm | 权益期数 | integer | Y |  |
| privilegePurchaseTime | 权益购买时间 | string(20) | Y | 格式：yyyy-MM-dd HH:mm:ss |
| privilegeActivateTime | 权益激活时间 | string(20) | Y | 格式：yyyy-MM-dd HH:mm:ss |
| privilegeStatus | 权益订单状态 | string(2) | Y | 00 - 处理中；01 - 还款中；02 - 逾期中；03 - 已结清；04 - 已退贷；05 - 已关单 |
| paidAmount | 支付金额 | string(20) | O | 权益订单状态03时必传 |
| privilegeSettleTime | 结清时间 | string(20) | O | 权益订单状态03时必传，格式：yyyy-MM-dd HH:mm:ss |
| privilegeCancelTime | 退贷时间 | string(20) | O | 权益订单状态04时必传，格式：yyyy-MM-dd HH:mm:ss |
| refundAmount | 退贷金额 | string(20) | O | 权益订单状态04时必传 |
| privilegeExpireTime | 过期时间 | string(20) | Y | 格式：yyyy-MM-dd HH:mm:ss |
| privilegeOverdueDays | 逾期天数 | integer | O | 权益订单状态02时必传 |
| privilegeRepayPlanList | 权益还款计划 | array[PrivilegeRepayPlan] | Y |  |

PrivilegeRepayPlan对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| periodNo | 当期期数 | integer | Y |  |
| dateDue | 应还款日 | string(10) | Y | 格式：yyyy-MM-dd |
| timeRepayEarliest | 最早可还款时间 | string(20) | O | 支持提前还当期时必传。如不传，默认最早可还款时间和应还款日一样。<br>格式：yyyy-MM-dd HH:mm:ss |
| deserveTotalAmt | 应还总金额 | decimal | Y | 还款计划生成后不再变化。单位元，支持小数点后两位。下同。 |
| deservePrinAmt | 应还本金 | decimal | N |  |
| deserveIntAmt | 应还利息 | decimal | N |  |
| deserveOintAmt | 应还罚息 | decimal | N |  |
| deserveLateFeeAmt | 应还滞纳金 | decimal | N |  |
| deserveOtherFeeAmt | 应还其他费用 | decimal | N |  |
| actTotalAmt | 已还总金额 | decimal | Y | 单位元，支持小数点后两位。下同。 |
| actPrinAmt | 已还本金 | decimal | N |  |
| actIntAmt | 已还利息 | decimal | N |  |
| actOintAmt | 已还罚息 | decimal | N |  |
| actLateFeeAmt | 已还滞纳金 | decimal | N |  |
| actOtherFeeAmt | 已还其他费用 | decimal | N |  |
| actDeductTotalAmt | 已减免总金额 | decimal | N |  |
| actDeductPrinAmt | 已减免本金 | decimal | N |  |
| actDeductIntAmt | 已减免利息 | decimal | N |  |
| actDeductOintAmt | 已减免罚息 | decimal | N |  |
| actDeductLateFeeAmt | 已减免滞纳金 | decimal | N |  |
| actDeductOtherFeeAmt | 已减免其他费用 | decimal | N |  |
| payType | 当期扣款方式 | string(2) | O | 01 - 系统批量扣款；02 - 客户主动还款<br>(当前状态为03时必传) |
| status | 当期状态 | string(2) | Y | 01 - 待还款；02 - 逾期中；03 - 当期已结清 |
| overdueDays | 当期逾期天数 | integer | O | 当期状态为02时必传，每一期的逾期天数 |
| settleTime | 当期结清时间 | string(20) | O | 当期状态为03时必传，格式：yyyy-MM-dd HH:mm:ss |
| remark | 描述 | string(256) | N | 备注信息 |

请求参数示例：

```json
{
"drawReqNo":"CR0716595246214803456",
"fundDrawNo":"FCR0716595246214803456",
"privilegeAmt":5000,
"privilegeTerm":3,
"privilegePurchaseTime":"2024-01-17 13:39:41",
"privilegeActivateTime":"2024-01-17 13:39:41",
"privilegeStatus":"01",
"privilegeSettleTime":0,
"privilegeCancelTime":0,
"privilegeOverdueDays":0,
"privilegeRepayPlanList":[
{
"periodNo":1,
"dateDue":"2024-01-17",
"timeRepayEarliest":"2024-01-17 13:39:41",
"deserveTotalAmt":1000,
"deservePrinAmt":800,
"deserveIntAmt":200,
"deserveOintAmt":null,
"deserveLateFeeAmt":null,
"deserveOtherFeeAmt":null,
"actTotalAmt":0,
"actPrinAmt":0,
"actIntAmt":0,
"actOintAmt":0,
"actLateFeeAmt":0,
"actOtherFeeAmt":0,
"actDeductTotalAmt":0,
"actDeductPrinAmt":0,
"actDeductIntAmt":0,
"actDeductOintAmt":0,
"actDeductLateFeeAmt":0,
"actDeductOtherFeeAmt":0,
"payType":"01",
"status":"01",
"overdueDays":0,
"settleTime":0,
"remark":""
},
{
"periodNo":2,
"dateDue":"2024-02-17",
"timeRepayEarliest":"2024-02-17 13:39:41",
"deserveTotalAmt":1000,
"deservePrinAmt":800,
"deserveIntAmt":200,
"deserveOintAmt":null,
"deserveLateFeeAmt":null,
"deserveOtherFeeAmt":null,
"actTotalAmt":0,
"actPrinAmt":0,
"actIntAmt":0,
"actOintAmt":0,
"actLateFeeAmt":0,
"actOtherFeeAmt":0,
"actDeductTotalAmt":0,
"actDeductPrinAmt":0,
"actDeductIntAmt":0,
"actDeductOintAmt":0,
"actDeductLateFeeAmt":0,
"actDeductOtherFeeAmt":0,
"payType":"01",
"status":"01",
"overdueDays":0,
"settleTime":0,
"remark":""
},
{
"periodNo":3,
"dateDue":"2024-03-17",
"timeRepayEarliest":"2024-03-17 13:39:41",
"deserveTotalAmt":1000,
"deservePrinAmt":800,
"deserveIntAmt":200,
"deserveOintAmt":null,
"deserveLateFeeAmt":null,
"deserveOtherFeeAmt":null,
"actTotalAmt":0,
"actPrinAmt":0,
"actIntAmt":0,
"actOintAmt":0,
"actLateFeeAmt":0,
"actOtherFeeAmt":0,
"actDeductTotalAmt":0,
"actDeductPrinAmt":0,
"actDeductIntAmt":0,
"actDeductOintAmt":0,
"actDeductLateFeeAmt":0,
"actDeductOtherFeeAmt":0,
"payType":"01",
"status":"01",
"overdueDays":0,
"settleTime":0,
"remark":""
}
]
}
```

<h4 id="nav-plat-2-6">2.6 推送还款结果</h4>

2.6.1 调用场景

机构合作方请求平台方接口，推送还款结果。

2.6.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/repayResultPush

2.6.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| repayReqNo | 平台还款申请号 | string(64) | Y | 非平台发起场景，包含H5还款、机构批扣等场景，可固定传 RA_RP-999999 |
| fundRepayNo | 机构还款申请号 | string(64) | N |  |
| fundDrawNo | 机构借款申请号 | string(64) | N | 平台借款申请号和机构借款申请号，必须传一个 |
| drawReqNo | 平台借款申请号 | string(64) | N | 平台借款申请号和机构借款申请号，必须传一个 |
| result | 还款结果 | integer(2) | Y | 1 - 还款成功（可继续调用查询借据及还款计划接口）<br>2 - 还款失败<br>3 - 还款处理中<br>4 - 无记录 |
| payType | 支付方式 | integer(2) | Y | 1 - 主动还款，2-批扣， 3 - 线下还款， 4 - 其他 |
| repayDesc | 还款描述 | string | O | 结果2、3时必传 |
| repayDetailInfo | 还款成功详情 | object | O | 结果1时必传 |

repayDetailInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| repaySuccTime | 还款成功时间 | string(20) | Y | yyyy-MM-dd HH:mm:ss |
| repayAmt | 还款总金额 | decimal | Y | 单位（元） |
| repayTerm | 还款期数 | array[integer] | Y | 如为多期还款，用逗号隔开 |
| cardNo | 还款银行卡号 | string(32) | N | 卡号明文 |
| bankCode | 还款银行编码 | string(32) | N | 银行编码与银行名称，详见附录 |
| bankName | 还款银行名称 | string(64) | N | 银行编码与银行名称，详见附录 |
| bankMobile | 还款银行预留手机号 | string(32) | N | 银行预留手机号明文 |

请求参数示例：

```json
{
"repayReqNo":"RP1798798127319823",
"fundRepayNo":"FRP179879812731982",
"result":1,
"payType":1,
"reasonDesc":"还款成功",
"repayDetailInfo":{
"repaySuccTime":"2024-01-15 10:30:00",
"repayAmt":1000,
"repayTerm":[
1
],
"cardNo":"6224567890123456",
"bankCode":"1234",
"bankName":"中国工商银行",
"bankMobile":"13812345678"
}
}
```

<h4 id="nav-plat-2-7">2.7 推送绑卡结果</h4>

2.7.1 调用场景

机构合作方请求平台方接口，推送银行卡绑定结果。适用于客户在机构H5页面完成绑卡、以及客户在机构侧发生换绑卡的场景。

2.7.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/cardBindResultPush

2.7.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userNo | 平台用户号 | string | Y | 平台用户对外唯一标识 |
| fundUserNo | 机构方用户号 | string | N | 机构方用户唯一标识 |
| result | 受理结果 | integer(2) | Y | 1 - 绑卡成功<br>2 - 绑卡失败<br>3 - 受理成功，已发送验证码<br>4 - 重新发送验证码 |
| cardNo | 银行卡号 | string(32) | O | 结果1时必传，卡号明文 |
| bankCode | 银行编码 | string(32) | O | 结果1时必传，银行编码与银行名称，详见附录 |
| bankName | 银行名称 | string(128) | O | 结果1时必传，银行编码与银行名称，详见附录 |
| bankMobile | 银行预留手机号 | string(32) | O | 结果1时必传，银行预留手机号明文 |
| bindTime | 绑定成功时间 | string(32) | O | 结果1时必传，时间格式：yyyy-MM-dd HH:mm:ss |
| reasonDesc | 失败原因描述 | string(256) | O | 结果2时必传 |

请求参数示例：

```json
// 成功
{
"userNo": "UR0670381649694875678",
"fundUserNo": "100159059",
"result": 1,
"cardNo": "621660990898353160",
"bankCode": "0001",
"bankName": "中国银行",
"bankMobile": "15012345678"
}

// 失败
{
"userNo": "UR0670381649694875678",
"fundUserNo": "100159059",
"result": 2,
"reasonDesc": "银行卡不支持"
}
```

<h4 id="nav-plat-2-8">2.8 推送权益还款结果</h4>

2.8.1 调用场景

机构合作方请求平台方接口，推送权益还款结果。

2.8.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/privilegeRepayResultPush

2.8.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| privilegeRepayReqNo | 平台权益还款申请号 | string(64) | Y | 平台权益还款申请请求号 |
| fundPrivilegeRepayNo | 机构权益还款申请号 | string(64) | N | 非平台发起场景，包含H5还款、机构批扣等场景，可固定传 RA_RP-999999 |
| fundDrawNo | 机构借款申请号 | string(64) | N | 平台借款申请号和机构借款申请号，必须传一个 |
| drawReqNo | 平台借款申请号 | string(64) | N | 平台借款申请号和机构借款申请号，必须传一个 |
| result | 还款结果 | integer(2) | Y | 1 - 还款成功（可继续调用查询借据及还款计划接口）<br>2 - 还款失败<br>3 - 还款处理中<br>4 - 无记录 |
| payType | 支付方式 | integer(2) | Y | 1 - 主动还款，2-批扣， 3 - 线下还款， 4 - 其他 |
| repayDesc | 还款描述 | string | O | 结果2、3时必传 |
| repayDetailInfo | 还款成功详情 | object | O | 结果1时必传 |

repayDetailInfo对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| repaySuccTime | 还款成功时间 | string(20) | Y | yyyy-MM-dd HH:mm:ss |
| repayAmt | 还款总金额 | decimal | Y | 单位（元） |
| repayTerm | 还款期数 | array[integer] | Y | 如为多期还款，用逗号隔开 |
| cardNo | 还款银行卡号 | string(32) | N | 卡号明文 |
| bankCode | 还款银行编码 | string(32) | N | 银行编码与银行名称，详见附录 |
| bankName | 还款银行名称 | string(64) | N | 银行编码与银行名称，详见附录 |
| bankMobile | 还款银行预留手机号 | string(32) | N | 银行预留手机号明文 |

请求参数示例：

```json
{
"privilegeRepayReqNo":"RP1798798127319823",
"fundPrivilegeRepayNo":"FRP179879812731982",
"result":1,
"payType":1,
"reasonDesc":"还款成功",
"repayDetailInfo":{
"repaySuccTime":"2024-01-15 10:30:00",
"repayAmt":1000,
"repayTerm":[1],
"cardNo":"6224567890123456",
"bankCode":"1234",
"bankName":"中国工商银行",
"bankMobile":"13812345678"
}
}
```

<h4 id="nav-plat-2-9">2.9 推送AMC订单信息及还款计划</h4>

2.9.1 调用场景

机构合作在放款成功推送AMC信息、AMC订单状态变更、AMC发生还款后，查询用户的AMC订单和还款计划信息。

2.9.2 调用说明

接口类型：同步

通讯方式：HTTP+POST

数据格式：JSON

请求地址：/amcPlanPush

2.9.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| fundOrderNo | 机构AMC订单号 | string(64) | Y |  |
| drawReqNo | 平台借款申请号 | string(64) | O | 平台发起的提现一定要有值<br>平台借款申请请求号 |
| fundDrawNo | 机构借款申请号 | string(64) | Y |  |
| amt | AMC金额 | decimal | Y | 单位：元(小数点后保留两位) |
| term | AMC期数 | integer | Y |  |
| status | AMC订单状态 | string(2) | Y | 00 - 处理中；01 - 还款中；02 - 逾期中；03 - 已结清；04 - 已退贷 ；05-已关单 |
| settleTime | 结清时间 | string(20) | O | AMC订单状态03时必传，格式：yyyy-MM-dd HH:mm:ss |
| cancelTime | 退贷时间 | string(20) | O | AMC订单状态04时必传，格式：yyyy-MM-dd HH:mm:ss |
| refundAmount | 退贷金额 | string(20) | O | AMC订单状态04时必传 |
| overdueDays | 逾期天数 | integer | O | 权益订单状态02时必传 |
| repayPlanList | AMC还款计划 | array[amcRpayPlan] | Y |  |

amcRpayPlan对象

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| periodNo | 当期期数 | integer | Y |  |
| dateDue | 应还款日 | string(10) | Y | 格式：yyyy-MM-dd |
| timeRepayEarliest | 最早可还款时间 | string(20) | O | 支持提前还当期时必传。如不传，默认最早可还款时间和应还款日一样。<br>格式：yyyy-MM-dd HH:mm:ss |
| deserveTotalAmt | 应还总金额 | decimal | Y | 还款计划生成后不再变化。单位元，支持小数点后两位。下同。 |
| deserveDebtConsultationFeeAmt | 应还债务咨询顾问服务费 | decimal | Y |  |
| deserveDebtConsultationPenaltyAmt | 应还债务咨询顾问服务违约金 | decimal | N |  |
| actTotalAmt | 已还总金额 | decimal | Y | 单位元，支持小数点后两位。下同。 |
| actDebtConsultationFeeAmt | 已还债务咨询顾问服务费 | decimal | N |  |
| actDebtConsultationPenaltyAmt | 已还债务咨询顾问服务违约金 | decimal | N |  |
| actDeductTotalAmt | 已减免总金额 | decimal | N |  |
| actDeductDebtConsultationFeeAmt | 已减免债务咨询顾问服务费 | decimal | N |  |
| actDeductDebtConsultationPenaltyAmt | 已减免债务咨询顾问服务违约金 | decimal | N |  |
| payType | 当期扣款方式 | string(2) | N | 01 - 系统批量扣款；02 - 客户主动还款 |
| status | 当期状态 | string(2) | Y | 01 - 待还款；02 - 逾期中；03 - 当期已结清 |
| overdueDays | 当期逾期天数 | integer | O | 当期状态为02时必传，每一期的逾期天数 |
| settleTime | 当期结清时间 | string(20) | O | 当期状态为03时必传，格式：yyyy-MM-dd HH:mm:ss |
| remark | 描述 | string(256) | N | 备注信息 |

请求参数示例：

| JSON |
| --- |

<h2 id="nav-l1-si">四、批量文件【根据实际需要对接】</h2>

<h3 id="nav-si-chunk-1">1. T-1日新增授信申请信息</h3>

<h4 id="nav-si-1-1">1.1 文件说明</h4>

T日上传T-1日新增授信申请信息

通讯方式：SFTP

文件方向：机构平台方 -> 平台方

文件目录：/upload/${机构合作方code}/yyyyMMdd

命名规则：

批量文件名：creditApply_${日期}.txt

实际传输文件名：

加密后文件：creditApply_${日期}.txt.enc

签名文件：creditApply_${日期}.txt.ok

字段分隔符：|+|

字符编码：UTF-8

<h4 id="nav-si-1-2">1.2 数据格式要求</h4>

| 参数名称 | 中文描述 | 参数说明 |
| --- | --- | --- |
| creditReqNo | 平台授信申请号 |  |
| fundCreditNo | 机构授信申请号 |  |
| result | 授信结果 | CR101 - 授信成功（可继续调用额度查询接口）<br>CR102 - 授信拒绝<br>CR103 - 授信申请取消<br>CR104 - 待补件<br>CR105 - 授信中<br>CR106 - 无记录 |
| reasonCode | 拒绝码 | 结果CR102时必传<br>C1010 内部处理失败<br>C1011 资料缺失<br>C1021 风控审核拒绝<br>C1022 资方审核拒绝<br>C2001 其他 |
| reasonDesc | 拒绝原因描述 | 结果CR102时必传 |
| creditFailTime | 授信拒绝时间 | 结果CR102时必传，yyyy-mm-dd hh:mm:ss |
| creditSuccTime | 授信成功时间 | 结果CR101时必传，yyyy-mm-dd hh:mm:ss |
| creditAmt | 授信额度 | 结果CR101时必传，单位元 |
| annualRate | 年利率 | 结果CR101时必传，年利率 |
| creditCancelTime | 授信申请取消时间 | 结果CR103时必传，yyyy-mm-dd hh:mm:ss |
| supplyType | 补件类型 | 结果CR104时必传，ID / FACE / CONTACT / CARD |

<h3 id="nav-si-chunk-2">2. T-1日新增借据信息</h3>

<h4 id="nav-si-2-1">2.1 文件说明</h4>

T日上传T-1日新增借据信息

通讯方式：SFTP

文件方向：机构平台方 -> 平台方

文件目录：/upload/${机构合作方code}/yyyyMMdd

命名规则：

批量文件名：loanCreate_${日期}.txt

实际传输文件名：

加密后文件：loanCreate_${日期}.txt.enc

签名文件：loanCreate_${日期}.txt.ok

字段分隔符：|+|

字符编码：UTF-8

<h4 id="nav-si-2-2">2.2 数据格式要求</h4>

| 参数名称 | 中文描述 | 参数说明 |
| --- | --- | --- |
| drawReqNo | 平台借款申请号 | 平台借款申请请求号 |
| fundDrawNo | 机构借款申请号 |  |
| loanAmt | 放款金额 | 单位：元(小数点后保留两位) |
| loanTerm | 放款期数 |  |
| loanYearRate | 放款年利率 | 默认传IRR计算方式下的年利率。传0.154代表IRR年利率15.4% |
| loanSuccTime | 放款成功时间 | 格式：yyyy-MM-dd HH:mm:ss |
| interestMethod | 计息方式 | 1 - 按日计息；2 - 按月计息 |
| repayMethod | 还款方式 | 1 - 等本等息；2 - 等额本息；3 - 等额本金；4 - 先息后本；5 - 随借随还；6 - 到期还本；7 - 锁期 |
| cardNo | 放款银行卡号 | 卡号明文 |
| bankCode | 放款银行编码 | 银行编码与银行名称，详见附录 |
| bankName | 放款银行名称 | 银行编码与银行名称，详见附录 |
| bankMobile | 放款银行预留手机号 | 银行预留手机号明文 |
| loanStatus | 借据状态 | 01 - 还款中；02 - 逾期中；03 - 已结清；04 - 已退贷 |
| loanSettleTime | 结清时间 | 借据状态03时必传，格式：yyyy-MM-dd HH:mm:ss |
| loanCancelTime | 退贷时间 | 借据状态04时必传，格式：yyyy-MM-dd HH:mm:ss |
| loanOverdueDays | 逾期天数 | 借据状态02时必传 |

<h3 id="nav-si-chunk-3">3. T-1日新增还款计划信息</h3>

<h4 id="nav-si-3-1">3.1 文件说明</h4>

T日上传T-1日新增还款计划信息

通讯方式：SFTP

文件方向：机构平台方 -> 平台方

文件目录：/upload/${机构合作方code}/yyyyMMdd

命名规则：

批量文件名：planCreate_${日期}.txt

实际传输文件名：

加密后文件：planCreate_${日期}.txt.enc

签名文件：planCreate_${日期}.txt.ok

字段分隔符：|+|

字符编码：UTF-8

<h4 id="nav-si-3-2">3.2 数据格式要求</h4>

| 参数名称 | 中文描述 | 参数说明 |
| --- | --- | --- |
| drawReqNo | 平台借款申请号 | 平台借款申请请求号 |
| fundDrawNo | 机构借款申请号 |  |
| periodNo | 当期期数 |  |
| dateDue | 应还款日 | 格式：yyyy-MM-dd |
| timeRepayEarliest | 最早可还款时间 | 支持提前还当期时必传。如不传，默认最早可还款时间和应还款日一样。<br>格式：yyyy-MM-dd HH:mm:ss |
| deserveTotalAmt | 应还总金额 | 还款计划生成后不再变化。单位元，支持小数点后两位。下同。 |
| deservePrinAmt | 应还本金 |  |
| deserveIntAmt | 应还利息 |  |
| deserveOintAmt | 应还罚息 |  |
| deserveLateFeeAmt | 应还滞纳金 |  |
| deserveOtherFeeAmt | 应还其他费用 |  |
| actTotalAmt | 已还总金额 | 单位元，支持小数点后两位。下同。 |
| actPrinAmt | 已还本金 |  |
| actIntAmt | 已还利息 |  |
| actOintAmt | 已还罚息 |  |
| actLateFeeAmt | 已还滞纳金 |  |
| actOtherFeeAmt | 已还其他费用 |  |
| actDeductTotalAmt | 已减免总金额 |  |
| actDeductPrinAmt | 已减免本金 |  |
| actDeductIntAmt | 已减免利息 |  |
| actDeductOintAmt | 已减免罚息 |  |
| actDeductLateFeeAmt | 已减免滞纳金 |  |
| actDeductOtherFeeAmt | 已减免其他费用 |  |
| payType | 当期扣款方式 | 01 - 系统批量扣款；02 - 客户主动还款 |
| status | 当期状态 | 01 - 待还款；02 - 逾期中；03 - 当期已结清 |
| overdueDays | 当期逾期天数 | 当期状态为02时必传，每一期的逾期天数 |
| settleTime | 当期结清时间 | 当期状态为03时必传，格式：yyyy-MM-dd HH:mm:ss |
| remark | 描述 | 备注信息 |

<h3 id="nav-si-chunk-4">4. T-1日变更借据信息</h3>

<h4 id="nav-si-4-1">4.1 文件说明</h4>

T日上传T-1日发生变动的借据信息

通讯方式：SFTP

文件方向：机构平台方 -> 平台方

文件目录：/upload/${机构合作方code}/yyyyMMdd

命名规则：

批量文件名：loanChange_${日期}.txt

实际传输文件名：

加密后文件：loanChange_${日期}.txt.enc

签名文件：loanChange_${日期}.txt.ok

字段分隔符：|+|

字符编码：UTF-8

<h4 id="nav-si-4-2">4.2 数据格式要求</h4>

| 参数名称 | 中文描述 | 参数说明 |
| --- | --- | --- |
| drawReqNo | 平台借款申请号 | 平台借款申请请求号 |
| fundDrawNo | 机构借款申请号 |  |
| loanAmt | 放款金额 | 单位：元(小数点后保留两位) |
| loanTerm | 放款期数 |  |
| loanYearRate | 放款年利率 | 默认传IRR计算方式下的年利率。传0.154代表IRR年利率15.4% |
| loanSuccTime | 放款成功时间 | 格式：yyyy-MM-dd HH:mm:ss |
| interestMethod | 计息方式 | 1 - 按日计息；2 - 按月计息 |
| repayMethod | 还款方式 | 1 - 等本等息；2 - 等额本息；3 - 等额本金；4 - 先息后本；5 - 随借随还；6 - 到期还本；7 - 锁期 |
| cardNo | 放款银行卡号 | 卡号明文 |
| bankCode | 放款银行编码 | 银行编码与银行名称，详见附录 |
| bankName | 放款银行名称 | 银行编码与银行名称，详见附录 |
| bankMobile | 放款银行预留手机号 | 银行预留手机号明文 |
| loanStatus | 借据状态 | 01 - 还款中；02 - 逾期中；03 - 已结清；04 - 已退贷 |
| loanSettleTime | 结清时间 | 借据状态03时必传，格式：yyyy-MM-dd HH:mm:ss |
| loanCancelTime | 退贷时间 | 借据状态04时必传，格式：yyyy-MM-dd HH:mm:ss |
| loanOverdueDays | 逾期天数 | 借据状态02时必传 |

<h3 id="nav-si-chunk-5">5. T-1日变更还款计划信息</h3>

<h4 id="nav-si-5-1">5.1 文件说明</h4>

T日上传T-1日发生变动的还款计划信息

通讯方式：SFTP

文件方向：机构平台方 -> 平台方

文件目录：/upload/${机构合作方code}/yyyyMMdd

命名规则：

批量文件名：planChange_${日期}.txt

实际传输文件名：

加密后文件：planChange_${日期}.txt.enc

签名文件：planChange_${日期}.txt.ok

字段分隔符：|+|

字符编码：UTF-8

<h4 id="nav-si-5-2">5.2 数据格式要求</h4>

| 参数名称 | 中文描述 | 参数说明 |
| --- | --- | --- |
| drawReqNo | 平台借款申请号 | 平台借款申请请求号 |
| fundDrawNo | 机构借款申请号 |  |
| periodNo | 当期期数 |  |
| dateDue | 应还款日 | 格式：yyyy-MM-dd |
| timeRepayEarliest | 最早可还款时间 | 支持提前还当期时必传。如不传，默认最早可还款时间和应还款日一样。<br>格式：yyyy-MM-dd HH:mm:ss |
| deserveTotalAmt | 应还总金额 | 还款计划生成后不再变化。单位元，支持小数点后两位。下同。 |
| deservePrinAmt | 应还本金 |  |
| deserveIntAmt | 应还利息 |  |
| deserveOintAmt | 应还罚息 |  |
| deserveLateFeeAmt | 应还滞纳金 |  |
| deserveOtherFeeAmt | 应还其他费用 |  |
| actTotalAmt | 已还总金额 | 单位元，支持小数点后两位。下同。 |
| actPrinAmt | 已还本金 |  |
| actIntAmt | 已还利息 |  |
| actOintAmt | 已还罚息 |  |
| actLateFeeAmt | 已还滞纳金 |  |
| actOtherFeeAmt | 已还其他费用 |  |
| actDeductTotalAmt | 已减免总金额 |  |
| actDeductPrinAmt | 已减免本金 |  |
| actDeductIntAmt | 已减免利息 |  |
| actDeductOintAmt | 已减免罚息 |  |
| actDeductLateFeeAmt | 已减免滞纳金 |  |
| actDeductOtherFeeAmt | 已减免其他费用 |  |
| payType | 当期扣款方式 | 01 - 系统批量扣款；02 - 客户主动还款 |
| status | 当期状态 | 01 - 待还款；02 - 逾期中；03 - 当期已结清 |
| overdueDays | 当期逾期天数 | 当期状态为02时必传，每一期的逾期天数 |
| settleTime | 当期结清时间 | 当期状态为03时必传，格式：yyyy-MM-dd HH:mm:ss |
| remark | 描述 | 备注信息 |

<h3 id="nav-si-chunk-6">6. T-1日放款交易流水</h3>

<h4 id="nav-si-6-1">6.1 文件说明</h4>

T日上传T-1日发生的放款交易流水

通讯方式：SFTP

文件方向：机构平台方 -> 平台方

文件目录：/upload/${机构合作方code}/yyyyMMdd

命名规则：

批量文件名：drawTransFlow_${日期}.txt

实际传输文件名：

加密后文件：drawTransFlow_${日期}.txt.enc

签名文件：drawTransFlow_${日期}.txt.ok

字段分隔符：|+|

字符编码：UTF-8

<h4 id="nav-si-6-2">6.2 数据格式要求</h4>

| 参数名称 | 中文描述 | 参数说明 |
| --- | --- | --- |
| creditReqNo | 平台授信申请号 |  |
| fundCreditNo | 机构授信申请号 |  |
| fundDrawNo | 机构借款申请号 | 结果非DR108时必传 |
| drawReqNo | 平台借款申请号 | 结果非DR108时，如果从平台发起的借款必传 |
| result | 放款结果 | DR101 - 放款成功（可继续调用查询借据及还款计划接口）<br>DR102 - 放款失败<br>DR103 - 放款拒绝<br>DR104 - 放款申请取消<br>DR105 - 待补件<br>DR106 - 需重新匹配资金方（需验证短信）<br>DR107 - 需重新匹配资金方（无需验证，直接发起新申请）<br>DR108 - 放款中<br>DR109 - 无记录（查无记录；或者半流程机构，授信通过未放款） |
| drawStatusUpdateTime | 放款状态变更时间 | 状态变更时必传，格式：yyyy-MM-dd HH:mm:ss |
| loanAmt | 放款金额 | 结果为DR101时必传，单位元 |
| loanTerm | 放款期数 | 结果为DR101时必传 |
| reasonCode | 失败原因码 | 结果为DR102、DR103时必传<br>D1010 内部处理失败<br>D1011 资料缺失<br>D1021 风控拒绝<br>D1022 资方审核拒绝<br>D2001 其他 |
| reasonDesc | 失败原因描述 | 结果为DR102、DR103时必传 |
| drawFreezeEndTime | 放款冻结结束时间 | 结果为DR102、DR103、DR104 时可传<br>格式：yyyy-MM-dd HH:mm:ss |
| supplyType | 补件类型 | 结果为DR105时必传，ID / FACE / CONTACT / PROFILE / CARD |
| isPrivilegeProcess | 权益标签 | 结果为DR101时必传，表示最终放款是否含权益。<br>Y - 放款有权益（可继续调用查询权益订单及还款计划接口）<br>N - 放款无权益 |
| fundPrivilegeOrderNo | 机构权益订单号 | 机构权益订单号。权益标识Y情况下，可传 |
| privilegeAmt | 权益放款金额 | 权益标识为Y的情况下必传 |
| privilegeTerm | 权益放款期数 | 权益标识为Y的情况下必传 |
| privilegePurchaseTime | 权益放款购买时间 | 权益标识为Y的情况下必传，格式：yyyy-MM-dd HH:mm:ss |

<h3 id="nav-si-chunk-7">7. T-1日还款交易流水</h3>

<h4 id="nav-si-7-1">7.1 文件说明</h4>

T日上传T-1日发生的还款交易流水

通讯方式：SFTP

文件方向：机构平台方 -> 平台方

文件目录：/upload/${机构合作方code}/yyyyMMdd

命名规则：

批量文件名：repayTransFlow_${日期}.txt

实际传输文件名：

加密后文件：repayTransFlow_${日期}.txt.enc

签名文件：repayTransFlow_${日期}.txt.ok

字段分隔符：|+|

字符编码：UTF-8

<h4 id="nav-si-7-2">7.2 数据格式要求</h4>

| 参数名称 | 中文描述 | 参数说明 |
| --- | --- | --- |
| drawReqNo | 平台借款申请号 |  |
| fundDrawNo | 机构借款申请号 |  |
| repayReqNo | 平台还款申请号 |  |
| fundRepayNo | 机构还款申请号 |  |
| result | 还款结果 | 1 - 还款成功（可继续调用查询借据及还款计划接口）<br>2 - 还款失败<br>3 - 还款处理中 |
| payType | 支付方式 | 1 - 主动还款，2-批扣， 3 - 线下还款， 4 - 其他 |
| repayDesc | 还款描述 | 结果2时必传 |
| repayDetailInfo | 还款成功详情 | 结果1时必传 |
| repayTerm | 还款期数 | 如为多期还款，用逗号隔开 |

<h3 id="nav-si-chunk-8">8. T-1日代偿交易流水</h3>

<h4 id="nav-si-8-1">8.1 文件说明</h4>

T日上传T-1日发生的代偿交易流水

通讯方式：SFTP

文件方向：机构平台方 -> 平台方

文件目录：/upload/${机构合作方code}/yyyyMMdd

命名规则：

批量文件名：compensateTransFlow_${日期}.txt

实际传输文件名：

加密后文件：compensateTransFlow_${日期}.txt.enc

签名文件：compensateTransFlow_${日期}.txt.ok

字段分隔符：|+|

字符编码：UTF-8

<h4 id="nav-si-8-2">8.2 数据格式要求</h4>

| 参数名称 | 中文描述 | 参数说明 |
| --- | --- | --- |
| drawReqNo | 平台借款申请号 | 平台借款申请请求号 |
| fundDrawNo | 机构借款申请号 |  |
| result | 代偿结果 | 1 - 代偿成功<br>2 - 代偿失败<br>3 - 代偿处理中 |
| reasonDesc | 失败原因描述 | 结果2时必传 |
| repaySuccTime | 代偿成功时间 | 结果1时必传 |
| repayAmt | 代偿总金额 | 单位元 |
| repayTerm | 代偿期数 | 如为多期还款，用逗号隔开 |

<h2 id="nav-l1-wu">五、附录</h2>

<h3 id="nav-wu-1">1. 婚姻状况</h3>

| 码值 | 说明 |
| --- | --- |
| 01 | 未婚 |
| 02 | 离异 |
| 03 | 已婚有子女 |
| 04 | 已婚无子女 |

<h3 id="nav-wu-2">2. 最高学历</h3>

| 码值 | 说明 |
| --- | --- |
| 01 | 研究生或以上 |
| 02 | 大学本科 |
| 03 | 大学专科 |
| 04 | 高中或中专 |
| 05 | 初中及以下 |

<h3 id="nav-wu-3">3. 负债情况</h3>

| 码值 | 说明 |
| --- | --- |
| 01 | 无负债 |
| 02 | 0-3000元 |
| 03 | 3000-6000元 |
| 04 | 6000-10000元 |
| 05 | 10000-15000元 |
| 06 | 15000-20000元 |
| 07 | 20000元以上 |

<h3 id="nav-wu-4">4. 住宅类型</h3>

| 码值 | 说明 |
| --- | --- |
| 01 | 租房 |
| 02 | 产权房产 |
| 03 | 公司宿舍 |
| 04 | 和家人同住 |
| 05 | 其他 |

<h3 id="nav-wu-5">5. 借款用途</h3>

| 码值 | 说明 |
| --- | --- |
| 01 | 购物 |
| 02 | 装修 |
| 03 | 旅游 |
| 04 | 买车 |
| 05 | 教育 |
| 06 | 结婚 |
| 07 | 医疗 |
| 08 | 其他 |

<h3 id="nav-wu-6">6. 行业</h3>

| 码值 | 说明 |
| --- | --- |
| 01 | 信息传输/软件/信息技术服务业 |
| 02 | 金融业 |
| 03 | 建筑业 |
| 04 | 房地产 |
| 05 | 批发/零售业 |
| 06 | 教育 |
| 07 | 文化/体育/娱乐业 |
| 08 | 卫生/社会工作 |
| 09 | 电力/热力/燃气/水生产/供应业 |
| 10 | 农业 |
| 11 | 制造业 |
| 12 | 居民服务/修理/其他服务业 |
| 13 | 公共管理/社会保障/社会组织/国际组织 |
| 14 | 住宿/餐饮业 |
| 15 | 其他 |

<h3 id="nav-wu-7">7. 职业类别</h3>

| 码值 | 说明 |
| --- | --- |
| 01 | 上班 |
| 02 | 兼职 |
| 03 | 企业主 |
| 04 | 无业 |
| 05 | 个体户 |

<h3 id="nav-wu-8">8. 收入类型</h3>

| 码值 | 说明 |
| --- | --- |
| 01 | 工资 |
| 02 | 经营收入 |
| 03 | 投资收入 |
| 04 | 房租收入 |
| 05 | 其他 |

<h3 id="nav-wu-9">9. 收入情况</h3>

| 码值 | 说明 |
| --- | --- |
| 01 | 3000以下 |
| 02 | 3000-6000 |
| 03 | 6000-10000 |
| 04 | 10000-30000 |
| 05 | 30000以上 |

<h3 id="nav-wu-10">10. 公司类型</h3>

| 码值 | 说明 |
| --- | --- |
| 01 | 政府或企事业单位 |
| 02 | 国企央企 |
| 03 | 外资企业 |
| 04 | 上市公司 |
| 05 | 普通民营企业 |
| 06 | 个体工商户 |
| 07 | 其他 |

<h3 id="nav-wu-11">11. 联系人关系</h3>

| 码值 | 说明 |
| --- | --- |
| 01 | 父亲 |
| 02 | 母亲 |
| 03 | 配偶 |
| 04 | 儿子 |
| 05 | 女儿 |
| 06 | 朋友 |
| 07 | 同事 |

<h3 id="nav-wu-12">12. 银行编码映射</h3>

| 银行编码 | 银行名称 |
| --- | --- |
| 0001 | 中国银行 |
| 0002 | 农业银行 |
| 0003 | 工商银行 |
| 0004 | 建设银行 |
| 0005 | 交通银行 |
| 0006 | 光大银行 |
| 0007 | 民生银行 |
| 0008 | 平安银行 |
| 0009 | 邮储银行 |
| 0010 | 广发银行 |
| 0011 | 中信银行 |
| 0012 | 华夏银行 |
| 0013 | 浦发银行 |
| 0014 | 兴业银行 |
| 0015 | 招商银行 |
| 0016 | 南京银行 |
| 0017 | 杭州银行 |
| 0018 | 上海银行 |
| 0019 | 北京银行 |
