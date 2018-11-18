'use strict'

// const del = require('del');
const gulp = require('gulp');
const babel = require('gulp-babel');
const runSequence = require('run-sequence');

const sass = require('gulp-sass');
const postcss = require('gulp-postcss');
const concat = require('gulp-concat');
const cssnext = require('postcss-cssnext');
const cleanCSS = require('gulp-clean-css');
const uglify = require('gulp-uglify');

const env = process.env || 'development';
const dist = env.DIST_PATH || '../static/';

// remove files
gulp.task('clean', () => {
  // var path = dist + '';

  // switch (env.NODE_ENV) {
  // case 'development':
  //   del([path + '/bundle-development.js']);
  //   del([path + '/bundle-development.map']);
  //   break
  // default:
  //   del([path + '/bundle.js']);
  //   del([path + '/bundle.map']);
  // }
});

gulp.task('web-images', () => {
  gulp.src([
    './node_modules/datatables/media/images/*',
  ])
  .pipe(gulp.dest(dist + 'images'));
});

gulp.task('web-font', () => {
  gulp.src([
    './node_modules/font-awesome/fonts/*',
    './node_modules/simple-line-icons/fonts/*',
  ])
  .pipe(gulp.dest(dist + 'fonts'));
});

gulp.task('web-flags', () => {
  gulp.src([
    './node_modules/flag-icon-css/flags/*/*'
  ])
  .pipe(gulp.dest(dist + 'flags'));
});

gulp.task('prepared-scss', () => {
  var processors = [
      cssnext()
  ];
  return gulp.src([
    './src/vendor/prepared/**/*.scss',
    './src/prepared/**/*.scss'
  ])
  .pipe(sass({outputStyle: 'expanded'}).on('error', sass.logError))
  .pipe(postcss(processors))
  .pipe(concat('prepared.min.css'))
  .pipe(cleanCSS({level: {1: {specialComments: 0}}}))
  .pipe(gulp.dest(dist + 'css'));
});

gulp.task('vendor-scss', () => {
  var processors = [
      cssnext()
  ];

  gulp.src([
    './node_modules/bootstrap/dist/css/bootstrap.min.css',
    './node_modules/bootswitch/dist/litera/bootstrap.min.css',
    './node_modules/datatables/media/css/jquery.dataTables.min.css',
    './node_modules/dropzone/dist/min/*.css',
    './src/vendor/css/**/*.scss',
    './src/vendor/css/**/*.css',
  ])
  .pipe(sass({outputStyle: 'expanded'}).on('error', sass.logError))
  .pipe(postcss(processors))
  .pipe(concat('vendor.min.css'))
  .pipe(cleanCSS({level: {1: {specialComments: 0}}}))
  .pipe(gulp.dest(dist + 'css'));
});

gulp.task('scss', () => {
  var processors = [
      cssnext()
  ];
  return gulp.src([
    './src/css/**/*.css',
    './src/css/**/*.scss'
  ])
  .pipe(sass({outputStyle: 'expanded'}).on('error', sass.logError))
  .pipe(postcss(processors))
  .pipe(concat('app.min.css'))
  .pipe(cleanCSS({level: {1: {specialComments: 0}}}))
  .pipe(gulp.dest(dist + 'css'));
});

gulp.task('prepared-js', () => {
  gulp.src([
    './node_modules/jquery/dist/jquery.min.js',
    './src/vendor/prepared/**/*.js',
    './src/prepared/**/*.js'
  ])
  .pipe(concat('prepared.min.js'))
  .pipe(uglify())
  .pipe(gulp.dest(dist + 'js'));
});

gulp.task('vendor-js', () => {
  gulp.src([
    './node_modules/bootstrap/dist/js/bootstrap.bundle.min.js',
    './node_modules/dropzone/dist/min/dropzone.min.js',
    './node_modules/datatables/media/js/jquery.dataTables.min.js',
    './src/vendor/js/**/*.js'])
  .pipe(concat('vendor.min.js'))
  .pipe(uglify())
  .pipe(gulp.dest(dist + 'js'));
});

// .on('error', function(e){ console.log(e); })

gulp.task('js', () => {
  gulp.src([
    './src/js/**/*.js'
  ])
  .pipe(concat('app.min.js'))
  .pipe(babel())
  .pipe(uglify())
  .pipe(gulp.dest(dist + 'js'));
});

// watch ts
gulp.task('watch', () => {
  gulp.watch('./src/vendor/prepared/*.js', ['prepared-js'])
  gulp.watch('./src/prepared/*.js', ['prepared-js'])
  gulp.watch('./src/vendor/prepared/*.scss', ['prepared-scss'])
  gulp.watch('./src/prepared/*.scss', ['prepared-scss'])
  gulp.watch('./src/css/**/*.css', ['scss']);
  gulp.watch('./src/css/**/*.scss', ['scss']);
  gulp.watch('./src/js/**/*.js', ['js']);
});

gulp.task('build', (callback) => runSequence('clean', 'prepared-scss', 'vendor-scss', 'scss', 'prepared-js', 'vendor-js', 'js', 'web-images', 'web-flags', 'web-font', callback));
gulp.task('default', (callback) => {
  switch (env.NODE_ENV) {
  case 'production':
    runSequence('clean', 'prepared-scss', 'vendor-scss', 'scss', 'prepared-js', 'vendor-js', 'js', 'web-images', 'web-flags', 'web-font', callback);
    break
  default:
    runSequence('clean', 'prepared-scss', 'vendor-scss', 'scss', 'prepared-js', 'vendor-js', 'js', 'web-images', 'web-flags', 'web-font', 'watch', callback);
  }
});
