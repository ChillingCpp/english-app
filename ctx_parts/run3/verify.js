const fs = require('fs');
const input = JSON.parse(fs.readFileSync('E:\\vibe_coding\\english-app\\ctx_input\\chunk_23.json', 'utf8'));
const output = fs.readFileSync('E:\\vibe_coding\\english-app\\ctx_parts\\run3\\chunk_23.txt', 'utf8');
const lines = output.trim().split('\n');

let totalMeanings = 0;
let totalWords = input.length;
for (const item of input) {
  totalMeanings += item.meanings.length;
}

console.log(`Words: ${totalWords}, Meanings: ${totalMeanings}, Lines: ${lines.length}`);

// Verify each line has correct format
let errors = [];
for (let i = 0; i < lines.length; i++) {
  const parts = lines[i].split('\t');
  if (parts.length !== 3) {
    errors.push(`Line ${i+1}: expected 3 tab-separated columns, got ${parts.length}`);
  }
  if (isNaN(parseInt(parts[1]))) {
    errors.push(`Line ${i+1}: meaning index is not a number`);
  }
}

// Check all words and meanings are covered
let idx = 0;
for (const item of input) {
  for (let m = 0; m < item.meanings.length; m++) {
    const parts = lines[idx].split('\t');
    if (parts[0] !== item.word) {
      errors.push(`Line ${idx+1}: expected word "${item.word}", got "${parts[0]}"`);
    }
    if (parseInt(parts[1]) !== m + 1) {
      errors.push(`Line ${idx+1}: expected meaning index ${m+1}, got ${parts[1]}`);
    }
    idx++;
  }
}

if (errors.length > 0) {
  console.log('ERRORS:');
  errors.forEach(e => console.log(e));
} else {
  console.log('All checks passed!');
}