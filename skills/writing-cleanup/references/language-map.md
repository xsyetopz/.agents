# Multilingual developer action map

Use these as starting points for plain developer instructions. Native review is
required for user-facing, safety-critical, or legally binding text. Translate
the surrounding sentence, not the command token.

| Action | English | German | Polish | French | Japanese |
| --- | --- | --- | --- | --- | --- |
| check | check | prüfen | sprawdzić | vérifier | 確認する |
| inspect | inspect | prüfen / untersuchen | sprawdzić / zbadać | inspecter / examiner | 調べる |
| run | run | ausführen | uruchomić | exécuter | 実行する |
| test | test | testen | testować | tester | テストする |
| deploy | deploy | bereitstellen | wdrożyć | déployer | デプロイする |
| parse | parse | parsen / analysieren | parsować / analizować | analyser / parser | パースする / 解析する |
| sync | sync | synchronisieren | synchronizować | synchroniser | 同期する |
| init | init | initialisieren | zainicjować | initialiser | 初期化する |
| exec | exec | ausführen | wykonać | exécuter | 実行する |
| replace | replace | ersetzen | zastąpić | remplacer | 置き換える |
| keep | keep | beibehalten | zachować | conserver | 維持する |
| rewrite | rewrite | neu formulieren | przeredagować | reformuler | 書き直す |
| translate | translate | übersetzen | przetłumaczyć | traduire | 翻訳する |
| use | use | verwenden | używać | utiliser | 使う |
| facilitate as help | help | helfen | pomóc | aider | 助ける |
| leverage as use | use | verwenden | użyć | utiliser | 使う |
| robust as reliable | reliable | zuverlässig | niezawodny | fiable | 信頼できる |

## Boundary rules

- Keep exec, init, sync, run, check, test, deploy, parse, inspect, and format
  unchanged inside commands, code, API names, protocols, and formal contracts.
- Translate “Run bun test” as a localized sentence while preserving bun test.
- Prefer the established borrowed term when a literal translation would make a
  developer instruction less clear.
- Do not translate product names, option names, environment variables, file
  paths, error strings, or citations.
- Avoid idioms, culture-bound jokes, unexplained abbreviations, and English
  word order. Check locale-specific punctuation and number formatting.

For a broad-surface audit, inspect filenames, flags, and identifiers as well as
sentences. Use the shortest established form for repository-owned names; do not
rename an external command or compatibility surface without an explicit
migration decision.
