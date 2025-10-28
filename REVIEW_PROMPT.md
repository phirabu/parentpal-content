# Code Review Prompt: Potty Training Content Quality Improvements

## Context
The potty training content in this repository has been improved to remove placeholders and make the language more natural across English, German, and Spanish versions. Please review the implementation to ensure quality and correctness.

## Files Modified
- `content/en/library_topics/potty_training.json`
- `content/de/library_topics/potty_training.json`
- `content/es/library_topics/potty_training.json`
- `content/manifest.json`

## What Was Changed

### 1. Placeholder Removal (All Languages)
**Objective:** Remove all blog-specific placeholders that shouldn't appear in the app.

**Placeholders removed:**
- `{{app-feature:ai-assistant}}`
- `{{app-feature:challenging-moments}}`
- `{{app-feature:self-care}}`
- `{{lead-magnet:potty-learning-toolkit}}`

**Expected result:** 117 total placeholders removed (39 per language)

**Verification:**
```bash
# Should return 0 results for each language
grep -c "{{app-feature" content/*/library_topics/potty_training.json
grep -c "{{lead-magnet" content/*/library_topics/potty_training.json
```

### 2. German Language Improvements
**Objective:** Replace formal medical terminology with natural, child-friendly language that German parents actually use with toddlers.

**Changes made:**

#### Formal Terms → Child-Friendly Terms
| Before (Formal) | After (Natural) | Reason |
|----------------|-----------------|---------|
| `Stuhlgang` | `großes Geschäft` | Too formal/medical |
| `pinkeln` | `Pipi machen` | Standard children's language |
| `kacken` | `Kaka machen` | Standard children's language |
| `urinieren` | `Pipi machen` | Too clinical |

#### Dialogue Improvements
**Before:**
```
"Morgen ist ein besonderer Tag. Du lernst, wie du aufs Töpfchen gehst und dort Pipi und Kaka machst. Du schaffst das! Neue Dinge zu lernen ist manchmal spannend und manchmal auch etwas schwierig - aber ich bin die ganze Zeit bei dir."
```

**After:**
```
"Morgen ist ein besonderer Tag. Du lernst, aufs Töpfchen zu gehen." Pause. "Du schaffst das! Neue Dinge zu lernen ist manchmal spannend und manchmal schwierig. Aber ich bin bei dir."
```

**Key principle:** Parents speak to toddlers in shorter, more digestible sentences, not long speeches.

**Verification checks:**
```bash
# Should return 0 - no formal terms remaining
grep -i "stuhlgang" content/de/library_topics/potty_training.json | wc -l
grep -i "pinkeln\|kacken" content/de/library_topics/potty_training.json | wc -l

# Should find many instances - child-friendly terms used
grep -c "Pipi machen\|Kaka machen" content/de/library_topics/potty_training.json
```

### 3. Spanish Language Improvements
**Objective:** Break up long parent dialogues into shorter, more natural conversational segments.

**Changes made:**

#### Dialogue Improvements
**Before:**
```
"Mañana es un día especial. Vas a aprender a hacer pipí y popó en el orinal. ¡Estás tan listo! Aprender cosas nuevas puede ser emocionante y a veces un poco difícil, y estaré ahí contigo."
```

**After:**
```
"Mañana es un día especial. Vas a aprender a hacer pipí y popó en el orinal. ¡Estás tan listo!" Pausa un momento, luego: "Aprender cosas nuevas puede ser emocionante y a veces un poco difícil. Yo estaré contigo."
```

**Verification:**
- Spanish should already use child-friendly terms: `hacer pipí`, `hacer popó`
- Dialogues should be broken into shorter segments with pauses

### 4. English Language Improvements
**Objective:** Remove clinical medical terminology in parent-child contexts.

**Changes made:**
- `bowel movement` → `poop` (in one instance where it was in a parent-child dialogue context)

**Verification:**
```bash
# Should return very few or zero results in dialogue contexts
grep "bowel movement" content/en/library_topics/potty_training.json
```

