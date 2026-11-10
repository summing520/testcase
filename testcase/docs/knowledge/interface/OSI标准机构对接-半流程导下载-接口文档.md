# [新版] 乐享借机构合作标准接口文档

## 一、概述

### 1. 文档简介

此文档作为乐享借平台与助贷机构合作方进行互联网信贷业务合作的对接文档，详细描述了乐享借平台与机构合作方之间的标准交互流程。

### 2. 版本变更记录

| 版本号 | 修订时间 | 修订内容 | 修订人 |
| --- | --- | --- | --- |
| V1.0 | 2026-4-27 | 初版 |  |

## 二、对接说明

### 1. 回调环境说明

- 开发环境：https://test2.xurongwl.com/cbg/goa/api/p/平台分配的机构编码/接口名
- 测试环境：https://test3.xurongwl.com/cbg/goa/api/p/平台分配的机构编码/接口名
- 生产环境：https://a.loloabz.com/cbg/goa/api/p/平台分配的机构编码/接口名

### 2. 接入说明

- 使用 HTTPS 协议进行数据通信
- 使用 POST json 方式发送请求，数据类型为application/json
- 使用 UTF-8 字符集编码
- 双方交换RSA公钥，乐享借提供机构编码、md5Salt给合作方

### 3. 数据安全

- 使用对称加密+非对称加密+签名保证安全，流程：
- 双方生成 RSA 的公私钥，交换 RSA 公钥
- 请求方生成随机的 AES 密钥，对明文进行加密，然后使用对方的RSA 的公钥对这个随机密钥进行加密
- 最后将 AES 加密后的数据、RSA 加密后的随机密钥、当前时间戳、md5盐值拼在一起，用 MD5 算法生成签名
- 接受方校验签名后，RSA 解密得到随机密钥，然后再做 AES 解密得到明文
- demo

> （原 Word 为 EMF 流程示意图，已省略。）

### 4. 参数结构

#### 4.1 说明

| - | 符号 | 说明 |
| --- | --- | --- |
| 是否必须 | Y | 必须 |
|  | N | 非必须 |
|  | O | 一定情况下必须 |

#### 4.2 请求参数结构

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| timestamp | 时间戳 | long | Y | 时间戳，毫秒值 |
| sign | 数据签名 | string | Y |  |
| key | 随机密钥 | string | Y |  |
| content | 请求业务数据 | string | Y | json加密后的string 详见各接口定义 |

请求参数示例：

| JSON { "timestamp":1705484734000, "key":"xxxxx", "sign":"xxxx", "content":"json加密后的值" } |
| --- |

#### 4.3 响应参数结构

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| timestamp | 时间戳 | long | Y | 时间戳，毫秒值 |
| sign | 数据签名 | string | Y |  |
| key | 随机密钥 | string | Y |  |
| content | 响应业务数据 | string | Y | json加密后的string |

content

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| code | 响应码 | string | Y | 详见4.4公用响应码定义 |
| msg | 响应信息 | string | O | code 不为 200时，必传 |
| bizData | 业务数据 | object | O | 详见各接口定义 |

响应参数示例：

| JSON { "timestamp":1705484736000, "key":"xxxxx", "sign":"xxxx", "content":"json加密后的值" } |
| --- |

#### 4.4 公用响应码

| 响应码 / code | 说明 |
| --- | --- |
| 200 | 响应成功 |
| 1001 | 系统异常（内部系统异常或网络异常） |
| 1002 | 参数错误 |
| 1003 | 签名错误 |
| 1100 | 其他 |

### 5. 接口总览

