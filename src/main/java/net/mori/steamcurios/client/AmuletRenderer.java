package net.mori.steamcurios.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.ItemRenderer;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.mori.steamcurios.SteamCuriosMod;
import top.theillusivec4.curios.api.SlotContext;
import top.theillusivec4.curios.api.client.ICurioRenderer;

/**
 * Body render: a visible chain (flat quad with a V of links, lying on the chest)
 * and the pendant below it, drawn as the item's own model so it follows the
 * fuel/water state overrides.
 *
 * Pose space facts (verified against Create's GogglesCurioRenderer and live shots):
 * origin near the hips, y negative = up, front = +Z.
 */
public class AmuletRenderer implements ICurioRenderer {

    private static final ResourceLocation CHAIN_TEXTURE = ResourceLocation.fromNamespaceAndPath(
            SteamCuriosMod.MOD_ID, "textures/entity/chain.png");

    @Override
    public <T extends LivingEntity, M extends EntityModel<T>> void render(
            ItemStack stack, SlotContext slotContext, PoseStack poseStack,
            RenderLayerParent<T, M> renderLayerParent, MultiBufferSource buffer,
            int light, float limbSwing, float limbSwingAmount, float partialTick,
            float ageInTicks, float netHeadYaw, float headPitch) {

        LivingEntity entity = slotContext.entity();
        ICurioRenderer.rotateIfSneaking(poseStack, entity);

        // chain: flat quad across the chest, top at the neck, bottom where the pendant hangs
        poseStack.pushPose();
        VertexConsumer vc = buffer.getBuffer(RenderType.entityCutoutNoCull(CHAIN_TEXTURE));
        var pose = poseStack.last();
        float x0 = -0.20F, x1 = 0.20F, yTop = -0.37F, yBot = -0.03F, z = 0.135F;
        vc.addVertex(pose, x0, yTop, z).setColor(255, 255, 255, 255).setUv(0F, 0F)
                .setOverlay(OverlayTexture.NO_OVERLAY).setLight(light).setNormal(0F, 0F, 1F);
        vc.addVertex(pose, x1, yTop, z).setColor(255, 255, 255, 255).setUv(1F, 0F)
                .setOverlay(OverlayTexture.NO_OVERLAY).setLight(light).setNormal(0F, 0F, 1F);
        vc.addVertex(pose, x1, yBot, z).setColor(255, 255, 255, 255).setUv(1F, 1F)
                .setOverlay(OverlayTexture.NO_OVERLAY).setLight(light).setNormal(0F, 0F, 1F);
        vc.addVertex(pose, x0, yBot, z).setColor(255, 255, 255, 255).setUv(0F, 1F)
                .setOverlay(OverlayTexture.NO_OVERLAY).setLight(light).setNormal(0F, 0F, 1F);
        poseStack.popPose();

        // pendant: the item icon itself
        poseStack.pushPose();
        poseStack.translate(0.0D, -0.10D, 0.16D);
        poseStack.scale(0.11F, 0.11F, 0.11F);
        poseStack.mulPose(com.mojang.math.Axis.XP.rotationDegrees(180.0F));
        Level level = entity.level();
        ItemRenderer itemRenderer = Minecraft.getInstance().getItemRenderer();
        BakedModel model = itemRenderer.getModel(stack, level, entity, 0);
        itemRenderer.render(stack, ItemDisplayContext.NONE, false, poseStack, buffer, light,
                OverlayTexture.NO_OVERLAY, model);
        poseStack.popPose();
    }
}
