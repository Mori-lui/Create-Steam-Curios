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

    /** Remaining water in abstract units. Absent = empty. */
    public static final Supplier<DataComponentType<Integer>> WATER_UNITS =
            DATA_COMPONENTS.register("water_units",
                    () -> DataComponentType.<Integer>builder()
                            .persistent(Codec.intRange(0, 64))
                            .networkSynchronized(ByteBufCodecs.VAR_INT)
                            .build());

    /** Display state: 0 idle, 1 steaming, 2 dry (fuel but no water). Drives item model overrides. */
    public static final Supplier<DataComponentType<Integer>> STATE =
            DATA_COMPONENTS.register("state",
                    () -> DataComponentType.<Integer>builder()
                            .persistent(Codec.intRange(0, 2))
                            .networkSynchronized(ByteBufCodecs.VAR_INT)
                            .build());

    private ModComponents() {
    }
}