| 接口类型 | 业务环节 | 对接接口 | 是否必须 | 备注说明 |
| --- | --- | --- | --- | --- |
| 机构合作方提供接口 | 准入授信 | 1.1 准入撞库 | Y |  |
| 机构合作方提供接口 | 准入授信 | 1.2 授信申请提交 | Y |  |
| 机构合作方提供接口 | 准入授信 | 1.3 查询授信申请结果 | Y |  |
| 机构合作方提供接口 | 通用 | 2.1 查询用户额度 | Y |  |
| 机构合作方提供接口 | 通用 | 2.2 查询用户协议 | Y | 只关注授信协议 |
| 机构合作方提供接口 | 通用 | 2.3 获取场景页面地址 | Y | 只关注下载地址 |
| 平台方提供接口 | - | 2.1 推送授信结果 | Y |  |
| 平台方提供接口 | - | 2.2 推送额度变更 | Y |  |

## 三、联机接口

### 1. 机构合作方提供接口

#### 1. 准入授信相关接口

##### 1.1 准入撞库

###### 1.1.1 调用场景

平台方请求机构合作方接口，合作方对用户进行前置准入检查、并返回准入结果，准入成功则可进行后续申请。

###### 1.1.2 调用说明

- 接口类型：同步
- 通讯方式：HTTP+POST
- 数据格式：JSON
- 请求地址：/userAccess

###### 1.1.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| mobileNoMd5 | 手机号md5 | string(64) | Y | 32位md5小写 |
| idNoMd5 | 身份证号md5 | string(64) | N | 32位md5小写 |
| mobileIdNoMd5 | ⼿机号+⾝份证号md5 | string(64) | N | 32位md5小写 |
| userName | 用户姓名 | string(64) | N | 明文 |

*手机号md5为必传，其他参数按照双方约定以实际需要传输*

请求参数示例：

| JSON { "mobileNoMd5": "77a8b9df79de0206dc622a74288e81a6", "idNoMd5": "2441abbcd153c7778ff2852552c494b8" } |
| --- |

###### 1.1.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 准入结果 | integer(2) | Y | 1 - 准入通过；2 - 准入拒绝 |
| reasonDesc | 拒绝原因描述 | string(256) | O | 结果2时必传 |

响应参数示例：

| JSON // 准入通过 { "result": 1 } // 准入拒绝 { "result": 2, "reasonDesc": "黑名单用户" } |
| --- |

##### 1.2 授信申请提交

###### 1.2.1 调用场景

平台方请求机构合作方接口，提供用户授信申请详细信息、向机构方进件，机构方返回申请受理成功和失败的结果。受理成功，则可继续调用查询授信结果接口。

###### 1.2.2 调用说明

- 接口类型：同步
- 通讯方式：HTTP+POST
- 数据格式：JSON
- 请求地址：/creditApply

###### 1.2.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| creditReqNo | 平台授信申请号 | string(64) | Y |  |
| userNo | 平台用户号 | string(64) | Y | 平台用户对外唯一标识 |
| fundUserNo | 机构方用户号 | string(64) | N | 机构方用户唯一标识 |
| userBaseInfo | 用户基本信息 | object | Y | 详见下表 |
| userProfileInfo | 用户详细信息 | object | Y | 详见下表 |
| cardInfo | 用户银行卡信息 | object | O | 绑卡在授信环节时，必传 |
| authIdInfo | 用户身份证信息 | object | Y | 详见下表 |
| authFaceInfo | 用户活体信息 | object | Y | 详见下表 |
| jobInfo | 用户公司信息 | object | Y | 详见下表 |
| contactInfo | 用户联系人信息 | object | Y | 详见下表 |
| deviceInfo | 设备信息 | object | Y | 详见下表 |
| geoInfo | 定位信息 | object | Y | 详见下表 |
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
| deviceModel |  | string(32) | N | IOS:设备类型名称：iphone/ipod/ipad Android：设备型号：PBEM00。有则传 |
| deviceBrand | 设备品牌 | string(32) | N | 设备品牌：OPPO（仅Android有）。有则传 |
| memory | MB设备内存 | float | N | 有则传 |
| storage | MB设备总存储 | float | N | 有则传 |
| unuseStorage | MB设备剩余存储 | float | N | 有则传 |
| deviceResolution | 设备屏幕分辨率 | string(32) | N | 有则传 |
| bettary | 设备当前电量百分比 | float | N | 有则传 |
| isProxy | 省呗是否使用代理 | int | N | 0.否 1.是 2.未知。有则传 |
| simCount | SIM的个数 | int | N | 0,1,2。有则传 |
| withSim | 是否有SIM | int | N | 0.否 1.是 2.未知。有则传 |
| teleNum | 运营商编码 | string(32) | N | 中国移动、中国联通、中国电信。有则传 |
| deviceUa | 浏览器 | string(32) | N | 浏览器UA。有则传 |
| debugState | 手机是否调试状态 | int | N | 0.否 1.是 2.未知。有则传 |
| isPpn | 是否使用VPN | int | N | 0.否 1.是 2.未知。有则传 |
| isUsbDebug | 是否开启USB调试 | int | N | 0.否 1.是 2.未知。有则传 |
| androidId | 设备唯一id | string(32) | N | 设备唯一id(仅Android设备有) |
| imei | 设备唯一id | string(32) | N | 设备唯一id(仅Android设备有) |
| oaid | 安全联盟统一id | string(32) | N | 仅Android设备有 |
| network | 网络类型 | int | N | 0.移动网络 1.WiFi 2.无网络 -1.未知网络（仅Android设备有） |
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

