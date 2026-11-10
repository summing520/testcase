-- 允许任务 status=generating（Agent 生成过程中的中间状态）
USE `qa`;

ALTER TABLE `testcase_tasks` DROP CHECK `chk_testcase_tasks_status`;

ALTER TABLE `testcase_tasks`
  ADD CONSTRAINT `chk_testcase_tasks_status`
  CHECK (`status` IN ('draft', 'parsed_confirming', 'generating', 'generated', 'adopted'));
