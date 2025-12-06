from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import os
import io
import textwrap

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def create_meme(image_path, top_text, bottom_text, output_path, font_size_percent=10):
    """Create meme with top and bottom text"""
    
    # Open image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    # Get image dimensions
    width, height = img.size
    
    # Calculate font size based on image height and percentage
    font_size = int(height * font_size_percent / 100)
    
    # Ensure minimum and maximum font sizes
    font_size = max(20, min(font_size, 100))
    
    # Load font (using default PIL font if system font not available)
    try:
        # Try multiple common font paths
        font_paths = [
            "arial.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "static/fonts/arial.ttf"
        ]
        
        font = None
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, font_size)
                break
            except:
                continue
        
        if font is None:
            raise Exception("No font found")
            
    except:
        # Fallback to default PIL font
        font = ImageFont.load_default()
        font_size = 30
    
    # Function to wrap text if too long
    def wrap_text(text, max_width, font):
        avg_char_width = font_size * 0.6
        max_chars = int(max_width / avg_char_width)
        return textwrap.fill(text, width=max_chars)
    
    # Function to draw text with outline
    def draw_text_with_outline(draw, text, position, font, fill_color="white", outline_color="black"):
        x, y = position
        
        # Split text into lines if needed
        lines = text.split('\n')
        line_height = font_size + 5
        
        for i, line in enumerate(lines):
            line_y = y + (i * line_height)
            
            # Draw outline (thicker outline for better readability)
            for dx in [-3, -2, -1, 0, 1, 2, 3]:
                for dy in [-3, -2, -1, 0, 1, 2, 3]:
                    if abs(dx) == 3 or abs(dy) == 3:  # Thicker outline
                        draw.text((x+dx, line_y+dy), line, font=font, fill=outline_color)
            
            # Draw main text
            draw.text((x, line_y), line, font=font, fill=fill_color)
    
    # Prepare and draw top text
    if top_text:
        # Wrap text if too long
        top_text = wrap_text(top_text, width * 0.9, font)
        
        # Calculate text dimensions
        lines = top_text.split('\n')
        line_height = font_size + 5
        text_height = len(lines) * line_height
        
        # Calculate position - centered horizontally, near top
        top_x = width / 2
        top_y = 20  # Increased from 10 for better positioning
        
        # For each line, calculate its position
        for i, line in enumerate(lines):
            line_width = draw.textlength(line, font=font)
            line_x = (width - line_width) / 2
            line_y = top_y + (i * line_height)
            draw_text_with_outline(draw, line, (line_x, line_y), font)
    
    # Prepare and draw bottom text
    if bottom_text:
        # Wrap text if too long
        bottom_text = wrap_text(bottom_text, width * 0.9, font)
        
        # Calculate text dimensions
        lines = bottom_text.split('\n')
        line_height = font_size + 5
        text_height = len(lines) * line_height
        
        # Calculate position - centered horizontally, near bottom
        bottom_x = width / 2
        bottom_y = height - text_height - 20  # Increased from 10
        
        # For each line, calculate its position
        for i, line in enumerate(lines):
            line_width = draw.textlength(line, font=font)
            line_x = (width - line_width) / 2
            line_y = bottom_y + (i * line_height)
            draw_text_with_outline(draw, line, (line_x, line_y), font)
    
    # Save image
    img.save(output_path, quality=95)
    return output_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if image was uploaded
        if 'image' not in request.files:
            return "No image uploaded", 400
        
        image_file = request.files['image']
        top_text = request.form.get('top_text', '')
        bottom_text = request.form.get('bottom_text', '')
        font_size_percent = int(request.form.get('font_size', 10))  # Default 10% of image height
        
        if image_file.filename == '':
            return "No image selected", 400
        
        if image_file:
            # Save uploaded image
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
            image_file.save(image_path)
            
            # Generate meme
            output_filename = f"meme_{os.path.basename(image_path)}"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            
            create_meme(image_path, top_text, bottom_text, output_path, font_size_percent)
            
            # Return generated meme
            return render_template('index.html', 
                                 meme_url=f"/static/uploads/{output_filename}",
                                 top_text=top_text,
                                 bottom_text=bottom_text,
                                 font_size=font_size_percent)
    
    return render_template('index.html')

@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)