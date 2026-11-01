package net.mori.steamcurios.client;

import net.mori.steamcurios.SteamCuriosMod;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.fml.event.lifecycle.FMLClientSetupEvent;

/**
 * Client mod-bus subscriber. References to Curios go through CuriosCompatClient,
 * which is only touched when Curios is loaded.
 */
@EventBusSubscriber(modid = SteamCuriosMod.MOD_ID, value = Dist.CLIENT)
public final class SteamCuriosClient {

    private SteamCuriosClient() {
    }

    /** No-op so the common side can force class loading order; kept for clarity. */
    public static void touch() {
    }

    @SubscribeEvent
    public static void onClientSetup(FMLClientSetupEvent event) {
        if (SteamCuriosMod.CURIOS_LOADED) {
            CuriosCompatClient.registerRenderers();
        }
    }
}
