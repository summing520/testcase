-- =============================================================================
-- Test Case Generator — MySQL 8 初始 schema
-- 来源：backend/db/sqlite.py（当前 SQLite 表结构）
-- 约定：所有业务表名使用 testcase_ 前缀
--
-- 执行前请根据环境修改库名、账号；建议单独建库，勿与 DB_QUERY_URL 业务库混用。
-- =============================================================================

SET NAMES utf8mb4;
SET time_zone = '+00:00';

-- ---------------------------------------------------------------------------
-- 1. 数据库（可按需改名或注释掉，改由 DBA 预先创建）
-- ---------------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS `qa`
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE `qa`;

-- ---------------------------------------------------------------------------
-- 2. 任务主表（原 tasks）
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `testcase_tasks` (
  `id`                          CHAR(36)      NOT NULL COMMENT 'UUID',
  `status`                      VARCHAR(32)   NOT NULL COMMENT 'draft|parsed_confirming|generating|generated|adopted',
  `requirement_url`             VARCHAR(2048) NOT NULL COMMENT '飞书需求文档 URL',
  `external_cooperation_url`    VARCHAR(2048) NOT NULL DEFAULT '' COMMENT '对接文档 URL（可选）',
  `interface_doc_path`          VARCHAR(512)  NOT NULL DEFAULT '' COMMENT '生成用例时使用的接口文档路径',
  `selected_knowledge_docs`     JSON          NOT NULL COMMENT '选中的知识库文档路径列表',
  `selected_checklist_docs`     JSON          NOT NULL COMMENT '选中的检查清单文档路径列表',
  `selected_rule_docs`          JSON          NOT NULL COMMENT '选中的规则文档路径列表',
  `requirement_markdown`        LONGTEXT      NULL COMMENT '解析后的需求 Markdown',
  `external_cooperation_markdown` LONGTEXT    NULL COMMENT '对接文档 Markdown',
  `confirmed_check_items`       JSON          NULL COMMENT '已确认检查项 / Agent 评分等 JSON',
  `generated_testcase_markdown` LONGTEXT      NULL COMMENT '生成的测试用例 Markdown',
  `requirement_kind`            VARCHAR(32)   NOT NULL DEFAULT '' COMMENT 'channel|institution|unknown',
  `inferred_checklist_doc`      VARCHAR(512)  NOT NULL DEFAULT '' COMMENT '系统自动推断的检查清单路径',
  `generation_options_json`     JSON          NULL COMMENT '生成步骤选项（用例类型、流程模式等）',
  `created_at`                  DATETIME(3)   NOT NULL COMMENT 'UTC',
  `updated_at`                  DATETIME(3)   NOT NULL COMMENT 'UTC',
  PRIMARY KEY (`id`),
  KEY `idx_testcase_tasks_status` (`status`),
  KEY `idx_testcase_tasks_created_at` (`created_at`),
  CONSTRAINT `chk_testcase_tasks_status`
    CHECK (`status` IN ('draft', 'parsed_confirming', 'generating', 'generated', 'adopted')),
  CONSTRAINT `chk_testcase_tasks_requirement_kind`
    CHECK (`requirement_kind` IN ('', 'channel', 'institution', 'unknown'))
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='测试用例生成任务';

-- ---------------------------------------------------------------------------
-- 3. 任务检查项（原 task_check_items）
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `testcase_task_check_items` (
  `id`              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `task_id`         CHAR(36)        NOT NULL,
  `item_key`        VARCHAR(255)    NOT NULL COMMENT '检查项稳定键',
  `item_text`       TEXT            NOT NULL COMMENT '检查项原文',
  `matched_text`    TEXT            NULL COMMENT '规则/记忆匹配到的值',
  `confirmed_text`  TEXT            NULL COMMENT '用户确认后的值',
  `match_source`    VARCHAR(64)     NULL COMMENT '匹配来源标识',
  `is_edited`       TINYINT(1)      NOT NULL DEFAULT 0 COMMENT '用户是否编辑过',
  `created_at`      DATETIME(3)     NOT NULL COMMENT 'UTC',
  `updated_at`      DATETIME(3)     NOT NULL COMMENT 'UTC',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_testcase_task_check_items_task_item` (`task_id`, `item_key`),
  KEY `idx_testcase_task_check_items_task_id` (`task_id`),
  CONSTRAINT `fk_testcase_task_check_items_task`
    FOREIGN KEY (`task_id`) REFERENCES `testcase_tasks` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='任务检查项明细';

-- ---------------------------------------------------------------------------
-- 4. 采纳用例库（原 test_case_library）
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `testcase_test_case_library` (
  `id`                 BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `task_id`            CHAR(36)        NOT NULL,
  `title`              VARCHAR(512)    NOT NULL,
  `content_markdown`   LONGTEXT        NOT NULL,
  `adopted_at`         DATETIME(3)     NOT NULL COMMENT 'UTC',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_testcase_test_case_library_task_id` (`task_id`),
  CONSTRAINT `fk_testcase_test_case_library_task`
    FOREIGN KEY (`task_id`) REFERENCES `testcase_tasks` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='已采纳测试用例库';

-- ---------------------------------------------------------------------------
-- 5. Agent 运行日志（原 task_agent_runs）
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `testcase_task_agent_runs` (
  `id`            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `task_id`       CHAR(36)        NOT NULL,
  `iteration`     INT             NOT NULL,
  `action`        VARCHAR(128)    NOT NULL,
  `observation`   LONGTEXT        NULL,
  `score_json`    JSON            NULL,
  `created_at`    DATETIME(3)     NOT NULL COMMENT 'UTC',
  PRIMARY KEY (`id`),
  KEY `idx_testcase_task_agent_runs_task_iter` (`task_id`, `iteration`),
  KEY `idx_testcase_task_agent_runs_created_at` (`created_at`),
  CONSTRAINT `fk_testcase_task_agent_runs_task`
    FOREIGN KEY (`task_id`) REFERENCES `testcase_tasks` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='用例生成 Agent 迭代记录';

-- ---------------------------------------------------------------------------
-- 6. 检查清单记忆（原 checklist_item_memory）
--    item_text 存 VARCHAR(2000)；主键用 item_text 的 SHA256 生成列，避免 utf8mb4 索引超 3072 字节
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `testcase_checklist_item_memory` (
  `checklist_fingerprint` CHAR(64)     NOT NULL COMMENT '检查清单文件集合 SHA256',
  `item_text`             VARCHAR(2000) NOT NULL COMMENT '检查项原文',
  `item_text_hash`        CHAR(64)      GENERATED ALWAYS AS (SHA2(`item_text`, 256)) STORED NOT NULL COMMENT 'item_text SHA256，供主键',
  `remembered_value`      TEXT         NOT NULL COMMENT '记忆取值',
  `source_task_id`        CHAR(36)     NULL COMMENT '最近一次写入来源任务',
  `updated_at`            DATETIME(3)  NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3) COMMENT 'UTC',
  PRIMARY KEY (`checklist_fingerprint`, `item_text_hash`),
  KEY `idx_testcase_checklist_item_memory_source_task` (`source_task_id`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='检查清单项跨任务记忆';

-- ---------------------------------------------------------------------------
-- 7. 流程配置（原 pipeline_config）
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `testcase_pipeline_config` (
  `id`           VARCHAR(64)  NOT NULL COMMENT '配置 ID，默认 default',
  `config_json`  JSON         NOT NULL COMMENT 'PipelineConfig 序列化',
  `updated_at`   DATETIME(3)  NOT NULL COMMENT 'UTC',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='前端流程步骤配置';

-- 默认流程配置（id=default）不在此插入，由应用首次读取时写入（见 pipeline_config_service）。
-- 若从 SQLite 迁移且库中已有 pipeline_config 行，见 003/004 迁移 SQL。
