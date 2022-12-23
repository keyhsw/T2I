from transformers import pipeline
import gradio as gr
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
        
extend_prompt_pipe = pipeline('text-generation', model='./model', max_length=77)

def extend_prompt(prompt):
    prompt_en = getTextTrans(prompt, source='zh', target='en')
    extend_prompt_en = extend_prompt_pipe(prompt_en+',', num_return_sequences=1)[0]["generated_text"]    
    if (prompt != prompt_en):
        extend_prompt_zh = getTextTrans(extend_prompt_en, source='en', target='zh')
        extend_prompt_out = f'{extend_prompt_zh} 【{extend_prompt_en}】'
    else:
        extend_prompt_out = extend_prompt_en

    return prompt_en, extend_prompt_en, extend_prompt_out

examples = [
            ['elon musk as thor'],
            ["giant dragon flying in the sky"],
            ['psychedelic liquids space'],
            ["a coconut laying on the beach"],
            ["peaceful village landscape"],
            ]

# model_ids = {
#             # "models/stabilityai/stable-diffusion-2-1":"sd-v2-1",
#             "models/stabilityai/stable-diffusion-2":"sd-v2-0",
#             # "models/runwayml/stable-diffusion-v1-5":"sd-v1-5",
#             # "models/CompVis/stable-diffusion-v1-4":"sd-v1-4",
#             "models/prompthero/openjourney":"openjourney",
#             "models/hakurei/waifu-diffusion":"waifu-diffusion",
#             "models/Linaqruf/anything-v3.0":"anything-v3.0",
#            }

space_ids = {
            "spaces/stabilityai/stable-diffusion":"Stable Diffusion 2.1",
            "spaces/stabilityai/stable-diffusion-1":"Stable Diffusion 1.0",
            # "spaces/hakurei/waifu-diffusion-demo":"waifu-diffusion",
            }

tab_actions = []
tab_titles = []

thanks_info = "Thanks: "
thanks_info += "[<a style='display:inline-block' href='https://huggingface.co/spaces/daspartho/prompt-extend' _blank><font style='color:blue;weight:bold;'>prompt-extend</font></a>]"

