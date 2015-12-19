/**
 * Created by yotam on 19/12/2015.
 */
module.exports = {
  bodyHasData: function (res) {
    res.body.should.not.be.empty();
  }
};
