package net.mori.steamcurios.client;

import net.mori.steamcurios.ModItems;
import net.minecraft.world.item.Item;
import top.theillusivec4.curios.api.client.CuriosRendererRegistry;

/**
 * Registers the on-body amulet renderer. Only called when Curios is loaded.
 */
public final class CuriosCompatClient {

    private CuriosCompatClient() {
    }

    /** No-op touch so the class is only ever loaded behind the CURIOS_LOADED flag. */
    public static void touch() {
    }

    public static void registerRenderers() {
        for (Item amulet : new Item[]{
                ModItems.STEAM_HEATER_CHARM.get(),
                ModItems.AUTO_THERMOSTAT.get(),
                ModItems.ISOTHERMAL_AMULET.get()}) {
            CuriosRendererRegistry.register(amulet, AmuletRenderer::new);
        }
    }
}
