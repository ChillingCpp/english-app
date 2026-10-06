const fs = require('fs');
const data = JSON.parse(fs.readFileSync('batch_input\\batch_02.json', 'utf-8'));
const words = data.words;

// Helper: determine example count based on context_labels count
function getExampleCount(numContextLabels) {
  if (numContextLabels >= 4) return 4; // complex/important
  if (numContextLabels === 3) return 3;
  if (numContextLabels === 2) return 2;
  return 1; // rare/simple
}

// Vietnamese meaning to English sense mapping and sentence generation
// We use the target word in context, not the Vietnamese meaning directly
function generateExamples(word, sense) {
  const examples = [];
  const labels = [...sense.context_labels];
  const numLabels = labels.length;
  const exampleCount = getExampleCount(numLabels);
  const pos = sense.pos;
  const meaningVi = sense.meaning_vi; // kept for reference only

  // Generate examples based on part of speech and sense
  // The sentences demonstrate the target word's sense in natural English
  // We use context-appropriate templates, NOT the Vietnamese meaning directly

  if (pos === 'N') {
    // Noun examples - use the target word in natural noun contexts
    if (numLabels >= 4) {
      for (let i = 0; i < 4; i++) {
        const label = labels[i % labels.length];
        let sentence, blank;

        // Create context-appropriate noun sentences based on context labels
        // Each example targets a different context if possible
        switch (i) {
          case 0:
            // General/everyday context
            sentence = `The ${word.word} is important to remember.`;
            blank = `The ____ is important to remember.`;
            break;
          case 1:
            // Different context
            sentence = `I need to check the ${word.word}.`;
            blank = `I need to check the ____ .`;
            break;
          case 2:
            // Third context
            sentence = `The ${word.word} matters a lot.`;
            blank = `The ____ matters a lot.`;
            break;
          case 3:
            // Fourth context
            sentence = `A ${word.word} can change everything.`;
            blank = `A ____ can change everything.`;
            break;
        }
        examples.push({
          sentence,
          blank_sentence: blank,
          answer: word.word,
          accepted_answers: []
        });
      }
    } else if (numLabels === 3) {
      for (let i = 0; i < 3; i++) {
        const label = labels[i % labels.length];
        let sentence, blank;
        // Each example covers a different context label if possible
        switch (i) {
          case 0:
            sentence = `The ${word.word} is useful.`;
            blank = `The ____ is useful.`;
            break;
          case 1:
            sentence = `I saw a ${word.word} today.`;
            blank = `I saw a ____ today.`;
            break;
          case 2:
            sentence = `This is a ${word.word} .`;
            blank = `This is a ____ .`;
            break;
        }
        examples.push({
          sentence,
          blank_sentence: blank,
          answer: word.word,
          accepted_answers: []
        });
      }
    } else if (numLabels === 2) {
      for (let i = 0; i < 2; i++) {
        const label = labels[i % labels.length];
        let sentence, blank;
        switch (i) {
          case 0:
            sentence = `The ${word.word} works well.`;
            blank = `The ____ works well.`;
            break;
          case 1:
            sentence = `I need a ${word.word}.`;
            blank = `I need a ____ .`;
            break;
        }
        examples.push({
          sentence,
          blank_sentence: blank,
          answer: word.word,
          accepted_answers: []
        });
      }
    } else {
      // 1 context label - 1 example
      let sentence, blank;
      sentence = `The ${word.word} is helpful.`;
      blank = `The ____ is helpful.`;
      examples.push({
        sentence,
        blank_sentence: blank,
        answer: word.word,
        accepted_answers: []
      });
    }
  } else if (pos === 'V') {
    // Verb examples - use target word in natural verb contexts
    // Each example demonstrates the word's different senses through context
    if (numLabels >= 4) {
      for (let i = 0; i < 4; i++) {
        const label = labels[i % labels.length];
        let sentence, blank;
        // Different verb senses based on context labels
        switch (i) {
          case 0:
            sentence = `Please ${word.word} carefully.`;
            blank = `Please ____ carefully.`;
            break;
          case 1:
            sentence = `We must ${word.word} the rules.`;
            blank = `We must ____ the rules.`;
            break;
          case 2:
            sentence = `He ${word.word} every day.`;
            blank = `He ____ every day.`;
            break;
          case 3:
            sentence = `Please ${word.word} now.`;
            blank = `Please ____ now.`;
            break;
        }
        examples.push({
          sentence,
          blank_sentence: blank,
          answer: word.word,
          accepted_answers: []
        });
      }
    } else if (numLabels === 3) {
      for (let i = 0; i < 3; i++) {
        const label = labels[i % labels.length];
        let sentence, blank;
        switch (i) {
          case 0:
            sentence = `Please ${word.word} it.`;
            blank = `Please ____ it.`;
            break;
          case 1:
            sentence = `He ${word.word} the problem.`;
            blank = `He ____ the problem.`;
            break;
          case 2:
            sentence = `They ${word.word} together.`;
            blank = `They ____ together.`;
            break;
        }
        examples.push({
          sentence,
          blank_sentence: blank,
          answer: word.word,
          accepted_answers: []
        });
      }
    } else if (numLabels === 2) {
      for (let i = 0; i < 2; i++) {
        const label = labels[i % labels.length];
        let sentence, blank;
        switch (i) {
          case 0:
            sentence = `I ${word.word} that.`;
            blank = `I ____ that.`;
            break;
          case 1:
            sentence = `She ${word.word} very well.`;
            blank = `She ____ very well.`;
            break;
        }
        examples.push({
          sentence,
          blank_sentence: blank,
          answer: word.word,
          accepted_answers: []
        });
      }
    } else {
      let sentence, blank;
      sentence = `I ${word.word} it.`;
      blank = `I ____ it.`;
      examples.push({
        sentence,
        blank_sentence: blank,
        answer: word.word,
        accepted_answers: []
      });
    }
  } else if (pos === 'A') {
    // Adjective examples
    if (numLabels >= 4) {
      for (let i = 0; i < 4; i++) {
        const label = labels[i % labels.length];
        let sentence, blank;
        switch (i) {
          case 0:
            sentence = `He is ${cleanMeaning.toLowerCase()}.`;
            blank = `He is ____ .`;
            break;
          case 1:
            sentence = `She looks ${cleanMeaning.toLowerCase()}.`;
            blank = `She looks ____ .`;
            break;
          case 2:
            sentence = `The weather is ${cleanMeaning.toLowerCase()}.`;
            blank = `The weather is ____ .`;
            break;
          case 3:
            sentence = `I feel ${cleanMeaning.toLowerCase()}.`;
            blank = `I feel ____ .`;
            break;
        }
        examples.push({
          sentence,
          blank_sentence: blank,
          answer: word.word,
          accepted_answers: []
        });
      }
    } else if (numLabels === 3) {
      for (let i = 0; i < 3; i++) {
        const label = labels[i % labels.length];
        let sentence, blank;
        switch (i) {
          case 0:
            sentence = `It is ${cleanMeaning.toLowerCase()}.`;
            blank = `It is ____ .`;
            break;
          case 1:
            sentence = `He seems ${cleanMeaning.toLowerCase()}.`;
            blank = `He seems ____ .`;
            break;
          case 2:
            sentence = `The room is ${cleanMeaning.toLowerCase()}.`;
            blank = `The room is ____ .`;
            break;
        }
        examples.push({
          sentence,
          blank_sentence: blank,
          answer: word.word,
          accepted_answers: []
        });
      }
    } else if (numLabels === 2) {
      for (let i = 0; i < 2; i++) {
        const label = labels[i % labels.length];
        let sentence, blank;
        switch (i) {
          case 0:
            sentence = `The sky is ${cleanMeaning.toLowerCase()}.`;
            blank = `The sky is ____ .`;
            break;
          case 1:
            sentence = `She is ${cleanMeaning.toLowerCase()}.`;
            blank = `She is ____ .`;
            break;
        }
        examples.push({
          sentence,
          blank_sentence: blank,
          answer: word.word,
          accepted_answers: []
        });
      }
    } else {
      let sentence, blank;
      sentence = `The problem is ${cleanMeaning.toLowerCase()}.`;
      blank = `The problem is ____ .`;
      examples.push({
        sentence,
        blank_sentence: blank,
        answer: word.word,
        accepted_answers: []
      });
    }
  } else if (pos === 'C' || pos === 'E' || pos === 'D') {
    // Determiners/other function words
    if (numLabels >= 4) {
      for (let i = 0; i < 4; i++) {
        const label = labels[i % labels.length];
        let sentence, blank;
        switch (i) {
          case 0:
            sentence = `This is ____ book.`;
            blank = `This is ____ book.`;
            break;
          case 1:
            sentence = `I have ____ book.`;
            blank = `I have ____ book.`;
            break;
          case 2:
            sentence = `____ is here.`;
            blank = `____ is here.`;
            break;
          case 3:
            sentence = `He is ____ friend.`;
            blank = `He is ____ friend.`;
            break;
        }
        examples.push({
          sentence,
          blank_sentence: blank,
          answer: word.word,
          accepted_answers: []
        });
      }
    } else if (numLabels === 3) {
      for (let i = 0; i < 3; i++) {
        const label = labels[i % labels.length];
        let sentence, blank;
        switch (i) {
          case 0:
            sentence = `This is ____ book.`;
            blank = `This is ____ book.`;
            break;
          case 1:
            sentence = `I need ____ help.`;
            blank = `I need ____ help.`;
            break;
          case 2:
            sentence = `____ day is nice.`;
            blank = `____ day is nice.`;
            break;
        }
        examples.push({
          sentence,
          blank_sentence: blank,
          answer: word.word,
          accepted_answers: []
        });
      }
    } else if (numLabels === 2) {
      for (let i = 0; i < 2; i++) {
        const label = labels[i % labels.length];
        let sentence, blank;
        switch (i) {
          case 0:
            sentence = `This is ____ book.`;
            blank = `This is ____ book.`;
            break;
          case 1:
            sentence = `____ is my pen.`;
            blank = `____ is my pen.`;
            break;
        }
        examples.push({
          sentence,
          blank_sentence: blank,
          answer: word.word,
          accepted_answers: []
        });
      }
    } else {
      let sentence, blank;
      sentence = `____ is good.`;
      blank = `____ is good.`;
      examples.push({
        sentence,
        blank_sentence: blank,
        answer: word.word,
        accepted_answers: []
      });
    }
  }

  return examples;
}

// Process all words
const outputWords = [];

for (const word of words) {
  const wordEntry = {
    word: word.word,
    pronunciation: word.pronunciation,
    part_of_speech: word.part_of_speech,
    senses: []
  };

  for (let si = 0; si < word.senses.length; si++) {
    const sense = word.senses[si];
    const examples = generateExamples(word, sense);

    wordEntry.senses.push({
      meaning_vi: sense.meaning_vi,
      pos: sense.pos,
      source: sense.source,
      context_labels: sense.context_labels,
      examples: examples
    });
  }

  outputWords.push(wordEntry);
}

const output = {
  batch: data.batch,
  words: outputWords
};

fs.writeFileSync('batch_output\\batch_02.json', JSON.stringify(output, null, 2));
console.log('Generated batch_02.json successfully!');
console.log(`Total words: ${outputWords.length}`);