import json
import os

def export_for_finetuning(input_file="qa_dataset.jsonl", output_file="pathu_pattu_finetune.jsonl"):
    """
    Converts our saved Q&A dataset into the exact format required by OpenAI for fine-tuning.
    Format required: {"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
    """
    if not os.path.exists(input_file):
        print(f"❌ {input_file} not found. Start using Pattu LLM to collect data first!")
        return

    valid_lines = 0
    with open(input_file, "r", encoding="utf-8") as infile, \
         open(output_file, "w", encoding="utf-8") as outfile:
        
        for line in infile:
            try:
                data = json.loads(line.strip())
                
                # Format for OpenAI Fine-tuning
                finetune_data = {
                    "messages": [
                        {
                            "role": "system", 
                            "content": "You are Pattu LLM, an expert AI created by Mohammed Saaqiv and his team. You specialize in Pathu Pattu Sangam literature and provide simplified meanings."
                        },
                        {
                            "role": "user", 
                            "content": data.get("question", "")
                        },
                        {
                            "role": "assistant", 
                            "content": data.get("answer", "")
                        }
                    ]
                }
                
                outfile.write(json.dumps(finetune_data, ensure_ascii=False) + "\n")
                valid_lines += 1
            except json.JSONDecodeError:
                continue
                
    print("\n" + "="*55)
    print("✅ PATTU LLM DATA EXPORTED FOR FINE-TUNING")
    print("="*55)
    print(f"Total Q&A pairs exported: {valid_lines}")
    print(f"File saved to: {output_file}")
    print("\nNext Steps:")
    print("1. Go to OpenAI Dashboard -> Fine-tuning")
    print(f"2. Upload {output_file}")
    print("3. Train your custom model on Pathu Pattu data!")

if __name__ == "__main__":
    export_for_finetuning()
