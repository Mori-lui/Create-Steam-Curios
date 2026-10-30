package net.mori.steamcurios;

import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;

/**
 * Core amulet behaviour, free of Curios and Cold Sweat imports (those live in
 * CuriosCompat / ColdSweatCompat and are only touched through the loaded flags).
 */
public final class SteamLogic {

    private SteamLogic() {
    }

    public static boolean isColdStressed(LivingEntity entity) {
        if (SteamCuriosMod.COLD_SWEAT_LOADED) {
            return ColdSweatCompat.isColdStressed(entity);
        }
        return entity.getTicksFrozen() > 0;
    }

    public static int getFuel(ItemStack stack) {
        return stack.getOrDefault(ModComponents.FUEL_TICKS.get(), 0);
    }

    public static void setFuel(ItemStack stack, int fuel) {
        if (fuel <= 0) {
            stack.remove(ModComponents.FUEL_TICKS.get());
        } else {
            stack.set(ModComponents.FUEL_TICKS.get(), fuel);
        }
    }

    /** Protection fraction of a single amulet stack, accounting for its fuel. */
    public static double stackFraction(ItemStack stack) {
        if (!(stack.getItem() instanceof SteamAmuletItem amulet)) {
            return 0.0D;
        }
        boolean fuelled = !amulet.tier().usesFuel() || getFuel(stack) > 0;
        return amulet.tier().fraction(fuelled);
    }

    /** Called every tick from the Curios slot while worn. */
    public static void serverAmuletTick(LivingEntity entity, ItemStack stack) {
        if (entity.level().isClientSide()) {
            return;
        }
        if (!(stack.getItem() instanceof SteamAmuletItem amulet)) {
            return;
        }
        boolean stressed = isColdStressed(entity);
        int fuel = getFuel(stack);
        boolean drain = amulet.tier().usesFuel() && fuel > 0
                && (!SteamCuriosConfig.SMART_DRAIN.get() || stressed);
        if (drain) {
            setFuel(stack, fuel - 1);
            if (entity.tickCount % 10 == 0) {
                spawnSteam(entity);
            }
        }
        if (entity.tickCount % 20 == 0 && stressed && SteamCuriosMod.COLD_SWEAT_LOADED
                && SteamCuriosConfig.ICE_RESISTANCE.get()
                && stackFraction(stack) >= 0.999D) {
            ColdSweatCompat.applyIceResistance(entity);
        }
    }

    /** 20-times-per-second fallback tick when Curios is absent (inventory amulet). */
    public static void inventoryPulse(Player player, ItemStack stack) {
        if (!(stack.getItem() instanceof SteamAmuletItem amulet) || player.level().isClientSide()) {
            return;
        }
        boolean stressed = isColdStressed(player);
        int fuel = getFuel(stack);
        boolean drain = amulet.tier().usesFuel() && fuel > 0
                && (!SteamCuriosConfig.SMART_DRAIN.get() || stressed);
        if (drain) {
            setFuel(stack, Math.max(0, fuel - 20));
            spawnSteam(player);
        }
        if (stressed && SteamCuriosMod.COLD_SWEAT_LOADED
                && SteamCuriosConfig.ICE_RESISTANCE.get()
                && stackFraction(stack) >= 0.999D) {
            ColdSweatCompat.applyIceResistance(player);
        }
    }

    private static void spawnSteam(LivingEntity entity) {
        if (!(entity.level() instanceof ServerLevel level)) {
            return;
        }
        level.sendParticles(ParticleTypes.CLOUD,
                entity.getX(), entity.getEyeY() - 0.35D, entity.getZ(),
                1, 0.08D, 0.05D, 0.08D, 0.004D);
    }

    /** The best amulet stack protecting this player: worn (Curios) or carried (fallback). */
    public static ItemStack findBestStack(Player player) {
        if (SteamCuriosMod.CURIOS_LOADED) {
            return CuriosCompat.findBestWorn(player);
        }
        if (!SteamCuriosConfig.WORK_WITHOUT_CURIOS.get()) {
            return null;
        }
        ItemStack best = null;
        double bestFraction = -1.0D;
        for (ItemStack stack : player.getInventory().items) {
            double fraction = stackFraction(stack);
            if (fraction > bestFraction) {
                bestFraction = fraction;
                best = stack;
            }
        }
        double offhandFraction = stackFraction(player.getOffhandItem());
        if (offhandFraction > bestFraction) {
            best = player.getOffhandItem();
        }
        return best;
    }

    public static double bestFraction(Player player) {
        ItemStack best = findBestStack(player);
        return best == null ? 0.0D : stackFraction(best);
    }

    /** World-temperature lift for a protection fraction, in Cold Sweat MC units. */
    public static double liftForFraction(double fraction) {
        if (fraction <= 0.0D || !SteamCuriosConfig.ENABLED.get()) {
            return 0.0D;
        }
        return SteamCuriosConfig.liftMc() * fraction;
    }

    /** Current world-temperature lift in Cold Sweat MC units; read live by the TempModifier. */
    public static double currentLiftMc(LivingEntity entity) {
        if (!(entity instanceof Player player)) {
            return 0.0D;
        }
        return liftForFraction(bestFraction(player));
    }
}