| JSON { "creditReqNo": "CR07103777521223233233380", "userNo": "U1703648207", "fundUserNo": "1703648219", "userBaseInfo": { "userName": "小张", "mobileNo": "12344434444" }, "userProfileInfo": { "marriage": "01", "monthIncome": "01", "education": "01", "debtSituation": "01", "expectedLoanAmt": 3000.00, "expectedLoanTerm": 12, "residentialType": "02", "autoAddress": "上海市-上海市辖区-浦东新区", "addressDetail": "上海市浦东新区花木街道杨高南路辅路中国石化上海浦东科研信息办公综合基地", "residentialProvince": "上海市", "residentialCity": "上海市辖区", "residentialDistrict": "浦东新区", "email": "4543949w899@163.com" }, "cardInfo": { "cardNo": "6230183543234564333333", "bankCode": "0001", "bankName": "中国银行", "bankMobile": "134271364934" }, "authIdInfo": { "idCardFrontImgUrl": "http://example.com/身份证/正面照片.jpg", "idCardBackImgUrl": "http://example.com/身份证/背面照片.jpg", "idCardNo": "2343224422234094494", "idCardSex": "0", "idCardBirthday": "1979-08-23", "idCardEthnicity": "汉", "idCardAddress": "上海市浦东新区花木街道杨高南路辅路中国石化上海浦东科研信息办公综合基地", "idCardStartDate": "20080314", "idCardEndDate": "20180314", "idCardAuthority": "深圳市公安局" }, "authFaceInfo": { "faceSource": 1, "faceImg1Url": "http://example.com/活体照片1.jpg", "faceImg2Url": "http://example.com/活体照片2.jpg", "faceScore": 95.5, "faceCollectTime": "2023-12-26 10:30:00" }, "jobInfo": { "jobIndustry": "01", "jobCategory": "01", "incomeType": "02", "companyName": "天益传媒有限公司", "companyType": "02", "companyAddress": "西藏自治区张家港兴山澳门街G座", "companyAddressDetail": "西藏自治区张家港兴山澳门街G座陈路B座", "companyTel": "021-54722222" }, "contactInfo": { "contactOneName": "张大", "contactOneTel": "13918239292", "contactOneRel": "01", "contactTwoName": "张大", "contactTwoTel": "13918232312", "contactTwoRel": "03" }, "deviceInfo": { "ip": "192.168.0.1", "os": "ios" }, "geoInfo": { "latitude": "35.359542", "longitude": "117.455610" } } |
| --- |

