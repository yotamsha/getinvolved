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
           host: "getinvolved.org.il",
           showDir : true,
           autoIndex: true,
           ext: "html",
           openBrowser : true
       }
    },
	shell:{
		startApiServer:{
			command: 'python -m org.gi.server.server --mode dev',
			options: {
                execOptions: {
                    cwd: '../../server'
                }
            }
		}	
	},
	concurrent: {
        all: ['http-server:dev', 'shell:startApiServer', 'watch'],
		withoutApi: ['http-server:dev', 'watch'],
		options: {
			logConcurrentOutput: true
		}
    }
  });

  // Default task(s).
  grunt.registerTask('default', ['sass', 'concurrent:withoutApi']);
  grunt.registerTask('with-server', ['sass','concurrent:all']);
};
