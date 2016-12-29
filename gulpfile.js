var gulp = require('gulp');
var fs = require('fs');
var filelog = require('gulp-filelog');
var jasmine = require('gulp-jasmine-phantom');
var include = require('gulp-include');
var colours = require('colors');
var uglify = require('gulp-uglify');
var sass = require('gulp-sass');

// Paths
var environment;
var repoRoot = __dirname + '/';
var bowerRoot = __dirname + '/bower_components';
var npmRoot = __dirname + '/node_modules';
var docsAssetsFolder = __dirname + '/docs/assets';
var buildToolsFolder = __dirname + '/build_tools';
var buildToolsAssetsFolder = buildToolsFolder + '/assets';

// Configuration
var sassOptions = {
  outputStyle: 'expanded',
  lineNumbers: true,
  includePaths: [
    buildToolsAssetsFolder + '/scss',
    repoRoot,
    npmRoot,
    npmRoot + '/govuk_frontend_toolkit/stylesheets/'
  ],
  sourceComments: true,
  errLogToConsole: true
};

var uglifyOptions = {
  mangle: false,
  output: {
    beautify: true,
    semicolons: true,
    comments: true,
    indent_level: 2
  },
  compress: false
};

var logErrorAndExit = function logErrorAndExit(err) {
  var printError = function (type, message) {
    console.log('gulp ' + colours.red('ERR! ') + type + ': ' + message);
  };

  printError('message', err.message);
  printError('file name', err.fileName);
  printError('line number', err.lineNumber);
  process.exit(1);

};

function copyFactory(resourceName, sourceFolder, targetFolder) {

  return function() {

    return gulp
      .src(sourceFolder + "/**/*", { base: sourceFolder })
      .pipe(gulp.dest(targetFolder))
      .on('end', function () {
        console.log('📂  Copied ' + resourceName);
      });

  };

}

gulp.task('clean', function (cb) {
  var count = 0;
  var complete = function () {
      count++;
      if (count === 4) {
        console.log('./docs/assets folder recreated');
        cb();
      }
  };

  fs.rmdir(docsAssetsFolder, function () {
    fs.mkdir(docsAssetsFolder, complete);
    fs.mkdir(docsAssetsFolder + '/stylesheets', complete);
    fs.mkdir(docsAssetsFolder + '/javascripts', complete);
    fs.mkdir(docsAssetsFolder + '/images', complete);
  });
});

gulp.task('sass', function () {
  var stream = gulp.src(buildToolsAssetsFolder + '/scss/application.scss')
    .pipe(filelog('Compressing SCSS files'))
    .pipe(
      sass(sassOptions))
        .on('error', logErrorAndExit)
    .pipe(gulp.dest(docsAssetsFolder + '/stylesheets'));

  stream.on('end', function () {
    console.log('💾  Compressed CSS saved as .css files in ' + docsAssetsFolder + '/stylesheets');
  });

  return stream;
});

gulp.task('js', function () {
  var stream = gulp.src(buildToolsAssetsFolder + '/javascripts/application.js')
    .pipe(filelog('Compressing JavaScript files'))
    .pipe(include())
    .pipe(uglify(
      uglifyOptions
    ))
    .pipe(gulp.dest(docsAssetsFolder + '/javascripts'));

  stream.on('end', function () {
    console.log('💾 Compressed JavaScript saved as ' + docsAssetsFolder + '/javascripts/application.js');
  });

  return stream;
})

gulp.task(
  'copy:govuk_template:stylesheets',
  copyFactory(
    "GOVUK Template stylesheets",
    bowerRoot + '/govuk_template/assets/stylesheets',
    docsAssetsFolder + '/stylesheets'
  )
);

gulp.task(
  'copy:govuk_template:javascripts',
  copyFactory(
    "GOVUK Template javascripts",
    bowerRoot + '/govuk_template/assets/javascripts',
    docsAssetsFolder + '/javascripts'
  )
);

gulp.task(
  'copy:govuk_template:images',
  copyFactory(
    "GOVUK Template images",
    bowerRoot + '/govuk_template/assets/images',
    docsAssetsFolder + '/images'
  )
);

gulp.task('test', function () {
  var manifest = require(repoRoot + 'spec/javascripts/manifest.js').manifest;

  manifest.support = manifest.support.map(function (val) {
    return val.replace(/^(\.\.\/)*/, function (match) {
      if (match === '../../../') {
        return '';
      }
      else {
        return 'spec/javascripts/support/'
      }
    });
  });
  manifest.test = manifest.test.map(function (val) {
    return val.replace(/^\.\.\//, 'spec/javascripts/');
  });

  return gulp.src(manifest.test)
    .pipe(jasmine({
      'jasmine': '2.0',
      'integration': true,
      'abortOnFail': true,
      'vendor': manifest.support
    }));
});

gulp.task(
  'copy',
  [
    'copy:govuk_template:stylesheets',
    'copy:govuk_template:javascripts',
    'copy:govuk_template:images'
  ]
);

gulp.task(
  'compile',
  [
    'copy'
  ],
  function() {
    gulp.start('sass');
    gulp.start('js');
  }
);

gulp.task('build:assets', ['clean'], function () {
  gulp.start('compile');
});
