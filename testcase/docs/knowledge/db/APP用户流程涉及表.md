# APP用户流程中操作的数据库表清单

## 下载APP

### 市场投放点击（新）
- `mds.t_ad_channel_click_xiaomi`：小米点击事件信息表
- `mds.t_ad_channel_click_vivo`：vivo信息流事件信息表
- `mds.t_ad_channel_click_huawei`：华为信息流事件信息表

### 市场投放点击（老）
- `mds.t_vivo_click_monitor`：vivo点击检测
- `mds.t_xiaomi_click_track_info`：小米广告位点击信息
- `mds.t_honor_click_track_info`：荣耀广告位点击信息
- `mds.t_huawei_click_track_info`：华为广告位点击信息

### 华为应用市场点击回传
- `mds.t_ad_channel_return_record_huawei`：华为应用市场回传记录

### APP下载记录
- `bcs.t_user_app_download_record`：下载记录
- `bcs.t_user_app_download_info_x`：用户APP下载记录表（分表）

---


## APP注册登录
- `micros_users.users_user`：老Python系统用户表
- `cis.u_user`：新系统用户表（默认）
- `cis.u_user_random`：用户随机数
- `cis.u_register_info_x`：用户注册表（分表，X 为 0–9；注意：X 为分表具体数值）
- `cis.u_login_info`：用户登录记录表
- `bcs.app_dau_info`：活跃信息
- `cis.u_user_login_ext`：用户产品新增记录表
- `cis.u_user_change_log`：用户变更日志（注销恢复）
- `trs.active_attribution_result`：登录用户启动APP归因结果

---


## 进入APP首页

### 设备信息采集
- `cis.u_device`：用户设备信息采集表

### 执行C00001分发规则
- `tds.flow_user_rule_exec`：用户分发执行记录
- `tds.flow_user_rule_exec_ext`：分发执行结果表
- `lps.ap_fund_distribution_record`：分发结果记录

### 风控
- `apv.ap_dist_apply`：分发申请表
- `apv.ap_apply_credit`：申请资信查询关联关系表
- `crs.cr_query_info`：资信查询信息表

---


## 点击领取额度，开始创建用户流程实例
- `apv.ap_app`：申请应用信息
- `lps.ap_flow`：申请流程记录表，对应一个用户的一次申请流程
- `lps.ap_sub_flow_recording`：入口点击子流程记录
- `lps.wf_task_curr`：任务表

---


## 实名认证

### 上传身份证
- `cis.u_idcard_ocr`：身份证正反面
- `cis.u_cust_cert`：申请阶段的客户信息表，（因c_cust表只有在人脸识别通过才写入，所以该表需要保存申请阶段客户五项信息的记录）
- `lps.wf_order`：授信流程实例

### 人脸认证（活体认证）
- `cis.u_face_detect`：人脸认证信息

### 创建客户
- `cis.c_cust`：客户信息
- `cis.c_cust_random`：客户随机数
- `apv.ap_app`：申请应用信息

---


## 用户在机构撞库
- `lps.ap_fund_check_request`：机构撞库记录表

---


## 填写详细资料
- `cis.c_person_info`：用户个人信息-详细资料
- `cis.c_job_info`：工作信息
- `cis.c_address`：居住地址
- `cis.u_geo`：经纬度
- `cis.u_user_mock_data`：通过mock规则生成的用户数据
- `lps.ap_fund_distribution_record`：分发结果

---


## 填写联系人

- `cis.c_contact`：联系人信息
- `cis.c_person_info`：个人信息-基本信息
- `lps.ap_fund_distribution_record`：执行C0002分发结果（含 flowNo）
- `lps.u_agreement_read`：用户阅读协议
- `lps.u_agreement_read_detail`：用户协议阅读明细表

---


## 四要素绑卡

- `cis.u_4factor_bind_card_req`：四要素绑卡申请表
- `cis.u_bankcard`：用户银行卡信息表
- `cis.c_bankcard`：客户银行卡信息表

---


## 阅读强弹协议

- `lps.u_agreement_force_read`：强阅读协议

---


## 授信申请

- `lps.ap_fund_request`：机构注册（仅部分机构有）
- `lps.ap_appl`：授信申请（平台母单）
- `lps.ap_fund_appl`：授信申请（平台子单）

---


## 账户

### 授信开户请求
- `ams.ac_credit_req`：授信开户请求

### 授信通过，开户
- `ams.ac_pilot_account`：账户信息
- `ams.ac_pilot_account_archive`：账户归档表
- `ams.ac_account_log`：账户变更日志
- `ams.ac_pilot_prd_term_fee`：账户-产品定价信息
- `ams.ac_pilot_prd_term_fee_archive`：导流账户-产品定价档案表

