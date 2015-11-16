/**
 * Created by Bar Wachtel on 24/09/2015.
 */
// Just a temp logger - winston is a good candidate...

var logger = {
    log: function(msg) {
        console.log(msg);
    },
    error: function(error) {
        console.error(error);
    }
}

module.exports = logger;