var  Barrels = require('barrels');
var hooks = require('hooks');
var barrels = new Barrels();



hooks.beforeAll(function(transactions) {
  hooks.log("beforeAll");

// Populate the DB
  barrels.populate(['users'],function(err) {
    if (!err){
      hooks.log("Test DB Populated");
    } else {
      hooks.log("Error: Test DB not populated");
    }
    done(err);
  });
});
hooks.log("Start tests hooks..");

hooks.afterEach(function(transaction) {
  hooks.log("afterEach..");

  //db.cleanUp();
});

/*before('Category > Delete a category', function() {
  db.createCategory({id:42});
});

before('Category Items > Create an item', function() {
  db.createCategory({id:42});
});*/
