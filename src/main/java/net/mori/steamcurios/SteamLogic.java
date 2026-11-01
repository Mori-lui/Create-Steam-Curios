package net.mori.steamcurios;

import net.minecraft.core.component.DataComponents;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundSource;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;

import java.util.concurrent.ThreadLocalRandom;

/**
 * Core amulet behaviour, free of Curios imports (that part lives in CuriosCompat).
 * Cold Sweat access is guarded by COLD_SWEAT_LOADED.
 *
 * Heating is adaptive: the amulet warms the world temperature only UP TO the comfort
 * point, never above, so it cannot overheat the player in mild weather.
 * Steam needs both fuel and water; both deplete while actually heating.
 */
public final class SteamLogic {

    /** Display states driving the custom_model_data texture overrides. */
    public static final int STATE_IDLE = 0;
    public static final int STATE_STEAMING = 1;
    public static final int STATE_DRY = 2; // has fuel but no water

    private SteamLogic() {
    }

    public static boolean isColdStressed(LivingEntity entity) {
        if (SteamCuriosMod.COLD_SWEAT_LOADED) {
            return ColdSweatCompat.isColdStressed(entity);
        }
        return entity.getTicksFrozen() > 0;
    }

    /** Current world temperature in MC units (Cold Sweat), or a vanilla proxy. */
    public static double worldTempMc(LivingEntity entity) {
        if (SteamCuriosMod.COLD_SWEAT_LOADED) {
            return ColdSweatCompat.worldTemp(entity);
        }
        // crude vanilla proxy: freezing ticks map to "below zero", else temperate
        return entity.getTicksFrozen() > 0 ? -0.5D : 1.0D;
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

    public static int getWater(ItemStack stack) {
        return stack.getOrDefault(ModComponents.WATER_UNITS.get(), 0);
    }

    public static void setWater(ItemStack stack, int water) {
        if (water <= 0) {
            stack.remove(ModComponents.WATER_UNITS.get());
        } else {
            stack.set(ModComponents.WATER_UNITS.get(), water);
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

    /**
     * Adaptive lift for a protection fraction at a given world temperature:
     * warm only up to comfort, capped by maxLift, scaled by the fraction.
     */
    public static double liftForFractionAt(double fraction, double tempMc) {
        if (fraction <= 0.0D || !SteamCuriosConfig.ENABLED.get()) {
            return 0.0D;
        }
        double wanted = SteamCuriosConfig.comfortMc() - tempMc;
        if (wanted <= 0.0D) {
            return 0.0D;
        }
        double lift = Math.min(wanted, SteamCuriosConfig.maxLiftMc());
        return lift * fraction;
    }

    /** True while this stack should burn: fuel + water present and the player below comfort. */
    public static boolean isSteaming(LivingEntity entity, ItemStack stack) {
        if (!(stack.getItem() instanceof SteamAmuletItem amulet) || !amulet.tier().usesFuel()) {
            return false;
        }
        if (getFuel(stack) <= 0 || getWater(stack) <= 0) {
            return false;
        }
        if (SteamCuriosConfig.SMART_DRAIN.get()) {
            return worldTempMc(entity) < SteamCuriosConfig.comfortMc();
        }
        return true;
    }

    /** Called every tick from the Curios slot while worn. */
    public static void serverAmuletTick(LivingEntity entity, ItemStack stack) {
        if (entity.level().isClientSide() || entity.tickCount % 20 != 0) {
            return;
        }
        if (!(stack.getItem() instanceof SteamAmuletItem amulet)) {
            return;
        }
        boolean steaming = isSteaming(entity, stack);
        if (steaming) {
            setFuel(stack, getFuel(stack) - 20);
            int water = getWater(stack);
            int unitTicks = Math.max(20, SteamCuriosConfig.WATER_UNIT_TICKS.get());
            if (entity.tickCount % Math.max(20, unitTicks) == 0 || unitTicks <= 20) {
                setWater(stack, water - 1);
            }
            spawnSteam(entity);
            chuff(entity);
        }
        if (entity.tickCount % 20 == 0 && isColdStressed(entity)
                && SteamCuriosMod.COLD_SWEAT_LOADED && SteamCuriosConfig.ICE_RESISTANCE.get()
                && stackFraction(stack) >= 0.999D) {
            ColdSweatCompat.applyIceResistance(entity);
        }
        updateState(stack, steaming);
    }

    /** 1-second fallback tick when Curios is absent (inventory amulet). */
    public static void inventoryPulse(Player player, ItemStack stack) {
        if (!(stack.getItem() instanceof SteamAmuletItem) || player.level().isClientSide()) {
            return;
        }
        boolean steaming = isSteaming(player, stack);
        if (steaming) {
            setFuel(stack, getFuel(stack) - 20);
            setWater(stack, getWater(stack) - 1);
            spawnSteam(player);
            chuff(player);
        }
        if (isColdStressed(player) && SteamCuriosMod.COLD_SWEAT_LOADED
                && SteamCuriosConfig.ICE_RESISTANCE.get() && stackFraction(stack) >= 0.999D) {
            ColdSweatCompat.applyIceResistance(player);
        }
        updateState(stack, steaming);
    }

    private static void updateState(ItemStack stack, boolean steaming) {
        int state = steaming ? STATE_STEAMING
                : (getFuel(stack) > 0 && getWater(stack) <= 0) ? STATE_DRY : STATE_IDLE;
        Integer current = stack.get(ModComponents.STATE.get());
        if (current == null || current != state) {
            stack.set(ModComponents.STATE.get(), state);
            stack.set(DataComponents.CUSTOM_MODEL_DATA, new net.minecraft.world.item.component.CustomModelData(state));
        }
    }

    private static void spawnSteam(LivingEntity entity) {
        if (!(entity.level() instanceof ServerLevel level)) {
            return;
        }
        level.sendParticles(ParticleTypes.CLOUD,
                entity.getX(), entity.getEyeY() - 0.3D, entity.getZ(),
                2, 0.12D, 0.08D, 0.12D, 0.01D);
    }

    private static void chuff(LivingEntity entity) {
        if (!SteamCuriosConfig.CHUFF_ENABLED.get()
                || !(entity.level() instanceof ServerLevel level)) {
            return;
        }
        int min = SteamCuriosConfig.CHUFF_MIN_INTERVAL.get();
        int max = Math.max(min + 1, SteamCuriosConfig.CHUFF_MAX_INTERVAL.get());
        if (ThreadLocalRandom.current().nextInt((max - min) * 20) < 20) {
            level.playSound(null, entity.blockPosition(), ModComponents.CHUFF.get(),
                    SoundSource.PLAYERS, 0.5F, 0.9F + ThreadLocalRandom.current().nextFloat() * 0.2F);
        }
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
}
