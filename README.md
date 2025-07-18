# Handwriting to Text Converter 📝

A full-stack web application that converts handwritten text from images using OCR.space API. Built with Flask backend and React frontend.

## Features ✨

- **Drag & Drop Interface**: Easy file upload with drag-and-drop functionality
- **Real-time Processing**: Convert handwritten text from images instantly
- **Multiple Format Support**: PNG, JPG, JPEG, GIF, and BMP files
- **Preview & Results**: See uploaded image and extracted text side by side
- **Copy to Clipboard**: One-click text copying
- **Responsive Design**: Works on desktop and mobile devices
- **Error Handling**: Comprehensive error handling and user feedback
- **File Validation**: Size and format validation for uploaded images

## Tech Stack 🛠️

- **Backend**: Python 3, Flask, OCR.space API
- **Frontend**: React (with HTML fallback), Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: requests library
- **Image Processing**: Pillow (PIL)

## Prerequisites 📋

- Python 3.7+
- OCR.space API key (free at [ocr.space](https://ocr.space/ocrapi))
- Node.js (optional, for React development)

## Installation 🚀

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/handwriting-to-text-converter.git
   cd handwriting-to-text-converter
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```
   OCR_SPACE_API_KEY=your_ocr_space_api_key_here
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Open your browser** and navigate to `http://localhost:5000`

## Usage 💡

1. **Upload an image** by dragging and dropping or clicking the upload area
2. **Select a file** containing handwritten text
3. **Click "Extract Text"** to process the image
4. **View the results** in the extracted text panel
5. **Copy the text** to your clipboard with one click

## Project Structure 📁

```
handwriting-to-text-converter/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── templates/
│   └── index.html        # React frontend
├── uploads/              # Temporary file storage
└── README.md
```

## API Endpoints 🔗

- `GET /` - Main application interface
- `POST /api/upload` - Upload and process images
- `POST /api/upload-base64` - Process base64 encoded images
- `GET /api/health` - Health check endpoint

## Configuration ⚙️

### Environment Variables

- `OCR_SPACE_API_KEY`: Your OCR.space API key (required)
- `SECRET_KEY`: Flask secret key (optional, defaults to a placeholder)

### OCR Settings

The application uses OCR.space API with the following settings:
- **Engine**: OCR Engine 2 (better for handwriting)
- **Language**: English (eng)
- **Orientation Detection**: Enabled
- **Scaling**: Enabled for better accuracy

## Error Handling 🛠️

- **File Size Limit**: 16MB maximum
- **File Type Validation**: Only image files allowed
- **API Error Handling**: Graceful handling of OCR service errors
- **Network Error Handling**: Retry logic and user feedback

## Browser Support 🌐

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- [OCR.space](https://ocr.space) for providing the OCR API
- [React](https://react.dev) for the frontend framework
- [Flask](https://flask.palletsprojects.com) for the backend framework
- [Tailwind CSS](https://tailwindcss.com) for styling

## Troubleshooting 🔧

**Common Issues:**

1. **"API key not configured"**: Make sure to set `OCR_SPACE_API_KEY` in your `.env` file
2. **File upload fails**: Check file size (max 16MB) and format (images only)
3. **OCR processing fails**: Ensure the image has clear, readable text
4. **Port already in use**: Change the port in `app.py` or stop other services on port 5000

**Getting Help:**
- Check the browser console for errors
- Review the Flask logs for backend issues
- Ensure your OCR.space API key is valid and has available credits

## Future Enhancements 🚀

- [ ] Support for multiple languages
- [ ] Batch processing of multiple images
- [ ] Export to different formats (PDF, Word, etc.)
- [ ] User authentication and file history
- [ ] Mobile app version
- [ ] Offline OCR capabilities

---

**Happy Converting! 🎉**
# image-to-text
