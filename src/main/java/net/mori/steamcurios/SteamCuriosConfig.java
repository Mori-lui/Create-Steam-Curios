package net.mori.steamcurios;

import net.neoforged.neoforge.common.ModConfigSpec;

/**
 * Temperature numbers follow Cold Sweat's units: 1 MC unit = 42 F = 23.333 C, 0 MC = 0 C.
 * Cold Sweat starts freezing the player below +0.4 MC (+9.3 C) world temperature by default.
 */
public final class SteamCuriosConfig {

    public static final ModConfigSpec SPEC;

    public static final ModConfigSpec.BooleanValue ENABLED;
    public static final ModConfigSpec.BooleanValue ICE_RESISTANCE;
    public static final ModConfigSpec.DoubleValue DAMAGE_REDUCTION;
    public static final ModConfigSpec.DoubleValue LIFT_CELSIUS;
    public static final ModConfigSpec.DoubleValue THRESHOLD_CELSIUS;

    public static final ModConfigSpec.IntValue FUEL_CAPACITY_TICKS;
    public static final ModConfigSpec.BooleanValue SMART_DRAIN;

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
        LIFT_CELSIUS = builder
                .comment("How much the amulet warms Cold Sweat's world temperature at full protection,",
                         "in degrees Celsius (the passive half-tier gets half of this).",
                         "For reference: a blizzard-night drop is 8-14 C; freezing starts below +9.3 C.")
                .defineInRange("liftCelsius", 16.0D, 0.0D, 40.0D);
        THRESHOLD_CELSIUS = builder
                .comment("World temperature below which the amulet counts as needed (fuel only burns",
                         "while needed, with smartDrain).")
                .defineInRange("thresholdCelsius", 9.3D, -20.0D, 40.0D);
        builder.pop();

        builder.push("fuel");
        FUEL_CAPACITY_TICKS = builder
                .comment("Maximum steam charge one amulet can hold, in ticks.",
                         "One coal smelts for 1600 ticks = 80 seconds of protection; 6400 = 4 coals.")
                .defineInRange("capacityTicks", 6400, 400, 1024000);
        SMART_DRAIN = builder
                .comment("Only burn fuel while the player is actually cold-stressed.",
                         "false = fuel burns whenever the amulet is worn.")
                .define("smartDrain", true);
        builder.pop();

        SPEC = builder.build();
    }

    private SteamCuriosConfig() {
    }

    /** Configured cold-stress threshold in Cold Sweat MC units. */
    public static double thresholdMc() {
        return THRESHOLD_CELSIUS.get() * MC_PER_CELSIUS;
    }

    /** Configured world-temperature lift at full protection, in MC units. */
    public static double liftMc() {
        return LIFT_CELSIUS.get() * MC_PER_CELSIUS;
    }
}
