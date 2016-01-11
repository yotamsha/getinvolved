/**
 * Created by Bar Wachtel on 03/12/2015.
 */

module.exports = {
  profileFields: ["id", "name", "email"],
  generateFacebookUsername: _generateFacebookUsername,
  generateRandomString: _generateRandomString,
  getFirstName: _getFirstName,
  getLastName: _getLastName
}

function _generateFacebookUsername(profile) {
  return _getFirstName(profile) + profile.id;
}

function _getFirstName(profile) {
  var firstName = '';
  if (notEmpty(profile.name.givenName)) {
    firstName = profile.name.givenName;
  } else if (notEmpty(profile.displayName)) {
    firstName = profile.displayName.split(' ')[0];
  }
  return firstName;
}

function _getLastName(profile) {
  var lastName = "";
  if (notEmpty(profile.name.familyName)) {
    lastName = profile.name.familyName;
  } else if (notEmpty(profile.displayName)) {
    var names = profile.displayName.split(' ');
    lastName = names[names.length - 1];
  }
  return lastName;
}

function notEmpty(str) {
  return str && str.length > 0;
}

function _generateRandomString(length) {
  length = length ? length : 7;
  // Since password is a required field, but could allow the user to login later
  return Math.random().toString(36).substring(length);
}
