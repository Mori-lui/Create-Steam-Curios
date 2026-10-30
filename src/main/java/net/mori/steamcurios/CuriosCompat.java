package net.mori.steamcurios;

import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import top.theillusivec4.curios.api.CuriosApi;
import top.theillusivec4.curios.api.SlotContext;
import top.theillusivec4.curios.api.SlotResult;
import top.theillusivec4.curios.api.type.capability.ICurioItem;

import java.util.Comparator;
import java.util.List;

/**
 * Curios bridge. Only touched through the CURIOS_LOADED flag; the adapter is
 * registered per item so SteamAmuletItem itself never implements a Curios type
 * and the mod loads fine without Curios installed.
 */
public final class CuriosCompat {

    private CuriosCompat() {
    }

    public static void init() {
        ICurioItem adapter = new Adapter();
        for (Item amulet : ModItems.amuletItems()) {
            CuriosApi.registerCurio(amulet, adapter);
        }
    }

    /** Best worn amulet stack (highest protection fraction), or null. */
    public static ItemStack findBestWorn(LivingEntity entity) {
        List<SlotResult> worn = CuriosApi.getCuriosInventory(entity)
                .map(handler -> handler.findCurios(
                        stack -> stack.getItem() instanceof SteamAmuletItem))
                .orElse(List.of());
        return worn.stream()
                .map(SlotResult::stack)
                .max(Comparator.comparingDouble(SteamLogic::stackFraction))
                .orElse(null);
    }

    private static final class Adapter implements ICurioItem {
        @Override
        public void curioTick(SlotContext slotContext, ItemStack stack) {
            SteamLogic.serverAmuletTick(slotContext.entity(), stack);
        }
    }
}