---


## 借款试算

- `lcs.pilot_putout_calc`：试算
- `lcs.pilot_putout_calc_detail`：试算-详情

---


## 绑定提现银行卡
- `cis.u_fund_bind_card_req`：银行卡绑定申请信息
- `cis.u_fund_bind_relation`：银行卡关联的机构
- `cis.u_fund_bankcard`：机构返回已绑卡信息表
- `cis.u_bankcard`：已绑定的银行卡

---


## 借款（提现）

### 借款申请
- `lps.i_iou_flow`：借款申请提交-动支流水
- `lps.i_iou`：借款申请

### 借款交易流水
- `lcs.pilot_tran_proc_db`：导流业务放款申请流水表
- `lcs.pilot_privilege_tran_proc`：权益交易流水表
- `lcs.pilot_addon_tran_proc`：借款搭售产品交易流水表

### 机构放款成功，生成平台借据、权益订单/AMC订单
- `lcs.pilot_loan`：导流借据表
- `lcs.pilot_privilege_order`：导流权益借据表
- `lcs.pilot_addon_order`：借款搭售产品订单表

### 平台借据还款计划、权益订单还款计划/AMC订单还款计划）
- `lcs.pilot_plan`：导流业务还款计划表
- `lcs.pilot_privilege_plan`：导流业务权益还款计划表
- `lcs.pilot_addon_plan`：借款搭售产品还款计划表

---


## 还款

### 还款试算
- `lcs.pilot_repay_trial`：还款试算记录表

### 还款申请提交
- `lcs.pilot_tran_proc_rp`：导流业务还款交易申请流水表

### 还款成功，更新借据
- `lcs.pilot_loan`：导流借据表
- `lcs.pilot_privilege_order`：导流权益借据表
- `lcs.pilot_addon_order`：借款搭售产品订单表

### 更新还款计划
- `lcs.pilot_plan`：导流业务还款计划表
- `lcs.pilot_privilege_plan`：导流业务权益还款计划表
- `lcs.pilot_addon_plan`：借款搭售产品还款计划表

---


## 注销

### 注销基本信息
- `bcs.t_sms_code_record`：发送验证码记录表
- `bcs.t_user_log_off_reason_record`：注销原因
- `cis.u_user_hesitate_logoff`：注销犹豫期
- `cis.u_user_logoff`：注销记录

### 注销成功，更新用户相关数据库相关表（逻辑删除：`delete_flag = 1`）

#### cis 数据库相关表
- `cis.c_address`
- `cis.c_contact`
- `cis.c_job_info`
- `cis.c_person_info`
- `cis.u_bankcard`
- `cis.u_face_detect`
- `cis.u_fund_bankcard`
- `cis.u_fund_bind_relation`
- `cis.u_idcard_ocr`
- `cis.u_login_his`

#### cos 数据库相关表
- `cos.vip_user`

#### lcs 数据库相关表
- `lcs.pilot_addon_order`
- `lcs.pilot_addon_order_his`
- `lcs.pilot_addon_tran_proc`
- `lcs.pilot_loan`
- `lcs.pilot_loan_fund_terminated`
- `lcs.pilot_privilege_order`
- `lcs.pilot_privilege_tran_proc`
- `lcs.pilot_reduction_notify`
- `lcs.pilot_tran_proc_db`
- `lcs.pilot_tran_proc_rp`
- `lcs.vp_flow_user_config`

#### ams 数据库相关表
- `ams.ac_pilot_account`
- `ams.ac_pilot_account_archive`
- `ams.ac_pilot_prd_term_fee`
- `ams.ac_pilot_prd_term_fee_archive`

#### lps 数据库相关表
- `lps.ap_appl`
- `lps.ap_appl_archive`
- `lps.ap_fund_appl`
- `lps.ap_fund_appl_archive`
- `lps.ap_supply`
- `lps.i_iou`
- `lps.i_iou_flow`
- `lps.im_mc_msg`

#### hub 数据库相关表
- `hub.hub_account_summary`
- `hub.hub_channel_ap_apply_summary`
- `hub.hub_channel_lending_record`
- `hub.hub_channel_request_info`
- `hub.hub_fund_ap_apply_summary`
- `hub.hub_fund_apply_state_change_msg`
- `hub.hub_fund_apply_state_trigger_push_task`
- `hub.hub_loan_summary`
- `hub.hub_tran_proc_db_summary`
