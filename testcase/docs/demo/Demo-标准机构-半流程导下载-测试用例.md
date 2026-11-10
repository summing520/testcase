# Demo-标准机构-半流程导下载-测试用例

> **机构流程**：半流程 — 出额导下载（授信走 API，用信走 H5 / 导下载至机构 APP）  
> **来源**：思维导图 `【聚融花】机构对接-测试大纲.mm` 解析整理；示例机构为聚融花。

---

## 一、产品概况

| 项 | 内容 |
|----|------|
| 机构 ID | 1047 |
| 机构编码 / 产品代码 | `juronghua` |
| 机构名称 / 产品名称 | 聚融花 |
| 类型 | OSI 标准机构 |
| 流程概要 | 授信 API + 提现/还款 H5 |
| 定价模式 | IIR 24% |
| 额度类型 | 单笔单批 |
| 结算方式 | CPA |
| 上线范围 | APP、HUB |

---

## 二、用户流程（账号矩阵）

- **账号1**：准入拒绝
- **账号2**：授信失败
- **账号3**：授信通过 → 授信过期 → 重新授信 → 机构准入拒绝
- **账号4**：授信通过 → **立即提现** → **跳转机构 APP 下载页** → 下载机构 APP
  - **Android**：下载安装机构 APP 包
  - **iOS**：跳转 App Store，打开机构 APP
  - **OpenHarmony OS**：跳转鸿蒙应用市场（**不支持**：机构 APP 未上架鸿蒙应用市场）
- **账号5（备用）**：授信通过
- **账号6（备用）**：授信通过

---

## 三、授信环节

### 3.1 1.1 准入撞库

**场景：APP · 活体认证完成后**

#### 准入失败

- **入参示例**

```json
{
  "mobileNoMd5": "63484f3d89890ef72152eca7f51e1241",
  "idNoMd5": "376134734fb8b6b5d6880fc896fe07ef",
  "fundCode": "juronghua"
}
```

- **出参要点**：`bizData.result = 2`，`reasonDesc` 有说明（例：黑名单用户）

```json
{
  "code": "200",
  "msg": "响应成功",
  "bizData": {
    "result": 2,
    "reasonDesc": "黑名单用户"
  }
}
```

#### 准入成功

- **出参要点**：`bizData.result = 1`

```json
{"code":"200","msg":"响应成功","bizData":{"result":1}}
```

- **分发**：分发列表包含本机构（排除其它分发规则影响）

---

### 3.2 5.2 查询用户协议

**场景：APP · 进入详细资料页**

#### 查询成功

- **入参示例**

```json
{
  "userNo": "UR1202465063521808384",
  "scene": "CREDIT",
  "fundCode": "juronghua"
}
```

- **出参要点**：`agreements` 含信息授权、隐私、注册等协议 URL；`isDefaultSelect`、`isForceRead` 等字段需符合接口文档
- **页面**：详细资料页展示接口返回的协议列表

示例协议（节选）：

- 聚融花信息授权协议：`https://rhxedb.com/juronghua/api/document/platform-protocol-agreement/tag-sqxy.html`
- 聚融花隐私协议：`https://rhxedb.com/juronghua/api/document/platform-protocol-agreement/tag-ysxy.html`
- 聚融花注册协议：`https://rhxedb.com/juronghua/api/document/platform-protocol-agreement/tag-zcxy.html`

---

### 3.3 1.4 授信申请提交

**场景：APP · 联系人页 · 提交**

#### 受理成功

- **入参**：参照《授信字段表 聚融花》；含 `creditReqNo`、`userNo`、`userBaseInfo`、`userProfileInfo`、`authIdInfo`、`authFaceInfo` 等（姓名、手机、婚姻、收入、身份证、活体等按字段表填写）。

- **出参要点**：`result = 1`，返回 `fundCreditNo`

```json
{
  "code": "200",
  "msg": "响应成功",
  "bizData": {
    "result": 1,
    "fundCreditNo": "CR1202466779229945856"
  }
}
```

#### 失败

- **出参**：`result = 2`，`reasonDesc` 有值

```json
{
  "code": "200",
  "msg": "响应成功",
  "bizData": {
    "result": 2,
    "reasonDesc": "进件失败！"
  }
}
```

---

### 3.4 1.5 查询授信申请结果

**场景：APP · 首页 · 刷新**

#### 授信中

- **入参示例**（执行聚融花用例时 `fundCode` 应与 `juronghua` 一致）

```json
{"creditReqNo":"CR1187471908152758272","fundCode":"juronghua"}
```

- **出参**：`result = "CR105"`（授信中），可带 `fundCreditNo`、`creditSuccTime`、`creditAmt`、`annualRate` 等

```json
{
  "code": "200",
  "msg": "响应成功",
  "bizData": {
    "result": "CR105",
    "fundCreditNo": "CR1202621102840713216",
    "creditSuccTime": "2026-04-22 16:41:37",
    "creditAmt": 26900,
    "annualRate": "0.2359"
  }
}
```

#### 授信拒绝

