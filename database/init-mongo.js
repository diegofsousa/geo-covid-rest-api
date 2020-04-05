db.createCollection("temporaly_data_user")
db.temporaly_data_user.createIndex( { "createdAt": 1 }, { expireAfterSeconds: 600 } )
db.temporaly_data_user.createIndex( { "validationHashLink": 2 } )

db.createCollection("covid_personal_user")
db.covid_personal_user.createIndex( { "user": 1 } )
