from transformers import pipeline
import gradio as gr
import random
import string
import paddlehub as hub 
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from loguru import logger

from utils import get_tmt_client, getTextTrans_tmt
tmt_client = get_tmt_client()

# language_translation_model = hub.Module(directory=f'./baidu_translate')
def getTextTrans(text, source='zh', target='en'):
    return getTextTrans_tmt(tmt_client, text, source, target)
    # def is_chinese(string):
    #     for ch in string:
    #         if u'\u4e00' <= ch <= u'\u9fff':
    #             return True
    #     return False
        
    # if not is_chinese(text) and target == 'en': 
    #     return text
        
    # try:
    #     text_translation = language_translation_model.translate(text, source, target)
    #     return text_translation
    # except Exception as e:
    #     return text 
        
space_ids = {
            "spaces/stabilityai/stable-diffusion": "SD 2.1",
            "spaces/runwayml/stable-diffusion-v1-5": "SD 1.5",
            "spaces/stabilityai/stable-diffusion-1": "SD 1.0",
            "dalle_mini_tab": "Dalle mini",
            "spaces/IDEA-CCNL/Taiyi-Stable-Diffusion-Chinese": "Taiyi(太乙)",
            }

tab_actions = []
tab_titles = []

extend_prompt_1 = True
extend_prompt_2 = True
extend_prompt_3 = True

thanks_info = "Thanks: "
if extend_prompt_1:
    extend_prompt_pipe = pipeline('text-generation', model='yizhangliu/prompt-extend', max_length=77, pad_token_id=0)
    thanks_info += "[<a style='display:inline-block' href='https://huggingface.co/spaces/daspartho/prompt-extend' _blank><font style='color:blue;weight:bold;'>prompt-extend(1)</font></a>]"
if extend_prompt_2:
    def load_prompter():
      prompter_model = AutoModelForCausalLM.from_pretrained("microsoft/Promptist")
      tokenizer = AutoTokenizer.from_pretrained("gpt2")
      tokenizer.pad_token = tokenizer.eos_token
      tokenizer.padding_side = "left"
      return prompter_model, tokenizer
    prompter_model, prompter_tokenizer = load_prompter()
    def extend_prompt_microsoft(in_text):
        input_ids = prompter_tokenizer(in_text.strip()+" Rephrase:", return_tensors="pt").input_ids
        eos_id = prompter_tokenizer.eos_token_id 
        outputs = prompter_model.generate(input_ids, do_sample=False, max_new_tokens=75, num_beams=8, num_return_sequences=8, eos_token_id=eos_id, pad_token_id=eos_id, length_penalty=-1.0)
        output_texts = prompter_tokenizer.batch_decode(outputs, skip_special_tokens=True)
        res = output_texts[0].replace(in_text+" Rephrase:", "").strip()
        return res    
    thanks_info += "[<a style='display:inline-block' href='https://huggingface.co/spaces/microsoft/Promptist' _blank><font style='color:blue;weight:bold;'>Promptist(2)</font></a>]"
if extend_prompt_3:
    MagicPrompt = gr.Interface.load("spaces/Gustavosta/MagicPrompt-Stable-Diffusion")
    thanks_info += "[<a style='display:inline-block' href='https://huggingface.co/spaces/Gustavosta/MagicPrompt-Stable-Diffusion' _blank><font style='color:blue;weight:bold;'>MagicPrompt(3)</font></a>]"

do_dreamlike_photoreal = False
if do_dreamlike_photoreal:
    def add_random_noise(prompt, noise_level=0.1):
        # Get the percentage of characters to add as noise
        percentage_noise = noise_level * 5
        # Get the number of characters to add as noise
        num_noise_chars = int(len(prompt) * (percentage_noise/100))
        # Get the indices of the characters to add noise to
        noise_indices = random.sample(range(len(prompt)), num_noise_chars)
        # Add noise to the selected characters
        prompt_list = list(prompt)
        for index in noise_indices:
            prompt_list[index] = random.choice(string.ascii_letters + string.punctuation)
        new_prompt = "".join(prompt_list)
        return new_prompt
        
    dreamlike_photoreal_2_0 = gr.Interface.load("models/dreamlike-art/dreamlike-photoreal-2.0")
    dreamlike_image = gr.Image(label="Dreamlike Photoreal 2.0")

    tab_actions.append(dreamlike_image)
    tab_titles.append("Dreamlike_2.0")
    thanks_info += "[<a style='display:inline-block' href='https://huggingface.co/dreamlike-art/dreamlike-photoreal-2.0' _blank><font style='color:blue;weight:bold;'>dreamlike-photoreal-2.0</font></a>]"

