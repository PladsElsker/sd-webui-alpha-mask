# sd-webui-alpha-mask

A very simple A1111 extension that returns inpainted images with transparent pixels in place of the region not masked.  
This can be useful for example when you want to add the image as a new layer in your favorite illustration software.  
![image](https://github.com/John-WL/sd-webui-alpha-mask/assets/34081873/059a9457-0c9c-4d36-a2b1-b23dbfd2a0cf)
![image](https://github.com/John-WL/sd-webui-alpha-mask/assets/34081873/4ff8ce12-063d-458f-9e34-be4450ac6aef)

## Minimal Delta Mask
Unlike shown in the above example, the extension now uses a patch conversion mechanism that extracts the minimal delta from the original image, where the transparency for each pixel value is as high as possible.  
  
The conversion can be explained with the mask overlay equation for a 2 layer canvas (it's a simple weighted sum):  
$$C_f = C_1 A + C_2 \left( 1 - A \right)$$, where    
- $$C_f$$ is the result of the composition.
- $$A$$ is the pixel-wise alpha values.
- $$C_1$$ is the top layer.
- $$C_2$$ is the bottom layer.

We consider that after a generation, we have $$C_f = C_1$$, with $$A = 1$$.  
The key is to modify $$C_1$$ in a way that allows solving for $$A \neq 1$$:  
$$A = min_{col} \left( \frac{C_f - C_2}{C_1' - C_2} \right), A \in \left[0, 1\right], C_{1}' \in \left[0; 255\right] $$,  
where $$min_{col}$$ chooses the smallest pixel-wise value in the channel dimension.  
  
Once $$A$$ is known, we can compute back the correctly bounded scaled values for $$C_1'$$:  
$$C_1' = C_2 + \frac{C_1 - C_2}{A}$$  

We then apply the mask $$A$$ to $$C_1'$$, and return the result to the viewport. 

## Features / Won't Implement / Won't Fix
- Additional images won't be shown in the `txt2img`, `img2img -> img2img` and `img2img -> sketch` tabs because it wouldn't make sense.  
- Additional images are not saved to your harddrive.  
- You might need to download images with the top right `download` button:  
![image](https://github.com/John-WL/sd-webui-alpha-mask/assets/34081873/39d8aabf-5d39-477b-9348-dc9b311b2bd3)  
Doing `right click -> copy image` converts the transparent pixels to black for me, which is a clipboard quirk on windows.  
