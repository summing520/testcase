# 信用飞API对接标准接口文档

> **来源**：信用飞API对接标准接口文档0512_1.pdf（HUB 信用飞渠道）  
> **转换**：	est_case_generator/skills/pdf-parser（pdfplumber 文本提取）

---

⼀、接⼊综述
1.1 引⾔
1.2 接⼊条件
1.3 接⼊总体说明
1.4 版本变更说明
1.1 引⾔
为了保证机构和信⻜更⾼效合作,推出信⻜商家服务平台。
1.2 接⼊条件
完成商务合作相关的前期沟通,达成合作意向。
合作机构向平台申请机构标识,索取ua(产品编号)与signkey。
1.3 接⼊总体说明
双⽅接⼝统⼀采⽤https协议,utf8编码,post请求传输数据,请求响应均采⽤application/json。
接⼝保持幂等性(重复请求请返回相同的结果)。
接⼝调⽤时每次都需要将接⼝指定参数、md5加密⽣成sign签名,然后将sign和ua、args、时间戳作
为进⾏参数传递。
1.4 版本变更说明
⽇期 接⼝ 说明
2024-
[3.1.1 ⽤户准⼊] 新增返回⻛险等级
08-08
2024-
[3.2.1 进件接⼝] 身份证参数必传
08-08
2024- [3.2.4 额度变更同
新增接⼝
08-08 步]
2024- [3.3.1 查询⽀持银
新增单号传参
08-08 ⾏卡列表]
2024- [3.4.1 查询放款结
新增复贷字段
08-08 果]
2024- [3.4.2 放款结果推
新增复贷字段
08-08 送]
2024- [3.5.1 主动还款试 还款类型参数调整 新增还款期数参数, 试算结果新增本⾦、利
08-08 算] 息、罚息明细

2024-
[3.5.2 主动还款] 还款类型参数调整 新增还款期数参数
08-08
2024-
[3.6.1 获取协议] 新增绑卡合同⽀持
08-15
2024- [3.5.1 主动还款试
新增费⽤返回值
08-21 算]
2024- [3.3.5 (借款)发送
新增银⾏卡传参
08-21 验证码接⼝]
2024-10- [3.3.0 已绑卡信息
新增已绑卡信息查询接⼝
23 查询]
2024-10-
[3.2.5 额度查询] 新增额度查询接⼝
23
2024-11- [3.5.6 (还款)发送
新增(还款)发送验证码接⼝
20 验证码接⼝]
2024-11- [3.5.7 (还款)校验验
新增(还款)校验验证码接⼝
20 证码接⼝]
2024-11- [3.5.4 还款结果推
移除 逾期还款 和 部分还款 类型
20 送接⼝]
2024-11- [3.5.5 还款结果查
移除 逾期还款 和 部分还款 类型
20 询接⼝]
2024-11- [3.4.3 查询还款计
增加减免项
28 划]
2024-11- [3.4.4 还款计划推
增加减免项
28 送]
2024-12-
[3.3.7 下单接⼝] 去掉借款⽤途
06
2024-12- [3.4.4 还款计划推
增加当期可还款⽇
06 送]
2024-12- [3.3.6 (借款)校验
去掉银⾏卡号
06 验证码接⼝]
2024-12- [3.3.5 (借款)发送
去掉借款⾦额,去掉期数
06 验证码接⼝]
2025-04- [3.2.2 查询申请结
增加⽀持额度类型
11 果]

2025-04- [3.2.3 审核结果推
增加⽀持额度类型
11 送]
2025-04- [3.2.4 额度变更同
增加⽀持额度类型
11 步]
2025-04-
[3.2.5 额度查询] 增加⽀持额度类型
11
2025-04- 传参新增：借款单号与授信单号区分
[3.3.7 下单接⼝]
15 返回值新增：机构⽅借款流⽔号
2025-04- [3.4.1 查询放款结
传参新增：借款单号,返回值新增：机构⽅借款流⽔号
15 果]
2025-04- [3.4.2 放款结果推
传参新增：借款单号,机构⽅借款流⽔号
15 送]
2025-04- [3.4.3 查询还款计
传参新增：借款单号
15 划]
2025-04- [3.4.4 还款计划推
传参新增：借款单号
15 送]
2025-04- [3.5.1 主动还款试
传参新增：借款单号
15 算]
2025-04-
[3.5.2 主动还款] 传参新增：借款单号
15
2025-04- [3.5.4 还款结果推
传参新增：借款单号
15 送]
2025-04- [3.5.5 还款结果查
传参新增：借款单号, 返回值新增：借款单号
15 询]
2025-04- [3.5.6 (还款)发送
传参新增：借款单号
15 验证码接⼝]
2025-04- [3.5.7 (还款)校验验
传参新增：借款单号
15 证码接⼝]
2025-04-
[3.6 相关协议获取] 还款⻚展示协议传参新增：借款单号
15
2025-04- [3.3.2 绑卡短信发
回参新增：绑卡流⽔号
28 送接⼝]
2025-04- [3.3.3 绑卡短信校
传参新增：绑卡流⽔号
28 验接⼝]

2025-04- [3.3.5 (借款)发送
回参新增：借款短验流⽔号
28 验证码接⼝]
2025-04- [3.3.6 (借款)校验
传参新增：借款短验流⽔号
28 验证码接⼝]
2025-04-
[3.3.7 下单接⼝] 传参新增：银⾏卡号
28
2025-04-
[3.5.2 主动还款] 传参新增：银⾏卡号
28
2025-05- [3.5.4 还款结果推
传参新增：还款类型
30 送]
2025-05- [3.5.8 还款流⽔同
接⼝新增
30 步]
2025-06- [3.3.4 借款试算接
回参新增：年费利率
04 ⼝]
2025-06- [3.3.5 (借款)发送
传参新增：借款单号
19 验证码接⼝]
2025-06- [3.3.6 (借款)校验
传参新增：借款单号
19 验证码接⼝]
2025-06- [3.2.4 额度变更同 增加额度变化类型，新增传参:变更前授信总额度，变更前可⽤
27 步] 额度，变更前额度失效时间，变更前额度状态
2025-06-
[3.2.1 进件接⼝] 传参新增：活体完成时间
27
2025-07- [3.5.4 还款结果推
传参新增：机构⽅还款流⽔号
04 送]
2025-07- [3.3.5 (借款)发送
传参新增：借款⾦额，借款期数
04 验证码接⼝]
2025-07-
[3.3.7 下单接⼝] 传参新增：验证码
04
2025-07- [3.5.6 (还款)发送
传参新增：还款类型，还款流⽔号
04 验证码接⼝]
2025-07-
[3.5.2 主动还款] 传参新增：验证码
04
2025-07- [3.2.2 查询申请结
回参新增：可⽤额度
07 果]

2025-07- [3.2.3 审核结果推
传参新增：可⽤额度
07 送]
2025-12-
[4.0.1 H5链接 ] 接⼝新增
24
⼆、对接说明
2.1 交互参数及示例
2.2 AES加解密&RSA签名验签
2.3 接⼝说明
2.1 交互参数及示例
PS:机构调⽤平台或平台调⽤机构通⽤
header请求参数规范
名称 类型 必填 备注 示例
trace-id string 是 请求流⽔号 2021010112121212341234
body请求规范
名称 类型 必填 备注 示例
平台分配给机构的
ua string 是 test
唯⼀标识
sign string 是 签名 dasdasdasdas
timestamp int 否 时间戳 1604649555
接⼝的调⽤参数,
args string 是 BVmSqWaovDyswziATBkOTQ==
加密字符串业务数据
请求示例
{
"ua": "test",
"sign": "dasdasdasdas",
"timestamp": 1604649555,
"args": "BVmSqWaovDyswziATBkOTQ=="
}
响应参数
名称 参数 类型 必填 描述