###### 1.2.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 受理结果 | integer | Y | 1 - 受理成功；2 - 受理失败 |
| reasonDesc | 失败原因描述 | string(200) | O | 结果2时必传 |
| fundCreditNo | 机构授信申请号 | string(64) | N | 结果1时可传 |

响应参数示例：

| JSON // 受理成功 { "result": 1, "fundCreditNo":"43848959939599495959" } // 受理失败 { "result": 2, "reasonDesc":"OCR姓名不符合规范" } |
| --- |

##### 1.3 查询授信申请结果

###### 1.3.1 调用场景

平台方请求机构合作方接口，查询用户授信申请结果。

###### 1.3.2 调用说明

- 接口类型：同步
- 通讯方式：HTTP+POST
- 数据格式：JSON
- 请求地址：/creditResultQuery

###### 1.3.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| creditReqNo | 平台授信申请号 | string(64) | Y |  |
| fundCreditNo | 机构授信申请号 | string(64) | N |  |

请求参数示例：

| JSON { "creditReqNo": "AP0710324673086914560", "fundCreditNo": "123412341234" } |
| --- |

###### 1.3.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| result | 授信结果 | string(8) | Y | CR101 - 授信成功（可继续调用额度查询接口） CR102 - 授信拒绝 CR103 - 授信申请取消 CR104 - 待补件【暂不支持】 CR105 - 授信中 CR106 - 无记录（如因网络等问题，授信申请未实际提交到合作方，导致合作方查询不到对应流水号的申请结果，需返回CR106无记录） |
| fundCreditNo | 机构授信申请号 | string(64) | O | 结果CR101时必传 |
| reasonCode | 拒绝码 | string(8) | O | 结果CR102时必传 C1010 内部处理失败 C1011 资料缺失 C1021 风控审核拒绝 C1022 资方审核拒绝 C2001 其他 |
| reasonDesc | 拒绝原因描述 | string(256) | O | 结果CR102时必传 |
| creditFailTime | 授信拒绝时间 | string(32) | O | 结果CR102时必传，yyyy-mm-dd hh:mm:ss |
| creditFailFrozenTime | 授信被拒封禁期 | string(32) | O | 结果CR102时必传，yyyy-mm-dd hh:mm:ss |
| creditSuccTime | 授信成功时间 | string(32) | O | 结果CR101时必传，yyyy-mm-dd hh:mm:ss |
| creditAmt | 授信额度 | decimal(32) | O | 结果CR101时必传，单位元 |
| annualRate | 年利率 | string(16) | O | 结果CR101时必传，年利率 示例0.2399，代表年化23.99% |
| creditCancelTime | 授信申请取消时间 | string(32) | O | 结果CR103时必传，yyyy-mm-dd hh:mm:ss |
| supplyType | 补件类型 | string(16) | O | 结果CR104时必传，ID / FACE / CONTACT / CARD |

响应参数示例：

| JSON // 成功 { "result": "CR101", "creditSuccTime": "2023-12-27 11:11:11", "creditAmt": "5000", "annualRate": "4.35" } // 拒绝 { "result": "CR102", "reasonCode": "C1011", "creditFailTime": "2023-12-27 11:11:11", "reasonDesc": "身份证资料缺失" } // 取消 { "result": "CR103", "creditCancelTime": "2023-12-27 11:11:11" } // 待补件 { "result": "CR104", "reasonDesc": "需要补充资料", "supplyType": "CONTACT" } // 授信申请中 { "result": "CR105" } |
| --- |

#### 2. 通用接口

##### 2.1 查询用户额度

###### 2.1.1 调用场景

平台方请求机构合作方接口，在授信成功后，查询用户额度、定价等相关信息。

###### 2.1.2 调用说明

- 接口类型：同步
- 通讯方式：HTTP+POST
- 数据格式：JSON
- 请求地址：/accountInfoQuery

