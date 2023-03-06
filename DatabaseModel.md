'''mermaid
  erDiagram
    entity Employee {
        * EmployeeID
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
        * SkillID
        --
        SkillName
        Description
    }
    entity Occupation {
        * OccupationID
        --
        OccupationName
        Description
    }
    entity Job {
        * JobID
        --
        JobTitle
        Description
        OccupationID
    }
    entity EmployeeSkill {
        * EmployeeID
        * SkillID
        --
        SkillLevel
    }
    entity JobSkill {
        * JobID
        * SkillID
        --
        SkillLevel
    }
    entity DevelopmentPlan {
        * PlanID
        --
        PlanName
        Description
        EmployeeID
    }
    entity PlanSkill {
        * PlanID
        * SkillID
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
    '''
