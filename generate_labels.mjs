import fs from 'fs';

const data = JSON.parse(fs.readFileSync('ctx_input/chunk_08.json', 'utf-8'));

const commonLabels = [
  'general', 'daily life', 'social', 'time', 'feelings', 'emotions', 'personality',
  'appearance', 'clothing', 'body', 'health', 'medicine', 'exercise', 'sleep',
  'education', 'work', 'career', 'business', 'finance', 'economy', 'money',
  'shopping', 'technology', 'programming', 'internet', 'media', 'communication',
  'travel', 'transportation', 'food', 'cooking', 'restaurant', 'family',
  'friendship', 'relationships', 'marriage', 'home', 'animals', 'plants', 'nature',
  'environment', 'weather', 'government', 'law', 'politics', 'crime', 'safety',
  'military', 'science', 'industry', 'mining', 'construction', 'engineering',
  'farming', 'sports', 'entertainment', 'arts', 'music', 'literature', 'photography',
  'design', 'history', 'geography', 'culture', 'religion', 'philosophy', 'psychology',
  'success', 'management', 'teamwork', 'competition', 'holiday', 'leisure', 'hobby',
  'tourism', 'urban', 'rural', 'formal', 'informal'
];

function assignLabels(meaning, word, meaningIndex) {
  const m = meaning.toLowerCase();
  let labels = [];
  
  // Assign labels based on meaning content analysis
  // Check for various keywords and map to appropriate context labels
  
  // === Geography, science, academic ===
  if (m.includes('khoa') || m.includes('học') || m.includes('học thuật') || m.includes('học tập')) {
    labels.push('education');
  }
  if (m.includes('địa lý') || m.includes('địa')) {
    labels.push('geography');
  }
  if (m.includes('khoa học') || m.includes('science')) {
    labels.push('science');
  }
  
  // === Family, home, relationships ===
  if (m.includes('gia đình') || m.includes('nuclear') || m.includes('family')) {
    labels.push('family');
  }
  if (m.includes('nhà') || m.includes('căn nhà') || m.includes('home')) {
    labels.push('home');
  }
  if (m.includes('ông bà') || m.includes('ông nội') || m.includes('bà nội') || m.includes('bà ngoại')) {
    labels.push('family');
  }
  if (m.includes('chị​y') || m.includes('cháu')) {
    labels.push('family');
  }
  
  // === Social, people, status ===
  if (m.includes('hào hoa') || m.includes('phong nhã') || m.includes('thượng lưu') || m.includes('quý phái')) {
    labels.push('social');
  }
  if (m.includes('người') || m.includes('người')) {
    // General person reference - could be social but let's be more specific
  }
  if (m.includes('cầm') || m.includes('quản trị')) {
    labels.push('work');
  }
  
  // === Money, finance, economy ===
  if (m.includes('tiền') || m.includes('tài') || m.includes('thu nhập') || m.includes('cân') || m.includes(' giàu')) {
    labels.push('finance');
  }
  if (m.includes('mua') || m.includes('mua hàng') || m.includes('shopping')) {
    labels.push('shopping');
  }
  if (m.includes('công việc') || m.includes('làm')) {
    labels.push('work');
  }
  
  // === Health, body ===
  if (m.includes('sức khỏe') || m.includes('sức khoẻ') || m.includes('thể chất')) {
    labels.push('health');
  }
  if (m.includes('bệnh') || m.includes('y tá')) {
    labels.push('medicine');
  }
  if (m.includes('tóc') || m.includes('lông') || m.includes('thân')) {
    labels.push('body');
  }
  
  // === Emotions, feelings ===
  if (m.includes('vui') || m.includes('hạnh phúc') || m.includes('sướng') || m.includes('mood')) {
    labels.push('feelings');
  }
  if (m.includes('cãm') || m.includes('ghét') || m.includes('thù')) {
    labels.push('emotions');
  }
  if (m.includes('sợ') || m.includes('ngại') || m.includes('lo âu')) {
    labels.push('emotions');
  }
  
  // === Time, movement ===
  if (m.includes('thời gian') || m.includes('giờ') || m.includes('lúc')) {
    labels.push('time');
  }
  if (m.includes('đi') || m.includes('đến') || m.includes('đang') || m.includes('chuyến')) {
    // Movement but need to be more specific
  }
  if (m.includes('bắt đầu') || m.includes('kết thúc') || m.includes('hoàn thành')) {
    labels.push('time');
  }
  
  // === Food, cooking ===
  if (m.includes('ăn') || m.includes('nấu') || m.includes('thức ăn') || m.includes('recipe')) {
    labels.push('food');
  }
  
  // === Travel, transportation ===
  if (m.includes('máy bay') || m.includes('hàng không') || m.includes('bay')) {
    labels.push('travel');
  }
  if (m.includes('đường') || m.includes('xe') || m.includes('lái')) {
    labels.push('transportation');
  }
  
  // === Work, career ===
  if (m.includes('việc làm') || m.includes('công việc') || m.includes('làm việc')) {
    labels.push('work');
  }
  if (m.includes('carrer') || m.includes('nghề')) {
    labels.push('career');
  }
  
  // === Technology, internet ===
  if (m.includes('mạng') || m.includes('internet') || m.includes('công nghệ') || m.includes('ứng dụng')) {
    labels.push('technology');
  }
  
  // === Entertainment, arts ===
  if (m.includes('âm nhạc') || m.includes('cạnh tác') || m.includes('hát') || m.includes('view')) {
    labels.push('entertainment');
  }
  if (m.includes('đồ họa') || m.includes('thiết kế')) {
    labels.push('design');
  }
  
  // === Nature, animals ===
  if (m.includes('cây') || m.includes('cỏ') || m.includes('trái')) {
    labels.push('nature');
  }
  if (m.includes('chó') || m.includes('mèo') || m.includes('con vật')) {
    labels.push('animals');
  }
  
  // === Government, law, politics ===
  if (m.includes('chính phủ') || m.includes('chính quyền') || m.includes('quản lý')) {
    labels.push('government');
  }
  if (m.includes('luật') || m.includes('pháp')) {
    labels.push('law');
  }
  if (m.includes('chính trị') || m.includes('chủ tịch')) {
    labels.push('politics');
  }
  
  // === Culture, religion ===
  if (m.includes('văn hóa') || m.includes('truyền thống')) {
    labels.push('culture');
  }
  if (m.includes('tôn giáo') || m.includes('thánh') || m.includes('linh')) {
    labels.push('religion');
  }
  
  // === If no specific labels assigned, use 'general'
  if (labels.length === 0) {
    labels.push('general');
  }
  
  // Limit to max 4 labels, and ensure at least 1
  return labels.slice(0, 4);
}

// Process each word and meaning
const outputLines = [];

for (const item of data) {
  const word = item.word;
  const meanings = item.meanings;
  
  for (let i = 0; i < meanings.length; i++) {
    const meaningIndex = i + 1; // 1-based
    const meaning = meanings[i];
    const labels = assignLabels(meaning, word, meaningIndex);
    
    const line = word + '\t' + meaningIndex + '\t' + labels.join(', ');
    outputLines.push(line);
  }
}

// Write output
const output = outputLines.join('\n');
fs.writeFileSync('ctx_parts/run3/chunk_08.txt', output + '\n');
console.log('Output written. Lines:', outputLines.length);

// Verify line count
if (outputLines.length === 1113) {
  console.log('Line count matches expected 1113 meanings!');
} else {
  console.log(`Line count: ${outputLines.length}, expected: 1113`);
  console.log(`Difference: ${1113 - outputLines.length}`);
}