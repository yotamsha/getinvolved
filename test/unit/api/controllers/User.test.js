/**
 * Created by yotam on 19/12/2015.
 */
var request = require('supertest');
//var should = require('should');
var helpers = require('./../../../testHelpers');
describe('UserController >>> ', function() {
  beforeEach(function(){

  });
  describe('Get All users >>> ', function() {
    it('should return success with a non empty array', function (done) {
      request(sails.hooks.http.app)
        .get('/user')
        .expect(200)
        .expect(helpers.bodyHasData)
        .end(done)

    });
  });
  describe('Get User by id >>> ', function() {
    it('should return success with a user >>> ', function (done) {
      request(sails.hooks.http.app)
        .get('/user/1')
        .expect(200)
        .expect(function(res){
          res.body.should.have.properties({
            "name": "Walter White",
            "email": "walter@heisenberg.com"
          })
        })
        .end(done)

    });
  });
  describe('Create a new user >>> ', function() {
    it('should return success with the created user.', function (done) {
      request(sails.hooks.http.app)
        .post('/user')
        .send({ name: 'Grant Hill', email : 'grant.hill@gmail.com', password : 123456})

        .expect(201)
        .expect(function(res){
          res.body.should.have.properties({
            "name": "Grant Hill",
            "email": "grant.hill@gmail.com"
          })
        })
        .end(done)
    });
    it('should not allow same email twice', function (done) {
      request(sails.hooks.http.app)
        .post('/user')
        .send({ name: 'Grant Hill', email : 'grant.hill@gmail.com', password : 123456})
        .expect(400)
        .end(done);
    });
    describe('fields validations >>> ', function () {
      describe('should fail to create user without mandatory fields >>> ', function () {

        it('No email field.', function (done) {
          request(sails.hooks.http.app)
            .post('/user')
            .send({ password : 123456})

            .expect(400)
            .end(done);
        });
        it('No password field', function (done) {
          request(sails.hooks.http.app)
            .post('/user')
            .send({ email : 'John.Stockton@gmail.com'})

            .expect(400)
            .end(done);
        });

      });
      describe('password field >>> ', function () {

        it('have at least 6 characters', function (done) {
          request(sails.hooks.http.app)
            .post('/user')
            .send({ name: 'Karl Malone', email : 'Karl.Malone@gmail.com', password : 12345})

            .expect(400)
            .end(done);
        });

      });

      describe('email field >>> ', function () {

        it('should be a valid email', function (done) {
          request(sails.hooks.http.app)
            .post('/user')
            .send({ name: 'Kareem Abdul Jabar', email : 'Karrem@@@gmail.com', password : 123456})

            .expect(400)
/*            .expect(function(res){
              res.body.should.have.properties({
                "error" : "SOME_ERROR"
              })
            })*/
            .end(done);
        });

      });

    });
  });
  describe('Update a user >>> ', function() {
    it('should return success with the updated user', function (done) {
      request(sails.hooks.http.app)
        .put('/user/1')
        .send({ name: 'George'})

        .expect(200)
        .expect(function(res){
          res.body.should.have.properties({
            id : 1,
            name: "George"
          })
        })
        .end(done)
    });
    it('should not allow same email twice', function (done) {
      request(sails.hooks.http.app)
        .put('/user/1')
        .send({ email : 'grant.hill@gmail.com'})
        .expect(400)
        .end(done);
    });
    it('should return error for non existing id', function (done) {
      request(sails.hooks.http.app)
        .put('/user/1000000')
        .send({ email : 'grant.hill123@gmail.com'})
        .expect(404)
        .end(done);
    });
    describe('fields validations >>> ', function () {
      describe('should fail to update user to invalid values >>> ', function () {

        it('bad email field', function (done) {
          request(sails.hooks.http.app)
            .put('/user/1')
            .send({ email : "bad_email"})

            .expect(400)
            .end(done);
        });
        it('Null email field', function (done) {
          request(sails.hooks.http.app)
            .put('/user/1')
            .send({ email : null})

            .expect(400)
            .end(done);
        });

      });
    });
  });
  describe('Delete a user >>> ', function() {
    it('should return success with the deleted user id', function (done) {
      request(sails.hooks.http.app)
        .delete('/user/1')
        .expect(200)
        .expect(function(res){
          res.body.should.have.properties({
            id : 1
          })
        })
        .end(done)
    });

    it('should return an error for a non existing id', function (done) {
      request(sails.hooks.http.app)
        .delete('/user/-100')
        .expect(404)
        .end(done)
    });
  });
});
