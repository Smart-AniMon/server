db.createUser(
        {
            user: "animon_processing",
            pwd: "animonproc",
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
            user: "animon_application",
            pwd: "animonapp",
            roles: [
                {
                    role: "readWrite",
                    db: "animon_db"
                }
            ]
        }
);

