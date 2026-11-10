# Demo-标准机构-借还H5-测试用例

> **流程类型**：全流程 — 授信 API + 借还款 H5（提现/借款 H5 + 还款 H5）  
> **来源**：思维导图 `哞花购-机构对接-测试大纲.mm` 解析整理  
> **说明**：以「借还 H5」为主轴的对接用例大纲；正文覆盖授信、用信（借款 H5）、还款 H5 全链路（示例机构：哞花购）。

---

## 一、产品概况

| 项 | 内容 |
|----|------|
| 机构 ID | 1044 |
| 机构编码 / 产品代码 | `mouhuagou` |
| 机构名称 / 产品名称 | 哞花购 |
| 类型 | OSI 标准机构 |
| 流程概要 | 授信 API + 提现/还款 H5 |
| 定价模式 | 24 利率（IRR 24%） |
| 额度类型 | 循环额度 |
| 结算方式 | CPA |
| 首复贷 | 未结清复贷 |
| 上线范围 | APP、HUB |

---

## 二、授信环节

### 2.1 1.1 准入撞库

#### 准入失败

**入参**

```json
{
  "mobileNoMd5": "2e5eda85adda4b721038a76edd06c485",
  "idNoMd5": "ad388a668b692ff2e222874bb9238cf8",
  "fundCode": "mouhuagou"
}
```

**出参（bizData 要点）**

```json
{"result": 2, "reasonDesc": "撞库拒绝: 用户已存在"}
```

#### 准入成功

**出参**

```json
{"code": "200", "msg": "成功", "bizData": {"result": 1}}
```

**分发**：分发列表包含本机构（排除其它分发规则影响）

---

### 2.2 5.2 查询用户协议

#### 查询成功

**入参**

```json
{"userNo": "UR0975883430313074688", "scene": "CREDIT", "fundCode": "mouhuagou"}
```

**出参要点**：`agreements` 含用户服务协议、隐私政策、儿童个人信息保护规则、数字证书服务协议、电子签名授权书、哞花卡用户注册协议、哞花卡隐私权政策、哞花卡服务协议、非在校学生承诺函、委托快捷签署授权书、个人信息收集及使用授权书等（URL 域名为 `mhgtest.hzbxhd.com/html/agreement/...`）；`isDefaultSelect`、`isForceRead` 为 `N`

**页面**：详细资料页展示返回的协议列表

---

### 2.3 1.4 授信申请提交

#### 成功

- **入参**：参照《授信字段表 哞花购》；含 `creditReqNo`、`userNo`、`userBaseInfo`、`userProfileInfo`、`authIdInfo`、`authFaceInfo`（含 `faceDetectBasicData`）、`jobInfo`、`contactInfo`、`deviceInfo`、`geoInfo`、`riskInfo`、`fundCode` 等

**出参**

```json
{"code": "200", "msg": "成功", "bizData": {"result": 1}}
```

#### 失败

- **出参**：`result = 2`（失败）

---

### 2.4 1.5 查询授信申请结果

#### 授信中

**入参**

```json
{"creditReqNo": "CR1187471908152758272", "fundCode": "mouhuagou"}
```

**出参**：`result = CR105`（授信中）

#### 授信拒绝

```json
{
  "code": "200",
  "msg": "成功",
  "bizData": {
    "result": "CR102",
    "reasonCode": "C1011",
    "reasonDesc": "不良信用记录",
    "creditFailTime": "2026-03-27 13:38:12"
  }
}
```

#### 授信通过

```json
{
  "code": "200",
  "msg": "成功",
  "bizData": {
    "result": "CR101",
    "creditSuccTime": "2026-03-27 13:56:59",
    "creditAmt": 6000,
    "annualRate": "23.90"
  }
}
```

**后续**：调用 **5.1 查询用户额度**

---

### 2.5 2.1 推送授信申请结果（机构 → 我方）

#### 授信中

- **入参要点**：`result = CR105`（授信中）
- **出参**：请求成功

#### 授信拒绝

```json
{
  "result": "CR102",
  "creditFailTime": "2026-03-27 11:30:47",
  "creditReqNo": "CR1187420622619369472",
  "reasonDesc": "不良信用记录"
}
```

#### 授信通过

