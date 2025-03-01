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
        image, _ = processing.apply_overlay(pp.image, p.paste_to, p.overlay_images[i])

        alpha = self._compute_optimal_alpha(np.array(p.init_images[0]), np.array(image))
        alpha = self._add_corner_alpha(alpha)
        mask = Image.fromarray(alpha * 255).convert('L')
        image = self._saturate_colors(np.array(p.init_images[0]), np.array(image), alpha)
        image = Image.fromarray(image).convert('RGBA')
        image.putalpha(mask)
        AlphaMaskGlobals.additional_images.append(image)

    def postprocess(self, _, res):
        if not AlphaMaskGlobals.extension_enabled:
            return

        amount_of_images = len(AlphaMaskGlobals.additional_images)
        res.images[amount_of_images:amount_of_images] = AlphaMaskGlobals.additional_images[:]

    def _compute_optimal_alpha(self, o: np.array, p: np.array) -> np.array:
        dt_p = p.astype(np.float32) - o.astype(np.float32)
        saturated_dt_p = np.clip(dt_p * 255, 0, 255)
        a = (dt_p) / (saturated_dt_p - o)
        a = np.nan_to_num(a, nan=0)
        a = np.min(a, axis=2)
        a = np.clip(a, 0, 1)
        return a
    
    def _add_corner_alpha(self, a: np.array) -> np.array:
        min_v = 1.5 / 255
        a = np.array(a)
        a[0, 0] = min_v
        a[-1, -1] = min_v
        return a

    def _saturate_colors(self, o: np.array, p: np.array, a: np.array) -> np.array:
        a = np.repeat(np.expand_dims(a, axis=2), 3, axis=2)
        dt_p = p.astype(np.float32) - o.astype(np.float32)
        res = o + np.nan_to_num(dt_p / a, nan=0)
        return np.clip(res, 0, 255).astype(np.uint8)