###### 2.1.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userNo | 平台用户号 | string(64) | Y | 平台用户对外唯一标识 |
| fundUserNo | 机构方用户号 | string(64) | N | 机构方用户唯一标识 |
| creditReqNo | 平台授信申请号 | string(64) | Y |  |
| fundCreditNo | 机构授信申请号 | string(64) | N |  |

请求参数示例：

| JSON { "creditReqNo": "AP0710324673086914560", "userNo": "UR0722566261684408320" } |
| --- |

###### 2.1.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| status | 额度状态 | integer(2) | Y | 1 - 可用（有可用额度，用户可发起借款申请） 2 - 失效（无可用额度，需重新授信） 3 - 锁定（额度已使用，借款审核中）【暂不支持】 |
| creditAmt | 授信额度 | decimal | Y | 单位元 |
| availableAmt | 可用额度 | decimal | Y | 单位元。 如存在额度临时冻结场景，可传额度状态=1，可用额度=0；额度恢复后再传更新后的可用额度。 额度失效情况下，可用额度=0。 |
| maxAvailableAmt | 最大可用额度 | decimal | Y | 单位元 |
| minAvailableAmt | 最小可用额度 | decimal | Y | 单位元 |
| step | 额度步长 | decimal | N | 单位元 |
| creditValidTime | 额度生效时间 | string(20) | Y | 格式：yyyy-MM-dd HH:mm:ss |
| creditExpireTime | 额度失效时间 | string(20) | Y | 格式：yyyy-MM-dd HH:mm:ss。 说明：变更额度状态/授信额度/可用额度时涉及更新 额度状态变更为额度失效时，需给小于当前时间的额度失效时间（否则无法触发我方额度失效逻辑）。 授信额度/可用额度更新时，根据实际需要更新额度失效时间。 |
| repayMethod | 还款方式 | integer | Y | 1 - 等本等息；2 - 等额本息；3 - 等额本金；4 - 先息后本；5 - 随借随还；6 - 到期还本；7 - 锁期 |
| rateType | 利率类型 | string(8) | Y | APR / IRR |
| rateUnit | 利率单位 | string(8) | Y | DAY - 日；MONTH - 月；YEAR - 年 |
| rate | 利率 | string(16) | Y | 如0.15，表示利率15.4% |
| availableTerms | 可借期数 | list[integer] | Y | 以此返回为准，对客展示 |
| capitalCode | 资方 | string(20) | N |  |

响应参数示例：

| JSON { "status": 1, "creditAmt": 10000.00, "maxAvailableAmt": 8000.00, "minAvailableAmt": 1000.00, "step": 1000.00, "creditValidTime": "2024-01-17 13:39:41", "creditExpireTime": "2024-01-17 13:39:41", "repayMethod": 1, "rateType": "APR", "rateUnit": "DAY", "rate": "0.55", "availableTerms": [6, 12, 18, 24], "capitalCode": "ABC123XYZ" } |
| --- |

##### 2.2 查询用户协议

###### 2.2.1 调用场景

平台方请求机构合作方接口，在授信、借款、绑卡等不同场景下调用，获取不同对客展示协议。

###### 2.2.2 调用说明

- 接口类型：同步
- 通讯方式：HTTP+POST
- 数据格式：JSON
- 请求地址：/agreementList

###### 2.2.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userNo | 平台用户号 | string(64) | Y | 平台用户对外唯一标识（scene为REGISTER，非必传） |
| scene | 查询场景 | string(32) | Y | REGISTER - 注册【暂不支持】 CREDIT - 授信 DRAW - 借款（非权益） PRIVILEGE_DRAW-借款（权益） BIND - 绑卡 LOAN - 借据详情【暂不支持】 REPAY - 还款【暂不支持】 PRIVILEGE - 权益 |
| creditReqNo | 授信申请号 | string(64) | N | scene为DRAW，必传 |
| drawReqNo | 借款申请号 | string(64) | N | scene为REPAY，必传 |
| loanAmt | 试算借款金额 | decimal | O | 单位：元(小数点后保留两位)。scene为DRAW，必传。 如需填充对客协议，可使用。 |
| loanTerm | 试算借款期数 | integer | O | 不支持传多个期数。scene为DRAW，必传。 如需填充对客协议，可使用。 |
| userName | 用户姓名 | string(64) | N | 明文。scene为CREDIT，有则传。 如需填充对客协议，可使用。 |
| idNo | 用户身份证号 | string(30) | N | 明文。scene为CREDIT，有则传。 如需填充对客协议，可使用。 |

