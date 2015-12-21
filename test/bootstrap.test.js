/**
 * Created by yotam on 25/11/2015.
 */
var Barrels = require('barrels');
var Sails = require('sails'),
  sails;

before(function(done) {

  // Increase the Mocha timeout so that Sails has enough time to lift.
  this.timeout(60000);

  Sails.lift({
    // configuration for testing purposes
    log: {
      level: 'error'
    },
    models: {
      connection: 'unitTests',
      migrate: 'drop'
    }
  }, function(err, server) {
    sails = server;
    if (err) return done(err);

    // Load fixtures
    var barrels = new Barrels();

    // Save original objects in `fixtures` variable
    fixtures = barrels.data;

    // Populate the DB
    barrels.populate(function(err) {
      if (!err) {

        console.log("Populated DB for tests.");
      } else {
        console.log("Unable to populate DB for tests.");

      }
      done(err);
    });
   // done(err, sails);
  });
});

after(function(done) {
  // here you can clear fixtures, etc.
  Sails.lower(done);
});
