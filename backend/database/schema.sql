-- ============================
-- UIL Archives Database Schema
-- ============================

-- Drop existing tables if they exist (only run this if you want to recreate)
-- DROP TABLE IF EXISTS individual_results;
-- DROP TABLE IF EXISTS team_results;
-- DROP TABLE IF EXISTS contests;
-- DROP TABLE IF EXISTS students;
-- DROP TABLE IF EXISTS schools;
-- DROP TABLE IF EXISTS events;
-- DROP TABLE IF EXISTS levels;
-- DROP TABLE IF EXISTS advancement_status;

-- ============================
-- Lookup Tables
-- ============================

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS advancement_status (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS levels (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS schools (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- ============================
-- Main Data Tables
-- ============================

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    school_id INTEGER NOT NULL,
    FOREIGN KEY (school_id) REFERENCES schools(id),
    UNIQUE(name, school_id)
);

CREATE TABLE IF NOT EXISTS contests (
    id INTEGER PRIMARY KEY,
    year INTEGER NOT NULL,
    level_id INTEGER NOT NULL,
    level_input INTEGER,  -- district/region number, NULL for state
    conference INTEGER NOT NULL,  -- 1-6 for 1A-6A
    event_id INTEGER NOT NULL,
    FOREIGN KEY (level_id) REFERENCES levels(id),
    FOREIGN KEY (event_id) REFERENCES events(id),
    UNIQUE(year, level_id, level_input, conference, event_id)
);

CREATE TABLE IF NOT EXISTS individual_results (
    id INTEGER PRIMARY KEY,
    contest_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    code TEXT,  -- competitor code/number
    placement INTEGER,  -- Changed to INTEGER: 1, 2, 3, etc.
    score INTEGER,  -- Changed to INTEGER
    tiebreaker INTEGER,  -- Changed to INTEGER
    objective_score INTEGER,  -- Changed to INTEGER
    essay_score INTEGER,  -- Changed to INTEGER
    biology_score INTEGER,  -- Changed to INTEGER
    chemistry_score INTEGER,  -- Changed to INTEGER
    physics_score INTEGER,  -- Changed to INTEGER
    points INTEGER,  -- Changed to INTEGER
    advancement_status_id INTEGER,
    FOREIGN KEY (contest_id) REFERENCES contests(id),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (advancement_status_id) REFERENCES advancement_status(id)
);

CREATE TABLE IF NOT EXISTS team_results (
    id INTEGER PRIMARY KEY,
    contest_id INTEGER NOT NULL,
    school_id INTEGER NOT NULL,
    placement INTEGER,  -- Changed to INTEGER: 1, 2, 3, etc.
    student_1_id INTEGER,
    student_2_id INTEGER,
    student_3_id INTEGER,
    student_4_id INTEGER,
    score INTEGER,  -- Changed to INTEGER
    programming_score INTEGER,  -- Changed to INTEGER (for Computer Science)
    points INTEGER,  -- Changed to INTEGER
    advancement_status_id INTEGER,
    FOREIGN KEY (contest_id) REFERENCES contests(id),
    FOREIGN KEY (school_id) REFERENCES schools(id),
    FOREIGN KEY (student_1_id) REFERENCES students(id),
    FOREIGN KEY (student_2_id) REFERENCES students(id),
    FOREIGN KEY (student_3_id) REFERENCES students(id),
    FOREIGN KEY (student_4_id) REFERENCES students(id),
    FOREIGN KEY (advancement_status_id) REFERENCES advancement_status(id)
);

-- ============================
-- Indexes for Performance
-- ============================

CREATE INDEX IF NOT EXISTS idx_individual_results_contest ON individual_results(contest_id);
CREATE INDEX IF NOT EXISTS idx_individual_results_student ON individual_results(student_id);
CREATE INDEX IF NOT EXISTS idx_individual_results_placement ON individual_results(placement);
CREATE INDEX IF NOT EXISTS idx_team_results_contest ON team_results(contest_id);
CREATE INDEX IF NOT EXISTS idx_team_results_school ON team_results(school_id);
CREATE INDEX IF NOT EXISTS idx_team_results_placement ON team_results(placement);
CREATE INDEX IF NOT EXISTS idx_students_school ON students(school_id);
CREATE INDEX IF NOT EXISTS idx_contests_year ON contests(year);
CREATE INDEX IF NOT EXISTS idx_contests_event ON contests(event_id);