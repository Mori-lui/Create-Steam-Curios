package net.mori.steamcurios;

import net.minecraft.ChatFormatting;
import net.minecraft.core.component.DataComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.world.level.Level;

import java.util.List;

/**
 * A wearable steampunk amulet. Fuel handling lives here (charge + water as data
 * components, refuel by right-clicking with fuel or water in the other hand);
 * protection logic lives in SteamLogic and runs from the Curios tick.
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
        if (offhand.isEmpty()) {
            return InteractionResultHolder.pass(stack);
        }

        // water first: bottle or bucket
        int bottleUnits = SteamCuriosConfig.BOTTLE_UNITS.get();
        int bucketUnits = SteamCuriosConfig.BUCKET_UNITS.get();
        int water = SteamLogic.getWater(stack);
        int waterCapacity = SteamCuriosConfig.WATER_CAPACITY_UNITS.get();

        if (isPlainWaterBottle(offhand) && water < waterCapacity) {
            if (!level.isClientSide()) {
                int added = Math.min(bottleUnits, waterCapacity - water);
                SteamLogic.setWater(stack, water + added);
                offhand.shrink(1);
                if (!player.hasInfiniteMaterials()) {
                    player.getInventory().placeItemBackInInventory(new ItemStack(Items.GLASS_BOTTLE));
                }
                refillFeedback(level, player, "message.steamcurios.water_refilled", added);
            }
            return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
        }
        if (offhand.is(Items.WATER_BUCKET) && water < waterCapacity) {
            if (!level.isClientSide()) {
                int added = Math.min(bucketUnits, waterCapacity - water);
                SteamLogic.setWater(stack, water + added);
                offhand.shrink(1);
                if (!player.hasInfiniteMaterials()) {
                    player.getInventory().placeItemBackInInventory(new ItemStack(Items.BUCKET));
                }
                refillFeedback(level, player, "message.steamcurios.water_refilled", added);
            }
            return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
        }

        // then fuel: value = furnace burn time (plank 15 s, coal 80 s, coal block 800 s)
        int burnTime = offhand.getBurnTime(RecipeType.SMELTING);
        int fuel = SteamLogic.getFuel(stack);
        int capacity = this.fuelCapacity();
        if (burnTime <= 0 || fuel >= capacity) {
            return InteractionResultHolder.pass(stack);
        }
        if (!level.isClientSide()) {
            int added = Math.min(burnTime, capacity - fuel);
            SteamLogic.setFuel(stack, fuel + added);
            offhand.shrink(1);
            level.playSound(null, player.blockPosition(),
                    SoundEvents.FLINTANDSTEEL_USE, SoundSource.PLAYERS, 0.6F, 0.7F);
            player.displayClientMessage(Component.translatable("message.steamcurios.refuelled",
                    added / 20), true);
        }
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
    }

    private static boolean isPlainWaterBottle(ItemStack stack) {
        var contents = stack.get(DataComponents.POTION_CONTENTS);
        return contents != null && contents.potion().isEmpty();
    }

    private static void refillFeedback(Level level, Player player, String key, int added) {
        level.playSound(null, player.blockPosition(),
                SoundEvents.BUCKET_FILL, SoundSource.PLAYERS, 0.7F, 1.1F);
        player.displayClientMessage(Component.translatable(key, added), true);
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
            int water = SteamLogic.getWater(stack);
            int waterCapacity = SteamCuriosConfig.WATER_CAPACITY_UNITS.get();
            tooltip.add(Component.translatable("tooltip.steamcurios.water", water, waterCapacity)
                    .withStyle(water > 0 ? ChatFormatting.BLUE : ChatFormatting.DARK_GRAY));
            if (fuel <= 0 || water <= 0) {
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
