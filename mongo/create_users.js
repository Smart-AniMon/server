db.createUser(
        {
            user: "user_processing",
            pwd: "pass_processing",
            roles: [
                {
                    role: "readWrite",
                    db: "animon_db"
                }
            ]
        }
);

db.createUser(
        {
            user: "user_application",
            pwd: "pass_application",
            roles: [
                {
                    role: "readWrite",
                    db: "animon_db"
                }
            ]
        }
);