import gradio as gr
import os
from modules.image_processor import ImageProcessor
from modules.audio_processor import AudioProcessor
from modules.prompt_builder import build_multimodal_prompt
from modules.llm_processor import LLMProcessor
from modules.tts_processor import TTSProcessor

print("Initializing AI Models... This may take a moment.")
# Initialize models
try:
    image_processor = ImageProcessor()
    print("Image model loaded.")
except Exception as e:
    print(f"Error loading image model: {e}")
    image_processor = None

try:
    audio_processor = AudioProcessor()
    print("Audio model loaded.")
except Exception as e:
    print(f"Error loading audio model: {e}")
    audio_processor = None

llm_processor = LLMProcessor()
print("LLM model initialized.")

try:
    tts_processor = TTSProcessor()
    print("TTS model loaded.")
except Exception as e:
    print(f"Error loading TTS model: {e}")
    tts_processor = None


def process_multimodal_input(text_input, image_input, audio_input):
    """
    Main processing function for Gradio interface.
    """
    image_caption = ""
    audio_transcript = ""

    # Process Image
    if image_input is not None and image_processor:
        image_caption = image_processor.process_image(image_input)
    
    # Process Audio
    if audio_input is not None and audio_processor:
        audio_transcript = audio_processor.process_audio(audio_input)

    # If no inputs are provided at all
    if not text_input and not image_caption and not audio_transcript:
        return "Please provide at least one input (Text, Image, or Audio).", "", "", "", None

    # Build Prompt
    final_prompt = build_multimodal_prompt(
        text_input=text_input,
        image_caption=image_caption,
        audio_transcript=audio_transcript
    )

    # Generate LLM Response
    llm_response = llm_processor.generate_response(final_prompt)

    # Optional TTS
    audio_output = None
    if tts_processor and "Error" not in llm_response:
        output_path = "output_audio.wav"
        audio_output = tts_processor.synthesize_speech(llm_response, output_path)

    return image_caption, audio_transcript, final_prompt, llm_response, audio_output


# Gradio Interface setup
with gr.Blocks(title="Multimodal AI Assistant", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🤖 Multimodal AI Assistant")
    gr.Markdown("Upload any combination of Text, Image, and Audio to receive a context-aware unified response.")
    
    with gr.Row():
        with gr.Column(scale=1):
            text_in = gr.Textbox(label="1. Text Input", placeholder="Ask a question or provide context...", lines=3)
            image_in = gr.Image(label="2. Image Upload", type="filepath")
            audio_in = gr.Audio(label="3. Audio Upload", type="filepath")
            submit_btn = gr.Button("Generate Response", variant="primary")
            
        with gr.Column(scale=1):
            gr.Markdown("### Processing Outputs")
            image_cap_out = gr.Textbox(label="Image Caption (BLIP)", lines=2, interactive=False)
            audio_trans_out = gr.Textbox(label="Audio Transcript (Whisper)", lines=2, interactive=False)
            fused_prompt_out = gr.Textbox(label="Fused Prompt / Multimodal Context", lines=4, interactive=False)
            
            gr.Markdown("### Final Synthesized Response")
            final_resp_out = gr.Textbox(label="AI Response (GPT-4o-mini)", lines=5, interactive=False)
            audio_out = gr.Audio(label="Spoken Response (Coqui TTS)", interactive=False)

    submit_btn.click(
        fn=process_multimodal_input,
        inputs=[text_in, image_in, audio_in],
        outputs=[image_cap_out, audio_trans_out, fused_prompt_out, final_resp_out, audio_out]
    )

if __name__ == "__main__":
    print("Starting Gradio App...")
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)
