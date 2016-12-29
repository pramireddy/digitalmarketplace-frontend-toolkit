var gulp = require('gulp');
var fs = require('fs');
var jasmine = require('gulp-jasmine-phantom');

// Paths
var environment;
var repoRoot = __dirname + '/';
var bowerRoot = __dirname + '/bower_components';
var docsAssetsFolder = __dirname + '/docs/assets';
var buildToolsFolder = __dirname + '/build_tools';

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
  function() {}
);

gulp.task('build:assets', ['clean'], function () {
  gulp.start('compile');
});
