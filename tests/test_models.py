import os
import sys
import pytest

# Add parent directory to path so modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.prompt_builder import build_multimodal_prompt

def test_prompt_builder_all_inputs():
    text = "What is the dog doing?"
    image_cap = "A brown dog running in a grassy park."
    audio_trans = "Is the dog happy?"
    
    prompt = build_multimodal_prompt(text, image_cap, audio_trans)
    
    assert "Image Caption:" in prompt
    assert "A brown dog running in a grassy park." in prompt
    assert "Audio Transcript:" in prompt
    assert "Is the dog happy?" in prompt
    assert "User Text:" in prompt
    assert "What is the dog doing?" in prompt

def test_prompt_builder_missing_inputs():
    text = ""
    image_cap = "A brown dog."
    audio_trans = ""
    
    prompt = build_multimodal_prompt(text, image_cap, audio_trans)
    
    assert "No text input provided." in prompt
    assert "No audio provided." in prompt
    assert "A brown dog." in prompt

def test_imports():
    """Test that all modules can be imported successfully."""
    try:
        import modules.image_processor
        import modules.audio_processor
        import modules.llm_processor
        import modules.tts_processor
        assert True
    except Exception as e:
        pytest.fail(f"Failed to import a module: {e}")
