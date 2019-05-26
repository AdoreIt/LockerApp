var MAX_SIZE = 20;
db = db.getSiblingDB('lockers')
db.createCollection('lockers', {capped: true, size: 100000, max: MAX_SIZE})

var i;
for (i = 0; i < MAX_SIZE; i++) {
    db.lockers.insert({"_id": i, "free": true})
}
