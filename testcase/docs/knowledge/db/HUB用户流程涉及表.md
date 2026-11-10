# HUB渠道用户流程中操作的数据库表清单


## 用户准入

### HUB渠道准入-撞库
- `mds.t_hub_channel_check_record`：渠道撞库结果
- `tds.risk_user_fund`：用户在机构风控结果

### HUB渠道用户-风控
- `lps.ap_fund_check_request`：用户在机构风控结果

### HUB渠道用户-分发
- `lps.ap_fund_distribution_record`：分发结果记录
- `lps.ap_fund_request`：机构准入记录
- `tds.risk_user_fund`：用户机构风控数据
- `tds.flow_user_rule_exec`：分发执行表
- `tds.flow_user_rule_exec_ext`：分发执行结果表

---


## 用户授信

### HUB渠道用户授信申请提交的资料
- `cis.u_hub_user`：hub 渠道用户信息表
- `cis.u_hub_address`：hub 渠道客户地址
- `cis.u_hub_contact`：hub 渠道用户联系人信息
- `cis.u_hub_job_info`：hub 渠道用户工作信息
- `cis.u_hub_person_info`：hub 渠道用户个人信息

### 乐享借-创建平台用户及客户信息（⚠️注意：OCR及人脸识别所使用的厂商是哪一家）
- `cis.u_user`：新系统用户表（默认）
- `cis.u_face_detect`：人脸识别活体检测信息表
- `cis.u_idcard_ocr`：证件照 OCR 识别信息表
- `cis.c_address`：居住地址
- `cis.c_job_info`：工作信息
- `cis.c_person_info`：联系人

### 流程与协议
- `lps.ap_sub_flow_recording`：流程记录表

### HUB渠道用户授信核心表
- `hub.hub_channel_ap_apply_summary`：HUB授信母表
- `hub.hub_fund_ap_apply_summary`：HUB授信子表
- `hub.hub_account_summary`：HUB账户摘要表
- `hub.hub_push_task`：HUB渠道推送任务表

### 乐享借平台用户授信表
- `lps.ap_appl`：授信申请表
- `lps.ap_fund_appl`：机构授信表（`ap_appl` 的子表）

---


## 用户借款（提现）

### 借款试算
- `lcs.pilot_putout_calc`：试算
- `lcs.pilot_putout_calc_detail`：试算-详情

### 绑定借款银行卡
- `cis.c_bankcard`：客户银行卡信息表
- `cis.u_bankcard`：用户银行卡信息表
- `cis.u_fund_bankcard`：机构返回已绑卡信息表
- `cis.u_fund_bind_relation`：用户和机构绑卡绑定关系表
- `cis.u_4factor_bind_card_req`：四要素绑卡申请表

### HUB借款摘要表
- `hub.hub_loan_summary`：HUB借据摘要表
- `hub.hub_tran_proc_db_summary`：HUB放款摘要表
- `hub.hub_channel_lending_record`：HUB借款用信记录表
- `hub.hub_push_task`：HUB渠道推送任务表

### 乐享借平台借款申请
- `lps.i_iou_flow`：借款申请提交-动支流水
- `lps.i_iou`：借款申请

### 乐享借平台借款交易流水
- `lcs.pilot_tran_proc_db`：导流业务放款申请流水表
- `lcs.pilot_privilege_tran_proc`：权益交易流水表
- `lcs.pilot_addon_tran_proc`：借款搭售产品交易流水表

### 乐享借平台借据、权益订单/AMC订单
- `lcs.pilot_loan`：导流借据表
- `lcs.pilot_privilege_order`：导流权益借据表
- `lcs.pilot_addon_order`：借款搭售产品订单表

### 乐享借平台借据还款计划、权益订单还款计划/AMC订单还款计划
- `lcs.pilot_plan`：导流业务还款计划表
- `lcs.pilot_privilege_plan`：导流业务权益还款计划表
- `lcs.pilot_addon_plan`：借款搭售产品还款计划表

### HUB渠道推送任务
- `hub.hub_push_task`：渠道推送任务表

---


## 用户还款

### 乐享借平台还款试算
- `lcs.pilot_repay_trial`：还款试算记录表

### 乐享借平台还款申请提交
- `lcs.pilot_tran_proc_rp`：还款交易申请流水

### 乐享借平台还款成功，更新借据
- `lcs.pilot_loan`：导流借据表
- `lcs.pilot_privilege_order`：导流权益借据表
- `lcs.pilot_addon_order`：借款搭售产品订单表

### 乐享借平台更新还款计划
- `lcs.pilot_plan`：导流业务还款计划表
- `lcs.pilot_privilege_plan`：导流业务权益还款计划表
- `lcs.pilot_addon_plan`：借款搭售产品还款计划表

### HUB渠道推送任务
- `hub.hub_push_task`：渠道推送任务表
