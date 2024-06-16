# sd-webui-alpha-mask

A very simple A1111 extension that returns inpainted images with transparent pixels in place of the region not masked.  
This can be useful for example when you want to add the image as a new layer in your favorite illustration software.  
![image](https://github.com/John-WL/sd-webui-alpha-mask/assets/34081873/059a9457-0c9c-4d36-a2b1-b23dbfd2a0cf)
![image](https://github.com/John-WL/sd-webui-alpha-mask/assets/34081873/4ff8ce12-063d-458f-9e34-be4450ac6aef)

## Features / Won't Implement / Won't Fix
- This extension won't show additional images in the `txt2img`, `img2img -> img2img` and `img2img -> sketch` tabs (doesn't make sense).  
- It also won't save them on your hard drive.  
- You might need to download images with the top right `download` button:  
![image](https://github.com/John-WL/sd-webui-alpha-mask/assets/34081873/39d8aabf-5d39-477b-9348-dc9b311b2bd3)  
Doing `right click -> copy image` converts the transparent pixels to black for me, which is clipboard quirk on windows.  
