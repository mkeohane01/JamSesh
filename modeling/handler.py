from typing import Any, Dict
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline

dtype = torch.bfloat16 if torch.cuda.get_device_capability()[0] == 8 else torch.float16

class EndpointHandler:
    def __init__(self, path=""):

        quantization_config = BitsAndBytesConfig(load_in_8bit=True)
        tokenizer = AutoTokenizer.from_pretrained(path, trust_remote_code = True)
        model = AutoModelForCausalLM.from_pretrained(
            path,
            return_dict = True,
            device_map = "auto",
            torch_dtype = dtype,
            trust_remote_code = True,
            quantization_config=quantization_config
        )
        
        gen_config = model.generation_config
        gen_config.max_new_tokens = 256
        gen_config.num_return_sequences = 1
        gen_config.pad_token_id = tokenizer.eos_token_id
        gen_config.eos_token_id = tokenizer.eos_token_id
        
        self.generation_config = gen_config
        
        self.pipeline = pipeline(
            'text-generation', model=model, tokenizer=tokenizer
        )
       
     
      
    def __call__(self, data: Dict[dict, Any]) -> Dict[str, Any]:
        prompt = data.pop("inputs", data)

        instruction = """Create a list of chords, a corresponding scale to improvise with, title, and style along with an example in ABC notation based on this input. Respond in JSON format.\n
                        Given the input, create an output exactly in this format: \n 
                            "output": {{
                                "chords": "## Suggested chord progression",
                                "scales": "## Suggested scale for improvising",
                                "title": "## Title of Jam",
                                "style": "## Style to play like",
                                "example": `
                                    ## ABC notation for an example section using these chords and notes
                                `
                            }}
                        """
        full_prompt = f"""<s>
        ### Instruction:
        {instruction}
        ### Input:
        {prompt}
        ### Response: 
        """
        
        result = self.pipeline(full_prompt, generation_config = self.generation_config)[0]
        
        return result