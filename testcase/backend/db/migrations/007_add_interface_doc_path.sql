-- 记录步骤2 保存/匹配的接口文档路径，供历史用例列表展示
USE `qa`;

ALTER TABLE `testcase_tasks`
  ADD COLUMN `interface_doc_path` VARCHAR(512) NOT NULL DEFAULT ''
    COMMENT '生成用例时使用的接口文档路径（docs/knowledge/interface/... 或 用户上传/文件名）'
    AFTER `external_cooperation_url`;