状态 status int 是 1-接⼝成功 参⻅附录：通⽤错误码明细
状态描述 message string 是 success
响应内容 response json｜null 是 null
响应示例
{
"status": 1,
"message": "success",
"response": null
}
2.2 AES加解密&RSA签名验签
加解密&签名⽣成描述
ua示例值（由信⻜侧分配的固定字符串）： test_org
加密密钥key示例值（由信⻜侧分配的固定字符串）： =H>7C={KK{u'J6xE
以准⼊接⼝为例,method： check-user
明⽂参数： {"type":3,"md5":"bdbe7e91190ab0022d50eba5c4bbcf35"}
加密
1.AES对报⽂加密：
1.1 使⽤加密密钥key对明⽂参数进⾏AES加密后,再base64_encode,得到密⽂参数args：
SBehH0Z3HevZvpLTj4kOGvMU3M7M0YQgR7mDt4SiDuRMJol+
z3eH85WMHxOJFaBvvZNQOZtFDDKesyi9n0cJ2Q==
2.⽣成签名sign：
2.1 拼接字符串ua+key+ua,⽣成signKey字符串：test_org=H>7C={KK{u'J6xEtest_org
2.2 拼接字符串signKey+method+signKey+密⽂参数+signKey,⽣成待MD5加密的字符串：
=test_org=H>7C={KK{u'J6xEtest_orgcheck-usertest_org=H>7C={KK
{u'J6xEtest_orgSBehH0Z3HevZvpLTj4kOGvMU3M7M0YQgR7mDt4SiDuRMJol
+z3eH85WMHxOJFaBvvZNQOZtFDDKesyi9n0cJ2Q==test_org=H>7C={KK{u'J6xEtest_org
2.3 MD5加密上⼀步⽣成的字符串,⽣成签名：e10ce2056a18669ad7c4667b51c2b2f0
3.将ua,timestamp,⽣成的加密参数,签名放到请求报⽂中,得到组装的请求报⽂：
{"args":
"SBehH0Z3HevZvpLTj4kOGvMU3M7M0YQgR7mDt4SiDuRMJol+
z3eH85WMHxOJFaBvvZNQOZtFDDKesyi9n0cJ2Q==",

"sign":"e10ce2056a18669ad7c4667b51c2b2f0",
"ua":"test_org","timestamp":1656924907}
解密
1.验签
1.1 根据签名⽣成规则⽣成待验证签名,与请求报⽂中的签名sign⽐较相等即可
2.AES解密
2.1 对请求报⽂中的args进⾏base64_decode
2.2 使⽤加密密钥key对2.1⽣成的结果进⾏AES解密
java语⾔函数代码示例
public class Main {
/**
* 说明：
* 线上和测试环境的密钥不同
*/
public static void main(String[] params) throws IOException {
//请求接⼝
String method = "check-user";
//AES秘钥
String key = "=H>7C={KK{u'J6xE";
//机构标识
String ua = "test_org";
//明⽂参数
String args= "
{\"type\":3,\"md5\":\"bdbe7e91190ab0022d50eba5c4bbcf35\"}";
//对明⽂参数进⾏AES加密
System.out.println("===========加密==========");
String encrypt_args = encrypt(args, key);
System.out.println("⽣成加密参数：" + encrypt_args);
//⽣成签名
String sign = sign(ua, method, key, encrypt_args);
System.out.println("⽣成签名：" + sign);
System.out.println("===========解密==========");
args = decrypt(encrypt_args, key);
System.out.println("⽣成解密参数：" + args);
}
//⽣成请求参数

public static String encrypt(String args, String key) {
try {
byte[] keyBytes = key.getBytes(Charsets.UTF_8);
byte[] contentBytes = args.getBytes(Charsets.UTF_8);
byte[] encryptedContentBytes =
AesUtil.encrypt(contentBytes, keyBytes);
String encryptedContent =
Base64Util.encode(encryptedContentBytes);
return encryptedContent;
} catch (Exception e) {
System.out.println("加密失败");
e.printStackTrace();
}
return null;
}
//⽣成签名
public static String sign(String ua, String method,
String key, String args) {
String signKey = ua + key + ua;
String signContent = signKey + method + signKey + args + signKey;
String sign = Md5Util.md5(signContent, Charsets.UTF_8);
return Md5Util.md5(signContent, Charsets.UTF_8);
}
// 解密数据
public static String decrypt(String args, String aesKey) {
try {
// 使⽤aes解密 消息内容
byte[] keyBytes = aesKey.getBytes(Charsets.UTF_8);
byte[] contentBytes = Base64Util.decode(args);
byte[] decryptedContent = AesUtil.decrypt(contentBytes,
keyBytes);
return new String(decryptedContent, Charsets.UTF_8);
} catch (Exception e) {
System.out.println("解密失败");
e.printStackTrace();
}
return null;
}
//验签
public static boolean checkSign(String sign, String ua, String method,
String key, String encrypt_args) {
String signContent = sign(ua, method, key, encrypt_args);

if (sign.equalsIgnoreCase(signContent)) {
return true;
}
return false;
}
}
php语⾔参数⽣成规则
//将请求数据（body中的args）转换成json字符串
$args = encrypt(json_encode($args),$signkey);
//签名⽣成规则：利⽤ua与signkey拼装⽣成signKey
$signKey = "{$ua}{$signkey}{$ua}";
//结合signKey、method、args ⽣成签名
$sign = md5("{$signKey}{$method}{$signKey}{$args}{$signKey}");
php语⾔函数代码示例
<?php
/**
* @AES(AES/ECB/PKCS5Padding)加密
* @param $data 业务数据
* @param $key AES密钥
* @return string
*/
public function encrypt($data, $key) {
$res = openssl_encrypt($data, 'AES-128-ECB', $key, OPENSSL_RAW_DATA);
return ($res === false) ? $res : base64_encode($res);
}
/**
* @AES(AES/ECB/PKCS5Padding)解密
* @param $data
* @param $key
* @return string
*/
public function decrypt($data, $key) {
$data = base64_decode($data);
return openssl_decrypt($data, 'AES-128-ECB', $key, OPENSSL_RAW_DATA);
}
/**
* @请求示例curl
* @param $method

* @param $header
* @param $args
* @return string
*/
function send_api_request($method, $header, $args){
//////////////////////////////////////////////////
// 以下部分为请求配置初始化部分
//////////////////////////////////////////////////
// 平台分配给合作机构唯⼀标识
$ua = "test_org"; // 接⼊标识UA
$key = "=H>7C={KK{u'J6xE" // 请求签名密钥key
$args = encrypt(json_encode($args), $key);
//////////////////////////////////////////////////
// 以下部分为请求签名部分
//////////////////////////////////////////////////
// 签名⽅式 php
$signKey = "{$ua}{$key}{$ua}";
$sign = md5("{$signKey}{$method}{$signKey}{$args}{$signKey}");
// 签名⽅式 java 伪代码
// String $signkey = $ua + $key + $ua;
// String $sign = md5( $signkey + $method + $signkey + $args + $signkey
);
//////////////////////////////////////////////////
// 以下部分为最终的HTTP请求发送部分
//////////////////////////////////////////////////
// 初始化 API 请求地址
$requstUrl =
"https://qa1-api.testxinfei.cn/platform-api/v1/".$method;
// 初始化 HTTP POST 请求参数
$postArgs = [];
$postArgs['args'] = $args;
$postArgs['sign'] = $sign;
$postArgs['ua'] = $ua;
$postArgs['timestamp'] = time();
// 初始化CURL来执⾏HTTP请求发送
$ch = curl_init();
// 设置CURL请求参数
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_USERAGENT, $ua);
curl_setopt($ch, CURLOPT_URL, $requstUrl);
// 设置POST参数和请求头
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($postArgs));

curl_setopt($ch, CURLOPT_HTTPHEADER,
array('Content-Type: application/json'));
// 设置CURL其他参数
curl_setopt($ch, CURLOPT_FRESH_CONNECT, false);
curl_setopt($ch, CURLOPT_FORBID_REUSE, false);
curl_setopt($ch, CURLOPT_HTTPHEADER, $header);
curl_setopt($ch, CURLOPT_ENCODING, 'gzip');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 10); //设置cURL允许执⾏的最⻓秒数
//在发起连接的超时时间,如果设置为0,则⽆限等待
curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 3);
// 调⽤接⼝, 同步等待接受响应数据
$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
if ($httpCode != 200 || curl_errno($ch) !== 0 ) {
$logMessage = "请求服务失败！\r\nURL: {$requstUrl}\r\nPOST:
" . var_export($postArgs, true) . "\r\nRET:". var_export($response,
true);
$logMessage .= "\r\nHTTP STATUS: {$httpCode}; \r\nCURL_ERRNO: "
. curl_errno($ch) . "; CURL_ERROR: " . curl_error($ch);
curl_close($ch); // 关闭curl, 释放资源
$result = array(
'response' => var_export($response, true),
'status' => -9999,
'message' => $logMessage
);
return $result;
}
curl_close($ch); // 关闭curl, 释放资源
$result = json_decode($response, true);
if($result==null){
$logMessage = "请求服务的返回结果处理失败！";
$logMessage .= "\r\nURL: {$requstUrl}\r\nPOST: " .
var_export($postArgs, true) . "\r\nRET: ". var_export($response,
true);
$result = array(
'response' => var_export($response, true),
'status' => -999,
'message' => $logMessage
);
}
return $result;
}
//////////////////////////////////////////////////
// 以下部分为请求数据部分

//////////////////////////////////////////////////
// 请求的接⼝标识
$method = "check-user"; //不含版本号,controller/action
// 要请求的接⼝的公共参数数组
$header = [
'trace-id' => '2021010112121212341234',
];
// 要请求的接⼝的请求参数数组
$args = '{"type":3,"md5":"bdbe7e91190ab0022d50eba5c4bbcf35"}';
$result = send_api_request($method, $header, $args);
print_r( $result ); // 打印接⼝返回结果
2.3 接⼝说明
相关推送接⼝均为平台提供,其他接⼝均为合作机构提供。
三、接⼝列表
3.1 撞库阶段
3.1.1 ⽤户准⼊
3.2 贷前申请阶段
3.2.1 进件接⼝
3.2.2 查询申请结果
3.2.3 审核结果推送
3.2.4 额度变更同步
3.2.5 额度查询
3.3 确认⽤信阶段
3.3.0 已绑卡信息查询
3.3.1 查询⽀持银⾏卡列表
3.3.2 绑卡短信发送接⼝
3.3.3 绑卡短信校验接⼝
3.3.4 借款试算接⼝
3.3.5 (借款)发送验证码接⼝
3.3.6 (借款)校验验证码接⼝
3.3.7 下单接⼝
3.4 放款阶段
3.4.1 查询放款结果
3.4.2 放款结果推送
3.4.3 查询还款计划
3.4.4 还款计划推送
3.5 还款阶段
3.5.1 主动还款试算
3.5.2 主动还款
3.5.3 H5还款
3.5.4 还款结果推送

3.5.5 还款结果查询
3.5.6 (还款)发送验证码接⼝
3.5.7 (还款)校验验证码接⼝
3.5.8 还款流⽔同步
3.6 相关协议获取
3.6.1 获取协议
3.7 其他接⼝
3.7.1、获取⻚⾯绑卡地址
3.7.2、查询绑卡结果
3.7.3、绑卡结果推送
3.1 撞库阶段
3.1.1、⽤户准⼊
3.1.1 ⽤户准⼊
此接⼝⽤于确认⽤户是否可以申请机构产品。
接⼝标识：check-user
请求参数
必
名称 参数 类型 描述
填
1 ⼿机号MD5
准⼊类 2 ⼿机号+身份证MD5（推荐）
type int 是
型 3 身份证号MD5
4 身份证号MD5和⼿机号md5都传
A3DCB4D229DE6FDE0DB5686DEE47145D type为4
MD5 md5 string 是
时传⼿机号md5
身份证 A3DCB4D229DE6FDE0DB5686DEE47145D type为4
idCardMd5 string 否
MD5 时必传
请求的args示例
{
"type": 1,
"md5":"A3DCB4D229DE6FDE0DB5686DEE47145D"
}
返回参数
名称 参数 类型 必填 描述

⻛险等级 risk_level string 否 对接机构⽅⽤户所属⻛险评级
准⼊成功返回示例
{
"status":1,
"message":"success",
"response": {
"risk_level":""
}
}
准⼊失败返回示例
{
"status": -1,
"message": "准⼊失败原因",//准⼊被拒原因
"response": {}
}
3.2 贷前申请阶段
3.2.1、进件接⼝
3.2.2、查询申请结果
3.2.3、审核结果推送
3.2.4、额度变更同步
3.2.5、 额度查询
3.2.1 进件接⼝
平台⽅收集完⽤户信息后,可调⽤机构接⼝将⽤户资料传输给机构,机构根据进件资料对⽤户注册、实名、
活体校验和⻛控校验。返回给平台这笔申请是否通过。
接⼝标识：approval
请求参数
必
名称 参数 类型 描述
填
平台订单号 order_no string 是 格式：⻓度不超过32个字符。
⼿机号 mobile string 是 13341888888
姓名 name string 是 张三

身份证号 id_card_number string 是 110588199911221888
出⽣⽇期 born_time string 是 1998-08-08
渠道app名
from_app_name string 否 xyf
称
照⽚ photos object 是 ⻅下⽂
基础信息 base_info object 是 ⻅下⽂
联系⼈ relations array 是 数组,⻅下⽂
1-个⼈⽇常消费,2-装修,3-旅游,4-教育,5-医
借款⽤途 purpose int 是
疗
借款⾦额 amount int 否 单位元 10000
借款期限 period int 否 12
设备信息 device_info object 否 ⻅下⽂
照⽚photos
名称 参数 类型 必填 描述
身份证正⾯照 id_positive string 是 图⽚地址
身份证反⾯照 id_negative string 是 图⽚地址
活体照⽚ face_photo string 是 图⽚地址
姓名（OCR） name string 是 张三
身份证号（OCR） id_card_number string 是 110588199911221888
身份证有效（OCR） id_due_time string 是
身份证地址（OCR） id_address string 是
性别（OCR） id_sex string 是
⺠族（OCR） id_ethnic string 是
签发机关（OCR） id_issue_org string 是
活体分 confidence string 否 活体分,未获取到时默认: 78
活体供应商 channel string 否 参⻅ 活体供应商枚举
活体完成时间 face_challenge_time long 否 时间戳（秒）
基础信息base_info
名称 参数 类型 必填 描述

教育程度 education string 是 参考教育程度枚举
职业类别 job string 是 参考职业类别枚举
⼯作单位 work_unit_name string 否 最少3个字符
⼯作地址 work_unit_address string 否 最少4个字符
⼯作地址·省份 work_unit_province string 否
⼯作地址·市 work_unit_city string 否
⼯作地址·区 work_unit_district string 否
居住地址 address string 否
居住地址·省份 province string 否
居住地址·市 city string 否
居住地址·区 district string 否
⽉收⼊ monthly_income string 是 参考⽉收⼊枚举
婚姻状况 marriage string 是 参考婚姻状况枚举
⾏业类型 industry string 否 参考⾏业枚举
联系⼈relations[]
注：亲属联系⼈和⾮亲属联系⼈必须各⼤于等于1个
名称 参数 类型 必填 描述
亲属联系⼈ relation string 是 参考联系⼈A枚举
紧急联系⼈姓名 name string 是
紧急联系⼈电话 phone string 是
名称 参数 类型 必填 描述
⾮亲属联系⼈ relation string 是 参考联系⼈B枚举
紧急联系⼈姓名 name string 是
紧急联系⼈电话 phone string 是
设备信息device_info
名称 参数 类型 必填 描述
经度 longitude string 否
纬度 latitude string 否

设备机型 model string 否
ip地址 ip string 否
设备id device_id string 否
设备imei码 imei string 否
设备idfa idfa string 否
设备idfv idfv string 否
安卓id android_id string 否
设备是否插⼊sim卡 is_sim int 否 1-有sim卡,0-⽆sim卡
设备类型 os_type string 否 ANDROID, IOS
请求的data示例
{
"order_no": "202205301553000910664243",
"mobile": "13248290888",
"name": "张三",
"id_card_number": "410225123456780123",
"born_time": "1990-11-04",
"purpose":1,
"amount":10000,
"period":12,
"photos": {
"id_sex": "男",
"id_ethnic": "汉",
"id_address": "河南省兰考县⼩宋乡⻰庄村⼀组",
"id_issue_org": "河南省兰考县⼩宋乡⻰庄村⼀组",
"id_due_time": "2020.01.22-2040.01.22",
"id_positive":
"https://xyf-test.oss-cn-beijing.aliyuncs.com/xyf/upload/ocr-photo/
front/20211104/202111041635052615497622.png?OSSAccessKeyId=
LTAI4GFYbsssC2gEQMXMDPZk&Expires=1654075972&Signature=%
2FxtKW5D4XclH6NH0xopEiaH7peE%3D",
"id_negative":
"https://xyf-test.oss-cn-beijing.aliyuncs.com/xyf/upload/ocr-photo/
back/20211104/202111041635052615497622.png?
OSSAccessKeyId=LTAI4GFYbsssC2gEQMXMDPZk&Expires=1654075972&
Signature=i0f9%2Bcx9ATGmfA%2BtS%2BvdeSCo96Y%3D",
"face_photo":
"https://xyf-test.oss-cn-beijing.aliyuncs.com/xyf/upload/
live-photo/best_image/20211104/202111041635233687404523.png?
OSSAccessKeyId=LTAI4GFYbsssC2gEQMXMDPZk&Expires=1654075972&

Signature=0PdxGpLzGJe2YOGVH0i4O3cFIP8%3D"
},
"base_info": {
"education": "本科",
"marriage": "20",
"job": "公司员⼯",
"work_unit_name": "黎明路吧唧吧唧",
"work_unit_address": "上海市上海市浦东新区周家渡街道上南路1430号世博源5区",
"monthly_income": "10,000~20,000",
"work_unit_province": "上海市",
"work_unit_city": "上海市",
"work_unit_district": "浦东新区"
},
"relations": [
{
"relation": "配偶",
"name": "初⼆",
"phone": "13262633502"
},
{
"relation": "其他",
"name": "初三",
"phone": "13262633599"
}
]
}
返回示例
{
"status":1,
"message":"success",
}
3.2.2 查询申请结果
可在需要的场景主动查询⽤户最终的审核结果。
接⼝标识：query-approval
请求参数
名称 参数 类型 必填 描述
平台订单号 order_no string 是 格式：⻓度不超过32个字符。
请求的data示例

{
"order_no":"PP071301044720611303424484"
}
返回参数
名称 参数 类型 必填 描述
10 审批中
审批结论 conclusion int 是 11 审批拒绝
12 审批通过
审批时间 audit_time int 是 审批时间,时间戳,精确到毫秒。
审批被拒特有
名称 参数 类型 必填 描述
审批被拒原因 failed_reason srting 是 例如：授信失败
审批通过特有
名称 参数 类型 必填 描述
授信总额度 amount int 是 同借款⾦额最⼤值,单位分。
可⽤额度 avail_amount int 是 可⽤额度,单位分
借款⾦额最⼤值 max_amount int 是 单位分。
借款⾦额最⼩值 min_amount int 是 单位分。
⾦额变更粒度步值 step_amount int 否 ⾦额梯度,单位分。
可借期数列表 periods array 是 ⽐如：[6,9,12]
额度失效时间 audit_overtime int 是 额度过期时间,时间戳,精确到毫秒。
额度类型 credit_type int 是 1:循环额度,2:⾮循环额度
审批成功示例
{
"status" : 1,
"message" : "success",
"response" :{
"conclusion":12,
"audit_time": "1539073086805",
"amount": 10000,
"max_amount":300000,
"min_amount":100000,
"step_amount":100,

"periods":[6,9,12],
"loan_type":1
}
}
审批拒绝示例
{
"status" : 1,
"message" : "success",
"response" :{
"conclusion":11,
"audit_time": "1539073086805",
"failed_reason": "授信失败"
}
}
3.2.3 审核结果推送
⽤户订单审核出结果后,机构会向平台⽅推送订单状态通知。平台可以根据此通知更新⾃⼰的订单状态
请求地址：https://xxxxxxx/notify/push-approval (域名+接⼝标识)。平台提供,接⼝标识为
notify/push-approval
请求参数
名称 参数 类型 必填 描述
平台订单编号 order_no string 是 PP071301044720611303424484
10 审批中
审批结论 conclusion int 是 11 审批拒绝
12 审批通过
审批时间 audit_time int 是 审批时间,时间戳,精确到毫秒。
审批拒绝特有：
名称 参数 类型 必填 描述
审批被拒原因 failed_reason string 是 例如：授信失败
审批通过特有：
名称 参数 类型 必填 描述
授信总额度 amount int 是 同借款⾦额最⼤值,单位分
可⽤额度 avail_amount int 是 可⽤额度,单位分

借款⾦额最⼤值 max_amount int 是 单位分
借款⾦额最⼩值 min_amount int 是 单位分
⾦额变更粒度步值 step_amount int 否 ⾦额梯度,单位分
可借期数列表 periods array 是 ⽐如：[6,9,12]
额度失效时间 audit_overtime int 是 额度过期时间,时间戳,精确到毫秒。
额度类型 credit_type int 是 1:循环额度,2:⾮循环额度
审批成功请求的data示例
{
"order_no":"PP071301044720611303424484",
"conclusion":12,
"audit_time": "1539073086805",
"amount": 10000,
"max_amount":300000,
"min_amount":100000,
"step_amount":100,
"periods":[6,9,12],
"loan_type":1
}
审批拒绝请求的data示例
{
"order_no":"PP071301044720611303424484",
"conclusion":11,
"audit_time": "1539073086805",
"failed_reason": "授信失败"
}
返回示例
{
"status":1,
"message":"success",
}
3.2.4 额度变更同步
⽤户授信成功后渠道⽅可对⽤户不同状态节点下进⾏授信额度变化同步

请求地址：https://xxxxxxx/notify/push-credit-amount (域名+接⼝标识)。平台提供,接⼝标识为
notify/push-credit-amount
请求参数
必
名称 参数 类型 描述
填
平台
订单 order_no string 是 PP071301044720611303424484
编号
额度
1 固定提额 2 固定降额 3 临时提升额度 4
变化 update_type int 是
额度有效期变更 5额度状态变更
类型
调整
update_time int 是 变更时间,时间戳,精确到毫秒。
时间
额度
credit_status int 是 0:正常,1:不可动⽀,2:额度失效
状态
变更
前额
credit_status_before int 是 0:正常,1:不可动⽀,2:额度失效
度状
态
额度
credit_type int 是 1:循环额度,2:⾮循环额度
类型
可⽤
avail_amount int 是 可⽤额度,单位分
额度
变更
前可
avail_amount_before int 是 可⽤额度,单位分
⽤额
度
授信
总额 amount int 是 单位分。
度
变更
前授
amount_before int 是 单位分。
信总
额度
额度
失效 credit_expire_time String 是 例：2024-10-01 00:00:00
时间

变更
前额
度失 credit_expire_time_before String 是 例：2024-10-01 00:00:00
效时
间
可借
期数 periods array 是 ⽐如：[6,9,12]
列表
借款
⾦额
max_amount int 是 单位分,最⼤可借额度
最⼤
值
借款
⾦额
min_amount int 是 单位分,最⼩可借额度
最⼩
值
⾦额
变更
step_amount int 否 ⾦额梯度,单位分
粒度
步值
请求的data示例
{
"order_no":"PP071301044720611303424484",
"update_type":1,
"update_time": 1539073086805,
"avail_amount": 10000,
"max_amount":300000,
"min_amount":100000,
"step_amount":100,
"loan_type":1
}
返回示例
{
"status":1,
"message":"success",
}
3.2.5 额度查询

接⼝标识：credit-amount-query
请求参数
名称 参数 类型 必填 描述
平台订单编号 order_no string 是 PP071301044720611303424484
返回参数
名称 参数 类型 必填 描述
额度状态 credit_status int 是 0:正常,1:不可动⽀,2:额度失效
额度类型 credit_type int 是 1:循环额度,2:⾮循环额度
可⽤额度 avail_amount int 是 可⽤额度,单位分
授信总额度 amount int 是 单位分。
额度失效时间 credit_expire_time String 是 例：2024-10-01 00:00:00
可借期数列表 periods array 是 ⽐如：[6,9,12]
借款⾦额最⼤值 max_amount int 是 单位分,最⼤可借额度
借款⾦额最⼩值 min_amount int 是 单位分,最⼩可借额度
⾦额变更粒度步值 step_amount int 否 ⾦额梯度,单位分
请求的data示例
{
"order_no":"PP071301044720611303424484"
}
返回示例
{
"status": 1,
"message": "success",
"response": {
"order_no":"PP071301044720611303424484",
"avail_amount": 10000,
"max_amount":300000,
"min_amount":100000,
"step_amount":100,
"loan_type":1
}
}

3.3 确认⽤信阶段
3.3.0 已绑卡信息查询
3.3.1 查询⽀持银⾏卡列表
3.3.2 绑卡短信发送接⼝
3.3.3 绑卡短信校验接⼝
3.3.4 借款试算接⼝
3.3.5 (借款)发送验证码接⼝
3.3.6 (借款)校验验证码接⼝
3.3.7 下单接⼝
3.3.0 已绑卡信息查询
查询⽤户在机构已绑定的银⾏卡信息
接⼝标识：bind-card-query
请求参数
名称 参数 类型 必填 描述
平台订单号 order_no string 是 PP071301044720611303424484,授信单号
card_list
名称 参数 类型 必填 描述
绑卡列表 card_list List< cardInfoDto > 是
cardInfoDto
名称 参数 类型 必填 描述
银⾏卡号 bank_card string 是
开户⾏编码 bank_code string 是 参考银⾏编码枚举
开户银⾏名称 bank_name string 是 如：⼯商银⾏
预留⼿机号 mobile string 否 13399999999
⽤户姓名 name string 否 张三
请求的data示例
{
"order_no": "PP071301044720611303424484"
}

返回参数
{
"status": 1,
"message": "success",
"response": {
"card_ist": [{
"order_no": "PP071301044720611303424484",
"bank_card": "621xxxxx",
"bank_code": "ICBC",
"bank_name": "⼯商银⾏",
"mobile": "13399999999",
"name": "张三",
}]
}
}
3.3.1 查询⽀持银⾏卡列表
平台⽅可通过机构接⼝查询⽀持银⾏卡列表,展示在前端供⽤户绑卡时选择。
接⼝标识：get-bank-list
请求参数
名称 参数 类型 必填 描述
平台订单号 order_no string 是 PP071301044720611303424484
请求的data示例
{
"order_no":"PP071301044720611303424484"
}
返回参数
名称 参数 类型 必填 描述
银⾏名称 name string 是 ⼯商银⾏
开户⾏编码 code string 是 参考银⾏编码枚举
返回示例
{
"status": "1",
"message": "success",

"response": [
{
"name": "⼯商银⾏",
"code": "ICBC",
},
{
"name": "农业银⾏",
"code": "ABC",
},
{
"name": "中国银⾏",
"code": "BOC",
}
]
}
3.3.2 绑卡短信发送接⼝
⽤户填写卡信息后,点击获取验证码,平台⽅调⽤机构绑卡短信发送接⼝,机构会发送短信给⽤户。
接⼝标识：send-bind-card-sms
请求参数
名称 参数 类型 必填 描述
平台订单号 order_no string 是 6511168057191059456
卡号 bank_card string 是 6222022005001212723
开户⾏编码 bank_code string 是 参考银⾏编码枚举
姓名 name string 是 张三
身份证 id_card_number string 是 110108198802019650
预留⼿机号 mobile string 是 13420504517
请求的data示例
{
"order_no":"6511168057191059456",
"bank_card":"6222022005001212723",
"bank_code":"ICBC",
"name":"张三",
"id_card_number":"110108198802019650",
"mobile":"13420504517"
}

返回参数
必
名称 参数 类型 描述
填
是否发送验证码:
短信发送结
send_sms string 是 0 不发送验证码
果
1 发送短信验证码
机构⽅短信流⽔号 （默认不传，如需要传需提前沟
绑卡流⽔号 serial_no string 否
通）
返回示例
{
"status":1,
"message":"success",
"response":{
"send_sms":0
}
}
3.3.3 绑卡短信校验接⼝
此处校验成功,表示绑卡成功；实时返回绑卡结果。
接⼝标识：verify-bind-card-sms
请求参数
必
名称 参数 类型 描述
填
平台订单
order_no string 是 6511168057191059456
号
卡号 bank_card string 是 6222022005001212723
开户⾏编
bank_code string 是 参考银⾏编码枚举
码
姓名 name string 是 张三
身份证 id_card_number string 是 110108198802019650
预留⼿机
mobile string 是 13341158888
号
验证码 verify_code string 否 1234

绑卡流⽔ 机构⽅短信流⽔号 （默认不传，如需要传需提前
serial_no string 否
号 沟通）
请求的data示例
{
"order_no":"6511168057191059456",
"bank_card":"6222022005001212723",
"bank_code":"ICBC",
"name":"张三",
"id_card_number":"110108198802019650",
"mobile":"13341158888",
"verify_code":"1234",
"sms_flow_no":"1798163471715"
}
绑卡成功返回示例
{
"status":1,
"message":"success"
}
绑卡失败返回示例
{
"status":4002,
"message":"验证码错误"
}
3.3.4 借款试算接⼝
接⼝标识：trial
请求参数
名称 参数 类型 必填 描述
平台订单号 order_no string 是 PP071301044720611303424484
借款⾦额 amount int 是 单位元
借款期数 period int 是 3
借款⽤途 purpose string 否 其他
请求的data示例

{
"order_no":"PP071301044720611303424484",
"amount":100000,
"period":3,
"purpose":"其他"
}
返回参数
必
名称 参数 类型 描述
填
应还总额 total_amount int 是 单位分
应还本⾦ principal int 是 单位分
应还总利息 interest int 是 单位分
应还其他费
fee int 是 单位分
⽤
⼩数，⼩数点后保留6位，例：年费利率24则传
年费利率 year_rate float 是
0.24
还款计划列
plan_list array 是 ⻅下⽂
表
还款计划表plan_list
必
名称 参数 类型 描述
填
还款期次 period int 是 ⽐如：12
试算当天作为放款⽇,格式：yyyy-mm-dd
账单⽇ repay_time string 是
hh:ii:ss
本期应还总额 amount int 是 单位分
本期应还本⾦ principal int 是 单位分
本期应还利息 interest int 是 单位分
本期应还其他费
fee int 是 单位分
⽤
返回示例
{
"status": 1,
"message": "success",

"response": {
"total_amount": 110000,
"principal": 100000,
"interest": 10000,
"fee": 79500,
"year_rate": 0.24
"plan_list":[
{
"period":1,
"repay_time":"2020-10-10 10:10:10",
"amount":55000,
"principal":50000,
"interest": 5000,
"fee": 5000
}
]
}
}
3.3.5 （借款）发送验证码接⼝
接⼝标识：send-code
合作⽅可根据实际需求对接
请求参数
必
名称 参数 类型 描述
填
平台订单
order_no string 是 6511168057191059456,授信单号
号
平台借款
loan_order_no string 是 6511168057191059459,借款单号
单号
6222022005001212723, （默认不传，如需要传
卡号 bank_card string 否
需提前沟通）
借款⽤途 purpose int 否 1-个⼈⽇常消费,2-装修,3-旅游,4-教育,5-医疗
借款⾦额 amount int 否 单位元 100000
期数 period int 否 12
请求的data示例
{
"order_no":"6511168057191059456",

"loan_order_no":"PLO6511168057191059456",
"amount":100000,
"period":1,
"bank_card":"6222022005001212723"
}
返回参数
必
名称 参数 类型 描述
填
是否需要校验 0:不需要发短信
need_verify_code int 否
验证码 1:需要校验验证码,并触发短信
是否需要活体 0:不需要
need_face_photo int 否
照⽚ 1:需要
借款短验流⽔ 机构⽅短信流⽔号 （默认不传，如需要
sms_flow_no string 否
号 传需提前沟通）
需要验证码返回示例
{
"status": 1,
"message": "success",
"response": {
"need_verify_code":1
}
}
3.3.6 （借款）校验验证码接⼝
接⼝标识：check-code
合作⽅可根据实际需求对接
请求参数
必
名称 参数 类型 描述
填
平台订单号 order_no string 是 6511168057191059456
平台借款单
loan_order_no string 是 6511168057191059459,借款单号
号
验证码 verify_code string 否 校验时必填

借款短验流 机构⽅短信流⽔号 （默认不传，如需要传需提
sms_flow_no string 否
⽔号 前沟通）
请求的data示例
{
"order_no":"6511168057191059456",
"loan_order_no":"PLO6511168057191059456",
"verify_code":"1234"
}
需要验证码返回示例
{
"status": 1,
"message": "success"
}
3.3.7 下单接⼝
接⼝标识：create-order
请求参数
必
名称 参数 类型 描述
填
平台订单
order_no string 是 6511168057191059456,授信单号
号
平台借款
loan_order_no string 是 6511168057191059459,借款单号
单号
借款⾦额 amount int 是 单位元 100000
期数 period int 是 12
活体照⽚ face_photo string 否 图⽚地址
6222022005001212723 （默认不传，如需要传
卡号 bank_card string 否
需提前沟通）
验证码 verify_code string 否 校验时必填
请求的data示例
{
"order_no":"6511168057191059456",

"loan_order_no": "6511168057191059459"
"amount":100000,
"period":12
}
返回参数
名称 参数 类型 必填 描述
机构借款单号 out_order_no int 否 PP071301044720611303424484
返回参数
{
"status": 1,
"message": "success",
"response": {
"out_order_no":"PP071301044720611303424484"
}
}
3.4 放款阶段
3.4.1 查询放款结果
3.4.2 放款结果推送
3.4.3 查询还款计划
3.4.4 还款计划推送
3.4.1 查询放款结果
接⼝标识：query-loan
请求参数
必
名称 参数 类型 描述
填
PP071301044720611303424483 （授信单
平台订单号 order_no string 是
号）
平台借款单 PP071301044720611303424484（借款单
loan_order_no string 是
号 号）
请求的data示例
{
"order_no":"PP071301044720611303424484",

"loan_order_no":"PP071301044720611303424484"
}
返回参数
必
名称 参数 类型 描述
填
机构借款单
out_order_no int 否 PP071301044720611303424484
号
放款状态 status int 是 参考放款状态枚举
借款审批⾦
amount int 是 单位分
额
期数 period int 是 1
审核时间 audit_time string 是 2020-10-10 10:30:30
放款时间 remit_time string 否 2020-10-10 10:30:30
失败原因 failed_reason string 否 status等于21时有值
0 ⾸贷⽤户借款 1 复贷⽤户借款（含在贷及已结
是否是复贷 is_again_loan int 否
清）
返回示例
{
"status": 1,
"message": "success",
"response": {
"status":22,
"amount":500000,
"period":9,
"audit_time":"2020-10-10 10:30:30",
"remit_time":"2020-10-10 10:30:30",
"failed_reason":"",
"is_again_loan":0,
"out_order_no":"PP071301044720611303424484"
}
}
3.4.2 放款结果推送
请求地址：https://xxxxxxx/notify/push-loan (域名+接⼝标识)。平台提供,接⼝标识为notify/push-
loan

请求参数
必
名称 参数 类型 描述
填
平台订单
order_no string 是 PP071301044720611303424484,授信单号
号
平台借款
loan_order_no string 是 PP071301044720611303424483,借款单号
单号
机构借款 PP0713010447206113034244, 机构借款流⽔
out_order_no string 是
单号 号
放款状态 status string 是 参考放款状态枚举
借款审批
amount int 是 单位分
⾦额
期数 period int 是 1
审核时间 audit_time string 是 2020-10-10 10:30:30
放款时间 remit_time string 否 2020-10-10 10:30:30
失败原因 failed_reason string 否 status等于21时有值
是否是复 0 ⾸贷⽤户借款 1 复贷⽤户借款（含在贷及已结
is_again_loan int 否
贷 清）
请求的data示例
{
"order_no":"PP071301044720611303424484",
"loan_order_no":"PP071301044720611303424483",
"out_order_no":"PP071301044720611303424482",
"status":20,
"amount":500000,
"period":9,
"audit_time":"2020-10-10 10:30:30",
"remit_time":"2020-10-10 10:30:30",
"failed_reason":"",
"is_again_loan":0
}
返回参数
{
"status":1,

"message":"success",
}
3.4.3 查询还款计划
接⼝标识：query-repay-plan
请求参数
名称 参数 类型 必填 描述
平台订单号 order_no string 是 PP071301044720611303424484,授信单号
平台借款单号 loan_order_no string 是 PP071301044720611303424483,借款单号
请求的data示例
{
"order_no":"PP071301044720611303424484",
"loan_order_no":"PP071301044720611303424483"
}
返回参数
名称 参数 类型 必填 描述
总期数 period int 是 12
订单状态 order_status string 是 参考还款状态枚举
账单列表 bill_list array 是 ⻅下⽂
bill_list[]
名称 参数 类型 必填 描述
期数 period_no int 是 1
当期账单⽇ payment_deadline string 是 格式：yyyy-mm-dd hh:ii:ss
unpaid-未还
当期还款状态 pay_status string 是 paid-已还
part_paid-部分还款
剩余应还总⾦额 amount int 是 单位分,（扣除减免项,如有）
剩余应还本⾦ principal int 是 单位分,（扣除减免项,如有）
剩余应还利息 interest int 是 单位分,（扣除减免项,如有）
剩余应还逾期费 overdue_fee int 是 单位分,（扣除减免项,如有）

应还总额,应还本⾦,
剩余应还其他费⽤ fee int 是 应还利息,应还逾期费
（扣除减免项,如有）
应还总⾦额减免 amount_exemption int 否 单位分
应还本⾦减免 principal_exemption int 否 单位分
应还利息减免 interest_exemption int 否 单位分
应还逾期费减免 overdue_fee_exemption int 否 单位分
应还总额,应还本⾦,
应还其他费⽤减免 fee_exemption int 否
应还利息,应还逾期费
实际还款时间 paid_time string 否 格式：yyyy-mm-dd hh:ii:ss
实际还款总额 paid_total_amount int 否 单位分
实还本⾦ paid_principal int 否 单位分
实还利息 paid_interest int 否 单位分
实还逾期费 paid_overdue_fee int 否 单位分
实还其他费⽤ paid_fee int 否 单位分
逾期天数 overdue_days int 否
当期可还款⽇ can_repay_time string 否 格式：yyyy-mm-dd hh:ii:ss
返回示例
{
"status": 1,
"message": "success",
"response": {
"order_status": 500,
"period": 3,
"bill_list": [
{
"period_no": 1,
"payment_deadline": "2020-04-09 23:59:59",
"pay_status": 1,
"amount": 728310,
"principal": 500000,
"interest": 4000,
"overdue_fee": 3858,
"fee": 16104,
"paid_time": "2020-05-09 23:59:59",
"paid_total_amount":728310,

"paid_principal":500000,
"paid_interest": 4000,
"paid_overdue_fee":6000,
"paid_fee":98346
},
{
"period_no": 2,
"payment_deadline": "2020-04-09 23:59:59",
"pay_status": 1,
"amount": 728310,
"principal": 500000,
"interest": 4000,
"overdue_fee": 3858,
"fee": 16104,
"paid_time": "2020-05-09 23:59:59",
"paid_total_amount": 728310,
"paid_principal":500000,
"paid_interest": 4000,
"paid_overdue_fee": 6000,
"paid_fee": 98346
},
{
"period_no": 3,
"payment_deadline": "2020-04-09 23:59:59",
"pay_status": 1,
"amount": 728310,
"principal": 500000,
"interest": 4000,
"overdue_fee": 3858,
"fee": 16104,
"paid_time": "2020-05-09 23:59:59",
"paid_total_amount": 728310,
"paid_principal":500000,
"paid_interest": 4000,
"paid_overdue_fee":6000,
"paid_fee": 98346
},
]
}
}
3.4.4 还款计划推送
订单的还款计划发⽣变更时,机构会消息推送给平台,供平台及时更新还款计划。 推送场景：逾期后、还
款后、结清后。

请求地址：https://xxxxxxx/notify/push-repay-plan (域名+接⼝标识)。平台提供,接⼝标识为
notify/push-repay-plan
请求参数
名称 参数 类型 必填 描述
平台订单号 order_no string 是 PP071301044720611303424484,授信单号
平台借款单号 loan_order_no string 是 PP071301044720611303424483,借款单号
总期数 period int 是 3
订单状态 order_status string 是 参考还款状态枚举
账单列表 bill_list array 是 ⻅下⽂
bill_list[]
名称 参数 类型 必填 描述
期数 period_no int 是 1
当期账单⽇ payment_deadline string 是 格式：yyyy-mm-dd hh:ii:ss
unpaid-未还
当期还款状态 pay_status string 是 paid-已还
part_paid-部分还款
总额 amount int 是 单位分,（扣除减免项,如有）
剩余应还本⾦ principal int 是 单位分,（扣除减免项,如有）
剩余应还利息 interest int 是 单位分,（扣除减免项,如有）
剩余应还逾期费 overdue_fee int 是 单位分,（扣除减免项,如有）
应还总额,应还本⾦,
剩余应还其他费⽤ fee int 是 应还利息,应还逾期费
（扣除减免项,如有）
应还总⾦额减免 amount_exemption int 否 单位分
应还本⾦减免 principal_exemption int 否 单位分
应还利息减免 interest_exemption int 否 单位分
应还逾期费减免 overdue_fee_exemption int 是 单位分
应还总额,应还本⾦,
应还其他费⽤减免 fee_exemption int 否
应还利息,应还逾期费
实际还款时间 paid_time string 否 格式：yyyy-mm-dd hh:ii:ss
实际还款总额 paid_total_amount int 否 单位分

实还本⾦ paid_principal int 否 单位分
实还利息 paid_interest int 否 单位分
实还逾期费 paid_overdue_fee int 否 单位分
实还其他费⽤ paid_fee int 否 单位分
逾期天数 overdue_days int 否
当期可还款⽇ can_repay_time string 否 格式：yyyy-mm-dd hh:ii:ss
请求的data示例
{
"order_no": "PP071301044720611303424484",
"loan_order_no": "PP071301044720611303424483",
"order_status": 500,
"period": 3,
"bill_list": [
{
"period_no": 1,
"payment_deadline": "2020-04-09 23:59:59",
"pay_status": 1,
"amount": 728310,
"principal": 500000,
"interest": 4000,
"overdue_fee": 3858,
"fee": 16104,
"paid_time": "2020-05-09 23:59:59",
"paid_total_amount": 728310,
"paid_principal":500000,
"paid_interest": 4000,
"paid_overdue_fee": 6000,
"paid_fee": 98346
},
{
"period_no": 2,
"payment_deadline": "2020-04-09 23:59:59",
"pay_status": 1,
"amount": 728310,
"principal": 500000,
"interest": 4000,
"overdue_fee": 3858,
"fee": 16104,
"paid_time": "2020-05-09 23:59:59",
"paid_total_amount": 728310,
"paid_principal":500000,

"paid_interest": 4000,
"paid_overdue_fee": 6000,
"paid_fee": 98346
},
{
"period_no": 3,
"payment_deadline": "2020-04-09 23:59:59",
"pay_status": 1,
"amount": 728310,
"principal": 500000,
"interest": 4000,
"overdue_fee": 3858,
"fee": 16104,
"paid_time": "2020-05-09 23:59:59",
"paid_total_amount": 728310,
"paid_principal":500000,
"paid_interest": 4000,
"paid_overdue_fee": 6000,
"paid_fee": 98346
},
]
}
返回参数
{
"status":1,
"message":"success",
}
3.5 还款阶段
3.5.1 主动还款试算
3.5.2 主动还款
3.5.3 H5还款
3.5.4 还款结果推送
3.5.5 还款结果查询
3.5.6 (还款)发送验证码接⼝
3.5.7 (还款)校验验证码接⼝
3.5.8 还款流⽔同步
3.5.1 主动还款试算
⽤户在平台点击主动还款,平台从合作机构获取根据当前时间计算出的还款⾦额等信息。

接⼝标识：repayment-trial
请求参数
名称 参数 类型 必填 描述
平台订单号 order_no string 是 订单号,授信单号
平台借款单号 loan_order_no string 是 PP071301044720611303424483,借款单号
还款类型 repay_type int 是 10-按期还款,20-提前结清
期数 period int 是 提前结清可不传,按期必传
请求的data示例
{
"order_no":"PP071301044720611303424484",
"loan_order_no":"PP071301044720611303424483",
"repay_type":10,
"period":1
}
返回参数
名称 参数 类型 必填 描述
单位分,当前试算未还总⾦额,
待还⾦额 repay_amount int 是
具体⾦额应当根据repayType和period来决定
单位分,当前试算未还包含本⾦,
本⾦ repay_principal int 是
具体⾦额应当根据repayType和period来决定
单位分,当前试算未还包含利息,
利息 repay_interest int 是
具体⾦额应当根据repayType和period来决定
单位分,当前试算未还所含逾期费⽤,
逾期费⽤ overdue_fee int 是
具体⾦额应当根据repayType和period来决定
其他费⽤ fee int 是 单位分,
返回示例
{
"status": 1,
"message": "success",
"response": {
"repay_amount":123,
"repay_principal":100,
"repay_interest":23,

"overdue_fee":0,
"fee":0
}
}
不⽀持提前结清示例
{
"status": 2,
"message": "不⽀持提前结清",
"response": {}
}
3.5.2 主动还款
⽤户在平台发起主动还款请求,平台调⽤合作机构提供的接⼝,通知合作机构进⾏扣款操作。 catpcha参数
⽤于还款时需要还款验证码
接⼝标识：repayment-operate 更新还款类型 期数传参
请求参数
必
名称 参数 类型 描述
填
平台订单
order_no string 是 授信订单号
号
平台借款
loan_order_no string 是 PP071301044720611303424483,借款单号
单号
还款类型 repay_type int 是 10-按期还款,20-提前结清
期数 period int 是 提前结清可不传,按期必传
还款流⽔
repay_no string 是 记录单次还款申请
号
机构⽅还
3.5.6 (还款)发送验证码接⼝ 获取 （默认不传，如
款短验流 serial_no string 否
需要传需提前沟通）
⽔号
6222022005001212723 （默认不传，如需要传
卡号 bank_card string 否
需提前沟通）
验证码 verify_code string 否 校验时必填
请求的data示例

{
"order_no":"PP071301044720611303424484",
"loan_order_no":"PP071301044720611303424483",
"repay_type":"1",
"period":"1",
"repay_no":"202111241841083272518939"
}
返回示例
{
"status": 1,
"message": "success",
"response": {
}
}
3.5.3 H5还款
⽤户在平台点击还款按钮时,调⽤机构接⼝获取机构的还款H5。
接⼝标识：manual-repay
请求参数
名称 参数 类型 必填 描述
平台订单号 order_no string 是 订单号
⽤户操作完后,要回到平台的地址,
回调地址 return_url string 是
需要urlencode()处理
请求的data示例
{
"order_no":"PP071301044720611303424484",
"return_url":"xxxxxxxxxxxxx"
}
返回参数
名称 参数 类型 必填 描述
还款⻚⾯地址 url string 是 机构还款⻚⾯地址
返回示例

{
"status": 1,
"message": "success",
"response": {
"url":"xxxxxxxxxxxxxx"
}
}
3.5.4 还款结果推送
请求地址：https://xxxxxxx/notify/push-repay (域名+接⼝标识)。平台提供,接⼝标识为notify/push-
repay
请求参数
必
名称 参数 类型 描述
填
订单号 order_no string 是 PP071301044720611303424484,授信单号
平台借款
loan_order_no string 是 PP071301044720611303424483,借款单号
单号
还款流⽔
repay_no string 否 主动还款推送需传
号
机构⽅还
out_repay_no string 否 ⾮主动还款推送需传
款流⽔号
1 正常还款
还款类型 repay_type int 是
2 提前结清
还款⾦额 amount int 是 单位分
还款期数 repay_period int 是 提前结清传0
2020-10-10 10:30:30，还款成功传扣款时间，还
还款时间 repay_time string 是
款失败传当前时间
还款本⾦ principal int 是 单位分，按实际扣款为准，未发⽣扣款传0
还款利息 interest int 是 单位分，按实际扣款为准，未发⽣扣款传0
还款逾期
overdue_fee int 是 单位分，按实际扣款为准，未发⽣扣款传0
费
还款其他
fee int 是 单位分，按实际扣款为准，未发⽣扣款传0
费⽤
还款状态 repay_status int 是 1-还款中 2-还款成功 3- 还款失败

失败原因 fail_reason string 否
1 主动还款
2 批扣
还款来源 repay_from int 是
3 线下还款
4其他
请求的data示例
{
"order_no":"PP071301044720611303424484",
"loan_order_no":"PP071301044720611303424483",
"repay_no":"",
"repay_type":1,
"amount":500000,
"repay_period":1,
"repay_time":"2020-10-10 10:30:30",
}
返回参数
{
"status":1,
"message":"success",
}
3.5.5 还款结果查询
接⼝标识：repayment-search
请求参数
名称 参数 类型 必填 描述
平台订单号 order_no string 是 订单号,授信单号
平台借款单号 loan_order_no string 是 PP071301044720611303424483,借款单号
还款流⽔号 repay_no stirng 是
期数 period string 否 1 提前结清可不传
请求的data示例
{
"order_no":"PP071301044720611303424484",

"loan_order_no":"PP071301044720611303424483",
"period":"1"
}
返回参数
必
名称 参数 类型 描述
填
订单号 order_no string 是 PP071301044720611303424484,授信单号
平台借
loan_order_no string 是 PP071301044720611303424483,借款单号
款单号
还款流
repay_no string 是 PP071301044720611303424484
⽔号
还款类 1 正常还款
repay_type int 是
型 2 提前结清
还款⾦
amount int 是 单位分
额
还款期
repay_period int 是 提前结清传0
数
还款时 2020-10-10 10:30:30，还款成功传扣款时间，还款
repay_time string 是
间 失败传当前时间
还款本
principal int 是 单位分，按实际扣款为准，未发⽣扣款传0
⾦
还款利
interest int 是 单位分，按实际扣款为准，未发⽣扣款传0
息
还款逾
overdue_fee int 是 单位分，按实际扣款为准，未发⽣扣款传0
期费
还款其
fee int 是 单位分，按实际扣款为准，未发⽣扣款传0
他费⽤
还款状
repay_status int 是 1-还款中 2-还款成功 3- 还款失败
态
返回示例
{
"status": 1,
"message": "success",
"response": {
"order_no":"PP071301044720611303424484",

"loan_order_no":"PP071301044720611303424483",
"repay_no":"PP071301044720611303424484",
"repay_type":1,
"amount":500000,
"repay_period":1,
"repay_time":"2020-10-10 10:30:30",
}
}
3.5.6 (还款)发送验证码接⼝
接⼝标识：send-code-repay
合作⽅可根据实际需求对接,如合作⽅不需要则平台会在该阶段进⾏验证码校验
请求参数
必
名称 参数 类型 描述
填
平台订
order_no string 是 6511168057191059456,授信单号
单号
平台借
loan_order_no string 是 PP071301044720611303424483,借款单号
款单号
期数 period int 是 当前还款期数
6222022005001212723, （默认不传，如需要传
卡号 bank_card string 否
需提前沟通）
还款类
repay_type int 否 10-按期还款,20-提前结清
型
还款流
repay_no string 否 记录单次还款申请
⽔号
请求的data示例
{
"order_no":"6511168057191059456",
"loan_order_no":"PP071301044720611303424483",
"bank_card":"6222022005001212723"
}
返回参数
类 必
名称 参数 描述
型 填

是否需要
0 不需要发短信
校验验证 need_verify_code int 否
1 需要校验验证码,并触发短信
码
机构⽅还 机构⽅流⽔号,3.5.7(还款)校验验证码接⼝,3.5.2
款短验流 serial_no int 否 主动还款 需要传⼊（默认不传，如需要传需提前
⽔号 沟通）
需要验证码返回示例
{
"status": 1,
"message": "success",
"response": {
"need_verify_code":1
}
}
3.5.7 (还款)校验验证码接⼝
接⼝标识：check-code-repay
合作⽅可根据实际需求对接,如合作⽅不需要则平台会在该阶段进⾏验证码校验
请求参数
必
名称 参数 类型 描述
填
平台订单
order_no string 是 6511168057191059456,授信单号
号
平台借款
loan_order_no string 是 PP071301044720611303424483,借款单号
单号
验证码 verify_code string 否 校验时必填
机构⽅还
3.5.6 (还款)发送验证码接⼝ 获取 （默认不传，如
款短验流 serial_no string 否
需要传需提前沟通）
⽔号
请求的data示例
{
"order_no":"6511168057191059456",
"loan_order_no":"6511168057191059453",
"verify_code":"1234"
}

需要验证码返回示例
{
"status": 1,
"message": "success"
}
3.5.8 还款流⽔同步
接⼝标识：sync-repay-detail
查询指定订单指定期数的还款流⽔，包括在机构⽅发起的还款，同⼀期账单如发⽣多次还款，需返回所
有的还款流⽔记录。
请求参数
必
名称 参数 类型 描述
填
PP071301044720611303424484,授信单
订单号 order_no string 是
号
平台借款单 PP071301044720611303424483,借款单
loan_order_no string 是
号 号
账单期数 periods List<int> 是 账单期数,可传多期
请求的data示例
{
"order_no":"6511168057191059456",
"loan_order_no":"6511168057191059453",
"periods": [2,3]
}
返回参数
名称 参数 类型 必填 描述
还款明细列表 details List<repay_detail> 是 还款明细列表
repay_detail
必
名称 参数 类型 描述
填
平台订
order_no string 是 6511168057191059456,授信单号
单号

平台借
loan_order_no string 是 PP071301044720611303424483,借款单号
款单号
机构⽅
借款单 out_order_no string 是 OUT71301044720611303424483,借款单号
号
平台侧 如果是机构⽅发起的还款，可以不传
还款流 repay_no string 否 如果是平台侧发起的还款则必传，同接⼝3.5.2
⽔号 repay_no
机构⽅
机构⽅的还款流⽔号，注：机构侧每发扣款⽣成时⽣
还款流 out_repay_no string 是
成的流⽔号，不同扣款批次流⽔号唯⼀
⽔号
还款类 1 正常还款
repay_type int 是
型 2 提前结清
1 主动还款
还款来 2 批扣
repay_from int 是
源 3 线下还款
4其他
还款⾦
amount int 是 单位分
额
还款期
repay_period int 是 提前结清传0
数
还款本
principal int 否 单位分
⾦
还款利
interest int 否 单位分
息
还款逾
overdue_fee int 否 单位分
期费
还款其
fee int 否 单位分
他费⽤
还款状
repay_status int 是 1-还款中 2-还款成功 3- 还款失败
态
失败原
fail_reason string 否
因
还款时
repay_time string 是 2020-10-10 10:30:30
间
返回示例

{
"status": 1,
"message": "success",
"response": {
"details": [
{
"order_no":"PP071301044720611303424484",
"loan_order_no":"PP071301044720611303424483",
"out_order_no":"PP071301044720611303424483",
"repay_no":"PP071301044720611303424484",
"out_repay_no":"OUT71301044720611303424484",
"repay_type":1,
"repay_from":1,
"amount":500000,
"repay_period":1,
"repay_time":"2020-10-10 10:30:30",
"repay_status":1,
}
]
}
}
3.6 相关协议获取
3.6.1 获取协议
3.6.1 获取协议
平台可通过此接⼝可获取各场景需要展示的⽤户协议。
接⼝标识：get-contract
请求参数
必
名称 参数 类型 描述
填
APPLY：授权合同
LOAN：借款确认⻚合同
类型 type string 是
REPAY：贷后合同
BANKCARD：绑卡⻚合同
订单号 order_no string 否 授信单号,除APPLY外必传
借款单号：
平台借款单
loan_order_no string 否 PP071301044720611303424483
号
REPAY：还款⻚合同 必传

请求的args示例
{
"type": "APPLY",
"order_no": "",
}
{
"type": "REPAY",
"order_no": "",
"loan_order_no": "",
}
返回参数
名称 参数 类型 必填 描述
列表数据,⻅下⽂详情
合同列表 contracts array 是 *注意：协议有多个时，需平铺放⼊contracts中,⽆需
合并成⼀个链接
contracts[]
名称 参数 类型 必填 描述
合同地址 url string 是 "url":"XXX" //合同地址
合同名称 name string 是 合同名称
返回示例
{
"status": 1,
"message": "success",
"response": {
"contracts": [
{
"name": "合同名称",
"url": "http://xxxx"
}
]
}
}
3.7 其他接⼝
3.7.1、获取⻚⾯绑卡地址

3.7.2、查询绑卡结果
3.7.3、绑卡结果推送
3.7.1 获取⻚⾯绑卡地址
机构h5⻚⾯绑卡时,需提供需要跳转的绑卡⻚url
接⼝标识：bind-card-url
请求参数
名称 参数 类型 必填 描述
平台订单号 order_no string 是
返回地址 return_url string 是 绑卡后返回的url地址
请求的data示例
{
"order_no":"6511168057191059456",
"return_url": "xxxxxxxxxxxxx",
}
返回参数
名称 参数 类型 必填 描述
绑卡地址 url string 是 xxxxx
绑卡成功返回示例
{
"status":1,
"message":"success",
"response" : {
"url": "xxxxx"
}
}
3.7.2 查询绑卡结果
平台⽅查询机构是否已经有有效绑卡,若有则返回订单相关的最新⼀条绑卡信息
接⼝标识：bind-result
请求参数

名称 参数 类型 必填 描述
平台订单号 order_no string 是 6511168057191059456
请求的data示例
{
"order_no":"6511168057191059456"
}
返回参数
名称 参数 类型 必填 描述
绑卡状态 bind_status int 是 0-未绑卡 1-成功 2-重路由
平台订单号 order_no string 是 PP071301044720611303424484
绑卡信息 card_info object 否 bind_status=1时必传
card_info
名称 参数 类型 必填 描述
银⾏卡号 bank_card string 是
开户⾏编码 bank_code string 是 参考银⾏编码枚举
开户银⾏名称 bank_name string 是 如：⼯商银⾏
预留⼿机号 mobile string 否 13399999999
⽤户姓名 name string 否 张三
绑卡成功返回示例
{
"status": 1,
"message": "success",
"response": {
"bind_status": 1,
"card_info": {
"order_no": "PP071301044720611303424484",
"bank_card": "621xxxxx",
"bank_code": "ICBC",
"bank_name": "⼯商银⾏",
"mobile": "13399999999",
"name": "张三"
}

}
}
⽆绑卡信息时返回示例
{
"status": 1,
"message": "success",
"response": {
"bind_status": 0
}
}
3.7.3 绑卡结果推送
请求地址：https://xxxxxxx/notify/push-bind-card (域名+接⼝标识)。平台提供,接⼝标识为
notify/push-bind-card
请求参数
名称 参数 类型 必填 描述
绑卡状态 bind_status int 是 0-未绑卡 1-成功 2-重路由
平台订单号 order_no string 是 PP071301044720611303424484
绑卡信息 card_info object 否 bind_status=1时必传
card_info
名称 参数 类型 必填 描述
银⾏卡号 bank_card string 是
开户⾏编码 bank_code string 是 参考银⾏编码枚举
开户银⾏名称 bank_name string 是 如：⼯商银⾏
预留⼿机号 mobile string 否 13399999999
⽤户姓名 name string 否 张三
请求的data示例
{
"bind_status": 1,
"order_no": "PP071301044720611303424484"
"card_info": {
"bank_card": "621xxxxx",

"bank_code": "ICBC",
"bank_name": "⼯商银⾏",
"mobile": "13399999999",
"name": "张三"
}
}
4.0.1 获取H5链接
平台⽅查询机各个业务节点对应的h5形式的访问地址，（绑卡，接⼝，还款等）
接⼝标识：h5-url
请求参数
名称 参数 类型 必填 描述
平台授信订单号 order_no string 是 PP071301044720611303424484
返回地址 return_url string 是 回跳地址
场景值 scene string 是 参考附录：H5链接业务场景枚举
返回参数
名称 参数 类型 必填 描述
指定场景的H5地址 url string 是
请求的data示例
{
"bind_status": 1,
"order_no": "PP071301044720611303424484",
"return_url":"https://xxxx.xxxx"
"scene":"LOAN"
}
返回参数
{
"status":1,
"message":"success",
"response": {
"url": "https://xxxx.xxxx"
}
}

附录
通⽤错误码明细
状态码 状态描述
1 操作成功
-1 操作失败
-2 header异常
-3 body参数异常
-30 数据库保存异常
-20 系统资源异常
状态码明细
进件相关状态
状态码 状态描述
1 已授信(勿重复授信)
10 进件中
11 进件失败
12 进件成功
绑卡相关状态
状态码 状态描述
0 未绑卡
1 已绑卡
2 未绑卡
放款状态（放款结果中订单状态）
状态码 状态描述
20 放款中
21 放款失败
22 放款成功

23 放款失败
24 放款取消
还款状态（还款计划中还款状态）
状态码 状态描述
30 正常还款中
31 已逾期
32 已偿清
33 已代偿
34 逾期已偿清
账单状态码
状态码 状态描述
unpaid 未还款
part_paid 部分还款
paid 已还款
枚举值明细
学历
数字枚举 枚举值描述
10 博⼠及以上
20 硕⼠
30 本科
40 专科
50 ⾼中/中专/技校
60 初中及以下
婚姻状况
枚举值 枚举值描述
20 已婚
10 未婚

30 离异
40 其他
职业类别
数字枚举 枚举值描述
10 事业单位
20 公司员⼯
30 私营业主
40 ⾃由职业者
45 学⽣
50 其他
⽉收⼊
数字枚举 枚举值描述
10 1,200以内
20 1,200~2,500
30 2,500~4,000
40 4,000~6,000
50 6,000~10,000
60 10,000~20,000
70 20,000~50,000
80 50,000以上
贷款⽤途
枚举值 枚举值描述
1 个⼈⽇常消费
2 装修
3 旅游
4 教育
5 医疗

亲属联系⼈A
数字枚举 枚举值描述
10 配偶
20 ⽗⺟
30 ⼦⼥
40 兄弟
50 姐妹
亲属联系⼈B
数字枚举 枚举值描述
60 朋友
70 同事
80 同学
90 其他
⾏业枚举
枚举值 枚举值描述
10 公共管理/社会保障/社会组织/国际组织（实际由“职业：事业单位”映射）
20 制造业（实际由“职业：公司员⼯”映射）
30 批发/零售业（实际由“职业：私营业主”映射）
40 ⽂化/体育/娱乐业（实际由“职业：⾃由职业”映射）
50 其他
活体供应商枚举
枚举值 枚举值描述
ks 旷世
tx 腾讯云
H5链接业务场景枚举
枚举值 枚举值描述
LOAN 借款

银⾏编码表
银⾏名称 银⾏code 银⾏名称 银⾏code
北京银⾏ BOB 上海银⾏ SHB
渤海银⾏ CBHB 浙商银⾏ CZB
恒丰银⾏ HFB 浦发银⾏ SPDB
兴业银⾏ CIB 招商银⾏ CMB
平安银⾏ PAB ⼴发银⾏ GDB
⺠⽣银⾏ CMBC 华夏银⾏ HXB
光⼤银⾏ CEB 中信银⾏ CITIC
交通银⾏ BCM 建设银⾏ CCB
中国银⾏ BOC 农业银⾏ ABC
⼯商银⾏ ICBC 邮储银⾏ PSBC
⽟⼭银⾏ ESB ⻄藏银⾏ TCB
温州银⾏ WZCB ⼴州银⾏ GZCB
富⺠银⾏ FMB 汉⼝银⾏ HKB
⻰江银⾏ BOLJ 盛京银⾏ BOSJ
湖南银⾏ HRXJBANK 辽沈银⾏ LSB
⼤连银⾏ BODL 衡⽔银⾏ HENGSHUIBANK
百信银⾏ BXB 宁波银⾏ BONB
众邦银⾏ ZBXB 新⽹银⾏ XWB
新疆银⾏ XJB 邯郸银⾏ HDCB
南京银⾏ NJCB 东莞银⾏ DONGGUANBANK
桂林银⾏ BOGL 上饶银⾏ BOSR
绍兴银⾏ SXCCB 成都银⾏ BOCD
富滇银⾏ FDB 安徽农信 AHNX
抚顺银⾏ BOFS 枣庄银⾏ ZZCCB
⾩新银⾏ BOFX 嘉兴银⾏ JXCCB
河北银⾏ HBB 杭州银⾏ HZB

遂宁银⾏ SNCB ⼤同银⾏ DTB
晋城银⾏ JCB 铁岭银⾏ TLCB
⼭⻄银⾏ SXCB 友利银⾏ WOORI
海南银⾏ HNB 鄞州银⾏ YZB
苏州银⾏ SZBANK 宁夏银⾏ BONX
⻬商银⾏ QSB 锦州银⾏ JZB
徽商银⾏ HSB 重庆银⾏ CQCB
湖北农信 HBXH 四川银⾏ SCB
天津银⾏ TJCB 郑州银⾏ BOZJ
廊坊银⾏ LCCB 湖州银⾏ BOHZ
陕⻄信合 SXNXS 蒙商银⾏ BOM
兰州银⾏ LZCB 江⻄银⾏ NCCBANK
晋商银⾏ BOJS ⻘岛银⾏ QDCCB
⼭⻄农信 SXNX 九江银⾏ JJCCB
柳州银⾏ BOLZ 莱商银⾏ LWB
贵阳银⾏ BOGY ⻄安银⾏ BOXIA
丹东银⾏ BODANDONG 泸州银⾏ LZB
张家⼝银⾏ ZJKB ⽢肃银⾏ BOGS
赣州银⾏ GZCCB 江苏银⾏ JSB
泉州银⾏ BOQZ 营⼝银⾏ BOYK
承德银⾏ CDB ⽇照银⾏ RZB
台州银⾏ BOTZ 唐⼭银⾏ TSBANK
东营银⾏ DYCCB 泰安银⾏ TAB
⻬鲁银⾏ QLB 烟台银⾏ YTCB
潍坊银⾏ WFCCB ⾃贡银⾏ ZGYH
德州银⾏ DZB ⻓治银⾏ CZCCB
湖北银⾏ HBCL 汇丰银⾏ HSBC
⾦华银⾏ JHCCB 临商银⾏ BOLS

辽阳银⾏ LYCB 渣打银⾏ SCBL
⻓安银⾏ CHAB 昆仑银⾏ BOKL
韩亚银⾏ HANABANK 济宁银⾏ BOJN
保定银⾏ BOBAODING 邢台银⾏ XTB
贵州银⾏ BOGZ 中原银⾏ ZYB
吉林银⾏ BOJL 东亚银⾏ BEA
鞍⼭银⾏ BOAS ⻓沙银⾏ BOCS
朝阳银⾏ BOCY 沧州银⾏ BOCZ
洛阳银⾏ BOLY ⻘海银⾏ BOQH
乌海银⾏ BOWH 厦⻔银⾏ BOXM
内蒙古银⾏ BOIMC 哈尔滨银⾏ BOHRB
⼴州农商⾏ GRCB 重庆农商⾏ CQRCB
武汉农商⾏ WHRCB 苏州农商⾏ WJRCB
⽆锡农商⾏ WXRCB 北京农商⾏ BJNCSYYH
葫芦岛银⾏ BOHLD 平顶⼭银⾏ BOPDS
⼤连农商⾏ DLNCSY ⽯嘴⼭银⾏ SZSCCB
秦皇岛银⾏ QHDBANK ⿊⻰江农信 HLJNX
江南农商⾏ JNBANK 四川天府银⾏ CGNB
⻓城华⻄银⾏ DYCCBANK 联合村镇银⾏ URB
天津⾦城银⾏ BOJC 宁波通商银⾏ NBCB
宁波东海银⾏ NBDHB 重庆三峡银⾏ CQTSB
本溪商业银⾏ BXCB 营⼝沿海银⾏ YKYHB
湖南三湘银⾏ HNSXB 凉⼭商业银⾏ LSCB
云南红塔银⾏ YNHTB 新疆汇和银⾏ BOHH
乌鲁⽊⻬银⾏ URCB 焦作中旅银⾏ JZCTB
江阴农商银⾏ JYBNAK 华侨永亨银⾏ OCBCW
⻘隆村镇银⾏ QXQLCB ⼴东华兴银⾏ GHBANK
成都农商银⾏ CDRCB 鄂尔多斯银⾏ ORDOS

华融湘江银⾏ BOXJ 厦⻔国际银⾏ XIB
⼴东南粤银⾏ GDNYB 福建海峡银⾏ FJHXBANK
浙江⽹商银⾏ MYBANK 珠海华润银⾏ ZHHRCB
上海农商银⾏ SRCB 昆⼭农商银⾏ KSRCB
常熟农商银⾏ CSRCBANK 顺德农商银⾏ FSSDRCCB
威海市商业银⾏ WHCCB 绵阳市商业银⾏ MYCCBANK
盘锦市商业银⾏ PJCCB 晋中市商业银⾏ JZSSCB
张家港农商银⾏ ZJGRCB 哈密市商业银⾏ HMCB
雅安市商业银⾏ YACB 宜宾市商业银⾏ YBCB
曲靖市商业银⾏ QJCB 新疆农村信⽤社 XJRCCB
阳泉市商业银⾏ YQCCB 达州市商业银⾏ DZCCB
吉林农信联合社 JLNLS ⼴⻄北部湾银⾏ BANKOFBBG
乐⼭市商业银⾏ SCLSLSSY 天津滨海农商⾏ BHRCB
浙江泰隆商业银⾏ ZJTLCB 江苏⻓江商业银⾏ CJCCB
云南省农村信⽤社 YNRCU 浙江⺠泰商业银⾏ MINTAIBANK
四川省农村信⽤社 SCRCU 江苏农村商业银⾏ JSRCB
秦皇岛市商业银⾏ QHDCB 太仓农村商业银⾏ TCRCB
天津武清村镇银⾏ TWRCB 库尔勒市商业银⾏ KELCB
河南省农村信⽤社 HRCU ⻘海省农村信⽤社 QHNX
内蒙古农村信⽤社 NMGNXS 天津农村商业银⾏ TJRCCB
浙江稠州商业银⾏ CZCB 鄞州农村合作银⾏ YZRCB
东莞农村商业银⾏ DGRCB 吴江农村商业银⾏ WRCB
⼴东省农村信⽤社 GDRCU 河北省农村信⽤社 HBRCU
海南省农村信⽤社 HNRCU 江苏省农村信⽤社 JSRCU
江⻄省农村信⽤社 JXRCU ⽢肃省农村信⽤社 GSRCU
⻩河农村商业银⾏ NXHHCRCB 深圳农村商业银⾏ SZRCB
攀枝花市商业银⾏ PZHCCB 乌鲁⽊⻬市商业银⾏ BOWRMQ
陕⻄秦农农村商业银⾏ SNQB 辽宁⾠州汇通村镇银⾏ CZHTB

⼴⻄农村信⽤社联合社 GXRCU 湖南省农村信⽤社联合社 HNRCC
辽宁省农村信⽤社联合社 LNRCC 福建省农村信⽤社联合社 FJNX
贵州省农村信⽤社联合社 GZRCU 江⻄裕⺠银⾏ JXYMYH