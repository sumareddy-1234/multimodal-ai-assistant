def build_multimodal_prompt(text_input: str, image_caption: str, audio_transcript: str) -> str:
    """
    Creates a unified prompt that fuses all available multimodal inputs.
    Missing inputs will be handled gracefully by indicating they are absent.
    """
    
    prompt = "You are a helpful Multimodal AI Assistant. Please use the available information to generate a single, coherent, unified response.\n\n"
    
    prompt += "Image Caption:\n"
    if image_caption:
        prompt += f"{image_caption}\n\n"
    else:
        prompt += "No image provided.\n\n"

    prompt += "Audio Transcript:\n"
    if audio_transcript:
        prompt += f"{audio_transcript}\n\n"
    else:
        prompt += "No audio provided.\n\n"

    prompt += "User Text:\n"
    if text_input:
        prompt += f"{text_input}\n\n"
    else:
        prompt += "No text input provided.\n\n"

    prompt += "Instructions:\nUse all available information from the provided modalities and generate a unified, contextually aware response. Answer any questions asked in the text or audio. If there are contradictions or relations, point them out."
    
    return prompt
