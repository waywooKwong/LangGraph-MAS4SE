
-- 建表语句

CREATE TABLE IF NOT EXISTS Admin (
  admin_id VARCHAR(32) NOT NULL,
  account INT NULL,
  password VARCHAR(32) NULL,
  PRIMARY KEY (admin_id),
  UNIQUE INDEX `account_UNIQUE` (`account` ASC));

CREATE TABLE IF NOT EXISTS User (
  user_id VARCHAR(32) NOT NULL,
  account INT NULL,
  password VARCHAR(32) NULL,
  balance INT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `account_UNIQUE` (`account` ASC));

CREATE TABLE IF NOT EXISTS Log (
  Log_id VARCHAR(32) NOT NULL,
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
INSERT INTO `mydb`.`Admin` (`admin_id`, `account`, `password`) VALUES
('admin1', 101, 'password123'),
('admin2', 102, 'password456'),
('admin3', 103, 'password789');

-- Insert statements for the User table
INSERT INTO `mydb`.`User` (`user_id`, `account`, `password`, `balance`) VALUES
('user1', 201, 'userpass123', 1000),
('user2', 202, 'userpass456', 2000),
('user3', 203, 'userpass789', 3000);

-- Insert statements for the Log table
INSERT INTO `mydb`.`Log` (`Log_id`, `timestamp`, `event`, `object`, `balance`, `state`, `User_user_id`) VALUES
('log1', '2024-07-03 10:00:00', 'Login', 'user1', 1000, 1, 'user1'),
('log2', '2024-07-03 11:00:00', 'Logout', 'user2', 2000, 0, 'user2'),
('log3', '2024-07-03 12:00:00', 'Transaction', 'user3', 1500, 1, 'user3');