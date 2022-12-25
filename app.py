from transformers import pipeline
import gradio as gr
import random
import paddlehub as hub
from loguru import logger

language_translation_model = hub.Module(directory=f'./baidu_translate')
def getTextTrans(text, source='zh', target='en'):
    def is_chinese(string):
        for ch in string:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False
        
    if not is_chinese(text) and target == 'en': 
        return text
        
    try:
        text_translation = language_translation_model.translate(text, source, target)
        return text_translation
    except Exception as e:
        return text 
        
extend_prompt_pipe = pipeline('text-generation', model='yizhangliu/prompt-extend', max_length=77, pad_token_id=0)

space_ids = {
            "spaces/stabilityai/stable-diffusion":"SD 2.1",
            "spaces/runwayml/stable-diffusion-v1-5":"SD 1.5",
            "spaces/stabilityai/stable-diffusion-1":"SD 1.0",
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
            if ([0, 1, 2].includes(i)) {
                tabitems[i].childNodes[0].children[0].style.display='none';
                for (var j = 0; j < tabitems[i].childNodes[0].children[1].children.length; j++) {
                    if (j != 1) {
                        tabitems[i].childNodes[0].children[1].children[j].style.display='none';
                    }
                }
            } else {
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
        window['gradioEl'].querySelector('#input_col1_row2').children[0].setAttribute('style', 'min-width:0px;width:50%;');
        window['gradioEl'].querySelector('#input_col1_row2').children[1].setAttribute('style', 'min-width:0px;width:50%;');
        page1.style.display = "none";
        page2.style.display = "block";    
        window['prevPrompt'] = '';
        window['doCheckPrompt'] = 0;
        window['checkPrompt'] = function checkPrompt() {
            try {
                    text_value = window['gradioEl'].querySelectorAll('#prompt_work')[0].querySelectorAll('textarea')[0].value;
                    progress_bar = window['gradioEl'].querySelectorAll('.progress-bar');
                    if (window['doCheckPrompt'] === 0 && window['prevPrompt'] !== text_value && progress_bar.length == 0) {
                            console.log('_____new prompt___[' + text_value + ']_');
                            window['doCheckPrompt'] = 1;
                            window['prevPrompt'] = text_value;
                            tabitems = window['gradioEl'].querySelectorAll('.tabitem');
                            for (var i = 0; i < tabitems.length; i++) {   
                                if ([0, 1, 2].includes(i)) {
                                    inputText = tabitems[i].children[0].children[1].children[0].querySelectorAll('.gr-text-input')[0];
                                } else {
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

def prompt_extend(prompt):    
    prompt_en = getTextTrans(prompt, source='zh', target='en')
    extend_prompt_en = extend_prompt_pipe(prompt_en+',', num_return_sequences=1)[0]["generated_text"]    
    if (prompt != prompt_en):
        logger.info(f"extend_prompt__1__")
        extend_prompt_out = getTextTrans(extend_prompt_en, source='en', target='zh')
    else:
        logger.info(f"extend_prompt__2__")
        extend_prompt_out = extend_prompt_en

    return extend_prompt_out

def prompt_draw(prompt):
    prompt_en = getTextTrans(prompt, source='zh', target='en')
    if (prompt != prompt_en):
        logger.info(f"draw_prompt______1__")
    else:
        logger.info(f"draw_prompt______2__")
    return prompt_en
        
with gr.Blocks(title='Text-to-Image') as demo:
    with gr.Group(elem_id="page_1", visible=True) as page_1:
        with gr.Box():            
            with gr.Row():
                start_button = gr.Button("Let's GO!", elem_id="start-btn", visible=True)                 
                start_button.click(fn=None, inputs=[], outputs=[], _js=start_work)   
                
    with gr.Group(elem_id="page_2", visible=False) as page_2:
            with gr.Row(elem_id="prompt_row0"):
                with gr.Column(id="input_col1"):
                    with gr.Row(elem_id="input_col1_row1"):
                        prompt_input0 = gr.Textbox(lines=2, label="Original prompt", visible=True)
                    with gr.Row(elem_id="input_col1_row2"):
                        with gr.Column(elem_id="input_col1_row2_col1"):
                            draw_btn_0 = gr.Button(value = "Generate(original)", elem_id="draw-btn-0")
                        with gr.Column(elem_id="input_col1_row2_col2"):
                            extend_btn = gr.Button(value = "Extend prompt",elem_id="extend-btn")                    
                with gr.Column(id="input_col2"):
                    prompt_input1 = gr.Textbox(lines=2, label="Extend prompt", visible=True)
                    draw_btn_1 = gr.Button(value = "Generate(extend)", elem_id="draw-btn-1")
                    prompt_work = gr.Textbox(lines=1, label="prompt_work", elem_id="prompt_work", visible=False)
            with gr.Row(elem_id='tab_demo', visible=True).style(height=200):
                tab_demo = gr.TabbedInterface(tab_actions, tab_titles) 
            with gr.Row():
                gr.HTML(f"<p>{thanks_info}</p>")

            extend_btn.click(fn=prompt_extend, inputs=[prompt_input0], outputs=[prompt_input1])
            draw_btn_0.click(fn=prompt_draw, inputs=[prompt_input0], outputs=[prompt_work])
            draw_btn_1.click(fn=prompt_draw, inputs=[prompt_input1], outputs=[prompt_work])
        
demo.launch()
