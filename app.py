
import gradio as gr
import sys
import random
import paddlehub as hub

language_translation_model = hub.Module(directory=f'./baidu_translate')
def getTextTrans(text, source='zh', target='en'):
    try:
        text_translation = language_translation_model.translate(text, source, target)
        return text_translation
    except Exception as e:
        return text 

model_ids = {"models/runwayml/stable-diffusion-v1-5":"stable-diffusion-v1-5",
           "models/stabilityai/stable-diffusion-2":"stable-diffusion-2",
           "models/prompthero/openjourney":"openjourney",
           }
tab_actions = []
tab_titles = []
for model_id in model_ids.keys():
    print(model_id, model_ids[model_id])
    try:
        tab = gr.Interface.load(model_id)
        tab_actions.append(tab)
        tab_titles.append(model_ids[model_id])
    except:
        pass

def infer(prompt):
    random.randint(0,sys.maxsize)    prompt = getTextTrans(prompt, source='zh', target='en') + f',{random.randint(0,sys.maxsize)}'
    return prompt

start_work = """async() => {
    function isMobile() {
        try {
            document.createEvent("TouchEvent"); return true;
        } catch(e) {
            return false; 
        }
    }

	function getClientHeight()
	{
	  var clientHeight=0;
	  if(document.body.clientHeight&&document.documentElement.clientHeight) {
		var clientHeight = (document.body.clientHeight<document.documentElement.clientHeight)?document.body.clientHeight:document.documentElement.clientHeight;
	  } else {
		var clientHeight = (document.body.clientHeight>document.documentElement.clientHeight)?document.body.clientHeight:document.documentElement.clientHeight;
	  }
	  return clientHeight;
	}
 
    function setNativeValue(element, value) {
      const valueSetter = Object.getOwnPropertyDescriptor(element.__proto__, 'value').set;
      const prototype = Object.getPrototypeOf(element);
      const prototypeValueSetter = Object.getOwnPropertyDescriptor(prototype, 'value').set;
      
      if (valueSetter && valueSetter !== prototypeValueSetter) {
            prototypeValueSetter.call(element, value);
      } else {
            valueSetter.call(element, value);
      }
    }

    var gradioEl = document.querySelector('body > gradio-app').shadowRoot;
    if (!gradioEl) {
        gradioEl = document.querySelector('body > gradio-app');
    }
    
    if (typeof window['gradioEl'] === 'undefined') {
        window['gradioEl'] = gradioEl;
        
        tabitems = window['gradioEl'].querySelectorAll('.tabitem');
        for (var i = 0; i < tabitems.length; i++) {    
            tabitems[i].childNodes[0].children[0].style.display='none';
            tabitems[i].childNodes[0].children[1].children[0].style.display='none';
            tabitems[i].childNodes[0].children[1].children[1].children[0].children[1].style.display="none"; 
        }    
        tab_demo = window['gradioEl'].querySelectorAll('#tab_demo')[0];
        tab_demo.style.display = "block";
        tab_demo.setAttribute('style', 'height: 100%;');

        const page1 = window['gradioEl'].querySelectorAll('#page_1')[0];
        const page2 = window['gradioEl'].querySelectorAll('#page_2')[0]; 
    
        page1.style.display = "none";
        page2.style.display = "block";    

        window['prevPrompt'] = '';
        window['doCheckPrompt'] = 0;
        window['checkPrompt'] = function checkPrompt() {
            try {
                    texts = window['gradioEl'].querySelectorAll('textarea');
                    text0 = texts[0];    
                    text1 = texts[1];
                    if (window['doCheckPrompt'] == 0 && window['prevPrompt'] != text1.value) {
                            window['doCheckPrompt'] = 1;
                            window['prevPrompt'] = text1.value;
                            for (var i = 2; i < texts.length; i++) {
                                setNativeValue(texts[i], text1.value);
                                texts[i].dispatchEvent(new Event('input', { bubbles: true }));
                            }                        
                            setTimeout(function() {
                                text1 = window['gradioEl'].querySelectorAll('textarea')[1];    
                                //console.log('do_click()_1_' + text1.value);
                                
                                btns = window['gradioEl'].querySelectorAll('button');
                                for (var i = 0; i < btns.length; i++) {
                                    if (btns[i].innerText == 'Submit') {
                                        btns[i].focus();
                                        btns[i].click();                
                                       //break;
                                    }
                                }
                                //console.log('do_click()_3_');
                                window['doCheckPrompt'] = 0;
                            }, 10);                   
                    }
            } catch(e) {
            }        
        }
        window['checkPrompt_interval'] = window.setInterval("window.checkPrompt()", 100);         
    }

    /*
    texts = gradioEl.querySelectorAll('textarea');
    text0 = gradioEl.querySelectorAll('textarea')[0];    
    text1 = gradioEl.querySelectorAll('textarea')[0];
    
    for (var i = 1; i < texts.length; i++) {
        setNativeValue(texts[i], text0.value);
        texts[i].dispatchEvent(new Event('input', { bubbles: true }));
    }

    var st = setTimeout(function() {
        text1 = window['gradioEl'].querySelectorAll('textarea')[1];    
        console.log('do_click()_1_' + text1.value);
        
        btns = window['gradioEl'].querySelectorAll('button');
        for (var i = 0; i < btns.length; i++) {
            if (btns[i].innerText == 'Submit') {
                btns[i].focus();
                btns[i].click();                
               //break;
            }
        }
        console.log('do_click()_3_');
    }, 10);
    */
    
    return false;
}"""