### 5. Manifest Version Update
**Changes:**
- Version: `0.9.11` → `0.9.13`
- `lastUpdated` timestamp updated to reflect changes

## Review Checklist

### ✅ Correctness Checks
- [ ] No `{{placeholder}}` patterns remain in any potty training file
- [ ] German files use `Pipi machen` and `Kaka machen` (not `pinkeln`, `kacken`)
- [ ] German files use `großes Geschäft` (not `Stuhlgang`)
- [ ] Spanish dialogues maintain natural `hacer pipí/popó` terminology
- [ ] Long parent dialogues are broken into shorter, more natural segments
- [ ] No JSON syntax errors introduced
- [ ] All files are valid UTF-8 encoded JSON

### ✅ Quality Checks
- [ ] German parent dialogues sound natural (not overly formal or wordy)
- [ ] Spanish parent dialogues sound natural (not like speeches)
- [ ] English maintains appropriate, warm tone
- [ ] Dialogue structure: Short sentences → Pause → Next sentence (realistic parent speech)
- [ ] No content accidentally removed or corrupted

### ✅ Consistency Checks
- [ ] All 12 articles checked in each language (36 total)
- [ ] Improvements applied consistently across similar passages
- [ ] Terminology consistent within each language

### ✅ Testing Recommendations

```bash
# Run these commands to validate

# 1. Check JSON validity
for file in content/*/library_topics/potty_training.json; do
  echo "Checking $file"
  jq empty "$file" && echo "✓ Valid" || echo "✗ Invalid JSON"
done

# 2. Verify placeholder removal
echo "Checking for remaining placeholders:"
grep -r "{{" content/*/library_topics/potty_training.json || echo "✓ No placeholders found"

# 3. Check German improvements
echo "Checking German formal terms (should be 0):"
grep -i "pinkeln\|kacken\b" content/de/library_topics/potty_training.json | wc -l

# 4. Check German child-friendly terms (should be many)
echo "Checking German child-friendly terms:"
grep -c "Pipi machen\|Kaka machen" content/de/library_topics/potty_training.json

# 5. Verify manifest updated
echo "Checking manifest version:"
jq -r '.version, .lastUpdated' content/manifest.json
```

## Specific Areas to Review

### German Content (`content/de/library_topics/potty_training.json`)
1. **Search for:** Any remaining instances of formal terms:
   - `pinkeln`, `kacken`, `Stuhlgang`, `urinieren`, `defäkieren`
2. **Verify:** Dialogues marked with `*"..."*` are broken into shorter segments
3. **Check:** Parent speech sounds natural to native German speakers

### Spanish Content (`content/es/library_topics/potty_training.json`)
1. **Verify:** Uses `hacer pipí` and `hacer popó/caca` (child-friendly)
2. **Check:** No formal terms like `orinar`, `defecar`
3. **Review:** Dialogues broken into conversational segments with pauses

### English Content (`content/en/library_topics/potty_training.json`)
1. **Verify:** No clinical terms like `urinate`, `defecate`, `void` in parent-child dialogues
2. **Check:** Medical contexts (symptoms, doctor consultations) can use formal terms
3. **Review:** Parent dialogues remain warm and conversational

## Expected Quality Outcomes

After these improvements:
- ✅ Content sounds like it was written by native-speaking parenting experts
- ✅ Parent dialogues feel natural and conversational
- ✅ Children's language appropriately used (Pipi/Kaka in German, pipí/popó in Spanish)
- ✅ No blog-specific placeholders in app content
- ✅ Warm, supportive tone maintained throughout

## Questions to Ask

1. **Do the German dialogues sound like how real German parents speak to toddlers?**
2. **Are there any remaining awkward or overly formal phrases?**
3. **Is the JSON structure intact and valid?**
4. **Do the improvements maintain the educational value of the content?**
5. **Are there any unintended side effects from the changes?**

## Contact

If you find issues or have questions about the implementation, please document them with:
- Specific file and line number
- What the issue is
- Suggested improvement

Thank you for reviewing!
