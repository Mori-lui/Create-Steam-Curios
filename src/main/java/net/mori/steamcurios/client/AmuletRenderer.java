package net.mori.steamcurios.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.mojang.math.Axis;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import net.mori.steamcurios.SteamCuriosMod;
import top.theillusivec4.curios.api.SlotContext;
import top.theillusivec4.curios.api.client.ICurioRenderer;

/**
 * Renders the amulet as a small brass medallion on the chest. Transforms are
 * tuned visually against the running game.
 */
public class AmuletRenderer implements ICurioRenderer {

    private static final ResourceLocation TEXTURE = ResourceLocation.fromNamespaceAndPath(
            SteamCuriosMod.MOD_ID, "textures/entity/amulet.png");

    private final AmuletModel model;

    public AmuletRenderer() {
        this.model = new AmuletModel(
                Minecraft.getInstance().getEntityModels().bakeLayer(AmuletModel.LAYER));
    }

    @Override
    public <T extends LivingEntity, M extends EntityModel<T>> void render(
            ItemStack stack, SlotContext slotContext, PoseStack poseStack,
            RenderLayerParent<T, M> renderLayerParent, MultiBufferSource buffer,
            int light, float limbSwing, float limbSwingAmount, float partialTick,
            float ageInTicks, float netHeadYaw, float headPitch) {

        LivingEntity entity = slotContext.entity();
        ICurioRenderer.rotateIfSneaking(poseStack, entity);

        poseStack.pushPose();
        // entity space: y negative = up, front = +Z (verified against Create's GogglesCurioRenderer)
        poseStack.translate(0.0D, -1.08D, 0.14D);
        poseStack.scale(0.6F, 0.6F, 0.6F);
        VertexConsumer consumer = buffer.getBuffer(RenderType.entityCutoutNoCull(TEXTURE));
        this.model.renderToBuffer(poseStack, consumer, light, OverlayTexture.NO_OVERLAY, -1);
        poseStack.popPose();
    }
}
