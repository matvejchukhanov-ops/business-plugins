# business-plugins — набор плагинов Claude для бизнеса

Одиннадцать плагинов в одном пакете: свой «Совет идей» и десять официальных бизнес-плагинов Anthropic.

| Плагин | Что делает |
|---|---|
| **idea-council** | Совет из шести агентов с разными методами мышления + критик. Вместо одного типового ответа — 5–7 нестандартных решений. Команда `/council <задача>` |
| small-business | Малый бизнес: еженедельные брифы, деньги, клиенты, найм, налоги, реклама (~45 навыков) |
| sales | Продажи: подготовка к звонкам, исследование клиентов, воронка, письма |
| marketing | Маркетинг: контент, кампании, конкуренты, SEO, отчёты |
| brand-voice | Голос бренда: собирает стиль из ваших материалов и проверяет тексты |
| finance | Финансы: проводки, сверки, отчётность, анализ отклонений |
| legal | Юридические: проверка договоров, NDA, комплаенс |
| product-management | Управление продуктом: спецификации, роадмап, исследования |
| design | Дизайн: критика макетов, UX-тексты, дизайн-система |
| productivity | Производительность: задачи, план дня, память о контексте |
| enterprise-search | Поиск по всем подключённым инструментам компании |

Плагины Anthropic рассчитаны на западный рынок (право и налоги США), отвечают на языке вопроса.

---

## Как установить

### Вариант 1. Claude Code

В Claude Code выполните:

```
/plugin marketplace add matvejchukhanov-ops/business-plugins
```

Затем установите нужные плагины — через меню `/plugin` или командами:

```
/plugin install idea-council@business-plugins
/plugin install small-business@business-plugins
```

Плагины начинают работать с нового чата. Обновления набора — командой `/plugin marketplace update business-plugins`.

Если на Windows установка падает с ошибкой `Filename too long`, разрешите Git длинные пути и повторите:

```
git config --global core.longpaths true
```

### Вариант 2. Обычный Claude — claude.ai, приложение на компьютере и телефоне, Cowork

1. Откройте **[Customize → Plugins](https://claude.ai/customize/plugins)** (в приложении: «Настроить» → «Плагины»).
2. **Add → Add marketplace** и введите `matvejchukhanov-ops/business-plugins`.
3. Плагины набора появятся в списке — добавьте нужные. Чтобы получать обновления сами, включите у маркетплейса **Sync automatically**.

Что работает где:

| | Обычный чат | Cowork | Claude Code |
|---|---|---|---|
| Навыки | ✅ | ✅ | ✅ |
| Команды (`/council`) | ✅ как навык, выбирается через `/` | ✅ | ✅ |
| Агенты | ❌ | ✅ | ✅ |
| Коннекторы к сервисам | ✅ после подключения | ✅ | ✅ |

В обычном чате агенты не загружаются, поэтому совет идей играет все роли сам по очереди — по тем же методам, результат того же вида, просто дольше. В Cowork и Claude Code мыслители работают параллельно.

Плагин, добавленный на claude.ai, автоматически появляется и в Claude Code под тем же аккаунтом.

Без GitHub: **Add → Upload plugin** и загрузите `.zip` плагина из [Releases](https://github.com/matvejchukhanov-ops/business-plugins/releases), если они там выложены.

### Вариант 3. Без GitHub — из архива

Распакуйте `business-plugins.zip` (например в `C:usiness-plugins`) и в Claude Code выполните `/plugin marketplace add C:usiness-plugins`, дальше как в варианте 1.

### Сколько ставить

Каждый плагин добавляет в чат описания своих навыков, а это токены. Ставьте то, чем реально пользуетесь: для начала хватит `idea-council` + `small-business` + 1–2 по профилю.

---

## Для автора набора: как обновлять

- Методы мыслителей и критика — `tools/build_agents.py`, общие правила — `tools/thinker-rules.md`; после правки `python tools/build_agents.py`.
- Порядок работы совета — `plugins/idea-council/skills/idea-council/SKILL.md`.
- Пересобрать весь набор (свежие версии плагинов Anthropic из кэша Claude Code + архивы в `dist/`): `python tools/build_bundle.py`.
- Выпуск для друзей: закоммитить и запушить, затем на GitHub создать Release и приложить архивы из `dist/claude-app/` и `dist/business-plugins.zip` (сама папка `dist/` в git не хранится).
- Поднимите `version` в `plugin.json` изменённого плагина, иначе у пользователей он не обновится.
- Обновить у себя (PowerShell):

```powershell
$cl = (Get-ChildItem "$env:APPDATA\Claude\claude-code\*\*\claude.exe" | Sort-Object LastWriteTime | Select-Object -Last 1).FullName
& $cl plugin marketplace update business-plugins
& $cl plugin update idea-council@business-plugins
```

Происхождение и лицензии — `NOTICE.md`.
