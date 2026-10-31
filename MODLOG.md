# MODLOG — Create: Steam Curios (Minecraft 1.21.1, NeoForge)

## Task
Steampunk amulets against the COLD (no heat line — user's winter pack): Curios necklace items in three
mechanical tiers, fuelled by furnace fuel, crafted partly on the vanilla table, partly only via Create
(no fallback recipes). User decisions (2026-10-30):
- three tiers: mechanical = fuel-only, easiest craft (Create precision mechanisms);
  automatic = hybrid (passive half + full on fuel), middle craft; isothermal = passive full, hardest craft;
- NO fallback recipes: some crafts vanilla-table-only, some Create-only;
- heat protection REMOVED entirely (winter pack);
- Cold Sweat: soft dep, deep integration when present + universal vanilla mode when absent;
- Create: soft dep, data-only (no Create classes in code);
- Curios: soft dep (adapter via CuriosApi.registerCurio, no `implements ICurioItem` on the item class);
- textures: own (Pillow, no fal key configured); art tier Б (icons + body model + steam particles);
  animations as a separate addon mod `steamcurios_animated`;
- config like the original + fuel; en/ru/uk localization; creative tab; advancement "Thermostat";
- author Mori, package net.mori.steamcurios, modid steamcurios, license GPL-3.0 (Cold Sweat linking);
- deploy into the user's Modrinth pack (same as blizzard-nights), adding Curios there (user approved).

## Environment (recon facts, nothing modified yet)
- JDK: C:\Program Files\Java\jdk-21.0.10 (javac works); Gradle 8.14.3 cached dist:
  `~/.gradle/wrapper/dists/gradle-8.14.3-bin/cv11ve7ro1n3o1j4so8xd9n66/gradle-8.14.3/bin/gradle`
- Template project (same user, works): `D:\mods\blizzard-nights` — MDG 2.0.148, neo 21.1.264,
  processResources expand neoforge.mods.toml (KB gotcha), compileOnly jars straight from the pack mods dir.
- Pack: `C:\Users\mori.DESKTOP-M97RSVL\AppData\Roaming\ModrinthApp\profiles\xyz\mods`
  (63 mods: ColdSweat-2.4.4, create-1.21.1-6.0.10, hoarfrost, blizzard-nights-0.2.0 deployed; NO Curios).
- Curios 9.5.1+1.21.1 (neoforge) downloaded from Modrinth into `libs/` (gitignored).
- Reference jar HotandColdCurios 1.4.1 (MCreator, ARR) extracted to %TEMP%\hcc141 — structure reference only,
  nothing copied.

## API facts (verified from jars, not memory)
- Curios 9.5.1: `ICurioItem.curioTick(SlotContext, ItemStack)` etc.; SlotContext record: identifier()/
  entity()/index(). `CuriosApi.registerCurio(Item, ICurioItem)` — attach behaviour without implementing
  the interface. `CuriosRendererRegistry.register(Item, Supplier<ICurioRenderer>)` client-side.
  `ICurioRenderer.render(stack, SlotContext, PoseStack, RenderLayerParent, MultiBufferSource, light, 6 floats)`
  + helpers rotateIfSneaking/followBodyRotations. Slot types: `data/curios/curios/slots/*.json`
  (validator "curios:tag"); item→slot binding = `data/curios/tags/item/necklace.json` (SINGULAR folders).
  Default player slots: unknown yet — check at first runClient (/curios), add
  `data/curios/curios/entities/builtin/players.json` if necklace not granted by default.
- Cold Sweat 2.4.4: TempModifier: `calculate(LivingEntity, Trait) -> Function<Double,Double>`, tick(entity),
  getNBT(); register: TempModifierRegisterEvent.register(id, supplier) (game bus, like blizzard-nights).
  Per-entity: `Temperature.addModifier(entity, modifier, Trait, Placement)`,
  `Temperature.removeModifiers(entity, Trait, Predicate|Class)`, `Temperature.get(entity, Trait)` (MC units,
  0 MC = 0 °C, 1 MC = 23.333 °C, freezing below +0.4 MC = +9.3 °C). Effects by registry id:
  `cold_sweat:ice_resistance`, `cold_sweat:grace`.
- Create 6.0.10 (data only): SA recipe = `data/create/recipe/sequenced_assembly/...` shape (see
  precision_mechanism.json: ingredient, loops, results[{id,chance}], sequence[{type create:deploying,
  ingredients [transitional, held], results}], transitional_item). Mechanical crafting: type
  create:mechanical_crafting, accept_mirrored, key, pattern, result{id,count}. Spouting format NOT in
  Create's own data — runtime-verify, plan B = deploying water_bucket/keepHeldItem.
- Items used: create:brass_ingot, create:brass_sheet, create:precision_mechanism, create:electron_tube,
  cold_sweat:chameleon_molt, tag cold_sweat:fur, cold_sweat:soulspring_lamp (auto 3x3), minecraft:nether_star.

## Item set (5 + 1 transitional)
| id | name | tier |
|---|---|---|
| brass_medallion | Brass Medallion | base (table: brass+glass_pane) |
| thermostat_core | Thermostat Core | intermediate (table: mechanism+tubes+brass) |
| incomplete_heater_charm | Unfinished Steam Brooch | SA transitional item |
| steam_heater_charm | Steam-Warmed Brooch | MECHANICAL (fuel-only), Create SA |
| auto_thermostat | Auto-Thermostat | AUTOMATIC (hybrid), Create mech 3x3 |
| isothermal_amulet | Isothermal Amulet | ISOTHERMAL (passive full), Create mech 5x5 |

Fuel: data component steamcurios:fuel_ticks; refuel = use() with furnace fuel in offhand; 1 coal = 1600
burn ticks (200 × 8); smart drain only while cold-stressed (CS world temp < threshold / vanilla: frozen);
steam CLOUD particles while burning; fuel shown as item durability-style bar (getBarWidth).

## Log
- (entries appended as work happens)

## Log
- 2026-10-31: build.gradle: localRuntime (NeoGradle-ism) -> runtimeOnly; DeferredRegister.createItems for
  registerSimpleItem; TAB is DeferredHolder; SoundEvents.FLINTANDSTEEL_USE; @EventBusSubscriber without
  deprecated bus attr. First clean build OK, jar contents verified (mods.toml expanded).
- runClient (dev): "[steamcurios] loaded; curios: true, cold_sweat: true, create: true" — soft deps OK,
  window renders, no errors from the mod. Killed client (PID kill) before gametests.
- GameTests: MDG run type is `type = "gameTestServer"` (no gameTestServer() factory); @GameTest is the
  VANILLA annotation (net.minecraft.gametest.framework.GameTest), only GameTestHolder/PrefixGameTestTemplate
  are neoforge.gametest; template must be "empty3x3" (namespace auto-prefixed -> double-ns crash otherwise);
  Registry has no get(TagKey) in 1.21.1 -> getTag; TempModifier.calculate is protected -> public applyTo hook.
  Empty structure template generated with tools/gen_structure.py (gzip NBT, DataVersion 3955).
- **Create 6.0.10 gotcha: `create:spouting` is NOT a recipe serializer (JEI-only category)** — SA recipe
  with a spouting step fails to parse ("Unknown registry key in ... recipe_serializer"). Replaced the
  water step with `create:deploying` + minecraft:water_bucket (deployer holds the bucket).
- GameTest round 2: ALL 6 TESTS PASS (items, necklace tag, 5 recipes no errors, fuel/tiers, damage tags,
  CS lift modifier add/remove + liftForFraction math). Mock players have no Curios capability -> worn-path
  lift can't be tested headless; verified in real game next.
- Deployed create-steam-curios-0.1.0.jar + curios-neoforge-9.5.1+1.21.1.jar into the pack mods/.
- Addon steamcurios_animated: resources-only jar (lowcodefml), animated item icons (mcmeta strips),
  depends on steamcurios. Visual override order = mod load order (addon loads after steamcurios).
- **Real-game bug found (user report): items could not be equipped anywhere.** Root cause: in Curios 9.5.1
  the player has NO necklace slot at all — the widget showed only Head and Charm (Curios' internal
  defaults). Slot TYPES (data/curios/curios/slots/*.json) and the item->slot TAG are not enough: which
  entities get which slots is entities data `data/<ns>/curios/entities/<name>.json`
  ({"entities":["player"],"slots":["necklace"]}); Curios ships none and merges files unless "replace":true.
  CuriosEntityManager source confirmed (SimpleJsonResourceReloadListener "curios/entities", config slots
  only as player fallback). Fix: data/steamcurios/curios/entities/player.json granting necklace +
  GameTest playerHasNecklaceSlot. Head/Charm in dev come from Curios' own defaults (not configs:
  curios-common.toml slots=[] and server toml has no slots list).
- UI note: in the curios widget the small circle is "Toggle Visibility" (cosmetic render toggle); the
  BUTTON itself is the slot (drag onto it); shift-click also targets first valid slot.
- **Pack bug (user report round 2): necklace still missing + SA recipe invisible in JEI in the pack, dev OK.**
  Root cause: the pack jar was the ORIGINAL first build — `gradle runGameTestServer`/`runClient` do NOT
  rebuild the jar; both earlier `cp`s copied the stale build/libs jar (spouting recipe -> SA parse error ->
  JEI shows nothing; no player.json -> no necklace). Dev worked because runs execute build/classes+resources.
  Lesson: deploy only after a real `gradle build`; verify jar contents (entities file present, no 'spouting').
  Fixed: rebuilt 12:12, verified, redeployed. User must restart the pack.
- Create fact: manual "Item Application" (RightClickBlock hook) works only on BLOCKS (brass casing etc.);
  item-on-item steps of SA require deployers. Minimal brooch rig: depot + 3 deployers facing it (held:
  precision mechanism / #cold_sweat:fur / water bucket) + rotation; deployers may fire in any order
  (wrong step is a no-op); result lands back on the depot.
- **User correction confirmed: `cold_sweat:fur` tag does NOT exist in CS 2.4.4** (the old tag came from the
  1.20.1 reference mod, which shipped it itself). Goat fur item = cold_sweat:goat_fur. Fix: own tag
  data/steamcurios/tags/item/fur.json (goat_fur, optional entry) + SA recipe now uses steamcurios:fur;
  gametest furTagContainsGoatFur. 8/8 tests, real gradle build, jar verified, redeployed.