```json
{
  "result": "CR101",
  "creditReqNo": "CR1187475944146952192",
  "creditSuccTime": "2026-03-27 13:48:10",
  "creditAmt": "6000.00",
  "annualRate": "23.90"
}
```

**后续**：调用 **5.1 查询用户额度**

---

### 2.6 5.1 查询用户额度

#### 查询成功

**入参**

```json
{
  "userNo": "UR1187479467762171904",
  "creditReqNo": "CR1187479487092318208",
  "fundCode": "mouhuagou"
}
```

**出参（额度信息示例）**

```json
{
  "code": "200",
  "msg": "成功",
  "bizData": {
    "status": 1,
    "creditAmt": 6000,
    "availableAmt": 6000,
    "maxAvailableAmt": 6000,
    "minAvailableAmt": 6000,
    "creditValidTime": "2026-03-27 13:56:59",
    "creditExpireTime": "2026-09-23 23:59:59",
    "repayMethod": 2,
    "rateType": "IRR",
    "rateUnit": "YEAR",
    "rate": "0.24",
    "availableTerms": [6]
  }
}
```

**客户端**：创建账户，APP 提现卡片展示可提现额度

---

## 三、用信环节（借款 H5）

### 3.1 5.3 查询场景页面地址（借款）

#### 查询成功

- **场景**：借款（`scene = DRAW`）

**入参**

```json
{
  "userNo": "UR1187475923004866560",
  "scene": "DRAW",
  "creditReqNo": "CR1187475944146952192",
  "returnUrl": "https://test3.xurongwl.com/clg/lps/api/p/common/v1/h5/return?data=5763354F2B497973466E2B6F676E507A63494F624A756A6A694E6931736F6E6D377554694D69614D73425A42352F63395134776E555A433042684C546D7A784F",
  "fundCode": "mouhuagou"
}
```

**出参**：`bizData.url` 为 **机构借款 H5 URL**（示例带 `token`、`channelSign`）

```json
{
  "code": "200",
  "msg": "成功",
  "bizData": {
    "url": "https://scfqtestmallm.hzbxhd.com?token=...&channelSign=..."
  }
}
```

### 3.2 APP · 首页 · 提现卡片 ·「立即提现」

- 跳转 **机构借款 H5 页面**
- **`return_url`**：可返回 APP

---

### 3.3 2.3 查询放款结果

#### 无记录（用户未在机构发生借款）

**入参**

```json
{"creditReqNo": "CR1187475944146952192", "fundCode": "mouhuagou"}
```

**出参示例**

```json
{
  "code": "200",
  "msg": "成功",
  "bizData": {
    "drawResultList": [
      {
        "result": "DR109",
        "drawStatusUpdateTime": "2026-03-27 13:48:22"
      }
    ]
  }
}
```

#### 放款中

1. **机构未推送订单**：用 **授信单号** 查询（入参同上单号维度）
2. **出参（订单列表示例）**：`result = DR108`，含 `fundDrawNo`、`loanTerm` 等

```json
{
  "code": "200",
  "msg": "成功",
  "bizData": {
    "drawResultList": [
      {
        "result": "DR108",
        "drawStatusUpdateTime": "2026-03-27 14:36:50",
        "fundDrawNo": "loan2037418482060611584",
        "loanTerm": 6
      }
    ]
  }
}
```

3. **机构已推送订单**：用 **订单号** 查询

**入参**

```json
{
  "drawReqNo": "FP1187495963859664897",
  "fundDrawNo": "loan2037418482060611584",
  "creditReqNo": "CR1187478274166706176",
  "fundCode": "mouhuagou"
}
```

**出参**：返回当前订单状态列表（与上结构类似）

#### 放款失败（已作废）

- **说明（3 月 30 日机构确认）**：放款失败 **机构不推送**；**查询接口也不返回**（按该约定设计用例）

#### 放款成功

```json
{
  "code": "200",
  "msg": "成功",
  "bizData": {
    "drawResultList": [
      {
        "result": "DR101",
        "drawStatusUpdateTime": "2026-03-27 14:40:01",
        "fundDrawNo": "loan2037418482060611584",
        "loanAmt": 4800.0,
        "loanTerm": 6
      }
    ]
  }
}
```

**后续**：调用 **2.4 查询借据及还款计划**  
**数据**：创建放款流水

---

### 3.4 2.3 推送放款结果

