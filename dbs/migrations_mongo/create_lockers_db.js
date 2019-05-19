db = db.getSiblingDB('lockers')
db.createCollection('lockers', {max: 20})
