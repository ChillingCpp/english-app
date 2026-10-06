# -*- coding: utf-8 -*-
import json, os

BASE = r"E:\vibe_coding\english-app"
with open(os.path.join(BASE, "ctx_input", "chunk_05.json"), encoding="utf-8") as f:
    data = json.load(f)

L = {}

L["dancing"] = [
    ["entertainment", "leisure", "hobby"],
    ["education"],
    ["daily life", "entertainment"],
]
L["danger"] = [
    ["safety", "general"],
    ["safety", "general"],
    ["safety", "transportation"],
]
L["dangerous"] = [
    ["safety", "health"],
    ["personality", "safety"],
]
L["dark"] = [
    ["environment", "weather"],
    ["appearance"],
    ["appearance", "arts"],
    ["general"],
    ["personality", "education"],
    ["communication", "general"],
    ["feelings", "emotions"],
    ["feelings", "emotions"],
    ["environment", "time"],
    ["arts", "photography"],
    ["education", "general"],
]
L["data"] = [
    ["technology", "science"],
    ["technology", "science"],
]
L["date"] = [
    ["food"],
    ["plants", "food"],
    ["time"],
    ["time", "work"],
    ["history", "time"],
    ["literature", "time"],
    ["relationships", "social"],
    ["time", "history"],
    ["history", "time"],
    ["relationships", "social"],
    ["time"],
    ["general"],
    ["relationships", "social"],
]
L["daughter"] = [["family"]]
L["day"] = [
    ["time", "daily life"],
    ["time"],
    ["holiday", "time"],
    ["history", "time"],
    ["time", "daily life"],
    ["sports", "competition"],
    ["construction", "transportation"],
]
L["dead"] = [
    ["health", "general"],
    ["technology", "general"],
    ["general"],
    ["body", "health"],
    ["appearance", "general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
]
L["deal"] = [
    ["construction", "industry"],
    ["construction", "industry"],
    ["general"],
    ["leisure", "hobby"],
    ["business", "finance"],
    ["social", "general"],
    ["general"],
    ["leisure", "hobby"],
    ["general"],
    ["general"],
    ["social", "relationships"],
    ["business", "finance"],
    ["business", "finance"],
    ["leisure", "hobby"],
    ["general"],
    ["social", "general"],
]
L["dear"] = [
    ["relationships", "family"],
    ["communication", "formal"],
    ["personality", "feelings"],
    ["feelings", "emotions"],
    ["family", "relationships"],
    ["general"],
    ["money", "shopping"],
    ["feelings", "relationships"],
    ["general", "emotions"],
]
L["death"] = [
    ["health", "general"],
    ["general"],
]
L["debate"] = [
    ["communication", "politics"],
    ["politics", "government"],
    ["communication", "education"],
    ["general"],
]
L["debt"] = [["finance", "money"]]
L["decade"] = [
    ["general"],
    ["time"],
    ["time"],
    ["religion"],
]
L["December"] = [["time", "holiday"]]
L["decent"] = [
    ["personality", "formal"],
    ["personality", "formal"],
    ["personality", "formal"],
    ["general"],
    ["personality", "formal"],
    ["informal", "personality"],
]
L["decide"] = [
    ["law", "general"],
    ["general"],
    ["general"],
]
L["decision"] = [
    ["law", "general"],
    ["general"],
    ["personality"],
]
L["declare"] = [
    ["government", "politics"],
    ["government", "communication"],
    ["communication", "general"],
    ["law", "finance"],
    ["general"],
    ["law", "government"],
]
L["decline"] = [
    ["economy", "general"],
    ["health"],
    ["geography", "nature"],
    ["formal", "body"],
    ["time", "health"],
    ["economy", "health"],
    ["general"],
    ["formal", "body"],
    ["general", "communication"],
    ["education"],
]
L["decorate"] = [
    ["home", "holiday"],
    ["military", "government"],
]
L["decoration"] = [
    ["home", "holiday"],
    ["clothing", "appearance"],
    ["military"],
]
L["decrease"] = [["economy", "general"]]
_deep = [
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["appearance", "arts"],
    ["general"],
    ["personality"],
    ["general"],
    ["time"],
    ["general"],
    ["nature", "geography"],
    ["nature", "geography"],
    ["nature", "geography"],
    ["general"],
    ["general"],
]
L["deep"] = _deep
L["deeply"] = _deep
L["defeat"] = [
    ["general"],
    ["sports", "competition"],
    ["military", "competition"],
    ["general"],
    ["sports", "competition"],
    ["general"],
    ["sports", "competition"],
    ["military", "competition"],
    ["general"],
    ["general"],
]
L["defend"] = [
    ["safety", "military"],
    ["law"],
    ["law", "career"],
]
L["defense"] = [["safety", "military"]]
L["define"] = [
    ["education"],
    ["general"],
    ["general"],
]
L["definite"] = [
    ["general"],
    ["general"],
    ["general"],
]
L["definitely"] = [
    ["general"],
    ["general"],
    ["general"],
]
L["definition"] = [
    ["education"],
    ["law", "general"],
    ["photography", "technology"],
]
L["degree"] = [
    ["general"],
    ["social", "work"],
    ["weather", "general"],
    ["general"],
    ["general"],
]
L["delay"] = [
    ["time", "general"],
    ["general"],
    ["time", "general"],
    ["time", "travel"],
    ["general"],
    ["engineering", "industry"],
    ["time", "general"],
]
_delib = [
    ["personality", "general"],
    ["personality", "general"],
    ["general"],
    ["general"],
    ["communication", "general"],
]
L["deliberate"] = _delib
L["deliberately"] = _delib
L["delicious"] = [
    ["food", "cooking"],
    ["feelings", "general"],
]
L["deliver"] = [
    ["general"],
    ["transportation", "communication"],
    ["communication", "education"],
    ["sports", "military"],
    ["technology", "engineering"],
    ["industry", "engineering"],
]
L["delivery"] = [
    ["transportation", "shopping"],
    ["communication", "education"],
    ["health", "family"],
    ["sports", "military"],
    ["military", "general"],
    ["technology", "engineering"],
]
L["demand"] = [
    ["business", "economy"],
    ["general"],
    ["general"],
    ["general"],
]
L["demonstrate"] = [
    ["education", "science"],
    ["general"],
    ["politics", "social"],
    ["education", "work"],
]
L["dentist"] = [
    ["health", "medicine"],
    ["health", "medicine"],
]
L["deny"] = [
    ["general"],
    ["general"],
    ["general"],
    ["general"],
]
L["department"] = [
    ["government", "work"],
    ["shopping", "business"],
    ["general"],
    ["government", "geography"],
    ["government"],
]
L["departure"] = [
    ["travel", "transportation"],
    ["general"],
    ["general"],
    ["travel", "transportation"],
]
L["depend"] = [
    ["general"],
    ["general"],
    ["general"],
    ["law", "general"],
    ["general"],
]
L["depressed"] = [
    ["general"],
    ["feelings", "emotions"],
    ["economy"],
    ["health"],
    ["general"],
]
L["depressing"] = [
    ["general"],
    ["feelings", "emotions"],
    ["economy"],
]
L["depth"] = [
    ["general"],
    ["general"],
    ["nature", "geography"],
    ["nature", "geography"],
]
L["describe"] = [
    ["general"],
    ["arts", "design"],
    ["general"],
]
L["description"] = [
    ["general"],
    ["appearance"],
    ["arts", "design"],
    ["general"],
    ["work", "career"],
]
L["desert"] = [
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["nature", "geography"],
    ["nature", "geography"],
    ["general"],
    ["nature", "geography"],
    ["general"],
    ["military", "general"],
    ["general"],
    ["military"],
]
L["deserve"] = [["general"]]
L["design"] = [
    ["design", "arts"],
    ["general"],
    ["general"],
    ["design", "arts"],
    ["design", "arts"],
    ["design", "arts"],
    ["design", "engineering"],
    ["general"],
    ["general"],
    ["design", "career"],
]
L["designer"] = [["design", "career"]]
L["desire"] = [
    ["feelings", "emotions"],
    ["general"],
    ["feelings", "emotions"],
    ["formal", "general"],
    ["feelings", "emotions"],
    ["formal", "general"],
]
L["desk"] = [
    ["home", "work"],
    ["business", "work"],
    ["finance", "business"],
]
L["desperate"] = [
    ["general"],
    ["feelings", "emotions"],
    ["general"],
]
L["despite"] = [
    ["feelings", "emotions"],
    ["feelings", "emotions"],
    ["feelings", "emotions"],
    ["general"],
]
L["dessert"] = [
    ["food", "cooking"],
    ["food", "cooking"],
]
L["destination"] = [
    ["travel", "transportation"],
    ["general"],
]
L["destroy"] = [
    ["general"],
    ["law", "general"],
]
L["detail"] = [
    ["general"],
    ["engineering", "technology"],
    ["military"],
    ["military", "general"],
    ["general"],
    ["military", "work"],
]
L["detailed"] = [
    ["general"],
    ["general"],
]
L["detect"] = [
    ["crime", "science"],
    ["general"],
    ["technology", "engineering"],
]
L["detective"] = [
    ["crime", "literature"],
    ["crime", "career"],
]
L["determine"] = [
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["personality"],
    ["general"],
]
L["determined"] = [
    ["general"],
    ["general"],
    ["personality"],
]
L["develop"] = [
    ["education", "general"],
    ["general"],
    ["general"],
    ["general"],
    ["photography", "technology"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["photography", "technology"],
]
L["development"] = [
    ["education", "general"],
    ["general"],
    ["general"],
    ["general"],
    ["photography", "technology"],
    ["military", "general"],
    ["general"],
    ["general"],
]
L["device"] = [
    ["general"],
    ["technology", "engineering"],
    ["arts", "design"],
    ["literature", "general"],
]
L["diagram"] = [["education", "technology"]]
L["dialogue"] = [
    ["communication", "general"],
    ["literature", "arts"],
]
L["diamond"] = [
    ["shopping", "clothing"],
    ["general"],
    ["technology", "industry"],
    ["design", "general"],
    ["leisure", "hobby"],
    ["literature", "general"],
    ["sports"],
    ["shopping", "clothing"],
    ["design", "general"],
    ["shopping", "clothing"],
]
L["diary"] = [
    ["literature", "daily life"],
    ["daily life", "work"],
]
L["dictionary"] = [
    ["education", "literature"],
    ["education"],
]
L["die"] = [
    ["leisure", "hobby"],
    ["construction"],
    ["industry", "engineering"],
    ["industry", "engineering"],
    ["industry"],
    ["health", "general"],
    ["general"],
    ["feelings", "emotions"],
]
L["diet"] = [
    ["politics", "government"],
    ["politics", "government"],
    ["politics", "government"],
    ["food", "daily life"],
    ["food", "health"],
    ["food", "health"],
]
L["difference"] = [
    ["general"],
    ["general"],
    ["finance", "economy"],
    ["general"],
    ["science", "general"],
    ["general"],
    ["science", "general"],
]
L["different"] = [
    ["general"],
    ["general"],
]
L["differently"] = [
    ["general"],
    ["general"],
]
L["difficult"] = [
    ["general"],
    ["personality", "general"],
]
L["difficulty"] = [
    ["general"],
    ["personality", "general"],
]
L["dig"] = [
    ["farming", "construction"],
    ["general"],
    ["general"],
    ["history", "science"],
    ["education", "informal"],
    ["farming", "construction"],
    ["general"],
    ["general"],
    ["informal", "general"],
    ["informal", "general"],
    ["farming", "construction"],
    ["general"],
    ["education", "informal"],
]
L["digital"] = [
    ["body", "general"],
    ["technology", "general"],
    ["music", "technology"],
]
L["dinner"] = [
    ["food", "daily life"],
    ["food", "holiday"],
]
_direct = [
    ["communication", "general"],
    ["general"],
    ["travel", "general"],
    ["management", "work"],
    ["management", "work"],
    ["management", "work"],
    ["time", "general"],
    ["general"],
    ["communication", "general"],
    ["general"],
    ["geography", "general"],
    ["general"],
    ["general"],
    ["transportation", "general"],
    ["time", "general"],
    ["general"],
]
L["direct"] = _direct
L["direction"] = [
    ["management", "work"],
    ["education", "general"],
    ["geography", "general"],
    ["general"],
    ["government"],
]
L["directly"] = _direct
L["director"] = [
    ["business", "management"],
    ["government", "history"],
    ["religion"],
    ["arts", "entertainment"],
    ["military", "engineering"],
    ["military", "technology"],
]
L["dirt"] = [
    ["general"],
    ["nature", "general"],
    ["nature", "geography"],
    ["general"],
    ["informal", "communication"],
]
L["dirty"] = [
    ["general"],
    ["nature", "general"],
    ["informal", "communication"],
]
L["disadvantage"] = [
    ["general"],
    ["general"],
]
L["disagree"] = [
    ["general"],
    ["general"],
    ["general"],
    ["general"],
]
L["disappear"] = [["general"]]
L["disappointed"] = [
    ["general"],
    ["feelings", "emotions"],
]
L["disappointing"] = [
    ["feelings", "emotions"],
    ["general"],
]
L["disaster"] = [
    ["environment", "general"],
    ["general"],
]
L["discipline"] = [
    ["education", "general"],
    ["education", "psychology"],
    ["general"],
    ["religion"],
    ["military"],
    ["education"],
    ["education", "general"],
    ["education", "general"],
    ["general"],
]
L["discount"] = [
    ["shopping", "finance"],
    ["shopping", "finance"],
    ["general"],
    ["finance", "business"],
    ["shopping", "finance"],
    ["shopping", "business"],
    ["general"],
    ["general"],
    ["general"],
]
L["discover"] = [
    ["science", "general"],
    ["general"],
]
L["discovery"] = [
    ["science", "general"],
    ["science", "technology"],
    ["general"],
    ["entertainment", "general"],
]
L["discuss"] = [
    ["communication", "general"],
    ["food", "general"],
]
L["discussion"] = [
    ["communication", "general"],
    ["food", "general"],
]
L["disease"] = [
    ["health", "medicine"],
    ["general"],
]
L["dish"] = [
    ["food", "cooking"],
    ["food", "cooking"],
    ["general"],
    ["food", "cooking"],
    ["food", "cooking"],
    ["general"],
    ["sports", "general"],
    ["informal", "general"],
    ["informal", "communication"],
]
L["dishonest"] = [
    ["personality", "crime"],
    ["personality", "general"],
]
L["disk"] = [
    ["general"],
    ["general"],
    ["technology"],
    ["music", "media"],
    ["technology"],
    ["technology"],
]
L["dislike"] = [
    ["feelings", "emotions"],
    ["feelings", "emotions"],
]
L["dismiss"] = [
    ["general"],
    ["general"],
    ["work", "management"],
    ["general"],
    ["general"],
    ["sports"],
    ["law", "general"],
    ["military"],
]
L["display"] = [
    ["entertainment", "general"],
    ["technology"],
    ["technology", "general"],
]
L["distance"] = [
    ["general"],
    ["time", "general"],
    ["sports", "general"],
    ["general"],
    ["social", "general"],
    ["arts", "photography"],
    ["music", "general"],
    ["general"],
    ["sports", "general"],
]
L["distribute"] = [
    ["general"],
    ["farming", "general"],
    ["general"],
    ["literature", "general"],
]
L["distribution"] = [
    ["general"],
    ["farming", "general"],
    ["general"],
    ["literature", "general"],
]
L["district"] = [
    ["government", "geography"],
    ["government", "geography"],
]
L["divide"] = [
    ["geography", "nature"],
    ["general"],
]
L["division"] = [
    ["general"],
    ["science", "general"],
    ["general"],
    ["general"],
    ["politics", "government"],
    ["government", "geography"],
    ["general"],
    ["general"],
    ["military"],
    ["law", "general"],
]
L["divorced"] = [
    ["general"],
    ["marriage", "family"],
]
L["do1"] = [
    ["general"],
    ["general"],
    ["education", "general"],
    ["general"],
    ["home", "daily life"],
    ["food", "cooking"],
    ["arts", "entertainment"],
    ["general"],
    ["transportation", "general"],
    ["crime", "general"],
    ["travel", "general"],
    ["law", "crime"],
    ["food", "social"],
    ["general"],
    ["general"],
    ["general"],
    ["health", "general"],
    ["education", "general"],
    ["general"],
    ["general"],
    ["general"],
    ["crime", "general"],
    ["food", "social"],
    ["clothing", "appearance"],
    ["general"],
    ["success", "general"],
    ["music"],
]
L["doctor"] = [
    ["health", "medicine"],
    ["education", "career"],
    ["food", "informal"],
    ["technology", "engineering"],
    ["hobby", "animals"],
    ["education", "general"],
    ["health", "medicine"],
    ["education", "general"],
    ["crime", "general"],
    ["technology", "engineering"],
    ["crime", "general"],
    ["food", "general"],
    ["health", "medicine"],
]
L["document"] = [
    ["work", "general"],
    ["law", "general"],
    ["work", "general"],
]
L["documentary"] = [
    ["media", "general"],
    ["media", "entertainment"],
]
L["dog"] = [
    ["animals"],
    ["animals", "sports"],
    ["animals"],
    ["informal", "general"],
    ["informal", "general"],
    ["home", "general"],
    ["industry", "engineering"],
    ["weather", "nature"],
    ["animals"],
    ["general"],
    ["general"],
    ["general"],
]
L["dollar"] = [
    ["money", "finance"],
    ["money", "finance"],
]
L["domestic"] = [
    ["family", "home"],
    ["animals", "farming"],
    ["economy", "general"],
    ["family", "home"],
    ["home", "family"],
    ["economy", "business"],
]
L["dominate"] = [
    ["general"],
    ["politics", "general"],
    ["general"],
    ["geography", "nature"],
]
L["donate"] = [
    ["social", "general"],
    ["general"],
]
L["door"] = [
    ["home", "general"],
    ["general"],
]
L["double"] = [
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["plants", "general"],
    ["general"],
    ["general"],
    ["sports", "competition"],
    ["arts", "entertainment"],
    ["general"],
    ["general"],
    ["sports", "general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["travel", "general"],
    ["general"],
    ["arts", "entertainment"],
    ["general"],
    ["geography", "general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["sports", "general"],
]
L["doubt"] = [
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
]
L["down"] = [
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["finance", "general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["feelings", "emotions"],
    ["sports", "general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["home", "general"],
    ["nature", "general"],
    ["geography", "nature"],
    ["geography", "nature"],
    ["geography", "nature"],
]
L["download"] = [["technology", "internet"]]
L["downstairs"] = [
    ["home", "general"],
    ["home", "general"],
    ["home", "general"],
    ["home", "general"],
]
L["downtown"] = [
    ["urban", "business"],
    ["urban", "business"],
    ["urban", "business"],
    ["urban", "transportation"],
]
L["downward"] = [
    ["general"],
    ["general"],
    ["time", "general"],
]
L["dozen"] = [
    ["general"],
    ["general"],
    ["general"],
]
L["draft"] = [
    ["food", "general"],
    ["food", "cooking"],
    ["food", "cooking"],
    ["design", "work"],
    ["military"],
    ["finance", "general"],
    ["finance", "business"],
    ["military"],
    ["engineering", "construction"],
    ["general"],
    ["construction", "engineering"],
    ["design", "work"],
    ["military"],
    ["military"],
    ["construction", "engineering"],
]
L["drag"] = [
    ["farming", "general"],
    ["transportation", "construction"],
    ["transportation", "general"],
    ["animals", "hobby"],
    ["fishing", "engineering"],
    ["transportation", "engineering"],
    ["general"],
    ["general"],
    ["general"],
    ["informal", "general"],
    ["informal", "social"],
    ["informal", "hobby"],
    ["informal", "hobby"],
    ["general"],
    ["general"],
    ["fishing", "general"],
    ["transportation", "engineering"],
    ["farming", "general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["fishing", "general"],
]
L["drama"] = [
    ["arts", "entertainment"],
    ["arts", "entertainment"],
    ["general"],
]
L["dramatic"] = [
    ["arts", "entertainment"],
    ["general"],
]
L["draw"] = [
    ["general"],
    ["general"],
    ["general"],
    ["sports", "general"],
    ["general"],
    ["general"],
    ["engineering", "general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["food", "cooking"],
    ["sports", "general"],
    ["general"],
    ["arts", "design"],
    ["finance", "general"],
    ["sports", "general"],
    ["general"],
    ["sports", "general"],
    ["general"],
    ["general"],
    ["home", "general"],
    ["food", "cooking"],
    ["transportation", "general"],
    ["general"],
    ["general"],
    ["arts", "design"],
]
L["drawing"] = [
    ["general"],
    ["arts", "design"],
    ["arts", "design"],
]
L["dream"] = [
    ["sleep", "general"],
    ["general"],
    ["general"],
    ["sleep", "general"],
    ["general"],
    ["general"],
]
L["dress"] = [
    ["clothing", "general"],
    ["general"],
    ["clothing", "daily life"],
    ["health", "medicine"],
    ["military", "general"],
    ["arts", "entertainment"],
    ["industry", "engineering"],
    ["industry", "engineering"],
    ["clothing", "general"],
    ["farming", "general"],
    ["food", "cooking"],
    ["farming", "general"],
    ["clothing", "daily life"],
    ["clothing", "formal"],
    ["military", "general"],
]
L["dressed"] = [["general"]]
L["drink"] = [
    ["food", "general"],
    ["food", "general"],
    ["food", "general"],
    ["health", "general"],
    ["informal", "nature"],
    ["food", "general"],
    ["general"],
    ["general"],
    ["general"],
    ["food", "social"],
    ["general"],
]
L["drive"] = [
    ["transportation", "general"],
    ["home", "general"],
    ["sports", "general"],
    ["sports", "general"],
    ["general"],
    ["general"],
    ["general"],
    ["sports", "general"],
    ["military", "general"],
    ["engineering", "general"],
    ["engineering", "general"],
    ["general"],
    ["general"],
    ["transportation", "general"],
    ["transportation", "general"],
    ["general"],
    ["general"],
    ["general"],
    ["construction", "general"],
    ["sports", "general"],
    ["technology", "general"],
    ["business", "general"],
    ["general"],
    ["transportation", "general"],
    ["transportation", "general"],
    ["sports", "general"],
    ["general"],
    ["general"],
    ["sports", "general"],
    ["general"],
    ["general"],
    ["farming", "general"],
]
L["driver"] = [
    ["transportation", "work"],
    ["technology"],
]
L["driving"] = [["transportation", "general"]]
L["drop"] = [
    ["general"],
    ["food", "general"],
    ["food", "general"],
    ["clothing", "general"],
    ["general"],
    ["general"],
    ["economy", "general"],
    ["transportation", "general"],
    ["entertainment", "general"],
    ["sports", "general"],
    ["general"],
    ["technology", "general"],
    ["technology", "general"],
    ["military", "general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["economy", "general"],
    ["general"],
    ["animals", "general"],
    ["general"],
    ["general"],
    ["general"],
    ["general"],
    ["farming", "animals"],
    ["general"],
    ["transportation", "general"],
    ["general"],
    ["sports", "general"],
    ["general"],
    ["sports", "general"],
]
L["drug"] = [
    ["health", "medicine"],
    ["health", "medicine"],
    ["business", "general"],
    ["crime", "health"],
    ["health", "medicine"],
    ["sports", "animals"],
    ["health", "medicine"],
    ["general"],
]
L["drum"] = [
    ["music"],
    ["music"],
    ["music", "work"],
    ["body", "health"],
    ["industry", "engineering"],
    ["general"],
    ["food", "social"],
    ["animals"],
    ["music"],
    ["general"],
    ["media", "general"],
    ["animals", "general"],
    ["music"],
    ["general"],
    ["media", "general"],
]
L["drunk"] = [["health", "informal"]]
L["dry"] = [
    ["weather", "general"],
    ["health", "general"],
    ["farming", "general"],
    ["weather", "general"],
    ["food", "general"],
    ["food", "general"],
    ["general"],
    ["personality", "general"],
    ["general"],
    ["arts", "general"],
    ["health", "general"],
    ["general"],
    ["general"],
    ["politics", "general"],
    ["general"],
    ["farming", "general"],
    ["general"],
]
L["due"] = [
    ["general"],
    ["finance", "money"],
    ["finance", "government"],
    ["finance", "general"],
    ["time", "general"],
    ["general"],
    ["general"],
    ["time", "general"],
    ["general"],
]
L["during"] = [["time", "general"]]
L["dust"] = [
    ["general"],
    ["general"],
    ["plants", "general"],
    ["general"],
    ["general"],
    ["general"],
    ["finance", "general"],
    ["general"],
    ["home", "daily life"],
    ["home", "daily life"],
]
L["duty"] = [
    ["general"],
    ["work", "general"],
    ["work", "general"],
    ["finance", "government"],
    ["technology", "engineering"],
]
L["DVD"] = [
    ["technology", "media"],
    ["health", "medicine"],
]
L["each"] = [
    ["general"],
    ["general"],
]
L["ear"] = [
    ["body"],
    ["general"],
    ["body", "general"],
    ["farming", "plants"],
    ["farming", "plants"],
]
L["early"] = [
    ["body"],
    ["general"],
    ["body", "general"],
    ["farming", "plants"],
    ["farming", "plants"],
    ["time", "general"],
]
L["earn"] = [["money", "work"]]
L["earth"] = [
    ["nature", "geography"],
    ["geography", "science"],
    ["nature", "geography"],
    ["animals", "nature"],
    ["general"],
    ["farming", "general"],
    ["animals", "nature"],
    ["animals", "nature"],
    ["technology", "engineering"],
    ["geography", "science"],
]

# validate
errors = []
for item in data:
    w = item["word"]
    if w not in L:
        errors.append("MISSING word: " + w)
        continue
    if len(L[w]) != len(item["meanings"]):
        errors.append("COUNT %s: labels=%d meanings=%d" % (w, len(L[w]), len(item["meanings"])))
extra = [w for w in L if w not in {i["word"] for i in data}]
if extra:
    errors.append("EXTRA words: %s" % extra)
if errors:
    print("\n".join(errors))
    raise SystemExit(1)

outdir = os.path.join(BASE, "ctx_parts", "run3")
os.makedirs(outdir, exist_ok=True)

words = [i["word"] for i in data]
splits = [words[:34], words[34:119], words[119:142], words[142:]]
names = ["chunk_05.txt", "chunk_05b.txt", "chunk_05c.txt", "chunk_05d.txt"]

total_lines = 0
for name, chunk in zip(names, splits):
    lines = []
    for item in data:
        if item["word"] not in chunk:
            continue
        for idx, labels in enumerate(L[item["word"]], start=1):
            lines.append("%s\t%d\t%s" % (item["word"], idx, ", ".join(labels)))
    with open(os.path.join(outdir, name), "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(lines) + "\n")
    total_lines += len(lines)
    print(name, len(lines))

print("words=%d meanings=%d lines=%d" % (len(data), sum(len(i["meanings"]) for i in data), total_lines))
