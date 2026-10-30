package net.mori.steamcurios;

import com.mojang.serialization.Codec;
import net.minecraft.core.component.DataComponentType;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.codec.ByteBufCodecs;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

import java.util.function.Supplier;

public final class ModComponents {

    public static final DeferredRegister<DataComponentType<?>> DATA_COMPONENTS =
            DeferredRegister.create(Registries.DATA_COMPONENT_TYPE, SteamCuriosMod.MOD_ID);

    /** Remaining steam charge in ticks. Absent = empty. */
    public static final Supplier<DataComponentType<Integer>> FUEL_TICKS =
            DATA_COMPONENTS.register("fuel_ticks",
                    () -> DataComponentType.<Integer>builder()
                            .persistent(Codec.intRange(0, 1 << 20))
                            .networkSynchronized(ByteBufCodecs.VAR_INT)
                            .build());

    private ModComponents() {
    }
}
