package net.mori.steamcurios;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.world.level.Level;

import java.util.List;

/**
 * A wearable steampunk amulet. Fuel handling lives here (charge as a data component,
 * refuel by right-clicking with furnace fuel in the other hand); protection logic
 * lives in SteamLogic and runs from the Curios tick (or the inventory fallback).
 */
public class SteamAmuletItem extends Item {

    private final AmuletTier tier;

    public SteamAmuletItem(Properties properties, AmuletTier tier) {
        super(properties);
        this.tier = tier;
    }

    public AmuletTier tier() {
        return this.tier;
    }

    public int fuelCapacity() {
        return SteamCuriosConfig.FUEL_CAPACITY_TICKS.get();
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand usedHand) {
        ItemStack stack = player.getItemInHand(usedHand);
        if (!this.tier.usesFuel()) {
            return InteractionResultHolder.pass(stack);
        }
        ItemStack offhand = player.getItemInHand(InteractionHand.OFF_HAND);
        int burnTime = offhand.getBurnTime(RecipeType.SMELTING);
        int fuel = SteamLogic.getFuel(stack);
        int capacity = this.fuelCapacity();
        if (burnTime <= 0 || fuel >= capacity || offhand.isEmpty()) {
            return InteractionResultHolder.pass(stack);
        }
        if (!level.isClientSide()) {
            int added = Math.min(burnTime, capacity - fuel);
            SteamLogic.setFuel(stack, fuel + added);
            if (!player.hasInfiniteMaterials()) {
                offhand.shrink(1);
            }
            level.playSound(null, player.blockPosition(),
                    SoundEvents.FLINTANDSTEEL_USE, SoundSource.PLAYERS, 0.6F, 0.7F);
            player.displayClientMessage(Component.translatable("message.steamcurios.refuelled",
                    added / 20), true);
        }
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context,
                                List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(this.tier.translationKey())
                .withStyle(ChatFormatting.GRAY));
        if (this.tier.usesFuel()) {
            int fuel = SteamLogic.getFuel(stack);
            int capacity = Math.max(1, this.fuelCapacity());
            int percent = (int) Math.round(100.0D * fuel / capacity);
            tooltip.add(Component.translatable("tooltip.steamcurios.steam", percent)
                    .withStyle(fuel > 0 ? ChatFormatting.AQUA : ChatFormatting.DARK_GRAY));
            if (fuel <= 0) {
                tooltip.add(Component.translatable("tooltip.steamcurios.refuel_hint")
                        .withStyle(ChatFormatting.DARK_GRAY));
            }
        }
    }

    @Override
    public boolean isBarVisible(ItemStack stack) {
        return this.tier.usesFuel();
    }

    @Override
    public int getBarWidth(ItemStack stack) {
        int capacity = Math.max(1, this.fuelCapacity());
        return Math.max(1, Math.round(13.0F * SteamLogic.getFuel(stack) / capacity));
    }

    @Override
    public int getBarColor(ItemStack stack) {
        return 0x9FC5E8;
    }
}
