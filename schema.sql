-- Drop tables if they exist (for reset convenience)
DROP TABLE IF EXISTS grievances;
DROP TABLE IF EXISTS departments;

-- Departments Table
CREATE TABLE departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT NOT NULL
);

-- Grievances Table
CREATE TABLE grievances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    citizen_name TEXT NOT NULL,
    contact_number TEXT NOT NULL,
    district TEXT NOT NULL,
    complaint_odia TEXT NOT NULL,
    complaint_english TEXT NOT NULL,
    predicted_department TEXT NOT NULL,
    assigned_department TEXT NOT NULL,
    sentiment TEXT NOT NULL,          -- Negative (Critical), Neutral, Positive
    sentiment_score REAL NOT NULL,     -- Range: -1.0 to 1.0
    status TEXT NOT NULL DEFAULT 'Pending', -- Pending, In Progress, Resolved, Rejected
    resolution_remarks TEXT,
    date_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(predicted_department) REFERENCES departments(name),
    FOREIGN KEY(assigned_department) REFERENCES departments(name)
);
