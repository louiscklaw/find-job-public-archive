`
// prompt
// D:\_workspace\vercel-louiscklaw-portfolio

// list all subdirectory in D:\_workspace\find-job\jupyter-findjob-tryout\notebook\jobsdb\_output\appium
// create subdirectory based on the result above based on this directory D:\_workspace\vercel-louiscklaw-portfolio\data\CV
// copy index.mdx based on the result above
// copy post.png based on the result above


// list all subdirectory in D:\_workspace\find-job\jupyter-findjob-tryout\notebook\jobsdb\_output\javascript
// create subdirectory based on the result above based on this directory D:\_workspace\vercel-louiscklaw-portfolio\data\CV
// copy index.mdx based on the result above
// copy post.png based on the result above
`;

const fs = require('fs');
const path = require('path');

function copyFiles(sourceDir, destinationDir) {
  try {
    console.log('processing dir: ' + sourceDir);

    // Read all subdirectories in the source directory
    fs.readdir(sourceDir, { withFileTypes: true }, (err, files) => {
      if (err) {
        console.error('error found, skipping... ' + sourceDir);
        return;
      }

      files.forEach(file => {
        if (file.isDirectory()) {
          const sourceSubDir = path.join(sourceDir, file.name);
          const destSubDir = path.join(destinationDir, file.name);

          // Create subdirectory in the destination directory
          fs.mkdir(destSubDir, { recursive: true }, err => {
            if (err) {
              console.error(err);
              return;
            }

            // Copy index.mdx and post.png to the newly created subdirectory
            fs.copyFile(path.join(sourceSubDir, 'index.mdx'), path.join(destSubDir, 'index.mdx'), err => {
              if (err) {
                console.error(err);
              }
            });

            fs.copyFile(path.join(sourceSubDir, 'post.png'), path.join(destSubDir, 'post.png'), err => {
              if (err) {
                console.error(err);
              }
            });
          });
        }
      });
    });
  } catch (error) {
    console.log('error during processing: ' + sourceDir);
  }
}

var SourceDir, DestinationDir;

// For appium subdirectory
const appiumSourceDir = 'D:/_workspace/find-job/jupyter-findjob-tryout/notebook/jobsdb/_output/appium';
const appiumDestinationDir = 'D:/_workspace/vercel-louiscklaw-portfolio/data/CV';
copyFiles(appiumSourceDir, appiumDestinationDir);

// For javascript subdirectory
const javascriptSourceDir = 'D:/_workspace/find-job/jupyter-findjob-tryout/notebook/jobsdb/_output/javascript';
const javascriptDestinationDir = 'D:/_workspace/vercel-louiscklaw-portfolio/data/CV';
copyFiles(javascriptSourceDir, javascriptDestinationDir);

// For javascript subdirectory
SourceDir = 'D:/_workspace/find-job/jupyter-findjob-tryout/notebook/jobsdb/_output/software testing';
DestinationDir = 'D:/_workspace/vercel-louiscklaw-portfolio/data/CV';
copyFiles(SourceDir, DestinationDir);

// For javascript subdirectory
SourceDir = 'D:/_workspace/find-job/jupyter-findjob-tryout/notebook/jobsdb/_output/software validation';
DestinationDir = 'D:/_workspace/vercel-louiscklaw-portfolio/data/CV';
copyFiles(SourceDir, DestinationDir);
