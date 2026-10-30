package net.mori.steamcurios;

import com.momosoftworks.coldsweat.api.temperature.modifier.TempModifier;
import com.momosoftworks.coldsweat.api.util.Temperature;
import net.minecraft.world.entity.LivingEntity;

import java.util.function.Function;

/**
 * Warms Cold Sweat's WORLD temperature by the live amulet lift while any amulet
 * protects the player. The lift is read on every calculate() so fuel state and
 * tier changes apply without re-adding the modifier.
 */
public class SteamWarmthModifier extends TempModifier {

    public SteamWarmthModifier() {
    }

    @Override
    protected Function<Double, Double> calculate(LivingEntity entity, Temperature.Trait trait) {
        double lift = SteamLogic.currentLiftMc(entity);
        if (Math.abs(lift) < 1.0E-4D) {
            return temp -> temp;
        }
        return temp -> temp + lift;
    }

    /** Public test hook: applies this modifier's function to a base temperature. */
    public double applyTo(double base, LivingEntity entity) {
        return this.calculate(entity, Temperature.Trait.WORLD).apply(base);
    }
}
