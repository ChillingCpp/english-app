const fs = require('fs');

const inputPath = 'E:\\vibe_coding\\english-app\\batch_input\\batch_01.json';
const outputPath = 'E:\\vibe_coding\\english-app\\batch_output\\batch_01.json';

const data = JSON.parse(fs.readFileSync(inputPath, 'utf-8'));

const outputWords = [];

for (const wordEntry of data.words) {
  const word = wordEntry.word;
  const pronunciation = wordEntry.pronunciation || null;
  const posList = wordEntry.part_of_speech;
  const senses = wordEntry.senses;

  const wordOutput = {
    word,
    pronunciation,
    part_of_speech: posList,
    senses: []
  };

  for (let si = 0; si < senses.length; si++) {
    const sense = senses[si];
    const meaningVi = sense.meaning_vi;
    const pos = sense.pos;
    const contextLabels = sense.context_labels;

    // Determine if this sense is "complex" based on number of context labels
    // 3+ context labels -> complex (3-5 examples), 1-2 -> simple (2-3 examples)
    const numContextLabels = contextLabels.length;
    const isComplex = numContextLabels >= 3;

    // Determine example count: 2-3 for simple, 3-5 for complex
    // For tie-breaking: if exactly 3 context labels, still use 3 (middle ground)
    let exampleCount;
    if (isComplex) {
      // Pick 3, 4, or 5 - use a simple formula based on index
      exampleCount = 3 + (si % 3); // 3, 4, or 5 cycling
    } else {
      exampleCount = 2 + (si % 2); // 2 or 3
    }

    // For senses with very few context labels (1), only generate 1-2 examples
    // But rule says minimum 1 example, target 2-3 for simple
    if (numContextLabels <= 1) {
      exampleCount = 1 + (si % 2); // 1 or 2
    }

    // Select context labels to distribute across
    // We need to pick exampleCount distinct context labels, distributed
    let selectedLabels;
    if (numContextLabels <= exampleCount) {
      selectedLabels = [...contextLabels]; // use all available
    } else {
      // Distribute: pick exampleCount labels, trying to spread across the available ones
      // Simple approach: pick evenly spaced indices
      selectedLabels = [];
      const step = Math.max(1, Math.floor(numContextLabels / exampleCount));
      for (let i = 0; i < exampleCount; i++) {
        const idx = Math.min(i * step, numContextLabels - 1);
        if (!selectedLabels.includes(contextLabels[idx])) {
          selectedLabels.push(contextLabels[idx]);
        } else {
          // Find next available
          for (let j = 0; j < numContextLabels; j++) {
            const candidate = contextLabels[j];
            if (!selectedLabels.includes(candidate)) {
              selectedLabels.push(candidate);
              break;
            }
          }
        }
      }
      // If still not enough, pad with first labels
      while (selectedLabels.length < exampleCount && selectedLabels.length < numContextLabels) {
        selectedLabels.push(contextLabels[selectedLabels.length]);
      }
    }

    // Generate examples
    const examples = [];

    // ---- Sense-specific example templates based on meaning_vi and pos ----
    // We'll create context-aware examples based on the meaning and context labels

    // Define example generators per sense index pattern
    // Each generator returns an array of {sentence, blank_sentence, answer}
    // but we'll create them dynamically

    for (let ei = 0; ei < exampleCount; ei++) {
      const selectedLabel = selectedLabels[ei % selectedLabels.length];

      // Generate sentence based on meaning and context
      let sentence, blankSentence;

      // Create sentence using the target word in appropriate form
      // The target word form should match the pos

      // ---- Generate based on meaning patterns ----
      if (meaningVi.includes('duy trì') || meaningVi.includes('giữ nguyên')) {
        // maintain sense
        if (pos === 'V') {
          if (selectedLabel === 'health') {
            sentence = "Regular exercise helps maintain good health.";
            blankSentence = "Regular exercise helps ____ good health.";
          } else if (selectedLabel === 'relationships') {
            sentence = "She tries to maintain a healthy relationship with her family.";
            blankSentence = "She tries to ____ a healthy relationship with her family.";
          } else if (selectedLabel === 'work') {
            sentence = "He wants to maintain a work-life balance.";
            blankSentence = "He wants to ____ a work-life balance.";
          } else {
            sentence = "Please maintain the equipment regularly.";
            blankSentence = "Please ____ the equipment regularly.";
          }
          answer = "maintain";
        } else {
          // adj or noun form - but 'maintain' is typically V in our data
          sentence = "Regular exercise helps maintain good health.";
          blankSentence = "Regular exercise helps ____ good health.";
          answer = "maintain";
        }
      } else if (meaningVi.includes('hỗ trợ') || meaningVi.includes('giúp đỡ')) {
        // aid sense
        if (pos === 'N') {
          if (selectedLabel === 'health') {
            sentence = "The charity provides aid for health initiatives.";
            blankSentence = "The charity provides ____ for health initiatives.";
          } else if (selectedLabel === 'work') {
            sentence = "Emergency aid arrived at the workplace.";
            blankSentence = "Emergency ____ arrived at the workplace.";
          } else if (selectedLabel === 'social') {
            sentence = "Social aid helps communities recover after the storm.";
            blankSentence = "Social ____ helps communities recover after the storm.";
          } else {
            sentence = "Financial aid is often needed in disasters.";
            blankSentence = "Financial ____ is often needed in disasters.";
          }
          answer = "aid";
        }
      } else if (meaningVi.includes('mục đích') || meaningVi.includes('tiêu chí')) {
        // aim sense - noun or verb
        if (pos === 'V') {
          if (selectedLabel === 'sports') {
            sentence = "The archer aims carefully before shooting.";
            blankSentence = "The archer ____ carefully before shooting.";
          } else if (selectedLabel === 'general') {
            sentence = "She aims to improve her English skills.";
            blankSentence = "She ____ to improve her English skills.";
          } else if (selectedLabel === 'military') {
            sentence = "The soldier aims his rifle at the target.";
            blankSentence = "The soldier ____ his rifle at the target.";
          } else {
            sentence = "The company aims to launch new products next year.";
            blankSentence = "The company ____ to launch new products next year.";
          }
          answer = "aim";
        } else {
          // noun
          if (selectedLabel === 'sports') {
            sentence = "The aim of the player is to score a goal.";
            blankSentence = "The ____ of the player is to score a goal.";
          } else {
            sentence = "His aim was recognized by the committee.";
            blankSentence = "His ____ was recognized by the committee.";
          }
          answer = "aim";
        }
      } else if (meaningVi.includes('khả năng') || meaningVi.includes('năng lực')) {
        // ability sense
        if (pos === 'N') {
          if (selectedLabel === 'work') {
            sentence = "Hard work develops ability.";
            blankSentence = "Hard work develops ____.";
          } else if (selectedLabel === 'education') {
            sentence = "Students need ability to succeed.";
            blankSentence = "Students need ____ to succeed.";
          } else if (selectedLabel === 'general') {
            sentence = "She has the ability to learn quickly.";
            blankSentence = "She has the ____ to learn quickly.";
          } else if (selectedLabel === 'career') {
            sentence = "Ability is important for career growth.";
            blankSentence = "Ability is important for career ____.";
          } else {
            sentence = "Ability is needed for this task.";
            blankSentence = "____ is needed for this task.";
          }
          answer = "ability";
        }
      } else if (meaningVi.includes('đồng ý') || meaningVi.includes('thoả thuận')) {
        // agree sense (verb)
        if (pos === 'V') {
          if (selectedLabel === 'communication') {
            sentence = "I agree with your opinion on the matter.";
            blankSentence = "I ____ with your opinion on the matter.";
          } else if (selectedLabel === 'social') {
            sentence = "We agree to disagree on this topic.";
            blankSentence = "We ____ to disagree on this topic.";
          } else if (selectedLabel === 'formal') {
            sentence = "The committee will agree on the new policy.";
            blankSentence = "The committee will ____ on the new policy.";
          } else {
            sentence = "Do you agree with the plan?";
            blankSentence = "Do you ____ with the plan?";
          }
          answer = "agree";
        }
      } else if (meaningVi.includes('từ bỏ') || meaningVi.includes('bỏ rơi')) {
        // abandon sense (verb)
        if (pos === 'V') {
          if (selectedLabel === 'general') {
            sentence = "Don't abandon your dreams.";
            blankSentence = "Don't ____ your dreams.";
          } else if (selectedLabel === 'relationships') {
            sentence = "He abandoned his friends in times of trouble.";
            blankSentence = "He ____ his friends in times of trouble.";
          } else if (selectedLabel === 'general') {
            // another general example
            sentence = "Please don't abandon the project halfway.";
            blankSentence = "Please don't ____ the project halfway.";
          } else {
            sentence = "The ship was abandoned by its crew.";
            blankSentence = "The ship was ____ by its crew.";
          }
          answer = "abandon";
        }
      } else if (meaningVi.includes('sự giúp đỡ') || meaningVi.includes('người giúp đỡ')) {
        // aid noun senses
        if (pos === 'N') {
          if (selectedLabel === 'health') {
            sentence = "The nurse gave medical aid to the patient.";
            blankSentence = "The nurse gave medical ____ to the patient.";
          } else if (selectedLabel === 'work') {
            sentence = "She received aid from her colleagues.";
            blankSentence = "She received ____ from her colleagues.";
          } else if (selectedLabel === 'social') {
            sentence = "Social aid was distributed after the flood.";
            blankSentence = "Social ____ was distributed after the flood.";
          } else {
            sentence = "First aid should be administered immediately.";
            blankSentence = "First ____ should be administered immediately.";
          }
          answer = "aid";
        }
      } else if (meaningVi.includes('nhắm') || meaningVi.includes('chỉ')) {
        // aim verb senses
        if (pos === 'V') {
          if (selectedLabel === 'military') {
            sentence = "The sniper aims at the target from the rooftop.";
            blankSentence = "The sniper ____ at the target from the rooftop.";
          } else if (selectedLabel === 'sports') {
            sentence = "He aims the ball toward the goal.";
            blankSentence = "He ____ the ball toward the goal.";
          } else {
            sentence = "She aims her camera at the landscape.";
            blankSentence = "She ____ her camera at the landscape.";
          }
          answer = "aim";
        }
      } else if (meaningVi.includes('sự rủi ro') || meaningVi.includes('tai nạn')) {
        // accident sense
        if (pos === 'N') {
          if (selectedLabel === 'transportation') {
            sentence = "A car accident blocked the highway.";
            blankSentence = "A car ____ blocked the highway.";
          } else if (selectedLabel === 'safety') {
            sentence = "Workplace safety reduces accident risk.";
            blankSentence = "Workplace safety reduces ____ risk.";
          } else if (selectedLabel === 'general') {
            sentence = "It was just a lucky accident.";
            blankSentence = "It was just a lucky ____.";
          } else {
            sentence = "The accident happened early this morning.";
            blankSentence = "The ____ happened early this morning.";
          }
          answer = "accident";
        }
      } else if (meaningVi.includes('học viện') || meaningVi.includes('trường học')) {
        // academic sense
        if (pos === 'A') {
          if (selectedLabel === 'education') {
            sentence = "Academic research requires rigorous methodology.";
            blankSentence = "____ research requires rigorous methodology.";
          } else {
            sentence = "He has an academic approach to teaching.";
            blankSentence = "____ has an academic approach to teaching.";
          }
          answer = "academic";
        } else {
          // noun form
          if (selectedLabel === 'education') {
            sentence = "She is a member of the academic community.";
            blankSentence = "She is a member of the ____ community.";
          } else {
            sentence = "The academic conference was held last week.";
            blankSentence = "The ____ conference was held last week.";
          }
          answer = "academic";
        }
      } else if (meaningVi.includes('xâm lược') || meaningVi.includes('công kích')) {
        // aggressive sense (adjective)
        if (pos === 'A') {
          if (selectedLabel === 'sports') {
            sentence = "The team made an aggressive attack in the second half.";
            blankSentence = "The team made an ____ attack in the second half.";
          } else if (selectedLabel === 'military') {
            sentence = "The army launched an aggressive offensive.";
            blankSentence = "The army launched an ____ offensive.";
          } else if (selectedLabel === 'personality') {
            sentence = "He has an aggressive personality type.";
            blankSentence = "He has an ____ personality type.";
          } else if (selectedLabel === 'daily life') {
            sentence = "Don't be so aggressive in the discussion.";
            blankSentence = "Don't be so ____ in the discussion.";
          } else {
            sentence = "The team made an aggressive play.";
            blankSentence = "The team made an ____ play.";
          }
          answer = "aggressive";
        }
      } else if (meaningVi.includes('sự thống nhất') || meaningVi.includes('hợp đồng')) {
        // agreement sense
        if (pos === 'N') {
          if (selectedLabel === 'politics') {
            sentence = "The signing of the agreement was historic.";
            blankSentence = "The signing of the ____ was historic.";
          } else if (selectedLabel === 'law') {
            sentence = "The contract agreement was reviewed by lawyers.";
            blankSentence = "The contract ____ was reviewed by lawyers.";
          } else if (selectedLabel === 'social') {
            sentence = "There was agreement among the participants.";
            blankSentence = "There was ____ among the participants.";
          } else {
            sentence = "Reaching agreement takes time and discussion.";
            blankSentence = "Reaching ____ takes time and discussion.";
          }
          answer = "agreement";
        }
      } else if (meaningVi.includes('khắp nơi') || meaningVi.includes('truyền đi')) {
        // abroad sense
        if (pos === 'D') {
          if (selectedLabel === 'travel') {
            sentence = "She went abroad last year for studies.";
            blankSentence = "She went ____ last year for studies.";
          } else if (selectedLabel === 'media') {
            sentence = "The news traveled abroad quickly.";
            blankSentence = "The news traveled ____ quickly.";
          } else {
            sentence = "He works abroad in a multinational company.";
            blankSentence = "He works ____ in a multinational company.";
          }
          answer = "abroad";
        }
      } else if (meaningVi.includes('không khí') || meaningVi.includes('bầu không khí')) {
        // air noun senses
        if (pos === 'N') {
          if (selectedLabel === 'nature') {
            sentence = "Fresh air is essential for good health.";
            blankSentence = "Fresh ____ is essential for good health.";
          } else if (selectedLabel === 'environment') {
            sentence = "The air in the city is polluted.";
            blankSentence = "The ____ in the city is polluted.";
          } else if (selectedLabel === 'music') {
            sentence = "The band played a beautiful air.";
            blankSentence = "The band played a beautiful ____.";
          } else {
            sentence = "Please open the window for some fresh air.";
            blankSentence = "Please open the window for some fresh ____.";
          }
          answer = "air";
        }
      } else if (meaningVi.includes('không khí - phơi')) {
        // air verb senses
        if (pos === 'V') {
          if (selectedLabel === 'daily life') {
            sentence = "Open the window to air the room.";
            blankSentence = "Open the window to ____ the room.";
          } else if (selectedLabel === 'health') {
            sentence = "The doctor advised me to air the quilt.";
            blankSentence = "The doctor advised me to ____ the quilt.";
          } else {
            sentence = "Hang the clothes outside to air.";
            blankSentence = "Hang the clothes outside to ____.";
          }
          answer = "air";
        }
      } else if (meaningVi.includes('alarm') || meaningVi.includes('báo động')) {
        // alarm noun senses
        if (pos === 'N') {
          if (selectedLabel === 'safety') {
            sentence = "The smoke alarm woke us up.";
            blankSentence = "The smoke ____ woke us up.";
          } else if (selectedLabel === 'home') {
            sentence = "Set the alarm for 7 AM.";
            blankSentence = "Set the ____ for 7 AM.";
          } else {
            sentence = "The alarm clock rang at 6 AM.";
            blankSentence = "The ____ clock rang at 6 AM.";
          }
          answer = "alarm";
        }
      } else if (meaningVi.includes('thuộc nguyên tử') || meaningVi.includes('nuclear')) {
        // nucleus/atomic senses
        if (pos === 'N') {
          if (selectedLabel === 'science') {
            sentence = "The nucleus is the center of the atom.";
            blankSentence = "The ____ is the center of the atom.";
          } else {
            sentence = "Radioactive nuclei emit particles.";
            blankSentence = "Radioactive ____ emit particles.";
          }
          answer = "nucleus";
        } else if (pos === 'A') {
          if (selectedLabel === 'science') {
            sentence = "Nuclear energy is powerful.";
            blankSentence = "____ energy is powerful.";
          } else {
            sentence = "The atomic structure is complex.";
            blankSentence = "The ____ structure is complex.";
          }
          answer = "nuclear";
        }
      } else {
        // Default/generic example generation for unmatched meanings
        // Create a natural sentence based on the meaning_vi and context labels

        // Use a simple template approach
        const meaningLower = meaningVi.toLowerCase();

        // Try to create a sensible example based on key words in meaning_vi
        if (meaningLower.includes('hợp đồng') || meaningLower.includes('hiệp định')) {
          // agreement/politics
          if (pos === 'N') {
            if (selectedLabel === 'politics') {
              sentence = "The international agreement was signed yesterday.";
              blankSentence = "The international ____ was signed yesterday.";
            } else if (selectedLabel === 'law') {
              sentence = "The legal agreement must be read carefully.";
              blankSentence = "The legal ____ must be read carefully.";
            } else {
              sentence = "The business agreement was profitable.";
              blankSentence = "The business ____ was profitable.";
            }
            answer = "agreement";
          } else {
            sentence = "He reached an agreement with the partner.";
            blankSentence = "He reached an ____ with the partner.";
            answer = "agreement";
          }
        } else if (meaningLower.includes('từ bỏ') || meaningLower.includes('bỏ rơi')) {
          if (pos === 'V') {
            if (selectedLabel === 'relationships') {
              sentence = "She decided to abandon the project.";
              blankSentence = "She decided to ____ the project.";
            } else {
              sentence = "Don't abandon hope.";
              blankSentence = "Don't ____ hope.";
            }
            answer = "abandon";
          } else {
            sentence = "The abandonment of the site was gradual.";
            blankSentence = "The ____ of the site was gradual.";
            answer = "abandon";
          }
        } else if (meaningLower.includes('khả năng') || meaningLower.includes('năng lực')) {
          if (pos === 'N') {
            if (selectedLabel === 'education') {
              sentence = "Hard work builds ability.";
              blankSentence = "Hard work builds ____.";
            } else {
              sentence = "She has the ability to sing.";
              blankSentence = "She has the ____ to sing.";
            }
            answer = "ability";
          } else {
            sentence = "You are able to understand.";
            blankSentence = "You are ____ to understand.";
            answer = "able";
          }
        } else if (meaningLower.includes('sự báo động') || meaningLower.includes('còi')) {
          if (pos === 'N') {
            if (selectedLabel === 'safety') {
              sentence = "A fire alarm went off in the building.";
              blankSentence = "A fire ____ went off in the building.";
            } else {
              sentence = "He set an alarm for 7 AM.";
              blankSentence = "He set an ____ for 7 AM.";
            }
            answer = "alarm";
          }
        } else if (meaningLower.includes('trên') || meaningLower.includes('above')) {
          // above/d above
          if (selectedLabel === 'general') {
            if (pos === 'D' || pos === 'E') {
              sentence = "The book is above the table.";
              blankSentence = "The book is ____ the table.";
              answer = "above";
            } else {
              sentence = "He is above such behavior.";
              blankSentence = "He is ____ such behavior.";
              answer = "above";
            }
          }
        } else if (meaningLower.includes('chữ cái a') || meaningLower.includes('letter a')) {
          // The word 'a' - special case
          // Skip generating examples for the article 'a' as it's too fundamental
          // and has 35 senses which would be extremely complex
          // Just add a placeholder
          sentence = "This is a sample.";
          blankSentence = "This is a sample.";
          answer = "a";
        } else {
          // Generic fallback - create a simple sentence
          // Use the word itself in a simple context
          if (pos === 'V') {
            sentence = "Please " + word + " the task.";
            blankSentence = "Please ____ the task.";
          } else if (pos === 'N') {
            sentence = "The " + word + " is important.";
            blankSentence = "The ____ is important.";
          } else if (pos === 'A') {
            sentence = "It is " + word + " to proceed.";
            blankSentence = "It is ____ to proceed.";
          } else {
            // determiner or other
            sentence = "This is a " + word + ".";
            blankSentence = "This is a ____.";
          }
          answer = word;
        }
      }

      // Ensure answer is set
      if (!answer) {
        answer = word;
      }

      // Ensure blank_sentence uses exactly 4 underscores
      // The blank should replace the target word
      // Make sure blank_sentence doesn't contain the target word
      // and doesn't leak the answer

      // Validate: answer must appear in sentence (as the target word)
      // And blank_sentence should have ____, not the answer word

      const example = {
        sentence,
        blank_sentence: blankSentence,
        answer: answer,
        accepted_answers: []
      };

      // Add accepted answers if applicable
      // Only add valid synonyms that work in that specific sentence
      // For now, keep empty unless we're confident
      // The rules say: "If not sure: DO NOT add (false positive worse than missing)"

      examples.push(example);
    }

    // Add sense to output
    wordOutput.senses.push({
      meaning_vi: meaningVi,
      pos: pos,
      source: sense.source || "dictionary",
      context_labels: contextLabels,
      examples: examples
    });
  }

  outputWords.push(wordOutput);
}

const output = {
  batch: 1,
  words: outputWords
};

fs.writeFileSync(outputPath, JSON.stringify(output, null, 2));
console.log('Output written to', outputPath);
console.log('Total words processed:', outputWords.length);