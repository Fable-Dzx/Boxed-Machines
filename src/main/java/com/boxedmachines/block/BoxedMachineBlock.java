package com.boxedmachines.block;

import com.boxedmachines.BoxedMachinesMod;
import com.boxedmachines.blockentity.BoxedMachineBlockEntity;
import com.boxedmachines.util.MachineType;
import com.mojang.serialization.MapCodec;
import net.minecraft.block.Block;
import net.minecraft.block.BlockRenderType;
import net.minecraft.block.BlockState;
import net.minecraft.block.BlockWithEntity;
import net.minecraft.block.entity.BlockEntity;
import net.minecraft.block.entity.BlockEntityTicker;
import net.minecraft.block.entity.BlockEntityType;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.ItemPlacementContext;
import net.minecraft.screen.NamedScreenHandlerFactory;
import net.minecraft.state.StateManager;
import net.minecraft.state.property.DirectionProperty;
import net.minecraft.state.property.Properties;
import net.minecraft.util.ActionResult;
import net.minecraft.util.hit.BlockHitResult;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Direction;
import net.minecraft.world.World;
import org.jetbrains.annotations.Nullable;

/**
 * 盒装机器的方块类。
 * 支持朝向（FACING）属性，右键打开 GUI，自动 tick 产出。
 */
public class BoxedMachineBlock extends BlockWithEntity {

    public static final DirectionProperty FACING = Properties.HORIZONTAL_FACING;
    public static final MapCodec<BoxedMachineBlock> CODEC = createCodec(BoxedMachineBlock::new);

    private final MachineType machineType;

    public BoxedMachineBlock(Settings settings, MachineType machineType) {
        super(settings);
        this.machineType = machineType;
        setDefaultState(getStateManager().getDefaultState().with(FACING, Direction.NORTH));
    }

    @Override
    protected MapCodec<? extends BlockWithEntity> getCodec() {
        return CODEC;
    }

    @Override
    protected void appendProperties(StateManager.Builder<Block, BlockState> builder) {
        builder.add(FACING);
    }

    @Override
    public BlockState getPlacementState(ItemPlacementContext ctx) {
        return getDefaultState().with(FACING, ctx.getHorizontalPlayerFacing().getOpposite());
    }

    @Override
    public BlockRenderType getRenderType(BlockState state) {
        return BlockRenderType.MODEL;
    }

    @Nullable
    @Override
    public BlockEntity createBlockEntity(BlockPos pos, BlockState state) {
        return new BoxedMachineBlockEntity(
                BoxedMachinesMod.MACHINE_BLOCK_ENTITY_TYPES.get(machineType),
                pos, state, machineType
        );
    }

    @Override
    protected ActionResult onUse(BlockState state, World world, BlockPos pos, BlockHitResult hit) {
        if (!world.isClient) {
            NamedScreenHandlerFactory factory = state.createScreenHandlerFactory(world, pos);
            if (factory != null) {
                PlayerEntity player = world.getPlayers().stream()
                        .filter(p -> p.getBlockPos().isWithinDistance(pos, 8))
                        .findFirst().orElse(null);
                if (player != null) {
                    player.openHandledScreen(factory);
                }
            }
        }
        return ActionResult.SUCCESS;
    }

    @Nullable
    @Override
    public <T extends BlockEntity> BlockEntityTicker<T> getTicker(World world, BlockState state, BlockEntityType<T> type) {
        if (world.isClient) return null;
        return (w, pos, s, blockEntity) -> {
            if (blockEntity instanceof BoxedMachineBlockEntity machine) {
                machine.tick(w, pos, s);
            }
        };
    }

    public MachineType getMachineType() {
        return machineType;
    }
}
