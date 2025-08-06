# Database Schema

This section describes the structure of the SQLite database used for storing UIL competition results. The design is normalized for clarity and efficiency, enabling flexible querying of individual and team results across multiple years, events, and competition levels. Note that the Database isn't stored on GitHub.

---

## Tables Overview

### 1. **schools**
Stores information about schools participating in UIL competitions.

- **Columns:**
  - `id` (INTEGER, PRIMARY KEY): Unique identifier for each school.
  - `name` (TEXT, UNIQUE, NOT NULL): Official name of the school.

---

### 2. **students**
Stores individual students participating in competitions.

- **Columns:**
  - `id` (INTEGER, PRIMARY KEY): Unique identifier for each student.
  - `name` (TEXT, NOT NULL): Full name of the student.
  - `school_id` (INTEGER, NOT NULL): Foreign key referencing `schools(id)`.

- **Notes:**
  - Students are linked to schools by `school_id`.
  - Duplicate names are allowed; students are uniquely identified by `id`.

---

### 3. **events**
Defines UIL competition events.

- **Columns:**
  - `id` (INTEGER, PRIMARY KEY): Unique event identifier.
  - `name` (TEXT, UNIQUE, NOT NULL): Name of the event (e.g., "Computer Science").

---

### 4. **levels**
Specifies competition levels.

- **Columns:**
  - `id` (INTEGER, PRIMARY KEY): Unique level identifier.
  - `name` (TEXT, UNIQUE, NOT NULL): Level name (e.g., "district", "region", "state").

---

### 5. **advancement_status**
Tracks advancement status for competitors.

- **Columns:**
  - `id` (INTEGER, PRIMARY KEY): Unique status identifier.
  - `name` (TEXT, UNIQUE, NOT NULL): Advancement stage (e.g., "Region", "State", "Alternate", or blank if no advancement).

---

### 6. **contests**
Represents specific contests held in a given year, level, conference, and event.

- **Columns:**
  - `id` (INTEGER, PRIMARY KEY): Unique contest identifier.
  - `year` (INTEGER, NOT NULL): Year of the contest (e.g., 2024).
  - `level_id` (INTEGER, NOT NULL): Foreign key referencing `levels(id)`.
  - `level_input` (INTEGER, NOT NULL): Specific level input number (e.g., district number, 1 for single state contest).
  - `conference` (INTEGER, NOT NULL): UIL conference number (e.g., 5 for 5A).
  - `event_id` (INTEGER, NOT NULL): Foreign key referencing `events(id)`.

---

### 7. **individual_results**
Stores results for individual students in contests.

- **Columns:**
  - `id` (INTEGER, PRIMARY KEY): Unique result identifier.
  - `contest_id` (INTEGER, NOT NULL): Foreign key referencing `contests(id)`.
  - `student_id` (INTEGER, NOT NULL): Foreign key referencing `students(id)`.
  - `code` (TEXT, NOT NULL): Entry code (e.g., "5A-02").
  - `placement` (INTEGER, NOT NULL): Placement ranking (e.g., 1 for 1st place).
  - `score` (REAL): Numeric score achieved.
  - `points` (REAL): Points awarded.
  - `advancement_status_id` (INTEGER, NOT NULL): Foreign key referencing `advancement_status(id)`.

---

### 8. **team_results**
Stores results for teams in contests.

- **Columns:**
  - `id` (INTEGER, PRIMARY KEY): Unique team result identifier.
  - `contest_id` (INTEGER, NOT NULL): Foreign key referencing `contests(id)`.
  - `school_id` (INTEGER, NOT NULL): Foreign key referencing `schools(id)`.
  - `placement` (INTEGER, NOT NULL): Team placement ranking.
  - `student_1_id` (INTEGER): Foreign key referencing `students(id)` (optional team member).
  - `student_2_id` (INTEGER): Foreign key referencing `students(id)` (optional team member).
  - `student_3_id` (INTEGER): Foreign key referencing `students(id)` (optional team member).
  - `student_4_id` (INTEGER): Foreign key referencing `students(id)` (optional team member).
  - `score` (REAL): Team score.
  - `points` (REAL): Points awarded to team.
  - `advancement_status_id` (INTEGER, NOT NULL): Foreign key referencing `advancement_status(id)`.

---

## Relationships and Integrity

- Foreign keys ensure data integrity between related tables (e.g., each `individual_result` must link to an existing student and contest).
- The schema enforces uniqueness where appropriate (e.g., unique school names, event names).
- Lookup tables like `levels`, `events`, and `advancement_status` prevent redundant text data in large result tables, improving consistency and query performance.

---

## Indexes

Indexes are created on frequently queried columns like:

- `students.school_id`
- `contests.year`
- `contests.level_id`
- `contests.conference`
- `contests.event_id`
- `individual_results.contest_id`
- `team_results.contest_id`

These improve query speed when filtering or joining.

---

## Extensibility

The schema is designed to be extensible for future features such as:

- Adding new events or levels without schema changes. (Non-Academic Events will sometimes have Zone, Bi-District, and Area)
- Expanding team sizes if needed.
- Adding more detailed scoring breakdowns (e.g., multiple scores per result).
- Handling school realignments by linking contests to specific years.

---