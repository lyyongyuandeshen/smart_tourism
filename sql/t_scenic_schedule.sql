-- 员工表
CREATE TABLE IF NOT EXISTS t_scenic_employee (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    employee_code VARCHAR(50) UNIQUE,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_employee_code (employee_code),
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='景区员工表';

-- 岗位表
CREATE TABLE IF NOT EXISTS t_scenic_position (
    position_id INT PRIMARY KEY AUTO_INCREMENT,
    position_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_position_name (position_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='景区岗位表';

-- 班次模板表
CREATE TABLE IF NOT EXISTS t_scenic_shift (
    shift_id INT PRIMARY KEY AUTO_INCREMENT,
    shift_name VARCHAR(100) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    position_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (position_id) REFERENCES t_scenic_position(position_id) ON DELETE SET NULL,
    INDEX idx_shift_name (shift_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='班次模板表';

-- 排班记录表
CREATE TABLE IF NOT EXISTS t_scenic_schedule (
    schedule_id INT PRIMARY KEY AUTO_INCREMENT,
    schedule_date DATE NOT NULL,
    shift_id INT NOT NULL,
    position_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_date_position (schedule_date, position_id),
    FOREIGN KEY (shift_id) REFERENCES t_scenic_shift(shift_id) ON DELETE CASCADE,
    FOREIGN KEY (position_id) REFERENCES t_scenic_position(position_id) ON DELETE CASCADE,
    INDEX idx_schedule_date (schedule_date),
    INDEX idx_position_id (position_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='排班记录表';

-- 排班员工关联表
CREATE TABLE IF NOT EXISTS t_scenic_schedule_employee (
    schedule_employee_id INT PRIMARY KEY AUTO_INCREMENT,
    schedule_id INT NOT NULL,
    employee_id INT NOT NULL,
    is_leader BOOLEAN DEFAULT FALSE,
    UNIQUE KEY uk_schedule_employee (schedule_id, employee_id),
    FOREIGN KEY (schedule_id) REFERENCES t_scenic_schedule(schedule_id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES t_scenic_employee(employee_id) ON DELETE CASCADE,
    INDEX idx_schedule_id (schedule_id),
    INDEX idx_employee_id (employee_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='排班员工关联表';

-- 插入员工测试数据
INSERT INTO t_scenic_employee (name, employee_code, phone) VALUES 
('李小明', 'E001', '13912345671'),
('王五', 'E002', '13912345672'),
('章小鱼', 'E003', '13912345673'),
('郭四', 'E004', '13912345674'),
('陈大鹏', 'E005', '13912345675'),
('刘美丽', 'E006', '13912345676');

-- 插入岗位测试数据
INSERT INTO t_scenic_position (position_name) VALUES 
('保洁'),       -- ID = 1
('巡逻安保'),   -- ID = 2
('引导员');     -- ID = 3

-- 插入班次测试数据
INSERT INTO t_scenic_shift (shift_name, start_time, end_time, position_id) VALUES 
('早班', '08:00:00', '17:00:00', 1),
('中班', '10:00:00', '19:00:00', 3),
('晚班', '17:00:00', '02:00:00', 2);

-- 插入排班记录测试数据
INSERT INTO t_scenic_schedule (schedule_date, shift_id, position_id) VALUES 
('2025-11-28', 2, 3), -- ID = 1：11/28 引导员
('2025-11-28', 3, 2), -- ID = 2：11/28 巡逻安保
('2025-11-29', 1, 1), -- ID = 3：11/29 保洁
('2025-11-29', 2, 3), -- ID = 4：11/29 引导员
('2025-11-30', 3, 2), -- ID = 5：11/30 巡逻安保
('2025-12-01', 1, 1), -- ID = 6：12/01 保洁
('2025-12-02', 2, 3), -- ID = 7：12/02 引导员
('2025-12-03', 1, 1), -- ID = 8：12/03 保洁
('2025-12-04', 3, 2), -- ID = 9：12/04 巡逻安保
('2025-12-05', 2, 3), -- ID = 10：12/05 引导员
('2025-12-06', 1, 1), -- ID = 11：12/06 保洁
('2025-12-07', 3, 2); -- ID = 12：12/07 巡逻安保

-- 插入排班员工关联测试数据
INSERT INTO t_scenic_schedule_employee (schedule_id, employee_id, is_leader) VALUES 
-- 11-28
(1, 1, TRUE),  -- 李小明 (引导员) - 负责人
(1, 6, FALSE), -- 刘美丽 (引导员)
(2, 2, TRUE),  -- 王五 (巡逻安保)
-- 11-29
(3, 3, FALSE), -- 章小鱼 (保洁)
(3, 4, TRUE),  -- 郭四 (保洁) - 负责人
(4, 5, TRUE),  -- 陈大鹏 (引导员)
-- 11-30
(5, 1, FALSE), -- 李小明 (巡逻安保)
(5, 2, TRUE),  -- 王五 (巡逻安保) - 负责人
-- 12-01
(6, 6, TRUE),  -- 刘美丽 (保洁)
-- 12-02
(7, 3, TRUE),  -- 章小鱼 (引导员)
-- 12-03
(8, 1, TRUE),  -- 李小明 (保洁) - 负责人
(8, 2, FALSE), -- 王五 (保洁)
-- 12-04
(9, 5, TRUE),  -- 陈大鹏 (巡逻安保)
(9, 4, FALSE), -- 郭四 (巡逻安保)
-- 12-05
(10, 6, TRUE), -- 刘美丽 (引导员) - 负责人
(10, 3, FALSE), -- 章小鱼 (引导员)
-- 12-06
(11, 1, TRUE), -- 李小明 (保洁)
-- 12-07
(12, 2, FALSE), -- 王五 (巡逻安保)
(12, 5, TRUE); -- 陈大鹏 (巡逻安保) - 负责人
