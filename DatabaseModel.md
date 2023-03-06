```mermaid
erDiagram
    Employee {
        PK EmployeeID
        FirstName
        LastName
        Email
        Phone
        Title
        Department
        FK ManagerID -> Employee.EmployeeID
    }
    Skill {
        PK SkillID
        SkillName
        Description
    }
    Occupation {
        PK OccupationID
        OccupationName
        Description
    }
    Job {
        PK JobID
        JobTitle
        Description
        FK OccupationID -> Occupation.OccupationID
    }
    EmployeeSkill {
        PK EmployeeID, SkillID
        SkillLevel
        FK EmployeeID -> Employee.EmployeeID
        FK SkillID -> Skill.SkillID
    }
    JobSkill {
        PK JobID, SkillID
        SkillLevel
        FK JobID -> Job.JobID
        FK SkillID -> Skill.SkillID
    }
    DevelopmentPlan {
        PK PlanID
        PlanName
        Description
        FK EmployeeID -> Employee.EmployeeID
    }
    PlanSkill {
        PK PlanID, SkillID
        SkillLevel
        FK PlanID -> DevelopmentPlan.PlanID
        FK SkillID -> Skill.SkillID
    }
    
    Employee ||--o{ EmployeeSkill : Has
    Employee ||--o{ DevelopmentPlan : Has
    DevelopmentPlan ||--o{ PlanSkill : Includes
    Occupation ||--o{ Job : Has
    Job ||--o{ JobSkill : Requires
    Skill ||--o{ JobSkill : Has
    Skill ||--o{ EmployeeSkill : Has
    Skill ||--o{ PlanSkill : Has
```
