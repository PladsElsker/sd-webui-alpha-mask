from PIL import Image
import numpy as np

from modules import processing, scripts

from lib_alpha_mask.globals import AlphaMaskGlobals


class MaskAlphaScript(scripts.Script):
    def title(self):
        return 'Alpha Mask'

    def ui(self, is_img2img):
        return []

    def show(self, is_img2img):
        AlphaMaskGlobals.additional_images = []
        return scripts.AlwaysVisible if is_img2img else False

    def postprocess_batch_list(self, *_, **__):
        if not AlphaMaskGlobals.extension_enabled:
            return

        AlphaMaskGlobals.additional_images = []
    
    def postprocess_image(self, p, pp, *_):
        if not AlphaMaskGlobals.extension_enabled:
            return

        if not p.overlay_images:
            return

        i = p.batch_index
        overlay = p.overlay_images[i]
        image, _ = processing.apply_overlay(pp.image, p.paste_to, p.overlay_images[i])

        image = image.convert('RGBA')
        inverted_mask = Image.fromarray(255 - np.array(overlay.getchannel("A")))
        image.putalpha(inverted_mask)
        AlphaMaskGlobals.additional_images.append(image)

    def postprocess(self, _, res):
        if not AlphaMaskGlobals.extension_enabled:
            return

        amount_of_images = len(AlphaMaskGlobals.additional_images)
        res.images[amount_of_images:amount_of_images] = AlphaMaskGlobals.additional_images[:]