for space_id in space_ids.keys():
    print(space_id, space_ids[space_id])
    try:
        tab_title = space_ids[space_id]
        tab_titles.append(tab_title)
        if (tab_title == 'Dalle mini'):
            tab_content = gr.Blocks(elem_id='dalle_mini')
            tab_actions.append(tab_content)            
        else:
            tab_content = gr.Interface.load(space_id)
            tab_actions.append(tab_content)
            thanks_info += f"[<a style='display:inline-block' href='https://huggingface.co/{space_id}' _blank><font style='color:blue;weight:bold;'>{tab_title}</font></a>]"
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
    window['tab_advanced'] = 0;
    
    var gradioEl = document.querySelector('body > gradio-app').shadowRoot;
    if (!gradioEl) {
        gradioEl = document.querySelector('body > gradio-app');
    }
    
    if (typeof window['gradioEl'] === 'undefined') {
        window['gradioEl'] = gradioEl;
        tabitems = window['gradioEl'].querySelectorAll('.tabitem');
        tabitems_title = window['gradioEl'].querySelectorAll('#tab_demo')[0].children[0].children[0].children;
        window['dalle_mini_block'] = null;
        window['dalle_mini_iframe'] = null;
        for (var i = 0; i < tabitems.length; i++) {   
            if (tabitems_title[i].innerText.indexOf('SD') >= 0) {
                tabitems[i].childNodes[0].children[0].style.display='none';
                for (var j = 0; j < tabitems[i].childNodes[0].children[1].children.length; j++) {
                    if (j != 1) {
                        tabitems[i].childNodes[0].children[1].children[j].style.display='none';
                    }
                }
                if (tabitems_title[i].innerText.indexOf('SD 1') >= 0) {
                    for (var j = 0; j < 4; j++) {
                        tabitems[i].childNodes[0].children[1].children[3].children[1].children[j].children[2].removeAttribute("disabled");
                    }
                } else if (tabitems_title[i].innerText.indexOf('SD 2') >= 0) {
                    tabitems[i].children[0].children[1].children[3].children[0].click();
                }
            } else if (tabitems_title[i].innerText.indexOf('Taiyi') >= 0) {
                tabitems[i].children[0].children[0].children[1].style.display='none';
                tabitems[i].children[0].children[0].children[0].children[0].children[1].style.display='none';
            } else if (tabitems_title[i].innerText.indexOf('Dreamlike') >= 0) {
                tabitems[i].childNodes[0].children[0].children[1].style.display='none';
            } else if (tabitems_title[i].innerText.indexOf('Dalle mini') >= 0) {
                window['dalle_mini_block']=  tabitems[i];
            }
        }  
        
        tab_demo = window['gradioEl'].querySelectorAll('#tab_demo')[0];
        tab_demo.style.display = "block";
        tab_demo.setAttribute('style', 'height: 100%;');
        const page1 = window['gradioEl'].querySelectorAll('#page_1')[0];
        const page2 = window['gradioEl'].querySelectorAll('#page_2')[0];
        
        btns_1 = window['gradioEl'].querySelector('#input_col1_row3').children;
        btns_1_split = 100 / btns_1.length;
        for (var i = 0; i < btns_1.length; i++) {
            btns_1[i].setAttribute('style', 'min-width:0px;width:' + btns_1_split + '%;');
        }
        page1.style.display = "none";
        page2.style.display = "block";  
        prompt_work = window['gradioEl'].querySelectorAll('#prompt_work');
        for (var i = 0; i < prompt_work.length; i++) {
            prompt_work[i].style.display='none';
        }         
        
        window['prevPrompt'] = '';
        window['doCheckPrompt'] = 0;
        window['checkPrompt'] = function checkPrompt() {
            try {
                    prompt_work = window['gradioEl'].querySelectorAll('#prompt_work');
                    if (prompt_work.length > 0 && prompt_work[0].children.length > 1) {
                        prompt_work[0].children[1].style.display='none';
                        prompt_work[0].style.display='block';
                    }            
                    text_value = window['gradioEl'].querySelectorAll('#prompt_work')[0].querySelectorAll('textarea')[0].value;
                    progress_bar = window['gradioEl'].querySelectorAll('.progress-bar');
                    if (window['doCheckPrompt'] === 0 && window['prevPrompt'] !== text_value && progress_bar.length == 0) {
                            console.log('_____new prompt___[' + text_value + ']_');
                            window['doCheckPrompt'] = 1;
                            window['prevPrompt'] = text_value;
                            tabitems = window['gradioEl'].querySelectorAll('.tabitem');
                            for (var i = 0; i < tabitems.length; i++) {  
                                if (tabitems_title[i].innerText.indexOf('Dalle mini') >= 0) {
                                    if (window['dalle_mini_block']) {
                                        if (window['dalle_mini_iframe'] === null) {
                                            window['dalle_mini_iframe'] = document.createElement('iframe');                                                
                                            window['dalle_mini_iframe'].height = 1000;
                                            window['dalle_mini_iframe'].width = '100%';        
                                            window['dalle_mini_iframe'].id = 'dalle_iframe';   
                                            window['dalle_mini_block'].appendChild(window['dalle_mini_iframe']);
                                        } 
                                        window['dalle_mini_iframe'].src = 'https://yizhangliu-dalleclone.hf.space/index.html?prompt=' + encodeURI(text_value);
                                        console.log('dalle_mini');
                                    }    
                                    continue;
                                }
                                inputText = null;
                                if (tabitems_title[i].innerText.indexOf('SD') >= 0) {
                                    text_value = window['gradioEl'].querySelectorAll('#prompt_work')[0].querySelectorAll('textarea')[0].value;
                                    inputText = tabitems[i].children[0].children[1].children[0].querySelectorAll('.gr-text-input')[0];
                                } else if (tabitems_title[i].innerText.indexOf('Taiyi') >= 0) {
                                    text_value = window['gradioEl'].querySelectorAll('#prompt_work_zh')[0].querySelectorAll('textarea')[0].value;
                                    inputText = tabitems[i].children[0].children[0].children[1].querySelectorAll('.gr-text-input')[0];
                                }
                                if (inputText) {
                                    setNativeValue(inputText, text_value);
                                    inputText.dispatchEvent(new Event('input', { bubbles: true }));
                                }                                
                            }
                           
                            setTimeout(function() {
                                btns = window['gradioEl'].querySelectorAll('button');
                                for (var i = 0; i < btns.length; i++) {
                                    if (['Generate image','Run', '生成图像(Generate)'].includes(btns[i].innerText)) {
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

switch_tab_advanced = """async() => {
    window['tab_advanced'] = 1 - window['tab_advanced'];
    if (window['tab_advanced']==0) {
        action = 'none';
    } else {
        action = 'block';
    }
    tabitems = window['gradioEl'].querySelectorAll('.tabitem');
    tabitems_title = window['gradioEl'].querySelectorAll('#tab_demo')[0].children[0].children[0].children;  
    for (var i = 0; i < tabitems.length; i++) {   
        if (tabitems_title[i].innerText.indexOf('SD') >= 0) {
            //tabitems[i].childNodes[0].children[1].children[0].style.display=action;
            //tabitems[i].childNodes[0].children[1].children[4].style.display=action;
            for (var j = 0; j < tabitems[i].childNodes[0].children[1].children.length; j++) {
                if (j != 1) {
                    tabitems[i].childNodes[0].children[1].children[j].style.display=action;
                }
            }            
        } else if (tabitems_title[i].innerText.indexOf('Taiyi') >= 0) {
            tabitems[i].children[0].children[0].children[1].style.display=action;
        }
    }
    return false;
}"""

def prompt_extend(prompt, PM):    
    prompt_en = getTextTrans(prompt, source='zh', target='en')
    if PM == 1:
        extend_prompt_en = extend_prompt_pipe(prompt_en+',', num_return_sequences=1)[0]["generated_text"]   
    elif PM == 2:
        extend_prompt_en = extend_prompt_microsoft(prompt_en)
    elif PM == 3:
        extend_prompt_en = MagicPrompt(prompt_en)        
        
    if (prompt != prompt_en):
        logger.info(f"extend_prompt__1_PM=[{PM}]_")
        extend_prompt_out = getTextTrans(extend_prompt_en, source='en', target='zh')
    else:
        logger.info(f"extend_prompt__2_PM=[{PM}]_")
        extend_prompt_out = extend_prompt_en

    return extend_prompt_out

def prompt_extend_1(prompt):  
    extend_prompt_out = prompt_extend(prompt, 1)
    return extend_prompt_out

def prompt_extend_2(prompt):  
    extend_prompt_out = prompt_extend(prompt, 2)
    return extend_prompt_out

def prompt_extend_3(prompt):  
    extend_prompt_out = prompt_extend(prompt, 3)
    return extend_prompt_out    

def prompt_draw_1(prompt, noise_level):
    prompt_en = getTextTrans(prompt, source='zh', target='en')
    if (prompt != prompt_en):
        logger.info(f"draw_prompt______1__")
        prompt_zh = prompt
    else:
        logger.info(f"draw_prompt______2__")
        prompt_zh = getTextTrans(prompt, source='en', target='zh')

    prompt_with_noise = add_random_noise(prompt_en, noise_level)
    dreamlike_output = dreamlike_photoreal_2_0(prompt_with_noise)
    return prompt_en, prompt_zh, dreamlike_output

def prompt_draw_2(prompt):
    prompt_en = getTextTrans(prompt, source='zh', target='en')
    if (prompt != prompt_en):
        logger.info(f"draw_prompt______1__")
        prompt_zh = prompt
    else:
        logger.info(f"draw_prompt______2__")
        prompt_zh = getTextTrans(prompt, source='en', target='zh')
    return prompt_en, prompt_zh

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
                        prompt_work = gr.Textbox(lines=1, label="prompt_work", elem_id="prompt_work", visible=True)                        
                    with gr.Row(elem_id="input_col1_row3"):
                        with gr.Column(elem_id="input_col1_row2_col0"):
                            draw_btn_0 = gr.Button(value = "Generate(original)", elem_id="draw-btn-0")
                        if extend_prompt_1:
                            with gr.Column(elem_id="input_col1_row2_col1"):
                                extend_btn_1 = gr.Button(value = "Extend_1",elem_id="extend-btn-1") 
                        if extend_prompt_2:
                            with gr.Column(elem_id="input_col1_row2_col2"):
                                extend_btn_2 = gr.Button(value = "Extend_2",elem_id="extend-btn-2")
                        if extend_prompt_3:                                
                            with gr.Column(elem_id="input_col1_row2_col3"):
                                extend_btn_3 = gr.Button(value = "Extend_3",elem_id="extend-btn-3") 
                with gr.Column(id="input_col2"):
                    prompt_input1 = gr.Textbox(lines=2, label="Extend prompt", visible=True)
                    draw_btn_1 = gr.Button(value = "Generate(extend)", elem_id="draw-btn-1")
            with gr.Row(elem_id="prompt_row1"):
                with gr.Column(id="input_col3"):
                    with gr.Row(elem_id="input_col3_row2"):
                        prompt_work_zh = gr.Textbox(lines=1, label="prompt_work_zh", elem_id="prompt_work_zh", visible=False)  
            with gr.Row(elem_id='tab_demo', visible=True).style(height=200):
                tab_demo = gr.TabbedInterface(tab_actions, tab_titles) 
            if do_dreamlike_photoreal:
                with gr.Row():
                    noise_level=gr.Slider(minimum=0.1, maximum=3, step=0.1, label="Dreamlike noise Level: [Higher noise level produces more diverse outputs, while lower noise level produces similar outputs.]")
            with gr.Row():                
                switch_tab_advanced_btn = gr.Button(value = "Switch_tab_advanced", elem_id="switch_tab_advanced_btn")
                switch_tab_advanced_btn.click(fn=None, inputs=[], outputs=[], _js=switch_tab_advanced)   
            with gr.Row():                
                gr.HTML(f"<p>{thanks_info}</p>") 

            if extend_prompt_1:
                extend_btn_1.click(fn=prompt_extend_1, inputs=[prompt_input0], outputs=[prompt_input1])
            if extend_prompt_2:
                extend_btn_2.click(fn=prompt_extend_2, inputs=[prompt_input0], outputs=[prompt_input1])
            if extend_prompt_3:                                
                extend_btn_3.click(fn=prompt_extend_3, inputs=[prompt_input0], outputs=[prompt_input1])

            if do_dreamlike_photoreal:
                draw_btn_0.click(fn=prompt_draw_1, inputs=[prompt_input0, noise_level], outputs=[prompt_work, prompt_work_zh, dreamlike_image])
                draw_btn_1.click(fn=prompt_draw_1, inputs=[prompt_input1, noise_level], outputs=[prompt_work, prompt_work_zh, dreamlike_image])
            else:
                draw_btn_0.click(fn=prompt_draw_2, inputs=[prompt_input0], outputs=[prompt_work, prompt_work_zh])
                draw_btn_1.click(fn=prompt_draw_2, inputs=[prompt_input1], outputs=[prompt_work, prompt_work_zh])                

demo.queue()
demo.launch()
