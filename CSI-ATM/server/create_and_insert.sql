-- 删除已有的表
DROP TABLE IF EXISTS Log;
DROP TABLE IF EXISTS Admin;
DROP TABLE IF EXISTS User;


-- 建表语句
CREATE TABLE IF NOT EXISTS Admin (
  admin_id VARCHAR(32) NOT NULL,
  account char(16) NULL,
  password VARCHAR(32) NULL,
  PRIMARY KEY (admin_id),
  UNIQUE INDEX `account_UNIQUE` (`account` ASC));

CREATE TABLE IF NOT EXISTS User (
  user_id VARCHAR(32) NOT NULL,
  account char(16) NULL,
  password VARCHAR(32) NULL,
  balance INT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `account_UNIQUE` (`account` ASC));

CREATE TABLE IF NOT EXISTS Log(
  Log_id int auto_increment ,
  timestamp TIMESTAMP NULL,
  event VARCHAR(256) NULL,
  object VARCHAR(256) NULL,
  balance INT NULL,
  state TINYINT NULL,
  User_user_id VARCHAR(32) NOT NULL,
  PRIMARY KEY (`Log_id`),
  INDEX fk_Log_User_idx (User_user_id ASC),
  CONSTRAINT fk_Log_User
    FOREIGN KEY (User_user_id)
    REFERENCES User (user_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

-- 插入初始信息
-- Insert statements for the Admin table
-- Insert statements for the Admin table
INSERT INTO Admin (admin_id, account, password) VALUES
('admin1', 1000100110021000, '123456'),
('admin2', 1000100110021001, '123456'),
('admin3', 1000100110021002, '123456'),
('admin4', 1111111111111111, '123456');

-- Insert statements for the User table
INSERT INTO User (user_id, account, password, balance) VALUES
('user1', 2000100110021000, '123456', 1000),
('user2', 2000100110021001, '123456', 2000),
('user3', 2000100110021002, '123456', 3000),
('user4', 2222222222222222, '123456', 4000);

-- Insert statements for the Log table
INSERT INTO Log (Log_id, timestamp, event, object, balance, state, User_user_id) VALUES
('1', '2024-07-03 10:00:00', 'Login', 'user1', 1000, 1, 'user1'),
('2', '2024-07-03 11:00:00', 'Logout', 'user2', 2000, 0, 'user2'),
('3', '2024-07-03 12:00:00', 'Trans', 'user3', 1500, 1, 'user3'),
('4', '2024-07-03 12:00:00', 'Trans', 'user1', 50, 1, 'user1');