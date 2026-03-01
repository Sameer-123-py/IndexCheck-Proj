#!/usr/bin/env python3
"""
Excel LLM Processor - Automate ETF/Stock Description Generation
================================================================

This script reads financial instrument data from Excel and generates
structured descriptions using an LLM (Language Learning Model).

Process:
1. Read prompt template from column G (row 2)
2. Read instrument data from column A (one per row)
3. For each row: combine prompt + data, send to LLM
4. Write LLM output to column B (same row)
"""

import openpyxl
from openpyxl.styles import Alignment
import os
from datetime import datetime
from .ai_generator import generate_ai_output
import logging

logger = logging.getLogger(__name__)


class ExcelLLMProcessor:
    """
    Main processor class for Excel LLM automation.
    """
    
    def __init__(self, file_path):
        """
        Initialize the processor.
        
        Args:
            file_path (str): Path to the Excel file
        """
        self.file_path = file_path
        self.workbook = None
        self.sheet = None
        self.stats = {
            'total_rows': 0,
            'processed': 0,
            'skipped': 0,
            'errors': 0
        }
        self.processed_data = []  # Store for preview
    
    def load_excel(self):
        """Load the Excel workbook and select active sheet."""
        try:
            logger.info(f"📂 Loading Excel file: {self.file_path}")
            self.workbook = openpyxl.load_workbook(self.file_path)
            self.sheet = self.workbook.active
            logger.info(f"✅ Loaded sheet: {self.sheet.title}")
            return True
        except FileNotFoundError:
            logger.error(f"❌ Error: File not found: {self.file_path}")
            return False
        except Exception as e:
            logger.error(f"❌ Error loading Excel: {str(e)}")
            return False
    
    def get_prompt_template(self):
        """
        Get the prompt template from column G (row 2).
        
        Returns:
            str: Prompt template or default prompt
        """
        try:
            prompt_cell = self.sheet['G2']
            prompt = prompt_cell.value
            
            if prompt and isinstance(prompt, str) and prompt.strip():
                logger.info(f"📝 Found prompt template in G2 ({len(prompt)} chars)")
                return prompt.strip()
            else:
                default_prompt = "Analyze the following financial instrument data and provide a structured description:"
                logger.warning(f"⚠️  No prompt in G2, using default prompt")
                return default_prompt
                
        except Exception as e:
            logger.warning(f"⚠️  Error reading prompt: {str(e)}, using default")
            return "Analyze the following financial instrument data and provide a structured description:"
    
    def process_row(self, row_num, prompt_template):
        """
        Process a single row: read data from column A, generate output, write to column B.
        
        Args:
            row_num (int): Row number to process
            prompt_template (str): The prompt template to use
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read data from column A
            data_cell = self.sheet[f'A{row_num}']
            data = data_cell.value
            
            # Skip empty rows
            if not data or not str(data).strip():
                logger.info(f"  ⏭️  Row {row_num}: Empty, skipping")
                self.stats['skipped'] += 1
                return False
            
            logger.info(f"  🔄 Row {row_num}: Processing... ({len(str(data))} chars)")
            
            # Combine prompt + data
            full_prompt = f"{prompt_template}\n\n{data}"
            
            # Generate AI response using actual OpenAI
            ai_output = generate_ai_output(full_prompt)
            
            # Write output to column B
            output_cell = self.sheet[f'B{row_num}']
            output_cell.value = ai_output
            
            # Set text wrap for better readability
            output_cell.alignment = Alignment(wrap_text=True, vertical='top')
            
            # Store for preview
            self.processed_data.append({
                'row_num': row_num,
                'instrument': str(data)[:100] + "..." if len(str(data)) > 100 else str(data),
                'description': ai_output[:300] + "..." if len(ai_output) > 300 else ai_output
            })
            
            logger.info(f"  ✅ Row {row_num}: Generated {len(ai_output)} chars")
            self.stats['processed'] += 1
            return True
            
        except Exception as e:
            logger.error(f"  ❌ Row {row_num}: Error - {str(e)}")
            
            # Write error to column B
            try:
                output_cell = self.sheet[f'B{row_num}']
                output_cell.value = f"Error generating description: {str(e)}"
                output_cell.alignment = Alignment(wrap_text=True, vertical='top')
            except:
                pass
            
            self.stats['errors'] += 1
            return False
    
    def process_all_rows(self):
        """
        Process all rows in the Excel file.
        Starts from row 2 (assuming row 1 is header).
        """
        logger.info("\n" + "=" * 60)
        logger.info("🚀 Starting LLM Processing")
        logger.info("=" * 60)
        
        # Get prompt template
        prompt_template = self.get_prompt_template()
        
        # Find last row with data in column A
        max_row = self.sheet.max_row
        last_data_row = 2
        
        for row in range(2, max_row + 1):
            cell_value = self.sheet[f'A{row}'].value
            if cell_value and str(cell_value).strip():
                last_data_row = row
        
        self.stats['total_rows'] = last_data_row - 1  # Excluding header
        
        logger.info(f"\n📊 Found {self.stats['total_rows']} rows to process")
        logger.info(f"📍 Processing rows 2 to {last_data_row}\n")
        
        # Process each row
        for row_num in range(2, last_data_row + 1):
            self.process_row(row_num, prompt_template)
        
        logger.info("\n" + "=" * 60)
        logger.info("📈 Processing Complete")
        logger.info("=" * 60)
        self.print_statistics()
    
    def save_excel(self, output_path=None):
        """
        Save the processed Excel file.
        
        Args:
            output_path (str, optional): Output file path. If None, creates new file.
        """
        try:
            if output_path is None:
                # Create output filename with timestamp
                base_name = os.path.splitext(self.file_path)[0]
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_path = f"{base_name}_processed_{timestamp}.xlsx"
            
            logger.info(f"\n💾 Saving results to: {output_path}")
            self.workbook.save(output_path)
            logger.info(f"✅ File saved successfully!")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ Error saving file: {str(e)}")
            return None
    
    def print_statistics(self):
        """Print processing statistics."""
        logger.info(f"\n📊 Statistics:")
        logger.info(f"   Total Rows:    {self.stats['total_rows']}")
        logger.info(f"   ✅ Processed:   {self.stats['processed']}")
        logger.info(f"   ⏭️  Skipped:     {self.stats['skipped']}")
        logger.info(f"   ❌ Errors:      {self.stats['errors']}")
        
        if self.stats['total_rows'] > 0:
            success_rate = (self.stats['processed'] / self.stats['total_rows']) * 100
            logger.info(f"   📈 Success Rate: {success_rate:.1f}%")
    
    def run(self, output_path=None):
        """
        Main execution method.
        
        Args:
            output_path (str, optional): Output file path
            
        Returns:
            tuple: (output_file_path, processed_data, stats) or (None, None, None) if failed
        """
        logger.info("\n" + "🤖 Excel LLM Processor ".center(60, "="))
        logger.info(f"Version: 1.0")
        logger.info(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
        # Load Excel file
        if not self.load_excel():
            return None, None, None
        
        # Process all rows
        self.process_all_rows()
        
        # Save results
        output_file = self.save_excel(output_path)
        
        logger.info("\n" + "✨ Processing Complete! ".center(60, "=") + "\n")
        
        return output_file, self.processed_data, self.stats