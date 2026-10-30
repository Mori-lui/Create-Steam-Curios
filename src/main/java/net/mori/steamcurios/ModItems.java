package net.mori.steamcurios;

import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.world.level.Level;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

import java.util.List;

public final class ModItems {

    public static final DeferredRegister.Items ITEMS =
            DeferredRegister.createItems(SteamCuriosMod.MOD_ID);
    public static final DeferredRegister<CreativeModeTab> TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, SteamCuriosMod.MOD_ID);

    public static final DeferredItem<Item> BRASS_MEDALLION =
            ITEMS.registerSimpleItem("brass_medallion", new Item.Properties().stacksTo(16));
    public static final DeferredItem<Item> THERMOSTAT_CORE =
            ITEMS.registerSimpleItem("thermostat_core", new Item.Properties());
    public static final DeferredItem<Item> INCOMPLETE_HEATER_CHARM =
            ITEMS.registerSimpleItem("incomplete_heater_charm", new Item.Properties().stacksTo(1));

    public static final DeferredItem<SteamAmuletItem> STEAM_HEATER_CHARM =
            ITEMS.register("steam_heater_charm",
                    () -> new SteamAmuletItem(new Item.Properties().stacksTo(1), AmuletTier.MECHANICAL));
    public static final DeferredItem<SteamAmuletItem> AUTO_THERMOSTAT =
            ITEMS.register("auto_thermostat",
                    () -> new SteamAmuletItem(new Item.Properties().stacksTo(1), AmuletTier.AUTOMATIC));
    public static final DeferredItem<SteamAmuletItem> ISOTHERMAL_AMULET =
            ITEMS.register("isothermal_amulet",
                    () -> new SteamAmuletItem(new Item.Properties().stacksTo(1).rarity(Rarity.EPIC), AmuletTier.ISOTHERMAL));

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> TAB = TABS.register("main",
            () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup.steamcurios"))
                    .icon(() -> new ItemStack(BRASS_MEDALLION.get()))
                    .displayItems((parameters, output) -> {
                        output.accept(BRASS_MEDALLION.get());
                        output.accept(THERMOSTAT_CORE.get());
                        output.accept(INCOMPLETE_HEATER_CHARM.get());
                        output.accept(STEAM_HEATER_CHARM.get());
                        output.accept(AUTO_THERMOSTAT.get());
                        output.accept(ISOTHERMAL_AMULET.get());
                    })
                    .build());

    private ModItems() {
    }

    /** The three wearable amulets, registration order. */
    public static List<Item> amuletItems() {
        return List.of(STEAM_HEATER_CHARM.get(), AUTO_THERMOSTAT.get(), ISOTHERMAL_AMULET.get());
    }
}
