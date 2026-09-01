# Data Relationships Specification

This document defines the schema architecture, primary keys, foreign keys, join relationships, and entity relationships across the Enterprise HR AI Workforce Intelligence Platform.

## 1. Entity Relationship Diagram

```
                 +-------------------------------+
                 |  EMPLOYEE ATTRITION MASTER    |
                 |  (employee_attrition.csv)     |
                 |  PK: EmployeeID               |
                 +---------------+---------------+
                                 |
         +-----------------------+-----------------------+
         | 1:1                                           | 1:N
         v                                               v
+-------------------------------+               +-------------------------------+
|  PERFORMANCE & ENGAGEMENT     |               |  EMPLOYEE CURRENT SKILLS      |
|  (hr_performance_engagement)  |               |  (employee_skills.csv)        |
|  FK: EmployeeID               |               |  FK: EmployeeID               |
+-------------------------------+               +---------------+---------------+
                                                                |
                                                                | N:1
                                                                v
                                                +-------------------------------+
                                                |  ROLE REQUIRED SKILLS         |
                                                |  (role_skills.csv)            |
                                                |  FK: Role -> JobRole          |
                                                +---------------+---------------+
                                                                |
                                                                | N:1
                                                                v
                                                +-------------------------------+
                                                |  UPSKILLING COURSES CATALOG   |
                                                |  (courses.csv)                |
                                                |  Key: TargetSkill -> Skill    |
                                                +-------------------------------+
```

## 2. Table Join Specifications

| Left Table | Right Table | Join Key | Cardinality | Business Purpose |
| :--- | :--- | :--- | :--- | :--- |
| `employee_attrition` | `hr_performance_engagement` | `EmployeeID` = `Employee ID` | 1-to-1 | Combines demographic & compensation data with performance and engagement metrics. |
| `employee_attrition` | `employee_skills` | `EmployeeID` | 1-to-Many | Links employee master profile to their verified skill inventory. |
| `employee_attrition` | `role_skills` | `JobRole` = `Role` | Many-to-Many | Compares employee assigned role against baseline essential & software skill requirements. |
| `role_skills` (Gaps) | `courses` | `MissingSkill` = `TargetSkill` | 1-to-Many | Recommends curated upskilling courses to close detected individual skill gaps. |
| `employee_attrition` | `occupation_data` | `JobRole` ~ `Title` | Many-to-1 | Standardizes internal titles against official O*NET-SOC occupation standards. |
| `occupation_data` | `onet_essential_skills_processed` | `O*NET-SOC Code` | 1-to-Many | Maps occupations to standardized core cognitive & technical skill elements with Importance & Level scores. |
| `occupation_data` | `onet_software_skills_processed` | `O*NET-SOC Code` | 1-to-Many | Maps occupations to workplace software tools, Hot Technologies, and In-Demand skills. |

## 3. Key Data Invariants & Validation Rules
- `EmployeeID`: Unique non-null integer.
- `Age`: Integer in range `[18, 100]`.
- `EngagementScore`: Numeric score in range `[0, 100]`.
- `AttritionRisk`: Categorical `Yes` / `No` (for ground truth) and probability `[0.0, 1.0]`.
- `Skill Gaps`: Computed as $RequiredSkills_{Role} \setminus EmployeeSkills_{EmployeeID}$.
