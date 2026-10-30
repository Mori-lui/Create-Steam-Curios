package net.mori.steamcurios;

import com.mojang.logging.LogUtils;
import net.mori.steamcurios.client.CuriosCompatClient;
import net.mori.steamcurios.client.SteamCuriosClient;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.fml.config.ModConfig;
import net.neoforged.fml.loading.moddiscovery.ModInfo;
import net.neoforged.fml.ModList;
import net.neoforged.neoforge.common.NeoForge;
import org.slf4j.Logger;

@Mod(SteamCuriosMod.MOD_ID)
public class SteamCuriosMod {

    public static final String MOD_ID = "steamcurios";
    public static final Logger LOGGER = LogUtils.getLogger();

    public static final boolean CURIOS_LOADED = ModList.get().isLoaded("curios");
    public static final boolean COLD_SWEAT_LOADED = ModList.get().isLoaded("cold_sweat");
    public static final boolean CREATE_LOADED = ModList.get().isLoaded("create");

    public SteamCuriosMod(IEventBus modEventBus, ModContainer modContainer) {
        modContainer.registerConfig(ModConfig.Type.SERVER, SteamCuriosConfig.SPEC);

        ModItems.ITEMS.register(modEventBus);
        ModItems.TABS.register(modEventBus);
        ModComponents.DATA_COMPONENTS.register(modEventBus);

        NeoForge.EVENT_BUS.register(ProtectionEvents.class);
        if (COLD_SWEAT_LOADED) {
            // class touches Cold Sweat types; only load it when Cold Sweat is present
            NeoForge.EVENT_BUS.register(ColdSweatCompat.class);
        }

        modEventBus.addListener(this::onCommonSetup);

        LOGGER.info("[steamcurios] loaded; curios: {}, cold_sweat: {}, create: {}",
                CURIOS_LOADED, COLD_SWEAT_LOADED, CREATE_LOADED);
    }

    private void onCommonSetup(FMLCommonSetupEvent event) {
        if (CURIOS_LOADED) {
            CuriosCompat.init();
        }
        // keep the client class referenced only through the dist subscriber; nothing to do here otherwise
        SteamCuriosClient.touch();
        CuriosCompatClient.touch();
    }
}
