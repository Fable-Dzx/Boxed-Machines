package net.boxedmachines.block;

import net.boxedmachines.ModBlockEntities;
import net.boxedmachines.block.entity.MachineBlockEntity;
import net.boxedmachines.machine.MachineSpec;
import com.mojang.serialization.MapCodec;
import net.minecraft.block.BlockState;
import net.minecraft.block.BlockWithEntity;
import net.minecraft.block.entity.BlockEntity;
import net.minecraft.block.entity.BlockEntityTicker;
import net.minecraft.block.entity.BlockEntityType;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.util.ActionResult;
import net.minecraft.util.hit.BlockHitResult;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Direction;
import net.minecraft.world.World;
import org.jetbrains.annotations.Nullable;

/**
 * 盒装机器方块：带方块实体，每 tick 自动产出；右键收取；可被比较器读取储量。
 */
public class MachineBlock extends BlockWithEntity {

    /** 方块状态编解码器（仅用于序列化路径，实际放置走注册表实例）。 */
    public static final MapCodec<MachineBlock> CODEC =
            createCodec(settings -> new MachineBlock(MachineSpec.EMPTY, settings));

    private final MachineSpec spec;

    public MachineBlock(MachineSpec spec, Settings settings) {
        super(settings);
        this.spec = spec;
    }

    public MachineSpec getSpec() {
        return spec;
    }

    @Override
    protected MapCodec<? extends BlockWithEntity> getCodec() {
        return CODEC;
    }

    @Override
    public BlockEntity createBlockEntity(BlockPos pos, BlockState state) {
        return new MachineBlockEntity(pos, state, spec);
    }

    @Override
    @Nullable
    public <T extends BlockEntity> BlockEntityTicker<T> getTicker(World world, BlockState state, BlockEntityType<T> type) {
        if (world.isClient()) {
            return null;
        }
        return validateTicker(type, ModBlockEntities.MACHINE, MachineBlockEntity::tick);
    }

    @Override
    protected ActionResult onUse(BlockState state, World world, BlockPos pos, PlayerEntity player, BlockHitResult hit) {
        if (!world.isClient()) {
            if (world.getBlockEntity(pos) instanceof MachineBlockEntity machine) {
                machine.collect(player);
            }
        }
        return ActionResult.SUCCESS;
    }

    @Override
    protected void onStateReplaced(BlockState state, ServerWorld world, BlockPos pos, boolean moved) {
        if (!state.isOf(world.getBlockState(pos).getBlock())) {
            if (!moved && world.getBlockEntity(pos) instanceof MachineBlockEntity machine) {
                machine.dropContents(world, pos);
                world.updateComparators(pos, this);
            }
        }
        super.onStateReplaced(state, world, pos, moved);
    }

    @Override
    protected boolean hasComparatorOutput(BlockState state) {
        return true;
    }

    @Override
    protected int getComparatorOutput(BlockState state, World world, BlockPos pos, Direction direction) {
        if (world.getBlockEntity(pos) instanceof MachineBlockEntity machine) {
            return machine.comparatorOutput();
        }
        return 0;
    }
}
