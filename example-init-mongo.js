db.createUser(
    {
        user: "myapiusername",
        pwd: "myexamplepassword",
        roles: [
            {
                role: "readWrite",
                db: "footyapp"
            }
        ]
    }
);
db.createCollection("games");
db.createCollection("players");
db.createCollection("tenant");