with gr.Blocks(title='Text to Image') as demo:
    with gr.Group(elem_id="page_1", visible=True) as page_1:
        with gr.Box():            
            with gr.Row():
                start_button = gr.Button("Let's GO!", elem_id="start-btn", visible=True) 
                start_button.click(fn=None, inputs=[], outputs=[], _js=start_work)
                
    with gr.Group(elem_id="page_2", visible=False) as page_2:                 
            with gr.Row(elem_id="prompt_row"):
                prompt_input0 = gr.Textbox(lines=4, label="prompt")
                prompt_input1 = gr.Textbox(lines=4, label="prompt", visible=True)
            with gr.Row():
                submit_btn = gr.Button(value = "submit",elem_id="erase-btn").style(
                        margin=True,
                        rounded=(True, True, True, True),
                    )
            with gr.Row(elem_id='tab_demo', visible=True).style(height=5):
                tab_demo = gr.TabbedInterface(tab_actions, tab_titles) 

            submit_btn.click(fn=infer, inputs=[prompt_input0], outputs=[prompt_input1])

# prompt_input = gr.Textbox(lines=4, label="Input prompt")
# tab_demo = gr.TabbedInterface([sd15_demo, sd20_demo, openjourney_demo], ["stable-diffusion-v1-5", "stable-diffusion-2", "openjourney"])

# demo = gr.Interface(fn=infer, 
#                      inputs=[prompt_input], 
#                      outputs=[tab_demo],
#                     )

if __name__ == "__main__":
    demo.launch()

    

# import os
# os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
# from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline, StableDiffusionInpaintPipeline, StableDiffusionInpaintPipelineLegacy

# import gradio as gr
# import PIL.Image
# import numpy as np
# import random
# import torch
# import subprocess

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# # print('Using device:', device)

# HF_TOKEN_SD=os.environ.get('HF_TOKEN_SD')

# if 0==0:
#     model_id = "runwayml/stable-diffusion-v1-5"

#     model_id = "prompthero/openjourney" 
    
#     # pipeClass = StableDiffusionImg2ImgPipeline
#     pipeClass = StableDiffusionPipeline     
#     className = pipeClass.__name__
#     if className == 'StableDiffusionInpaintPipeline':
#         model_id = "runwayml/stable-diffusion-inpainting"    
        
#     sd_pipe = pipeClass.from_pretrained(
#         model_id, 
#         # revision="fp16",
#         torch_dtype=torch.float16, 
#         # use_auth_token=HF_TOKEN_SD
#       ) # .to(device)

# def predict(prompt, steps=100, seed=42, guidance_scale=6.0):
#     #torch.cuda.empty_cache()
#     # print(subprocess.check_output(["nvidia-smi"], stderr=subprocess.STDOUT).decode("utf8"))
#     generator = torch.manual_seed(seed)
#     images = sd_pipe([prompt], 
#             generator=generator, 
#             num_inference_steps=steps, 
#             eta=0.3, 
#             guidance_scale=guidance_scale)["sample"]
#     # print(subprocess.check_output(["nvidia-smi"], stderr=subprocess.STDOUT).decode("utf8"))
#     return images[0]

# random_seed = random.randint(0, 2147483647)
# gr.Interface(
#     predict,
#     inputs=[
#         gr.inputs.Textbox(label='Prompt', default='a chalk pastel drawing of a llama wearing a wizard hat'),
#         gr.inputs.Slider(1, 100, label='Inference Steps', default=50, step=1),
#         gr.inputs.Slider(0, 2147483647, label='Seed', default=random_seed, step=1),
#         gr.inputs.Slider(1.0, 20.0, label='Guidance Scale - how much the prompt will influence the results', default=6.0, step=0.1),
#     ],
#     outputs=gr.Image(shape=[256,256], type="pil", elem_id="output_image"),
#     css="#output_image{width: 256px}",
#     title="Text-to-Image_Latent_Diffusion",
#     # description="This Spaces contains a text-to-image Latent Diffusion process for the <a href=\"https://huggingface.co/CompVis/ldm-text2im-large-256\">ldm-text2im-large-256</a> model by <a href=\"https://huggingface.co/CompVis\">CompVis</a> using the <a href=\"https://github.com/huggingface/diffusers\">diffusers library</a>. The goal of this demo is to showcase the diffusers library and you can check how the code works here. If you want the state-of-the-art experience with Latent Diffusion text-to-image check out the <a href=\"https://huggingface.co/spaces/multimodalart/latentdiffusion\">main Spaces</a>.",
# ).launch()
