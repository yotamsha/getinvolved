/**
 * Run unit tests.
 *
 * ---------------------------------------------------------------
 *
 * This grunt task is configured to run the Mocha unit tests
 *
 * For usage docs see:
 * https://github.com/pghalliday/grunt-mocha-test
 */
module.exports = function(grunt) {

	grunt.config.set('mochaTest', {
    test: {
      options: {
        reporter: 'spec'
      },
      src: ['test/unit/**/*.test.js']
    }
	});

	grunt.loadNpmTasks('grunt-mocha-test');
};
