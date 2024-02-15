# sd-webui-alpha-mask

A very simple A1111 extension that returns inpainted images with transparent pixels in place of the region not masked.  
This can be useful when you want to add the image as a new layer in your favorite illustration software, for example:  
![image](https://github.com/John-WL/sd-webui-alpha-mask/assets/34081873/059a9457-0c9c-4d36-a2b1-b23dbfd2a0cf)
![image](https://github.com/John-WL/sd-webui-alpha-mask/assets/34081873/4ff8ce12-063d-458f-9e34-be4450ac6aef)

> This extension won't show additional images in the `txt2img`, `img2img -> img2img` and `img2img -> sketch` tabs.
> You might need to download the image with your browser with the top right download button. `left click -> copy image` converts the transparent pixels to black for me, probably a gradio bug. 