for space_id in space_ids.keys():
    print(space_id, space_ids[space_id])
    try:
        tab = gr.Interface.load(space_id)
        tab_actions.append(tab)
        tab_titles.append(space_ids[space_id])
        thanks_info += f"[<a style='display:inline-block' href='https://huggingface.co/{space_id}' _blank><font style='color:blue;weight:bold;'>{space_ids[space_id]}</font></a>]"
    except Exception as e:
        logger.info(f"load_fail__{space_id}_{e}")

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
            if ([0, 1].includes(i)) {
                tabitems[i].childNodes[0].children[0].style.display='none';
                for (var j = 0; j < tabitems[i].childNodes[0].children[1].children.length; j++) {
                    if (j != 1) {
                        tabitems[i].childNodes[0].children[1].children[j].style.display='none';
                    }
                }
            } else if (i==2) {
                tabitems[i].childNodes[0].children[0].style.display='none';
                tabitems[i].childNodes[0].children[1].style.display='none';
                tabitems[i].childNodes[0].children[2].children[0].style.display='none';
                tabitems[i].childNodes[0].children[3].style.display='none';
                
            }
            
        }  
        
        tab_demo = window['gradioEl'].querySelectorAll('#tab_demo')[0];
        tab_demo.style.display = "block";
        tab_demo.setAttribute('style', 'height: 100%;');
        const page1 = window['gradioEl'].querySelectorAll('#page_1')[0];
        const page2 = window['gradioEl'].querySelectorAll('#page_2')[0];
        window['gradioEl'].querySelectorAll('.gr-radio')[0].disabled = "";
        window['gradioEl'].querySelectorAll('.gr-radio')[1].disabled = "";
    
        page1.style.display = "none";
        page2.style.display = "block";    
        window['prevPrompt'] = '';
        window['doCheckPrompt'] = 0;
        window['checkPrompt'] = function checkPrompt() {
            try {
                    texts = window['gradioEl'].querySelectorAll('textarea');
                    text0 = texts[0];    
                    text1 = texts[1];
                    text2 = texts[2];
                    if (window['gradioEl'].querySelectorAll('.gr-radio')[0].checked) {
                        text_value = text1.value;
                    } else {
                        text_value = text2.value;
                    }
                    progress_bar = window['gradioEl'].querySelectorAll('.progress-bar');
                    if (window['doCheckPrompt'] === 0 && window['prevPrompt'] !== text_value && progress_bar.length == 0) {
                            console.log('_____new prompt___[' + text_value + ']_');
                            window['doCheckPrompt'] = 1;
                            window['prevPrompt'] = text_value;
                            tabitems = window['gradioEl'].querySelectorAll('.tabitem');
                            for (var i = 0; i < tabitems.length; i++) {   
                                if ([0, 1].includes(i)) {
                                    inputText = tabitems[i].children[0].children[1].children[0].querySelectorAll('.gr-text-input')[0];
                                } else if (i==2) {
                                    inputText = tabitems[i].childNodes[0].children[2].children[0].children[0].querySelectorAll('.gr-text-input')[0];
                                }
                                setNativeValue(inputText, text_value);
                                inputText.dispatchEvent(new Event('input', { bubbles: true }));
                            }
                           
                            setTimeout(function() {
                                btns = window['gradioEl'].querySelectorAll('button');
                                for (var i = 0; i < btns.length; i++) {
                                    if (['Generate image','Run'].includes(btns[i].innerText)) {
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

descriptions = "Thanks: "
descriptions += "[<a style='display:inline-block' href='https://huggingface.co/spaces/daspartho/prompt-extend' _blank><font style='color:blue;weight:bold;'>prompt-extend</font></a>]"
descriptions += "[<a style='display:inline-block' href='https://huggingface.co/spaces/stabilityai/stable-diffusion-1' _blank><font style='color:blue;weight:bold;'>Stable Diffusion 1.0</font></a>]"
descriptions += "[<a style='display:inline-block' href='https://huggingface.co/spaces/stabilityai/stable-diffusion-1' _blank><font style='color:blue;weight:bold;'>Stable Diffusion 1.0</font></a>]"
descriptions += "[<a style='display:inline-block' href='https://huggingface.co/spaces/hakurei/waifu-diffusion-demo' _blank><font style='color:blue;weight:bold;'>waifu-diffusion-demo</font></a>]"
descriptions = f"<p>{descriptions}</p>"

with gr.Blocks(title='prompt-extend/') as demo:
    # gr.HTML(descriptions)
    with gr.Group(elem_id="page_1", visible=True) as page_1:
        with gr.Box():            
            with gr.Row():
                start_button = gr.Button("Let's GO!", elem_id="start-btn", visible=True)                 
                start_button.click(fn=None, inputs=[], outputs=[], _js=start_work)   
                
    with gr.Group(elem_id="page_2", visible=False) as page_2:
            with gr.Row(elem_id="prompt_row0"):
                with gr.Column(id="input_col1"):
                    prompt_input0 = gr.Textbox(lines=1, label="Original prompt", visible=True)
                    prompt_input0_en = gr.Textbox(lines=1, label="Original prompt", visible=False)
                    prompt_radio = gr.Radio(["Original prompt", "Extend prompt"], elem_id="prompt_radio",value="Extend prompt", show_label=False)
            # with gr.Row(elem_id="prompt_row1"):
                with gr.Column(id="input_col2"):
                    prompt_input1 = gr.Textbox(lines=2, label="Extend prompt", visible=False)
                    prompt_input2 = gr.Textbox(lines=2, label="Extend prompt", visible=True)
            with gr.Row():
                submit_btn = gr.Button(value = "submit",elem_id="submit-btn").style(
                        margin=True,
                        rounded=(True, True, True, True),
                    )
                submit_btn.click(fn=extend_prompt, inputs=[prompt_input0], outputs=[prompt_input0_en, prompt_input1, prompt_input2])
            with gr.Row(elem_id='tab_demo', visible=True).style(height=200):
                tab_demo = gr.TabbedInterface(tab_actions, tab_titles) 
            with gr.Row():
                gr.HTML(f"<p>{thanks_info}</p>")

demo.launch()