- **出参**：`result = "CR102"`，`reasonCode`、`creditFailTime`、`creditFailFrozenTime` 等

```json
{
  "code": "200",
  "msg": "响应成功",
  "bizData": {
    "result": "CR102",
    "reasonCode": "C2001",
    "creditFailTime": "2026-04-22 16:52:53",
    "creditFailFrozenTime": "2999-12-31 23:59:59"
  }
}
```

#### 授信通过

- **出参**：`result = "CR101"`，额度、利率、成功时间等

```json
{
  "code": "200",
  "msg": "响应成功",
  "bizData": {
    "result": "CR101",
    "fundCreditNo": "CR1202506684375072768",
    "creditSuccTime": "2026-04-22 11:57:26",
    "creditAmt": 25900,
    "annualRate": "0.12"
  }
}
```

- **后续**：调用 **5.1 查询用户额度**

---

### 3.5 2.1 推送授信申请结果（机构回调）

**场景：机构授信通过/拒绝，回调通知我方**

#### 授信拒绝 · 入参示例

```json
{
  "creditReqNo": "CR1202628211481350144",
  "result": "CR102",
  "reasonCode": "C2001",
  "creditFailTime": "2026-04-22 16:59:16",
  "creditFailFrozenTime": "2999-12-31 23:59:59"
}
```

#### 授信通过 · 入参示例

```json
{
  "creditReqNo": "CR1202466779229945856",
  "result": "CR101",
  "creditSuccTime": "2026-04-22 10:18:20",
  "creditAmt": 29800.00,
  "annualRate": "0.12"
}
```

- **后续**：调用 **5.1 查询用户额度**

---

### 3.6 5.1 查询用户额度

**场景：APP · 首页 · 刷新**

#### 查询成功

- **入参**：授信单号（按接口约定传 `creditReqNo` 等）
- **出参 · 额度可用**：`status = 1`，含 `creditAmt`、`availableAmt`、`maxAvailableAmt`、`minAvailableAmt`、`creditValidTime`、`creditExpireTime`、`repayMethod`、`rateType`、`rateUnit`、`rate`、`availableTerms` 等

```json
{
  "status": 1,
  "creditAmt": 29200,
  "availableAmt": 29200,
  "maxAvailableAmt": 29200,
  "minAvailableAmt": 29200,
  "creditValidTime": "2026-04-22 14:28:44",
  "creditExpireTime": "2026-04-27 14:28:47",
  "repayMethod": 1,
  "rateType": "IRR",
  "rateUnit": "YEAR",
  "rate": "0.2359",
  "availableTerms": [1, 3, 6, 9, 12]
}
```

#### 额度失效

- **出参示例**：`status = 2`，其余额度结构类似

```json
{
  "code": "200",
  "msg": "响应成功",
  "bizData": {
    "status": 2,
    "creditAmt": 27900,
    "availableAmt": 27900,
    "maxAvailableAmt": 27900,
    "minAvailableAmt": 27900,
    "creditValidTime": "2026-04-22 17:16:02",
    "creditExpireTime": "2026-04-27 17:35:19",
    "repayMethod": 1,
    "rateType": "IRR",
    "rateUnit": "YEAR",
    "rate": "0.2359",
    "availableTerms": [1, 3, 6, 9, 12]
  }
}
```

- **客户端**：创建账户后，APP 提现卡片展示可提现额度

---

## 四、用信环节（出额导下载）

### 4.1 5.3 查询场景页面地址

**场景：APP · 首页 · 刷新**

#### 查询成功

- **入参**：`scene = DRAW`（提现场景）
- **出参**：`bizData.url` = **机构 APP 下载 URL**（H5 带 token、channelSign 等）

```json
{
  "code": "200",
  "msg": "成功",
  "bizData": {
    "url": "https://scfqtestmallm.hzbxhd.com?token=...&channelSign=..."
  }
}
```

> 完整 URL 以环境实际返回为准；大纲中原示例含长 JWT 与签名参数，此处省略中间片段。

---

### 4.2 APP · 首页 · 提现卡片 ·「立即提现」

- 跳转到 **机构 APP 下载页**
- 验证 **返回 APP** 等交互与产品说明一致

---

## 五、半流程 · 出额导下载 — 链路摘要

1. **授信**：准入撞库 → 查询用户协议 → 授信申请提交 → 查询授信结果 / 机构推送结果 → **5.1 查询用户额度**。
2. **用信**：**5.3 查询场景页面地址**（`scene=DRAW`）获取下载 URL → 提现卡片「立即提现」→ 跳转机构 APP 下载页（Android / iOS；鸿蒙按不支持或未上架处理）。
3. **账号**：用账号 1～6 覆盖准入拒绝、授信失败、过期重授信、导下载全路径及备用授信通过。

---

## 六、备注

- 具体字段枚举、错误码与《标准机构对接-接口文档》《授信字段表》保持一致时为准。
- 原思维导图中个别示例 `fundCode` 非 `juronghua`，落库用例时已统一为聚融花编码说明；实际联调以 `juronghua` 为准。