请求参数示例：

| JSON { "userNo": null, "fundUserNo": null, "scene": "REGISTER", "creditReqNo": null， "drawReqNo": null } |
| --- |

###### 3.2.4 响应参数

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

| JSON { "agreements": [ { "agreementName": "用户隐私协议", "agreementUrl": "https://mswl.info/protocol/content/direct/t_lxj_ys_KHF7YD" }, { "agreementName": "用户服务协议", "agreementUrl": "https://stc.xurongwl.com/protocol/register/fuwu.html" } ], "isDefaultselect": "N", "isForceRead": "N", "forceReadTime": null } |
| --- |

##### 2.3 查询场景页面地址

###### 2.3.1 调用场景

根据机构合作方流程和产品要求，可选择对接此接口。平台方请求机构合作方接口，在授信、借款、绑卡等不同场景下调用，获取机构H5页面跳转地址。

###### 2.3.2 调用说明

- 接口类型：同步
- 通讯方式：HTTP+POST
- 数据格式：JSON
- 请求地址：/sceneUrlQuery

###### 2.3.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userNo | 平台用户号 | string(64) | Y | 平台用户对外唯一标识 |
| scene | 查询场景 | string(64) | Y | DRAW - H5借款地址 DRAW_PRIVILEGE_REDEEM- H5权益兑换地址 REPAY - H5还款地址 REPAY_PRIVILEGE - H5权益还款地址 BIND - H5绑卡地址 SIGN - H5签约地址 SUPPLY - H5补充资料地址 DOWN - H5下载地址 |
| creditReqNo | 平台授信申请号 | string(64) | N |  |
| fundDrawNo | 机构借款申请号 | string(64) | N | 获取还款地址时，必传 |
| returnUrl | 回跳地址 | string(512) | N |  |

请求参数示例：

| JSON { "userNo":"UR0710379035226226688", "scene":"BIND", "creditReqNo":"CR0673827201381298176", "fundDrawNo":"Fund0673827201381298175", "returnUrl":"https://xxxx.com/xxxx", } |
| --- |

###### 2.3.4 响应参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| url | 页面地址 | string(512) | Y |  |

响应参数示例：

| JSON { "url":"https://xxxx/bindcardurl/xxxx" } |
| --- |

### 2. 平台方提供接口

#### 2.1 推送授信结果

###### 2.1.1 调用场景

机构合作方请求平台方接口，推送授信结果。

###### 2.1.2 调用说明

- 接口类型：同步
- 通讯方式：HTTP+POST
- 数据格式：JSON
- 请求地址：/creditResultPush

