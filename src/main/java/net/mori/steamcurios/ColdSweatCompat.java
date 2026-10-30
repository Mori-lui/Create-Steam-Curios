package net.mori.steamcurios;

import com.momosoftworks.coldsweat.api.event.core.registry.TempModifierRegisterEvent;
import com.momosoftworks.coldsweat.api.temperature.modifier.TempModifier;
import com.momosoftworks.coldsweat.api.util.Temperature;
import com.momosoftworks.coldsweat.api.util.placement.Placement;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.neoforged.bus.api.SubscribeEvent;

/**
 * Cold Sweat bridge. Every class reference here is only loaded through the
 * COLD_SWEAT_LOADED flag; never touch this class when Cold Sweat is absent.
 */
public final class ColdSweatCompat {

    public static final ResourceLocation MODIFIER_ID =
            ResourceLocation.fromNamespaceAndPath(SteamCuriosMod.MOD_ID, "steam_warmth");

    private static final ResourceLocation ICE_RESISTANCE_ID =
            ResourceLocation.fromNamespaceAndPath("cold_sweat", "ice_resistance");

    private ColdSweatCompat() {
    }

    @SubscribeEvent
    public static void onRegisterModifiers(TempModifierRegisterEvent event) {
        event.register(MODIFIER_ID, SteamWarmthModifier::new);
    }

    public static boolean isColdStressed(LivingEntity entity) {
        return Temperature.get(entity, Temperature.Trait.WORLD) < SteamCuriosConfig.thresholdMc();
    }

    public static void applyIceResistance(LivingEntity entity) {
        BuiltInRegistries.MOB_EFFECT.getOptional(ICE_RESISTANCE_ID).ifPresent(effect ->
                entity.addEffect(new MobEffectInstance(
                        BuiltInRegistries.MOB_EFFECT.wrapAsHolder(effect), 60, 0, true, false)));
    }

    /** Keep exactly one steam_warmth modifier on the player while any amulet protects them. */
    public static void syncModifier(Player player, double fraction) {
        boolean present = Temperature.getModifiers(player, Temperature.Trait.WORLD).stream()
                .anyMatch(modifier -> modifier instanceof SteamWarmthModifier);
        if (fraction > 0.0D && !present) {
            Temperature.addModifier(player, new SteamWarmthModifier(),
                    Temperature.Trait.WORLD, Placement.LAST);
        } else if (fraction <= 0.0D && present) {
            Temperature.removeModifiers(player, Temperature.Trait.WORLD,
                    modifier -> modifier instanceof SteamWarmthModifier);
        }
    }
}
