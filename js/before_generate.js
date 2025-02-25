const fs = require('fs-extra');
const path = require('path');

function copyFolder(source, target) {
  // Create the target folder if it doesn't exist
  fs.ensureDirSync(target);

  // Get the list of files in the source folder
  const files = fs.readdirSync(source);

  // Loop through each file and copy it to the target folder
  files.forEach((file) => {
    const sourcePath = path.join(source, file);
    const targetPath = path.join(target, file);

    if (fs.statSync(sourcePath).isDirectory()) {
      // Recursively copy subfolders
      copyFolder(sourcePath, targetPath);
    } else {
      // Copy the file
      fs.copyFileSync(sourcePath, targetPath);
    }
  });
}

copyFolder('./CDN', './public/.github');
