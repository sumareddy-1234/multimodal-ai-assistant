from PIL import Image, ImageDraw, ImageFont
import os

def create_architecture_diagram():
    # Ensure assets directory exists
    os.makedirs('assets', exist_ok=True)
    
    # Create a blank white image
    width, height = 800, 600
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Colors
    box_color = "#3498db"
    text_color = "white"
    line_color = "black"
    
    # Define boxes (x1, y1, x2, y2)
    boxes = {
        "User Text": (50, 50, 200, 100),
        "User Image": (50, 250, 200, 300),
        "User Audio": (50, 450, 200, 500),
        
        "BLIP Captioning": (250, 250, 400, 300),
        "Whisper STT": (250, 450, 400, 500),
        
        "Prompt Builder\n(Multimodal Fusion)": (450, 250, 600, 300),
        
        "Groq Llama 3": (650, 250, 750, 300),
        
        "Final Text\nResponse": (650, 150, 750, 200)
    }
    
    # Draw boxes and text
    for text, (x1, y1, x2, y2) in boxes.items():
        draw.rectangle([x1, y1, x2, y2], fill=box_color, outline="black", width=2)
        # Approximate text centering
        text_x = x1 + 10
        text_y = y1 + 15
        draw.text((text_x, text_y), text, fill=text_color)
        
    # Draw connecting lines
    def draw_arrow(start, end):
        draw.line([start, end], fill=line_color, width=2)
        # Draw basic arrowhead
        draw.polygon([end, (end[0]-10, end[1]-5), (end[0]-10, end[1]+5)], fill=line_color)

    # Connections
    draw_arrow((200, 75), (525, 250)) # Text -> Fusion
    draw_arrow((200, 275), (250, 275)) # Image -> BLIP
    draw_arrow((400, 275), (450, 275)) # BLIP -> Fusion
    draw_arrow((200, 475), (250, 475)) # Audio -> Whisper
    draw_arrow((400, 475), (525, 300)) # Whisper -> Fusion
    
    draw_arrow((600, 275), (650, 275)) # Fusion -> LLM
    draw_arrow((700, 250), (700, 200)) # LLM -> Text Out
    
    # Save the image
    image.save('assets/architecture.png')
    print("Architecture diagram generated at assets/architecture.png")

if __name__ == "__main__":
    create_architecture_diagram()
