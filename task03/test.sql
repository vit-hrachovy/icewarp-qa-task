CREATE TABLE IF NOT EXISTS PotentialCustomers (
  cust_id INTEGER PRIMARY KEY AUTOINCREMENT,
  cust_name TEXT NOT NULL,
  cust_email TEXT,
  cust_contact_date DATETIME DEFAULT CURRENT_TIMESTAMP,
  cust_no_users INTEGER,
  cust_phone_no INTEGER,
  cust_role TEXT,
  cust_country TEXT
);

INSERT INTO
  PotentialCustomers (cust_name, cust_email, cust_contact_date, cust_no_users, cust_phone_no, cust_role, cust_country)
VALUES
  ('John Doe', 'john@example.com', 1714138048, 10, 123456789, 'IT Manager', 'Czech');
