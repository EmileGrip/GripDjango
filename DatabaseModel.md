```mermaid
  erDiagram
    entity Employee {
        EmployeeID PK
        --
        FirstName
        LastName
        Email
        Phone
        Title
        Department
        ManagerID
    }
    entity Skill {
        SkillID PK
        --
        SkillName
        Description
    }
    entity Occupation {
        OccupationID PK
        --
        OccupationName
        Description
    }
    entity Job {
        JobID PK
        --
        JobTitle
        Description
        OccupationID
    }
    entity EmployeeSkill {
        EmployeeID PK
        SkillID PK
        --
        SkillLevel
    }
    entity JobSkill {
        JobID PK
        SkillID PK
        --
        SkillLevel
    }
    entity DevelopmentPlan {
        PlanID PK
        --
        PlanName
        Description
        EmployeeID
    }
    entity PlanSkill {
        PlanID PK
        SkillID PK
        --
        SkillLevel
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
