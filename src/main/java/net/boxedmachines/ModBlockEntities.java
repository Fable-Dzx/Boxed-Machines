package net.boxedmachines;

import net.boxedmachines.block.MachineBlock;
import net.boxedmachines.block.entity.MachineBlockEntity;
import net.fabricmc.fabric.api.object.builder.v1.block.entity.FabricBlockEntityTypeBuilder;
import net.minecraft.block.Block;
import net.minecraft.block.entity.BlockEntityType;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.util.Identifier;

/**
 * 机器方块实体的注册：所有盒装机器共用一个方块实体类型。
 */
public final class ModBlockEntities {

    public static BlockEntityType<MachineBlockEntity> MACHINE;

    private ModBlockEntities() {
    }

    public static void initialize() {
        MACHINE = Registry.register(
                Registries.BLOCK_ENTITY_TYPE,
                Identifier.of(BoxedMachines.MOD_ID, "machine"),
                FabricBlockEntityTypeBuilder.<MachineBlockEntity>create(
                        (pos, state) -> {
                            if (state.getBlock() instanceof MachineBlock machineBlock) {
                                return new MachineBlockEntity(pos, state, machineBlock.getSpec());
                            }
                            return new MachineBlockEntity(pos, state, net.boxedmachines.machine.MachineSpec.EMPTY);
                        },
                        ModBlocks.ALL_MACHINES.toArray(new Block[0])
                ).build());
    }
}
