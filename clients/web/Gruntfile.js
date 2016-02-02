module.exports = function(grunt) {
  require('load-grunt-tasks')(grunt);

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    sass: {
        options: {
            sourceMap: true
        },
         dist: {
           files: [
              {src: 'app/assets/css/app.scss', dest: 'app/assets/css/app.css'},
            ],
         }
    }
  });

  // Default task(s).
  grunt.registerTask('default', ['sass']);

};