- 与 **2.3 查询放款结果** 对照，**关注入参**（状态与订单字段一致）

---

### 3.5 2.4 查询借据及还款计划（用信侧 · 初始计划）

**入参**

```json
{
  "drawReqNo": "FP1187495963859664897",
  "fundDrawNo": "loan2037418482060611584",
  "fundCode": "mouhuagou"
}
```

**出参校验要点**

- 账单状态全部为 **待还**
- 期数：**3 期 / 6 期**（按产品）
- **本金不高于授信额度**

**数据与页面**：生成放款流水、借据、还款计划；APP 展示待还账单、还款计划、还款按钮

---

### 3.6 6.4 推送借据和还款计划

- 参照 **2.4 查询借据及还款计划**，**关注入参**

---

## 四、还款环节（还款 H5）

### 4.1 5.3 查询场景页面地址（还款）

#### 查询成功

- **场景**：还款（`scene = REPAY`）

**入参**

```json
{
  "userNo": "UR1187478247588806656",
  "scene": "REPAY",
  "creditReqNo": "CR1187478274166706176",
  "fundDrawNo": "loan2037418482060611584",
  "drawReqNo": "FP1187495963859664897",
  "returnUrl": "https://test3.xurongwl.com/clg/lps/api/p/common/v1/h5/return?data=5763354F2B497973466E2B6F676E507A63494F624A756A6A694E6931736F6E6D377554694D69614D7342596E526D726530736D376A544836426947704B4E62624F714834616B4A59766357744946443579386D2B4F773D3D",
  "fundCode": "mouhuagou"
}
```

**出参**：`bizData.url` 为 **机构还款页面 URL**

```json
{
  "code": "200",
  "msg": "成功",
  "bizData": {
    "url": "https://scfqtestmallm.hzbxhd.com?token=...&channelSign=..."
  }
}
```

### 4.2 跳转机构还款页面

- **`return_url`**：可返回 APP

---

### 4.3 2.4 查询借据及还款计划（还款侧状态矩阵）

- 初始待还款
- **单期逾期** → 查看 APP 待还款账单、还款计划
- 单期正常已还
- 单期逾期还款
- 全部结清
- **已退贷**：`loanStatus = 04`

### 4.4 6.4 推送借据和还款计划

- 参照 **2.4 查询借据及还款计划**

---

## 五、循环额度

- **多笔借据**：复用 **用信环节** 与 **还款环节** 相关接口组合验证

---

## 六、复贷

- **额度有效期内复贷**：多笔借据
- **额度过期后重新授信，发起第二笔借据**
  - 机构准入拒绝示例：`{"result": 2, "reasonDesc": "撞库拒绝: 用户已存在"}`

---

## 七、用户流程（账号矩阵）

| 账号 | 路径摘要 |
|------|----------|
| **账号1** | 准入拒绝 |
| **账号2** | 授信失败 |
| **账号3** | 放款失败 |
| **账号4** | 放款成功 → 初始待还 → 首期逾期 → 首期逾期还款 → 2 期正常还款 → **发起第二笔借款（未结清复贷）** |
| **账号5** | 放款成功 → 提前结清 → 授信过期 → **重新授信 - 准入拦截** |
| **账号6（备用）** | 放款成功 |
| **账号7（备用）** | 放款成功 |

---

## 八、全流程链路摘要

1. **授信**：撞库 → 协议 → 授信提交 → 查授信结果 / 推送授信结果 → **5.1 查额度**
2. **借款 H5**：**5.3（DRAW）** 取借款 URL → 立即提现进 H5 → **2.3 查放款**（无记录 / 放款中 / 成功；失败按机构约定不推送、查询不返回）→ 推送放款对齐查询 → **2.4 / 6.4** 借据与计划
3. **还款 H5**：**5.3（REPAY）** 取还款 URL → **`return_url` 回 APP** → **2.4** 各账单状态（含逾期、结清、退贷 `loanStatus=04`）→ **6.4** 推送计划
4. **循环 / 复贷**：多笔借据 + 过期重授信与准入拦截

---

## 九、备注

- 接口编号、字段枚举与《哞花购机构接口文档》《授信字段表》一致时为准。
- 大纲中「2.3」同时用于「查询放款结果」与「推送放款结果」，以接口文档区分的实际路径名为准。
