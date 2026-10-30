package net.mori.steamcurios;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.TagKey;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.damagesource.DamageType;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.neoforge.event.entity.living.LivingIncomingDamageEvent;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;

/**
 * Always-registered server logic: the no-Curios inventory fallback and cold damage
 * reduction. Cold Sweat deep integration is reached through guarded calls.
 */
public final class ProtectionEvents {

    private static final TagKey<DamageType> COLD_DAMAGE =
            TagKey.create(Registries.DAMAGE_TYPE,
                    ResourceLocation.fromNamespaceAndPath(SteamCuriosMod.MOD_ID, "cold_damage"));
    private static final TagKey<DamageType> TEMPERATURE_DAMAGE =
            TagKey.create(Registries.DAMAGE_TYPE,
                    ResourceLocation.fromNamespaceAndPath(SteamCuriosMod.MOD_ID, "temperature_damage"));

    private ProtectionEvents() {
    }

    @SubscribeEvent
    public static void onPlayerTick(PlayerTickEvent.Post event) {
        Player player = event.getEntity();
        if (player.level().isClientSide() || !SteamCuriosConfig.ENABLED.get()) {
            return;
        }
        if (player.tickCount % 20 != 0) {
            return;
        }
        if (!SteamCuriosMod.CURIOS_LOADED) {
            ItemStack best = SteamLogic.findBestStack(player);
            if (best != null) {
                SteamLogic.inventoryPulse(player, best);
            }
        }
        if (SteamCuriosMod.COLD_SWEAT_LOADED) {
            ColdSweatCompat.syncModifier(player, SteamLogic.bestFraction(player));
        }
    }

    @SubscribeEvent
    public static void onIncomingDamage(LivingIncomingDamageEvent event) {
        if (!SteamCuriosConfig.ENABLED.get() || event.isCanceled()) {
            return;
        }
        if (!(event.getEntity() instanceof Player player)) {
            return;
        }
        DamageSource source = event.getSource();
        if (!source.is(COLD_DAMAGE) && !source.is(TEMPERATURE_DAMAGE)) {
            return;
        }
        double fraction = SteamLogic.bestFraction(player);
        if (fraction <= 0.0D) {
            return;
        }
        double reduction = Math.min(1.0D, fraction * SteamCuriosConfig.DAMAGE_REDUCTION.get());
        float amount = event.getContainer().getNewDamage();
        float reduced = amount * (float) (1.0D - reduction);
        if (reduced < 0.01F) {
            event.setCanceled(true);
        } else {
            event.getContainer().setNewDamage(reduced);
        }
    }
}
