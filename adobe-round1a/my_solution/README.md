# Connecting the Dots Challenge - Round 1A Submission

This project extracts a structured outline (Title, H1, H2, H3) from PDF documents and outputs it as a JSON file.

## My Approach

The solution uses a heuristic-based approach to identify document structure without relying on complex models, ensuring it is fast and lightweight. The core logic is implemented in Python using the `PyMuPDF` library.

The process is as follows:
1.  **Text Block Extraction**: The script iterates through each page of the PDF and extracts all text blocks using `PyMuPDF`. Crucially, it captures not just the text but also its properties: font size, font name (e.g., 'Helvetica-Bold'), and page number.
2.  **Style Analysis**: It analyzes the properties of all text blocks to find patterns. It identifies the unique font sizes present in the document and sorts them from largest to smallest.
3.  **Heuristic Classification**: Headings are classified based on a combination of features:
    * **Font Size**: The largest font size is assumed to be the document **Title**. The next largest sizes are assigned to **H1**, **H2**, and **H3** respectively.
    * **Font Weight**: Text that is **bold** is given a much higher chance of being a heading. This helps differentiate between a large-font body text and a true heading.
4.  **JSON Output**: The script assembles the findings into the required JSON format, including the level, text, and page number for each identified heading.

This method is robust because it doesn't rely solely on font size, which can be inconsistent across different PDFs.

## Models or Libraries Used

-   **PyMuPDF (`fitz`)**: A high-performance Python library for PDF parsing. It was chosen for its speed, low memory footprint, and ability to extract detailed text metadata (fonts, sizes, etc.) without external dependencies.
-   **Standard Libraries**: `os` for file path manipulation and `json` for creating the output file.

No pre-trained models are used in this solution.

## How to Build and Run the Solution

### Prerequisites
- Docker must be installed and running on your system.

### Build the Docker Image
Navigate to the root directory of this project and run the following command:

```bash
docker build --platform linux/amd64 -t mysolution .