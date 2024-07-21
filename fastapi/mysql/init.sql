-- 모든 호스트에서 root 사용자에게 접근 권한 부여
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '${MYSQL_ROOT_PASSWORD}' WITH GRANT OPTION;

-- 권한 적용
FLUSH PRIVILEGES;

-- 문자 인코딩 설정
SET NAMES 'utf8mb4';

-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS email_db;

-- 데이터베이스 사용
USE email_db;

-- 테이블 생성
CREATE TABLE IF NOT EXISTS emails (
  id INT AUTO_INCREMENT PRIMARY KEY,
  subject VARCHAR(255) NOT NULL,
  body TEXT NOT NULL,
  recipient_email VARCHAR(255) NOT NULL,
  sender_email VARCHAR(255) NOT NULL,
  file_name VARCHAR(255),
  sent_at DATETIME NOT NULL
);