###### 2.1.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| creditReqNo | 平台授信申请号 | string(64) | Y |  |
| fundCreditNo | 机构授信申请号 | string(64) | N |  |
| result | 授信结果 | string(8) | Y | CR101 - 授信成功（可继续调用额度查询接口） CR102 - 授信拒绝 CR103 - 授信申请取消 CR104 - 待补件【暂不支持】 CR105 - 授信中 CR106 - 无记录（如因网络等问题，授信申请未实际提交到合作方，导致合作方查询不到对应流水号的申请结果，需返回CR106无记录） |
| reasonCode | 拒绝码 | string(8) | O | 结果CR102时必传 C1010 内部处理失败 C1011 资料缺失 C1021 风控审核拒绝 C1022 资方审核拒绝 C2001 其他 |
| reasonDesc | 拒绝原因描述 | string(256) | O | 结果CR102时必传 |
| creditFailTime | 授信拒绝时间 | string(32) | O | 结果CR102时必传，yyyy-mm-dd hh:mm:ss |
| creditSuccTime | 授信成功时间 | string(32) | O | 结果CR101时必传，yyyy-mm-dd hh:mm:ss |
| creditAmt | 授信额度 | decimal(32) | O | 结果CR101时必传，单位元 |
| annualRate | 年利率 | string(16) | O | 结果CR101时必传，年利率 示例0.2399，代表年化23.99% |
| creditCancelTime | 授信申请取消时间 | string(32) | O | 结果CR103时必传，yyyy-mm-dd hh:mm:ss |
| supplyType | 补件类型 | string(16) | O | 结果CR104时必传，ID / FACE / CONTACT / CARD |
| creditFailFrozenTime | 授信被拒封禁期 | string(32) | O | 结果CR102时必传，yyyy-mm-dd hh:mm:ss |

请求参数示例：

| Java // 成功 { "creditReqNo": "AP0710324673086914560", "fundCreditNo": "123412341234", "result": "CR101", "creditSuccTime": "2023-12-27 11:11:11", "creditAmt": "5000" } // 拒绝 { "creditReqNo": "AP0710324673086914560", "fundCreditNo": "123412341234", "result": "CR102", "reasonDesc": "身份证信息不合法" } // 待补件 { "creditReqNo": "AP0710324673086914560", "fundCreditNo": "123412341234", "result": "CR104", "reasonDesc": "需要补充资料", "supplyType": "CONTACT" } // 取消 { "creditReqNo": "AP0710324673086914560", "fundCreditNo": "123412341234", "result": "CR103", "creditCancelTime": "2023-12-27 11:11:11" } |
| --- |

#### 2.2 推送额度变更

###### 2.2.1 调用场景

机构合作方请求平台方接口，在授信成功后，推送用户额度、定价等相关信息。有额度状态及额度的变化时，也通过该接口推送。

###### 2.2.2 调用说明

- 接口类型：同步
- 通讯方式：HTTP+POST
- 数据格式：JSON
- 请求地址：/accountInfoPush

###### 2.2.3 请求参数

| 参数名称 | 中文描述 | 参数类型 | 是否必须 | 参数说明 |
| --- | --- | --- | --- | --- |
| userNo | 平台用户号 | string(64) | Y | 平台用户对外唯一标识 |
| fundUserNo | 机构方用户号 | string(64) | N | 机构方用户唯一标识 |
| creditReqNo | 平台授信申请号 | string(64) | Y |  |
| fundCreditNo | 机构授信申请号 | string(64) | N |  |
| status | 额度状态 | integer(2) | Y | 1 - 可用（有可用额度，用户可发起借款申请） 2 - 失效（无可用额度，需重新授信） 3 - 锁定（额度已使用，借款审核中）【暂不支持】 |
| creditAmt | 授信额度 | decimal | Y | 单位元 |
| availableAmt | 可用额度 | decimal | Y | 单位元。 如存在额度临时冻结场景，可传额度状态=1，可用额度=0；额度恢复后再传更新后的可用额度。 额度失效情况下，可用额度=0。 |
| maxAvailableAmt | 最大可用额度 | decimal | Y | 单位元 |
| minAvailableAmt | 最小可用额度 | decimal | Y | 单位元 |
| step | 额度步长 | decimal | N | 单位元 |
| creditValidTime | 额度生效时间 | string(20) | Y | 格式：yyyy-MM-dd HH:mm:ss |
| creditExpireTime | 额度失效时间 | string(20) | Y | 格式：yyyy-MM-dd HH:mm:ss。 说明：变更额度状态/授信额度/可用额度时涉及更新 额度状态变更为额度失效时，需给小于当前时间的额度失效时间（否则无法触发我方额度失效逻辑）。 授信额度/可用额度更新时，根据实际需要更新额度失效时间。 |
| repayMethod | 还款方式 | integer | Y | 1 - 等本等息；2 - 等额本息；3 - 等额本金；4 - 先息后本；5 - 随借随还；6 - 到期还本；7 - 锁期 |
| rateType | 利率类型 | string(8) | Y | APR / IRR |
| rateUnit | 利率单位 | string(8) | Y | DAY - 日；MONTH - 月；YEAR - 年 |
| rate | 利率 | string(16) | Y | 如0.15，表示利率15.4% |
| availableTerms | 可借期数 | list[integer] | Y |  |
| capitalCode | 资方 | string(20) | N |  |
| changeType | 变更类型 | integer(2) | N | 1 - 提额（触发短信营销） 2 - 降息 |

