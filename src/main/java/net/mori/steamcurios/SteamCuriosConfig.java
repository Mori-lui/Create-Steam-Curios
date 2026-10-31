package net.mori.steamcurios;

import net.neoforged.neoforge.common.ModConfigSpec;

/**
 * Temperature numbers follow Cold Sweat's units: 1 MC unit = 42 F = 23.333 C, 0 MC = 0 C.
 * Cold Sweat starts freezing the player below +0.4 MC (+9.3 C) world temperature by default.
 * The amulet never warms above comfortCelsius, so it cannot overheat the player.
 */
public final class SteamCuriosConfig {

    public static final ModConfigSpec SPEC;

    public static final ModConfigSpec.BooleanValue ENABLED;
    public static final ModConfigSpec.BooleanValue ICE_RESISTANCE;
    public static final ModConfigSpec.DoubleValue DAMAGE_REDUCTION;
    public static final ModConfigSpec.DoubleValue MAX_LIFT_CELSIUS;
    public static final ModConfigSpec.DoubleValue COMFORT_CELSIUS;
    public static final ModConfigSpec.DoubleValue THRESHOLD_CELSIUS;

    public static final ModConfigSpec.IntValue FUEL_CAPACITY_TICKS;
    public static final ModConfigSpec.IntValue WATER_CAPACITY_UNITS;
    public static final ModConfigSpec.IntValue WATER_UNIT_TICKS;
    public static final ModConfigSpec.IntValue BOTTLE_UNITS;
    public static final ModConfigSpec.IntValue BUCKET_UNITS;
    public static final ModConfigSpec.BooleanValue SMART_DRAIN;

    public static final ModConfigSpec.BooleanValue CHUFF_ENABLED;
    public static final ModConfigSpec.IntValue CHUFF_MIN_INTERVAL;
    public static final ModConfigSpec.IntValue CHUFF_MAX_INTERVAL;

    public static final ModConfigSpec.BooleanValue WORK_WITHOUT_CURIOS;

    public static final double MC_PER_CELSIUS = 1.0D / (42.0D / 1.8D);

    static {
        ModConfigSpec.Builder builder = new ModConfigSpec.Builder();

        builder.push("general");
        ENABLED = builder
                .comment("Master switch for all amulet protection.")
                .define("enabled", true);
        WORK_WITHOUT_CURIOS = builder
                .comment("When the Curios mod is absent, amulets protect from anywhere in the inventory.",
                         "With Curios present, amulets only work while worn in a curio slot.")
                .define("workWithoutCurios", true);
        builder.pop();

        builder.push("protection");
        ICE_RESISTANCE = builder
                .comment("Full-tier amulets apply Cold Sweat's ice_resistance effect while cold-stressed",
                         "(only when Cold Sweat is installed).")
                .define("iceResistance", true);
        DAMAGE_REDUCTION = builder
                .comment("Share of cold/temperature damage removed at full protection (0 to 1).",
                         "The hybrid tier gets half of this passively, the full amount while fuelled.")
                .defineInRange("damageReduction", 1.0D, 0.0D, 1.0D);
        MAX_LIFT_CELSIUS = builder
                .comment("Maximum world-temperature lift the amulet can produce, in degrees Celsius.",
                         "The lift is adaptive: it only warms up TO comfortCelsius, never above,",
                         "so a worn amulet cannot overheat you in mild weather.")
                .defineInRange("maxLiftCelsius", 16.0D, 0.0D, 40.0D);
        COMFORT_CELSIUS = builder
                .comment("Target world temperature the amulet warms you up to, in degrees Celsius.",
                         "Below comfort it heats (as much as maxLift allows), at/above it does nothing.")
                .defineInRange("comfortCelsius", 15.0D, -5.0D, 30.0D);
        THRESHOLD_CELSIUS = builder
                .comment("World temperature below which Cold Sweat starts freezing (reference value",
                         "used for ice_resistance timing; Cold Sweat's own config stays authoritative).")
                .defineInRange("thresholdCelsius", 9.3D, -20.0D, 40.0D);
        builder.pop();

        builder.push("fuel");
        FUEL_CAPACITY_TICKS = builder
                .comment("Maximum steam charge one amulet can hold, in ticks.",
                         "Fuel value = the item's furnace burn time: a plank adds 15 s,",
                         "a coal 80 s, a coal block 800 s. Right-click with it in the offhand.")
                .defineInRange("capacityTicks", 6400, 400, 1024000);
        builder.comment("Water is consumed to make steam: while the boiler burns, one water unit",
                        "evaporates every waterUnitTicks. Bottle adds bottleUnits, a bucket bucketUnits.");
        WATER_CAPACITY_UNITS = builder
                .comment("Maximum water units one amulet can hold.")
                .defineInRange("waterCapacity", 12, 1, 64);
        WATER_UNIT_TICKS = builder
                .comment("Ticks of steaming that evaporate one water unit (20 ticks = 1 s).")
                .defineInRange("waterUnitTicks", 320, 20, 72000);
        BOTTLE_UNITS = builder
                .comment("Water units added by one water bottle (the empty bottle is returned).")
                .defineInRange("bottleUnits", 3, 1, 64);
        BUCKET_UNITS = builder
                .comment("Water units added by one water bucket (the empty bucket is returned).")
                .defineInRange("bucketUnits", 12, 1, 64);
        SMART_DRAIN = builder
                .comment("Only burn fuel and evaporate water while the amulet is actually heating",
                         "(world temperature below comfort). false = burns whenever worn.")
                .define("smartDrain", true);
        builder.pop();

        builder.push("sound");
        CHUFF_ENABLED = builder
                .comment("Steam locomotive chuff while the boiler is running.")
                .define("chuffEnabled", true);
        CHUFF_MIN_INTERVAL = builder
                .comment("Minimum seconds between chuffs while steaming.")
                .defineInRange("chuffMinInterval", 4, 1, 60);
        CHUFF_MAX_INTERVAL = builder
                .comment("Maximum seconds between chuffs while steaming.")
                .defineInRange("chuffMaxInterval", 9, 1, 120);
        builder.pop();

        SPEC = builder.build();
    }

    private SteamCuriosConfig() {
    }

    /** Cold-stress reference threshold in Cold Sweat MC units. */
    public static double thresholdMc() {
        return THRESHOLD_CELSIUS.get() * MC_PER_CELSIUS;
    }

    /** Comfort target in MC units. */
    public static double comfortMc() {
        return COMFORT_CELSIUS.get() * MC_PER_CELSIUS;
    }

    /** Maximum lift in MC units. */
    public static double maxLiftMc() {
        return MAX_LIFT_CELSIUS.get() * MC_PER_CELSIUS;
    }
}
