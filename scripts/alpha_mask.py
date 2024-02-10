import functools
from PIL import Image
import numpy as np

from modules import processing, scripts

from lib_alpha_mask.one_time_callable import one_time_callable
from lib_alpha_mask.globals import AlphaMaskGlobals


@one_time_callable
def highjack_processing_process_images_inner():
    def highjacked_func(*args, original_function, **kwargs):
        res = original_function(*args, **kwargs)
        if not AlphaMaskGlobals.extension_enabled:
            return res
        
        res.images.extend(AlphaMaskGlobals.additional_images)
        return res

    processing.process_images_inner = functools.partial(highjacked_func, original_function=processing.process_images_inner)


if AlphaMaskGlobals.extension_enabled:
    highjack_processing_process_images_inner()


class MaskAlphaScript(scripts.Script):
    def title(self):
        return 'Alpha Mask'

    def ui(self, is_img2img):
        return []

    def show(self, is_img2img):
        return False

    def postprocess_batch_list(self, *_, **__):
        if not AlphaMaskGlobals.extension_enabled:
            return

        AlphaMaskGlobals.additional_images = []
    
    def postprocess_image(self, p, pp, *_):
        if not AlphaMaskGlobals.extension_enabled:
            return

        i = p.batch_index
        overlay = p.overlay_images[i]
        image = processing.apply_overlay(pp.image, p.paste_to, i, p.overlay_images)

        image = image.convert('RGBA')
        inverted_mask = Image.fromarray(255 - np.array(overlay.getchannel("A")))
        image.putalpha(inverted_mask)
        AlphaMaskGlobals.additional_images.append(image)