请求参数示例：

| JSON { "creditReqNo":"AP0710324673086914560", "userNo":"UR0722566261684408320", "status":1, "creditAmt":10000, "maxAvailableAmt":8000, "minAvailableAmt":1000, "step":1000, "creditValidTime":"2024-01-17 13:39:41", "creditExpireTime":"2024-01-17 13:39:41", "repayMethod":1, "rateType":"APR", "rateUnit":"DAY", "rate":"0.55", "availableTerms":[ 6, 12, 18, 24 ], "capitalCode":"ABC123XYZ" } |
| --- |

## 四、附录

### 1. 婚姻状况

| 码值 | 说明 |
| --- | --- |
| 01 | 未婚 |
| 02 | 离异 |
| 03 | 已婚有子女 |
| 04 | 已婚无子女 |

### 2. 最高学历

| 码值 | 说明 |
| --- | --- |
| 01 | 研究生或以上 |
| 02 | 大学本科 |
| 03 | 大学专科 |
| 04 | 高中或中专 |
| 05 | 初中及以下 |

### 3. 负债情况

| 码值 | 说明 |
| --- | --- |
| 01 | 无负债 |
| 02 | 0-3000元 |
| 03 | 3000-6000元 |
| 04 | 6000-10000元 |
| 05 | 10000-15000元 |
| 06 | 15000-20000元 |
| 07 | 20000元以上 |

### 4. 住宅类型

| 码值 | 说明 |
| --- | --- |
| 01 | 租房 |
| 02 | 产权房产 |
| 03 | 公司宿舍 |
| 04 | 和家人同住 |
| 05 | 其他 |

### 5. 借款用途

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

### 6. 行业

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

### 7. 职业类别

| 码值 | 说明 |
| --- | --- |
| 01 | 上班 |
| 02 | 兼职 |
| 03 | 企业主 |
| 04 | 无业 |
| 05 | 个体户 |

### 8. 收入类型

| 码值 | 说明 |
| --- | --- |
| 01 | 工资 |
| 02 | 经营收入 |
| 03 | 投资收入 |
| 04 | 房租收入 |
| 05 | 其他 |

### 9. 收入情况

| 码值 | 说明 |
| --- | --- |
| 01 | 3000以下 |
| 02 | 3000-6000 |
| 03 | 6000-10000 |
| 04 | 10000-30000 |
| 05 | 30000以上 |

### 10. 公司类型

| 码值 | 说明 |
| --- | --- |
| 01 | 政府或企事业单位 |
| 02 | 国企央企 |
| 03 | 外资企业 |
| 04 | 上市公司 |
| 05 | 普通民营企业 |
| 06 | 个体工商户 |
| 07 | 其他 |

### 11. 联系人关系

| 码值 | 说明 |
| --- | --- |
| 01 | 父亲 |
| 02 | 母亲 |
| 03 | 配偶 |
| 04 | 儿子 |
| 05 | 女儿 |
| 06 | 朋友 |
| 07 | 同事 |

### 12. 银行编码映射

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
