const mongoose = require("mongoose");

const handleDBConnect = () => {
  console.log("✅ Connected to DB");
};
const handleDBError = error => {
  console.log("❌ DB Error", error);
};

const connect = async () => mongoose
  .connect(
    `mongodb+srv://${process.env.DB_USER}:${process.env.DB_PWD}@${process.env.DB_NAME}.awwmmyt.mongodb.net/?retryWrites=true&w=majority`,
    {
      useNewUrlParser: true,
      dbName: 'caffeine-out'
    },
  )
  .then(handleDBConnect, handleDBError);

module.exports = { connect };
