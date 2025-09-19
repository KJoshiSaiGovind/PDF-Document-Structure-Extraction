import fitz
import json
import os
import re

INPUT_DIR = '/app/input'
OUTPUT_DIR = '/app/output'

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def analyze_pdf_structure(pdf_path):
    doc = fitz.open(pdf_path)

    title = "Untitled Document"
    outline = []

    blocks = []
    for page_num, page in enumerate(doc):
        page_blocks = page.get_text("dict")["blocks"]
        for block in page_blocks:
            if block['type'] == 0:
                for line in block['lines']:
                    for span in line['spans']:
                        text = clean_text(span['text'])
                        if len(text) > 1:
                            blocks.append({
                                'text': text,
                                'size': round(span['size']),
                                'font': span['font'],
                                'page': page_num + 1
                            })

    if not blocks:
        return {"title": title, "outline": []}

    font_sizes = sorted(set(b['size'] for b in blocks), reverse=True)

    size_h1 = font_sizes[1] if len(font_sizes) > 1 else font_sizes[0]
    size_h2 = font_sizes[2] if len(font_sizes) > 2 else None
    size_h3 = font_sizes[3] if len(font_sizes) > 3 else None

    # Set document title
    title_candidates = [b for b in blocks if b['size'] == font_sizes[0]]
    if title_candidates:
        title = title_candidates[0]['text']

    for block in blocks:
        is_bold = "bold" in block['font'].lower()
        size = block['size']
        text = block['text']

        level = None

        # Detect headings using regex and font size
        heading_pattern = re.match(r'^(\d+(\.\d+){0,2})\s+[A-Za-z]', text)
        if size >= size_h1 and (is_bold or heading_pattern):
            level = "H1"
        elif size == size_h2 and heading_pattern:
            level = "H2"
        elif size == size_h3 and heading_pattern:
            level = "H3"

        # Skip broken or too short lines
        if level and len(text.split()) >= 2:
            outline.append({
                "level": level,
                "text": text,
                "page": block['page']
            })

    return {"title": title, "outline": outline}

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(INPUT_DIR, filename)
            output_filename = os.path.splitext(filename)[0] + '.json'
            output_path = os.path.join(OUTPUT_DIR, output_filename)

            print(f"Processing {pdf_path}...")

            try:
                result = analyze_pdf_structure(pdf_path)
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"Successfully created {output_path}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    main()
