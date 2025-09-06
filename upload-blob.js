const { put } = require('@vercel/blob');
const fs = require('fs');
const path = require('path');

async function uploadFile() {
  const filePath = path.join(__dirname, 'psychologist_responses_10k.json');
  const fileContent = fs.readFileSync(filePath, 'utf-8');
  
  const blob = await put('psychologist_responses_10k.json', fileContent, {
    access: 'public',
  });

  console.log('File uploaded successfully!');
  console.log('URL:', blob.url);
  return blob.url;
}

uploadFile().catch(console.error);