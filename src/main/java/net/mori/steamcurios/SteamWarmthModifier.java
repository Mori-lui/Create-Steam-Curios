package net.mori.steamcurios;

import com.momosoftworks.coldsweat.api.temperature.modifier.TempModifier;
import com.momosoftworks.coldsweat.api.util.Temperature;
import net.minecraft.world.entity.LivingEntity;

import java.util.function.Function;

/**
 * Warms Cold Sweat's WORLD temperature adaptively: only up to the comfort point,
 * never above it, so the amulet cannot overheat the player in mild weather.
 * The lift is read on every calculate() so fuel/water state applies live.
 */
public class SteamWarmthModifier extends TempModifier {

    public SteamWarmthModifier() {
    }

    @Override
    protected Function<Double, Double> calculate(LivingEntity entity, Temperature.Trait trait) {
        return temp -> temp + SteamLogic.liftForFractionAt(
                SteamLogic.bestFraction((net.minecraft.world.entity.player.Player) entity), temp);
    }

    /** Public test hook: applies this modifier's function to a base temperature. */
    public double applyTo(double base, LivingEntity entity) {
        return this.calculate(entity, Temperature.Trait.WORLD).apply(base);
    }
}
