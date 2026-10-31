package net.mori.steamcurios;

import com.momosoftworks.coldsweat.api.temperature.modifier.TempModifier;
import com.momosoftworks.coldsweat.api.util.Temperature;
import net.minecraft.core.Holder;
import net.minecraft.core.HolderSet;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.RecipeManager;
import net.minecraft.world.level.GameType;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;

@GameTestHolder(SteamCuriosMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class SteamCuriosGameTests {

    private static final String EMPTY = "empty3x3";

    @GameTest(template = EMPTY, timeoutTicks = 100)
    public static void itemsRegistered(GameTestHelper helper) {
        for (String name : new String[]{"brass_medallion", "thermostat_core", "incomplete_heater_charm",
                "steam_heater_charm", "auto_thermostat", "isothermal_amulet"}) {
            Item item = BuiltInRegistries.ITEM.get(
                    ResourceLocation.fromNamespaceAndPath(SteamCuriosMod.MOD_ID, name));
            helper.assertTrue(item != net.minecraft.world.item.Items.AIR, name + " registered");
        }
        helper.succeed();
    }

    @GameTest(template = EMPTY, timeoutTicks = 100)
    public static void necklaceTagContainsAmulets(GameTestHelper helper) {
        TagKey<Item> necklace = TagKey.create(Registries.ITEM,
                ResourceLocation.fromNamespaceAndPath("curios", "necklace"));
        Set<Item> tagged = BuiltInRegistries.ITEM.getTag(necklace)
                .map(holders -> holders.stream().map(Holder::value).collect(Collectors.toSet()))
                .orElse(Set.of());
        for (Item amulet : ModItems.amuletItems()) {
            helper.assertTrue(tagged.contains(amulet), "amulet in curios:necklace tag: " + amulet);
        }
        helper.succeed();
    }

    @GameTest(template = EMPTY, timeoutTicks = 100)
    public static void recipesLoaded(GameTestHelper helper) {
        RecipeManager recipes = helper.getLevel().getServer().getRecipeManager();
        helper.assertFalse(recipes.hadErrorsLoading(), "recipe manager had no load errors");
        long mine = recipes.getRecipes().stream()
                .filter(holder -> holder.id().getNamespace().equals(SteamCuriosMod.MOD_ID))
                .count();
        helper.assertTrue(mine == 5, "expected 5 steamcurios recipes, found " + mine);
        helper.succeed();
    }

    @GameTest(template = EMPTY, timeoutTicks = 100)
    public static void fuelAndTierFractions(GameTestHelper helper) {
        ItemStack mechanical = new ItemStack(ModItems.STEAM_HEATER_CHARM.get());
        helper.assertTrue(SteamLogic.stackFraction(mechanical) == 0.0D, "mechanical empty protects nothing");
        SteamLogic.setFuel(mechanical, 100);
        helper.assertTrue(SteamLogic.getFuel(mechanical) == 100, "fuel stored");
        helper.assertTrue(SteamLogic.stackFraction(mechanical) == 1.0D, "mechanical fuelled protects fully");

        ItemStack automatic = new ItemStack(ModItems.AUTO_THERMOSTAT.get());
        helper.assertTrue(SteamLogic.stackFraction(automatic) == 0.5D, "automatic passive is half");

        ItemStack isothermal = new ItemStack(ModItems.ISOTHERMAL_AMULET.get());
        helper.assertTrue(SteamLogic.stackFraction(isothermal) == 1.0D, "isothermal always full");
        helper.succeed();
    }

    @GameTest(template = EMPTY, timeoutTicks = 100)
    public static void damageTagsResolve(GameTestHelper helper) {
        var damageTypes = helper.getLevel().registryAccess().registryOrThrow(Registries.DAMAGE_TYPE);
        var coldTag = TagKey.create(Registries.DAMAGE_TYPE,
                ResourceLocation.fromNamespaceAndPath(SteamCuriosMod.MOD_ID, "cold_damage"));
        var tempTag = TagKey.create(Registries.DAMAGE_TYPE,
                ResourceLocation.fromNamespaceAndPath(SteamCuriosMod.MOD_ID, "temperature_damage"));
        Holder<net.minecraft.world.damagesource.DamageType> freeze = damageTypes.getHolderOrThrow(
                ResourceKey.create(Registries.DAMAGE_TYPE, ResourceLocation.withDefaultNamespace("freeze")));
        Optional<HolderSet.Named<net.minecraft.world.damagesource.DamageType>> cold =
                damageTypes.getTag(coldTag);
        Optional<HolderSet.Named<net.minecraft.world.damagesource.DamageType>> temp =
                damageTypes.getTag(tempTag);
        helper.assertTrue(cold.isPresent(), "cold_damage tag exists");
        helper.assertTrue(temp.isPresent(), "temperature_damage tag exists");
        helper.assertTrue(cold.get().contains(freeze), "freeze in cold_damage");
        boolean nested = cold.get().stream().allMatch(h -> temp.get().contains(h));
        helper.assertTrue(nested, "cold_damage in temperature_damage");
        helper.succeed();
    }

    @GameTest(template = EMPTY, timeoutTicks = 100)
    public static void playerHasNecklaceSlot(GameTestHelper helper) {
        if (!SteamCuriosMod.CURIOS_LOADED) {
            helper.succeed();
            return;
        }
        var slots = top.theillusivec4.curios.api.CuriosApi.getEntitySlots(
                net.minecraft.world.entity.EntityType.PLAYER, helper.getLevel());
        helper.assertTrue(slots != null && slots.containsKey("necklace"),
                "player has necklace slot, has: " + (slots == null ? "null" : slots.keySet()));
        helper.succeed();
    }

    @GameTest(template = EMPTY, timeoutTicks = 100)
    public static void furTagContainsGoatFur(GameTestHelper helper) {
        TagKey<Item> furTag = TagKey.create(Registries.ITEM,
                ResourceLocation.fromNamespaceAndPath(SteamCuriosMod.MOD_ID, "fur"));
        Set<Item> tagged = BuiltInRegistries.ITEM.getTag(furTag)
                .map(holders -> holders.stream().map(Holder::value).collect(Collectors.toSet()))
                .orElse(Set.of());
        helper.assertFalse(tagged.isEmpty(), "steamcurios:fur tag is not empty");
        if (SteamCuriosMod.COLD_SWEAT_LOADED) {
            Item goatFur = BuiltInRegistries.ITEM.get(
                    ResourceLocation.fromNamespaceAndPath("cold_sweat", "goat_fur"));
            helper.assertTrue(tagged.contains(goatFur), "goat_fur in steamcurios:fur tag");
        }
        helper.succeed();
    }

    @GameTest(template = EMPTY, timeoutTicks = 100)
    public static void coldSweatLiftModifier(GameTestHelper helper) {
        if (!SteamCuriosMod.COLD_SWEAT_LOADED) {
            helper.succeed();
            return;
        }
        var player = helper.makeMockPlayer(GameType.SURVIVAL);

        double full = SteamLogic.liftForFraction(1.0D);
        double half = SteamLogic.liftForFraction(0.5D);
        double expected = SteamCuriosConfig.liftMc();
        helper.assertTrue(Math.abs(full - expected) < 1.0E-4D, "full lift is liftMc, got " + full);
        helper.assertTrue(Math.abs(half - expected / 2.0D) < 1.0E-4D, "half lift is liftMc/2, got " + half);

        ColdSweatCompat.syncModifier(player, 1.0D);
        List<TempModifier> world = Temperature.getModifiers(player, Temperature.Trait.WORLD);
        helper.assertTrue(world.stream().anyMatch(m -> m instanceof SteamWarmthModifier), "steam_warmth added");

        TempModifier modifier = world.stream()
                .filter(m -> m instanceof SteamWarmthModifier).findFirst().orElseThrow();
        double bare = ((SteamWarmthModifier) modifier).applyTo(0.0D, player);
        helper.assertTrue(Math.abs(bare) < 1.0E-4D,
                "no amulet carried -> no lift, got " + bare);

        ColdSweatCompat.syncModifier(player, 0.0D);
        helper.assertTrue(Temperature.getModifiers(player, Temperature.Trait.WORLD).stream()
                        .noneMatch(m -> m instanceof SteamWarmthModifier),
                "steam_warmth removed");
        helper.succeed();
    }

    private SteamCuriosGameTests() {
    }
}
