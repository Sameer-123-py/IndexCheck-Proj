# IndexCheck-Proj

A powerful Django-based web application that automatically generates professional, structured ETF and stock descriptions using OpenAI's GPT models. Simply upload your Excel file, and let AI do the rest!

## ✨ Features

- 📤 **Easy Upload** - Drag and drop or select Excel files
- 🤖 **AI-Powered** - Generates detailed financial descriptions using GPT-4o-mini
- 📋 **Batch Processing** - Process multiple instruments in one go
- 💾 **Excel Integration** - Reads from Column A, writes to Column B
- 🎯 **Structured Output** - Consistent, professional formatting
- 🔒 **Secure** - API keys stored in environment variables
- 📱 **Responsive UI** - Clean, modern web interface
- 🚀 **Fast Processing** - Parallel processing for speed

## 📋 How It Works

1. **Input Format**: Excel file with:
   - **Column A**: Raw ETF/Stock data (semicolon-separated)
   - **Column G (Row 2)**: Prompt template for AI
   
2. **Processing**:
   - Reads one instrument per row from Column A
   - Combines with prompt template
   - Sends to OpenAI API
   - Writes formatted description to Column B

3. **Output**: Same Excel file with AI-generated descriptions in Column B

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API Key
- Git (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sameer-123-py/IndexCheck-Proj.git
   cd IndexCheck-Proj
