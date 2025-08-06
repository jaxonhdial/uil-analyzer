-- Schools table
CREATE TABLE schools (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Events table
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Levels lookup table
CREATE TABLE levels (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Advancement status lookup table
CREATE TABLE advancement_status (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Contests table
CREATE TABLE contests (
    id INTEGER PRIMARY KEY,
    year INTEGER NOT NULL,
    level_id INTEGER NOT NULL,
    level_input INTEGER NOT NULL,
    conference INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    FOREIGN KEY (level_id) REFERENCES levels(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);

-- Students table
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    school_id INTEGER NOT NULL,
    FOREIGN KEY (school_id) REFERENCES schools(id)
);

-- Individual results table
CREATE TABLE individual_results (
    id INTEGER PRIMARY KEY,
    contest_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    code TEXT,
    placement INTEGER,
    score REAL,
    tiebreaker REAL,
    objective_score REAL,
    essay_score REAL,
    biology_score REAL,
    chemistry_score REAL,
    physics_score REAL,
    points INTEGER,
    advancement_status_id INTEGER,
    FOREIGN KEY (contest_id) REFERENCES contests(id),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (advancement_status_id) REFERENCES advancement_status(id)
);

-- Team results table
CREATE TABLE team_results (
    id INTEGER PRIMARY KEY,
    contest_id INTEGER NOT NULL,
    school_id INTEGER NOT NULL,
    placement INTEGER,
    student_1_id INTEGER,
    student_2_id INTEGER,
    student_3_id INTEGER,
    student_4_id INTEGER,
    score REAL,
    programming_score REAL,
    points INTEGER,
    advancement_status_id INTEGER,
    FOREIGN KEY (contest_id) REFERENCES contests(id),
    FOREIGN KEY (school_id) REFERENCES schools(id),
    FOREIGN KEY (student_1_id) REFERENCES students(id),
    FOREIGN KEY (student_2_id) REFERENCES students(id),
    FOREIGN KEY (student_3_id) REFERENCES students(id),
    FOREIGN KEY (student_4_id) REFERENCES students(id),
    FOREIGN KEY (advancement_status_id) REFERENCES advancement_status(id)
);

-- Indexes for performance
CREATE INDEX idx_contests_event ON contests(event_id);
CREATE INDEX idx_contests_year ON contests(year);
CREATE INDEX idx_contests_level ON contests(level_id);
CREATE INDEX idx_results_contest_id ON individual_results(contest_id);
CREATE INDEX idx_results_student_id ON individual_results(student_id);
CREATE INDEX idx_results_advancement ON individual_results(advancement_status_id);
CREATE INDEX idx_team_results_contest_id ON team_results(contest_id);
CREATE INDEX idx_team_results_advancement ON team_results(advancement_status_id);
