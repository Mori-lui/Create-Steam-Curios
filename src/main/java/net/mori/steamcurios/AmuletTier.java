package net.mori.steamcurios;

/**
 * The three amulet mechanics, one per crafting tier.
 */
public enum AmuletTier {

    /** Fuel-only: protects nothing without steam charge; easiest craft (Create sequenced assembly). */
    MECHANICAL("tooltip.steamcurios.tier.mechanical", true),

    /** Hybrid: half protection passively, full protection while fuelled; middle craft. */
    AUTOMATIC("tooltip.steamcurios.tier.automatic", true),

    /** Passive: full protection, never needs fuel; hardest craft (5x5 mechanical crafting). */
    ISOTHERMAL("tooltip.steamcurios.tier.isothermal", false);

    private final String translationKey;
    private final boolean usesFuel;

    AmuletTier(String translationKey, boolean usesFuel) {
        this.translationKey = translationKey;
        this.usesFuel = usesFuel;
    }

    public String translationKey() {
        return this.translationKey;
    }

    public boolean usesFuel() {
        return this.usesFuel;
    }

    /** Protection fraction this tier provides given whether the stack has fuel. */
    public double fraction(boolean fuelled) {
        return switch (this) {
            case MECHANICAL -> fuelled ? 1.0D : 0.0D;
            case AUTOMATIC -> fuelled ? 1.0D : 0.5D;
            case ISOTHERMAL -> 1.0D;
        };
    }
}
