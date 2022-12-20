
import gradio as gr
import sys
import random
import paddlehub as hub
from loguru import logger

language_translation_model = hub.Module(directory=f'./baidu_translate')
def getTextTrans(text, source='zh', target='en'):
    try:
        text_translation = language_translation_model.translate(text, source, target)
        return text_translation
    except Exception as e:
        return text 


model_ids = {
            "models/stabilityai/stable-diffusion-2-1":"sd-v2-1",
            "models/stabilityai/stable-diffusion-2":"sd-v2-0",
            "models/runwayml/stable-diffusion-v1-5":"sd-v1-5",
            # "models/CompVis/stable-diffusion-v1-4":"sd-v1-4",
            "models/prompthero/openjourney":"openjourney",
            "models/hakurei/waifu-diffusion":"waifu-diffusion",
            "models/Linaqruf/anything-v3.0":"anything-v3.0",
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
        logger.info(f"load_fail__{model_id}_")

def infer(prompt):
    logger.info(f"infer_1__")
    prompt = getTextTrans(prompt, source='zh', target='en') + f',{random.randint(0,sys.maxsize)}'
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
                    if (window['doCheckPrompt'] === 0 && window['prevPrompt'] !== text1.value) {
                            console.log('_____new prompt___[' + text1.value + ']_');
                            window['doCheckPrompt'] = 1;
                            window['prevPrompt'] = text1.value;
                            for (var i = 2; i < texts.length; i++) {
                                setNativeValue(texts[i], text1.value);
                                texts[i].dispatchEvent(new Event('input', { bubbles: true }));
                            }                        
                            setTimeout(function() {
                                btns = window['gradioEl'].querySelectorAll('button');
                                for (var i = 0; i < btns.length; i++) {
                                    if (btns[i].innerText == 'Submit') {
                                        btns[i].click();                
                                    }
                                }
                                window['doCheckPrompt'] = 0;
                            }, 10);                   
                    }
            } catch(e) {
            }        
        }
        window['checkPrompt_interval'] = window.setInterval("window.checkPrompt()", 100);         
    }
   
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
                prompt_input1 = gr.Textbox(lines=4, label="prompt", visible=False)
            with gr.Row():
                submit_btn = gr.Button(value = "submit",elem_id="erase-btn").style(
                        margin=True,
                        rounded=(True, True, True, True),
                    )
            with gr.Row(elem_id='tab_demo', visible=True).style(height=5):
                tab_demo = gr.TabbedInterface(tab_actions, tab_titles) 

            submit_btn.click(fn=infer, inputs=[prompt_input0], outputs=[prompt_input1])

if __name__ == "__main__":
    demo.launch()


