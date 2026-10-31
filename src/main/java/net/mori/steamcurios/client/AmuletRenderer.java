package net.mori.steamcurios.client;

import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.entity.ItemRenderer;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.mori.steamcurios.SteamCuriosMod;
import top.theillusivec4.curios.api.SlotContext;
import top.theillusivec4.curios.api.client.ICurioRenderer;

/**
 * Renders the amulet as its own item model (the icon) on the chest — the same
 * approach as Create's GogglesCurioRenderer. Rendering the item model (instead
 * of a separate mesh) also keeps the on-body look in sync with the fuel/water
 * state overrides of the item model.
 */
public class AmuletRenderer implements ICurioRenderer {

    @Override
    public <T extends LivingEntity, M extends EntityModel<T>> void render(
            ItemStack stack, SlotContext slotContext, PoseStack poseStack,
            RenderLayerParent<T, M> renderLayerParent, MultiBufferSource buffer,
            int light, float limbSwing, float limbSwingAmount, float partialTick,
            float ageInTicks, float netHeadYaw, float headPitch) {

        LivingEntity entity = slotContext.entity();
        ICurioRenderer.rotateIfSneaking(poseStack, entity);

        poseStack.pushPose();
        // entity space: y negative = up, front = +Z (Create's GogglesCurioRenderer convention)
        poseStack.translate(0.0D, -0.13D, 0.14D);
        poseStack.scale(0.13F, 0.13F, 0.13F);
        poseStack.mulPose(com.mojang.math.Axis.XP.rotationDegrees(180.0F));
        Level level = entity.level();
        ItemRenderer itemRenderer = Minecraft.getInstance().getItemRenderer();
        BakedModel model = itemRenderer.getModel(stack, level, entity, 0);
        itemRenderer.render(stack, ItemDisplayContext.NONE, false, poseStack, buffer, light,
                net.minecraft.client.renderer.texture.OverlayTexture.NO_OVERLAY, model);
        poseStack.popPose();
    }
}
