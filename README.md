# Create: Steam Curios

Steampunk amulets that keep you warm in winter. For **Minecraft 1.21.1 + NeoForge**.

Works standalone, richer with friends:
- **Curios** — amulets are worn in the necklace slot (soft dep)
- **Cold Sweat** — real temperature integration (warms the world temperature, ice resistance) (soft dep)
- **Create** — part of the crafting chain only exists on Create machines (soft dep)

Built with AI (ZCode), authored by Mori. License: GPL-3.0 (links against Cold Sweat's API).

## The amulets

| Item | Tier | How it protects | Craft |
|---|---|---|---|
| Brass Medallion | base | — | crafting table: brass ingots + sheets + glass pane |
| Steam-Warmed Brooch | **Mechanical** | only while it has steam charge | Create sequenced assembly (deployers + spout) |
| Auto-Thermostat | **Automatic** | half passively, full on fuel | Create mechanical crafting 3×3 |
| Isothermal Amulet | **Isothermal** | full, never needs fuel | Create mechanical crafting 5×5 |
| Thermostat Core | intermediate | — | crafting table: precision mechanism + electron tubes + brass |

## Fuel
- Refuel: hold any furnace fuel (coal, planks, coal block…) in the **offhand** and right-click the amulet.
- 1 coal = 1600 burn ticks = 80 s of full protection. Capacity 6400 ticks (4 coals) by default.
- Smart drain (default): fuel only burns while you are actually freezing.
- Steam charge shows as the item durability bar and in the tooltip.

## Protection (how it plays with Cold Sweat)
- Warms Cold Sweat's world temperature by +16 °C-equivalent at full protection (config `liftCelsius`),
  so a blizzard night (~ −12 °C) stays survivable; applies `cold_sweat:ice_resistance` while freezing.
- Without Cold Sweat: cancels cold/temperature damage (freeze and the `steamcurios:cold_damage` tag)
  and works against vanilla freezing; without Curios it also works from the inventory
  (`workWithoutCurios`, on by default).

## Crafting chain (no fallback recipes — by design)
1. **Brass Medallion** — crafting table.
2. **Thermostat Core** — crafting table (needs Create's precision mechanism and electron tubes).
3. **Steam-Warmed Brooch** — Create **sequenced assembly**: medallion → deploy precision mechanism →
   deploy `#cold_sweat:fur` → spout water → done.
4. **Auto-Thermostat** — Create **mechanical crafting** 3×3 (brooch + core + mechanisms + tubes).
5. **Isothermal Amulet** — Create **mechanical crafting** 5×5 (thermostat + chameleon molt +
   nether star + mechanisms, tubes, brass sheets).

## Config (`config/steamcurios-server.toml`)
`enabled`, `workWithoutCurios`, `iceResistance`, `damageReduction` (1.0), `liftCelsius` (16),
`thresholdCelsius` (9.3), `capacityTicks` (6400), `smartDrain` (true).

## Building & running
```
gradlew build      # jar in build/libs/
gradlew runClient  # dev client with Curios + Cold Sweat + Create
```
JDK 21 required. Dependency jars are compile-time only (Curios in `libs/`, Cold Sweat and Create
straight from the local Modrinth pack) — none of them are required at runtime.

## Install
Drop `create-steam-curios-<version>.jar` into `mods/`. If you use Curios, install it too
(tested with curios-neoforge-9.5.1+1.21.1). Works without Curios, Cold Sweat and Create.
