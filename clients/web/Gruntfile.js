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
    },
    watch: {
      scripts: {
        files: ['**/*.scss'],
        tasks: ['sass'],
        options: {
          spawn: false,
          livereload: true,
        },
      },
    },
    'http-server': {
       'dev': {
           root: "app",
           port: 8000,
           host: "127.0.0.1",
           showDir : true,
           autoIndex: true,
           ext: "html",
           openBrowser : true
       }
    }
  });

  // Default task(s).
  grunt.registerTask('default', ['sass']);
  grunt.registerTask('start', ['http-server:dev']);
};
