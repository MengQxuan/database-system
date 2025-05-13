-- DROP DATABASE IF EXISTS homework;
create database homework;
use homework;

-- 创建 Club 表
CREATE TABLE IF NOT EXISTS Club (
   clubname             VARCHAR(256)                  NOT NULL,
   coachname            VARCHAR(256)                  NULL,
   city                 VARCHAR(256)                  NULL,
   homecourt            VARCHAR(256)                  NULL,
   PRIMARY KEY (clubname)
) ENGINE=InnoDB;

-- 创建 Coach 表
CREATE TABLE IF NOT EXISTS Coach (
   coachname            VARCHAR(256)                  NOT NULL,
   clubname             VARCHAR(256)                  NULL,
   coachnation          VARCHAR(256)                  NULL,
   coachage             INTEGER                        NULL,
   PRIMARY KEY (coachname),
   FOREIGN KEY (clubname) REFERENCES Club (clubname) ON UPDATE RESTRICT ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 创建 Data 表
CREATE TABLE IF NOT EXISTS Data (
   goals                INTEGER                        NOT NULL,
   assists              INTEGER                        NULL,
   yellowcard          INTEGER                        NULL,
   redcard             INTEGER                        NULL,
   PRIMARY KEY (goals)
) ENGINE=InnoDB;

-- 创建 Player 表
CREATE TABLE IF NOT EXISTS Player (
   name                 VARCHAR(256)                  NOT NULL,
   clubname             VARCHAR(256)                  NULL,
   goals                INTEGER                        NULL,
   nation               VARCHAR(256)                  NULL,
   age                  INTEGER                   NULL,
   position             VARCHAR(256)                  NULL,
   number               VARCHAR(256)                  NOT NULL,
   PRIMARY KEY (name),
   FOREIGN KEY (clubname) REFERENCES Club (clubname) ON UPDATE RESTRICT ON DELETE RESTRICT,
   FOREIGN KEY (goals) REFERENCES Data (goals) ON UPDATE RESTRICT ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 创建 foreignaid 表
CREATE TABLE IF NOT EXISTS foreignaid (
   name                 VARCHAR(256)                  NOT NULL,
   clubname             VARCHAR(256)                  NULL,
   goals                INTEGER                        NULL,
   nation               VARCHAR(256)                  NULL,
   age                  INTEGER                   NULL,
   position             VARCHAR(256)                  NULL,
   number               VARCHAR(256)                  NOT NULL,
   PRIMARY KEY (name),
   FOREIGN KEY (name) REFERENCES Player (name) ON UPDATE RESTRICT ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 创建 mainland 表
CREATE TABLE IF NOT EXISTS mainland (
   name                 VARCHAR(256)                  NOT NULL,
   clubname             VARCHAR(256)                  NULL,
   goals                INTEGER                        NULL,
   nation               VARCHAR(256)                  NULL,
   age                  INTEGER                  NULL,
   position             VARCHAR(256)                  NULL,
   number               VARCHAR(256)                  NOT NULL,
   PRIMARY KEY (name),
   FOREIGN KEY (name) REFERENCES Player (name) ON UPDATE RESTRICT ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 视图，查看player信息
CREATE VIEW playerview AS
SELECT 
    p.name,
    p.clubname,
    c.coachname,
    p.goals,
    p.nation,
    p.age,
    p.position,
    p.number,
    d.assists,
    d.yellowcard,
    d.redcard
    
FROM 
    Player p
LEFT JOIN 
    Data d ON p.goals = d.goals
LEFT JOIN 
    Coach c ON p.clubname = c.clubname;



-- 触发器
DELIMITER //

-- 创建触发器，在删除 Club 表中的一行时，级联删除相关的 Coach 和 Player 表中的记录
CREATE TRIGGER cascade_delete_coach_player
BEFORE DELETE ON Club
FOR EACH ROW
BEGIN
    -- 删除与要删除的 Club 相关的 Coach 记录
    DELETE FROM Coach WHERE clubname = OLD.clubname;
    
    -- 删除与要删除的 Club 相关的 Player 记录
    DELETE FROM Player WHERE clubname = OLD.clubname;
END //

-- 创建触发器，确保在插入到 Data 表之前，所有数值字段都不是负数
CREATE TRIGGER before_insert_data
BEFORE INSERT ON Data
FOR EACH ROW
BEGIN
   IF NEW.goals < 0 THEN
       SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot insert negative value for goals';
   END IF;
   IF NEW.assists < 0 THEN
       SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot insert negative value for assists';
   END IF;
   IF NEW.yellowcard < 0 THEN
       SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot insert negative value for yellowcard';
   END IF;
   IF NEW.redcard < 0 THEN
       SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot insert negative value for redcard';
   END IF;
END //

-- 创建触发器，确保在更新 Data 表之前，所有数值字段都不是负数
CREATE TRIGGER before_update_data
BEFORE UPDATE ON Data
FOR EACH ROW
BEGIN
   IF NEW.goals < 0 THEN
       SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot update with negative value for goals';
   END IF;
   IF NEW.assists < 0 THEN
       SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot update with negative value for assists';
   END IF;
   IF NEW.yellowcard < 0 THEN
       SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot update with negative value for yellowcard';
   END IF;
   IF NEW.redcard < 0 THEN
       SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot update with negative value for redcard';
   END IF;
END //

-- 创建存储过程，用于更新 Player 表中的 clubname 和 goals
CREATE PROCEDURE update_player_info(
    IN p_name VARCHAR(256),
    IN new_clubname VARCHAR(256),
    IN new_goals INTEGER
)
BEGIN
    DECLARE clubExists INT;
    DECLARE goalsExists INT;

    -- 验证新的 clubname 是否存在于 Club 表中
    SELECT COUNT(*) INTO clubExists FROM Club WHERE clubname = new_clubname;
    IF clubExists = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'New clubname does not exist';
    END IF;

    -- 验证新的 goals 是否存在于 Data 表中
    SELECT COUNT(*) INTO goalsExists FROM Data WHERE goals = new_goals;
    IF goalsExists = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'New goals value does not exist in Data table';
    END IF;

    -- 更新 Player 表中的 clubname 和 goals
    UPDATE Player
    SET clubname = new_clubname, goals = new_goals
    WHERE name = p_name;
END //

DELIMITER ;
